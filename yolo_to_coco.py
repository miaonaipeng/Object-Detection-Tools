import json
import os
import shutil

import numpy as np
from PIL import Image


def yolo_to_coco(yolo_images, yolo_labels, coco_images, coco_annotations, class_names):
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Categories
    for i, class_name in enumerate(class_names):
        coco_data["categories"].append({
            "id": i,
            "name": class_name,
            "supercategory": "none"
        })

    # Images and annotations
    annotation_id = 0
    for filename in os.listdir(yolo_labels):
        if filename.endswith(".txt"):
            image_id = filename.split(".")[0]

            # Image
            img_path = os.path.join(yolo_images, image_id + ".jpg")
            img = Image.open(img_path)
            width, height = img.size
            coco_data["images"].append({
                "file_name": image_id + ".jpg",
                "height": height,
                "width": width,
                "id": image_id
            })

            # Annotations
            with open(os.path.join(yolo_labels, filename)) as file:
                for line in file:
                    line = line.strip().split(" ")
                    class_id, x, y, w, h = list(map(float, line))
                    class_id = int(class_id)

                    x_min = (x - w / 2) * width
                    x_max = (x + w / 2) * width
                    y_min = (y - h / 2) * height
                    y_max = (y + h / 2) * height

                    width = x_max - x_min
                    height = y_max - y_min

                    coco_data["annotations"].append({
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": class_id,
                        "bbox": [x_min, y_min, width, height],
                        "area": width * height,
                        "iscrowd": 0,
                        "segmentation": []
                    })

                    annotation_id += 1

            # Copy image to COCO images folder
            shutil.copy(img_path, os.path.join(coco_images, image_id + ".jpg"))

    # Save COCO annotations to file
    with open(coco_annotations, "w") as file:
        json.dump(coco_data, file)


def process_subset(yolo_data_root, coco_data_root, subset, class_names):
    yolo_images = os.path.join(yolo_data_root, subset, "images")
    yolo_labels = os.path.join(yolo_data_root, subset, "labels")
    coco_images = os.path.join(coco_data_root, f"{subset}2017")
    coco_annotations = os.path.join(coco_data_root, "annotations", f"instances_{subset}2017.json")

    os.makedirs(coco_images, exist_ok=True)
    os.makedirs(os.path.dirname(coco_annotations), exist_ok=True)

    yolo_to_coco(yolo_images, yolo_labels, coco_images, coco_annotations, class_names)

if __name__ == "__main__":
    yolo_data_root = "D:\\GitHub\\data\\mnp_data\\infrared_dataset_Guigang_yolo"
    coco_data_root = "D:\\GitHub\\data\\mnp_data\\infrared_dataset_Guigang_coco"
    class_names = ["insulator", "clamp connection"]

    # Process all subsets: test, train, val
    for subset in ["test", "train", "val"]:
        process_subset(yolo_data_root, coco_data_root, subset, class_names)

    print("YOLO dataset has been successfully converted to COCO format.")

