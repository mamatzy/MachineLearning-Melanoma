# 🚀 Google Colab Guide - CIFAR-10 Classification

## Kenapa Gunakan Google Colab?

✅ **GPU Gratis** - NVIDIA Tesla T4 (10x lebih cepat dari CPU)  
✅ **Unlimited Storage** - Google Drive integration  
✅ **RAM Besar** - 12-16GB tersedia  
✅ **Tidak Perlu Install** - Semua sudah tersedia  
✅ **Cocok untuk ML** - Dibuat khusus untuk machine learning  

---

## 📋 Langkah-Langkah Menggunakan Colab

### 1. Upload Notebook ke Colab

**Opsi A: Dari Google Drive**
```
1. Buka Google Drive: drive.google.com
2. Upload file CIFAR10_Colab.ipynb
3. Klik kanan → Open with → Google Colaboratory
```

**Opsi B: Langsung dari URL**
```
1. Buka: colab.research.google.com
2. File → Upload notebook
3. Pilih CIFAR10_Colab.ipynb dari device Anda
```

**Opsi C: Dari GitHub (jika sudah di-push)**
```
1. Buka: colab.research.google.com
2. File → Open notebook
3. Masukkan GitHub URL notebook
```

### 2. Enable GPU

```
1. Klik Menu: Runtime
2. Pilih: Change runtime type
3. Hardware accelerator: Pilih "GPU"
4. Klik "Save"
```

⚠️ **PENTING**: Jangan lupa mengaktifkan GPU sebelum training!

### 3. Run Notebook

```
1. Klik tombol Play (▶) atau tekan Shift+Enter untuk setiap cell
2. Atau: Runtime → Run all (untuk menjalankan semua sekaligus)
```

---

## ⏱️ Waktu Eksekusi Diperkirakan

| Tahap | Waktu (GPU) | Waktu (CPU) |
|-------|-----------|-----------|
| Data Loading | 2-3 min | 2-3 min |
| VGG Training | 8-10 min | 60-80 min |
| ResNet Training | 5-8 min | 40-50 min |
| Evaluation | 2-3 min | 5-10 min |
| **Total** | **30-35 min** | **2-3 jam** |

**Rekomendasi**: Gunakan GPU untuk hasil lebih cepat!

---

## 📥 Download Results

Setelah training selesai, semua file hasil disimpan otomatis:

### Dari Colab Local Storage
```
1. Klik folder icon (Files) di sidebar kiri
2. Cari dan klik kanan file yang mau didownload
3. Pilih Download
```

### Dari Google Drive
```
1. Di notebook cell terakhir, tambahkan:
   from google.colab import files
   files.download('training_curves.png')
   files.download('cifar10_results.json')
```

### Files yang Dihasilkan
- `training_curves.png` - Loss dan accuracy graphs
- `accuracy_comparison.png` - Perbandingan akurasi
- `confusion_matrices.png` - Confusion matrices
- `computational_metrics.png` - Model size & training time
- `cifar10_results.json` - Detailed results

---

## 💾 Save to Google Drive

Untuk menyimpan semua hasil ke Google Drive otomatis:

**Tambahkan cell ini di awal notebook (setelah imports):**

```python
from google.colab import drive
drive.mount('/content/drive')

# Buat folder untuk results
import os
os.makedirs('/content/drive/My Drive/CIFAR10_Results', exist_ok=True)
```

**Di akhir notebook, ganti path file dengan:**

```python
import shutil

# Copy semua results ke Google Drive
results_dir = '/content/drive/My Drive/CIFAR10_Results'
for file in ['training_curves.png', 'accuracy_comparison.png', 'confusion_matrices.png', 'computational_metrics.png', 'cifar10_results.json']:
    if os.path.exists(file):
        shutil.copy(file, results_dir)

print(f"✓ All files saved to Google Drive!")
```

---

## ⚙️ Customize Parameters

Di cell "Step 2: Configuration", ubah nilai berikut sesuai kebutuhan:

```python
CONFIG = {
    'num_epochs': 50,      # Ganti ke 10, 20, dst untuk test cepat
    'batch_size': 32,      # Kurangi jika out of memory
    'learning_rate': 0.1,  # Learning rate SGD
    'num_classes': 10,     # Jangan ubah (CIFAR-10 punya 10 kelas)
    'print_interval': 10   # Print stats setiap 10 epoch
}
```

---

## 🐛 Troubleshooting

### Error: "CUDA out of memory"
```
Solusi:
1. Kurangi batch_size: 32 → 16
2. Kurangi num_epochs: 50 → 20
3. Restart runtime dan coba lagi
```

### Error: "ConnectionResetError"
```
Solusi:
1. Sudah diperbaiki dengan num_workers=0
2. Jika masih error, restart runtime
```

### Session Timeout
```
Solusi:
1. Colab timeout setelah ~12 jam inactivity
2. Untuk long training, simpan checkpoint setiap N epoch
3. Gunakan Google Drive untuk save results otomatis
```

### Runtime GPU Disconnect
```
Solusi:
1. Klik: Runtime → Restart runtime
2. Jalankan dari awal atau dari checkpoint
```

---

## 📊 Monitoring Training

**Selama training berjalan:**

1. Lihat Cell Output untuk metrics
2. Gunakan TensorBoard untuk real-time visualization:
   ```python
   %tensorboard --logdir=./logs
   ```
3. Bisa buka multiple terminals di Colab untuk monitoring

---

## 🎯 Tips & Tricks

1. **Test Cepat**: Set `num_epochs = 2` untuk test sebelum full training
2. **Save Checkpoints**: Save model setiap N epoch (sudah ada di code)
3. **Cek GPU Memory**: Jalankan cell ini:
   ```python
   !nvidia-smi
   ```
4. **Parallel Download**: Download semua files di awal notebook
5. **Resume Training**: Save/load state untuk continue training

---

## 🔗 Useful Links

- **Google Colab**: https://colab.research.google.com
- **Google Drive**: https://drive.google.com
- **PyTorch Docs**: https://pytorch.org/docs/stable/index.html
- **CIFAR-10 Info**: https://www.cs.toronto.edu/~kriz/cifar.html

---

## 💡 Alternatif Cloud Services

Jika Colab lambat, coba alternatif lain:

| Service | GPU | Price | Waktu | Note |
|---------|-----|-------|-------|------|
| Google Colab | Tesla T4 (Free) | Free | 12h/day | Terbaik |
| Kaggle | Tesla P100 (Free) | Free | 20h/week | Bagus |
| AWS SageMaker | Pilihan | $0.25-3/hr | Unlimited | Bayar |
| Azure ML | Pilihan | $0.50-4/hr | Unlimited | Bayar |

---

## ✅ Checklist

Sebelum run, pastikan:
- [ ] File notebook sudah di-upload
- [ ] GPU sudah di-enable (Runtime → Change runtime type)
- [ ] Internet connection stabil
- [ ] Cukup Google Drive space (1-2GB untuk hasil)
- [ ] Tidak ada tab lain yang butuh resource berat

---

## 🎉 Done!

Selesai! Training akan berjalan otomatis dan hasil akan disimpan.

**Estimasi waktu total dengan GPU: 30-35 menit** ⚡

Nikmati training yang lebih cepat di Google Colab! 🚀
