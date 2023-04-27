import os

train_images_folder = "D:\GitHub\data\mnp_data\infra_inspection\images"
train_labels_folder = "D:\GitHub\data\mnp_data\infra_inspection\labels"

image_files = set([f.replace('.JPG', '') for f in os.listdir(train_images_folder) if f.endswith('.JPG')])
label_files = set([f.replace('.txt', '') for f in os.listdir(train_labels_folder) if f.endswith('.txt')])


extra_labels = label_files - image_files
extra_images = image_files - label_files

print(f"Extra label files: {extra_labels}")
print(f"Extra image files: {extra_images}")