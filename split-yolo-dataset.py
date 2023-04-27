import os
import shutil
import splitfolders


def move_labels(input_folder, output_folder):
    labels_path = os.path.join(input_folder, 'labels')
    images_path = os.path.join(input_folder, 'images')
    label_files = os.listdir(labels_path)

    for label_file in label_files:
        img_file = label_file.replace('.txt', '.jpg')  # 如果图像格式为PNG，请将.jpg更改为.png
        img_path = os.path.join(images_path, img_file)

        if os.path.isfile(img_path):
            shutil.move(img_path, os.path.join(output_folder, 'images', img_file))
            shutil.move(os.path.join(labels_path, label_file), os.path.join(output_folder, 'labels', label_file))


input_folder = "D:\GitHub\data\mnp_data\infra_inspection"
output_folder = "./"
ratios = (0.7, 0.2, 0.1)

splitfolders.ratio(input_folder, output=output_folder, seed=42, ratio=ratios, group_prefix=None)

# Create the labels subfolders
os.makedirs(os.path.join(output_folder, 'train', 'labels'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'val', 'labels'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'test', 'labels'), exist_ok=True)

move_labels(os.path.join(output_folder, 'train'), os.path.join(output_folder, 'train'))
move_labels(os.path.join(output_folder, 'val'), os.path.join(output_folder, 'val'))
move_labels(os.path.join(output_folder, 'test'), os.path.join(output_folder, 'test'))
