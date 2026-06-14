import os
import glob
import zipfile
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split
from ultralytics import YOLO


zip_path = '/home/mamat/kuliah/ml/melanoma/archive.zip'
extract_path = '/home/mamat/kuliah/ml/melanoma/dataset'
yolo_dataset_path = '/home/mamat/kuliah/ml/melanoma/yolo_dataset' # Folder baru untuk struktur YOLO

# Ekstrak zip jika belum diekstrak
if not os.path.exists(extract_path):
    print("Mengekstrak dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Ekstraksi selesai.")

# ==========================================
# 2. PERSIAPAN METADATA & PATH GAMBAR
# ==========================================
metadata_path = f'{extract_path}/HAM10000_metadata.csv'
df = pd.read_csv(metadata_path)

# Label mapping tidak diubah
classes = ['nv','mel','bkl','bcc','akiec','vasc','df']
label2idx = {c:i for i,c in enumerate(classes)}
df['label'] = df['dx'].map(label2idx)

print(f"Dimensi DataFrame: {df.shape}")

# Mengumpulkan path semua gambar
img_dir1 = f'{extract_path}/HAM10000_images_part_1'
img_dir2 = f'{extract_path}/HAM10000_images_part_2'

all_image_paths = {}
for d in [img_dir1, img_dir2]:
    for f in glob.glob(os.path.join(d, '*.jpg')):
        image_id = os.path.basename(f).replace('.jpg', '')
        all_image_paths[image_id] = f

# ==========================================
# 3. DATA SPLIT (TRAIN, VAL, TEST)
# ==========================================
train_df, temp_df = train_test_split(df, test_size=0.3, stratify=df['label'], random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, stratify=temp_df['label'], random_state=42)

print(f"Jumlah Data -> Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

# ==========================================
# 4. RESTRUKTURISASI FOLDER UNTUK YOLOv8
# ==========================================
print("Menyiapkan struktur folder untuk YOLOv8...")

# Membuat folder train, val, test dan sub-folder kelasnya
for split in ['train', 'val', 'test']:
    for cls in classes:
        os.makedirs(os.path.join(yolo_dataset_path, split, cls), exist_ok=True)

# Fungsi untuk memindahkan/mengkopi gambar sesuai split
def copy_images_to_yolo_dir(dataframe, split_name):
    for _, row in dataframe.iterrows():
        img_id = row['image_id']
        cls_name = row['dx']
        
        src_path = all_image_paths.get(img_id)
        if src_path:
            dst_path = os.path.join(yolo_dataset_path, split_name, cls_name, f"{img_id}.jpg")
            # Menggunakan copy2 untuk mempertahankan metadata file
            if not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)

copy_images_to_yolo_dir(train_df, 'train')
copy_images_to_yolo_dir(val_df, 'val')
copy_images_to_yolo_dir(test_df, 'test')

print("Struktur dataset YOLO siap!")

# ==========================================
# 5. INISIALISASI & TRAINING MODEL YOLOv8
# ==========================================
print("Memulai proses training YOLOv8...")

# Menggunakan model klasifikasi pre-trained YOLOv8 nano
model = YOLO('yolov8n-cls.pt')

# Training model
# Ultralytics secara otomatis melakukan augmentasi dan menghitung loss/metrics
results = model.train(
    data=yolo_dataset_path, 
    epochs=15,             # Sesuai kodemu sebelumnya
    imgsz=224,             # Sesuai kodemu sebelumnya
    batch=32,              # Sesuai kodemu sebelumnya
    project='/home/mamat/kuliah/ml/melanoma/YOLO_Runs',
    name='baseline_yolov8',
    pretrained=True
)

# ==========================================
# 6. EVALUASI (TESTING)
# ==========================================
print("\n=== Mengevaluasi model pada data Test ===")
# Ultralytics dapat memvalidasi langsung menggunakan folder 'test' yang sudah kita buat
# Kita cukup mengubah path data validasi ke test saat memanggil model.val()
metrics = model.val(data=yolo_dataset_path, split='test')

print("Proses selesai. Model dan hasil tersimpan di folder project Google Drive-mu.")