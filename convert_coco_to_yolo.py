import os
import json
import shutil


def convert_coco_to_yolo(coco_annotation_file, image_dir, output_image_dir, output_label_dir):
    with open(coco_annotation_file) as f:
        coco_data = json.load(f)

    image_id_to_file = {image["id"]: image["file_name"] for image in coco_data["images"]}
    image_id_to_size = {image["id"]: (image["width"], image["height"]) for image in coco_data["images"]}
    categories = {category["id"]: category["name"] for category in coco_data["categories"]}

    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    for annotation in coco_data["annotations"]:
        image_id = annotation["image_id"]
        image_file = image_id_to_file[image_id]
        image_width, image_height = image_id_to_size[image_id]
        category_id = annotation["category_id"]
        category_name = categories[category_id]

        bbox = annotation["bbox"]
        x, y, width, height = bbox

        # Normalize the bounding box values
        x_center = (x + width / 2) / image_width
        y_center = (y + height / 2) / image_height
        width /= image_width
        height /= image_height

        image_file_name = os.path.basename(image_file)
        output_label_file = os.path.join(output_label_dir, os.path.splitext(image_file_name)[0] + ".txt")
        with open(output_label_file, "a") as f:
            f.write(f"{category_id} {x_center} {y_center} {width} {height}\n")

        # Copy the image file
        shutil.copy(os.path.join(image_dir, image_file_name), os.path.join(output_image_dir, image_file_name))

# Set your dataset paths
dataset_root = r"D:\GitHub\data\FLIR"
output_root = r"D:\GitHub\data\mnp_data\FLIR_yolo"

train_annotation_file = os.path.join(dataset_root, "train", "thermal_annotations.json")
val_annotation_file = os.path.join(dataset_root, "val", "thermal_annotations.json")
train_image_dir = os.path.join(dataset_root, "train", "thermal_8_bit")
val_image_dir = os.path.join(dataset_root, "val", "thermal_8_bit")

train_output_image_dir = os.path.join(output_root, "train", "images")
val_output_image_dir = os.path.join(output_root, "val", "images")
train_output_label_dir = os.path.join(output_root, "train", "labels")
val_output_label_dir = os.path.join(output_root, "val", "labels")
# Create output directories
os.makedirs(train_output_image_dir, exist_ok=True)
os.makedirs(val_output_image_dir, exist_ok=True)
os.makedirs(train_output_label_dir, exist_ok=True)
os.makedirs(val_output_label_dir, exist_ok=True)

# Convert annotations to YOLO format and copy images
convert_coco_to_yolo(train_annotation_file, train_image_dir, train_output_image_dir, train_output_label_dir)
convert_coco_to_yolo(val_annotation_file, val_image_dir, val_output_image_dir, val_output_label_dir)