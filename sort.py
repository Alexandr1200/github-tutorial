import os
import shutil
from pathlib import Path


extensions = {
    'image': ['jpeg', 'png', 'jpg', 'svg'],
    'documents': ['pdf', 'txt', 'doc', 'docx'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'archive': ['zip', 'gz', 'tar']
}


cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ !#$%&()*+,-;<=>?@[]↑←"
translation_symbols = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_",
                 "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")


TRANS = {}
for c, l in zip(cyrillic_symbols, translation_symbols):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()    


def translate(name):
    return name.translate(TRANS)


def normalize_dir(f_path):
        for rootdir, dirs, files in os.walk(f_path):
            for file in files:
                try:
                    os.rename(os.path.join(rootdir), os.path.join(translate(rootdir)))
                except FileNotFoundError:
                    return


def normalize_file(f_path):
        for rootdir, dirs, files in os.walk(f_path):
            for file in files:       
                os.rename(os.path.join(rootdir, file), os.path.join(rootdir, translate(file)))
            
        return


def create_folders_from_extensions(f_path, f_names):
    for f in f_names:
        if not os.path.exists(f'{f_path}\\{f}'):
            os.mkdir(f'{f_path}\\{f}')


def get_file_paths(f_path):
    file_paths = []
    for rootdir, dirs, files in os.walk(f_path):
        for file in files:       
            if(file.split('.')[-1]):
                file_paths.append(os.path.join(rootdir, file))

    return file_paths


def unpack_archives(f_path):
    for rootdir, dirs, files in os.walk(f_path + '\\archive'):
        for file in files:       
            if(file.split('.')[-1]):
                archive_paths = (os.path.join(rootdir, file))
                shutil.unpack_archive(archive_paths, f_path + '\\archive')
    return 


def sort_files(f_path):
    file_paths = get_file_paths(f_path)
    ext_list = list(extensions.items())
    

    for file_path in file_paths:
        extension = file_path.split('.')[-1]
        file_name = file_path.split('\\')[-1]


        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                # print(f'Moving {file_name} in {ext_list[dict_key_int][0]} folder\n')
                os.rename(file_path, f'{main_path}\\{ext_list[dict_key_int][0]}\\{file_name}')


def remove_empty_folders(f_path):
    walk = list(os.walk(f_path))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            shutil.rmtree(path)


if __name__ == "__main__":
    print('Please write main path for sorting files, for example: C:\\Users\\User name')
    main_path = input('>>> ')
    if not Path(main_path).exists():
        print('Path is wrong')
    else:
        create_folders_from_extensions(main_path, extensions)
        sort_files(main_path)
        remove_empty_folders(main_path)
    print('Sorting done') 
    print('Normalize folders name? wryte -> y')
    input1 = input('>>> ')
    if input1 == 'y':
        normalize_dir(main_path)
        print('Folders normalized')
    else:
        print('Folders are not normalized')
    print('Normalize files name? wryte: y')
    input2 = input('>>> ')
    if input2 == 'y':
        normalize_file(main_path)
        print('Files normalized')
    else:
        print('Files are not normalized')
    print('Need unpack archives? wryte: y')
    input3 = input('>>> ')
    if input3 == 'y':
        unpack_archives(main_path)
        print('Archives unpacked')
    else:
        print('Archives not unpacked')