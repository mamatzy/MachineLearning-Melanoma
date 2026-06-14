from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')
results = model.train(
            data='masukinpath/dataset.yaml', 
            epochs=150,
            imgsz=320,
            batch=16,
            project="detect_melanoma",
            name=f"result_train_all_preprocessing"
        )