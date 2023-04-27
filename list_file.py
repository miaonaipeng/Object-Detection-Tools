import os


def list_directories(start_path, indent=''):
    print(indent + os.path.basename(start_path) + '/')
    indent += '    '

    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            list_directories(item_path, indent)

start_path = 'D:\GitHub\data\FLIR'
list_directories(start_path)

