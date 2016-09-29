import os
import argparse


def validate_enter_dir(dir1, dir2):
    list_valid_dir = []
    for num, valid_dir in enumerate((dir1, dir2), start=1):
        if os.path.exists(valid_dir):
            if os.path.isdir(valid_dir):
                list_valid_dir.append(os.path.abspath(valid_dir))
            else:
                print('Enter path %s is not directory!' % num)
        else:
            print('Directory %s not found!' % num)
    return list_valid_dir


def get_full_file_name(file_path):
    for root, dirs, file_names in os.walk(file_path):
        for file_name in file_names:
            yield os.path.join(root, file_name)


def compare_files(file_name_1, file_name_2, duplicate_files_dict):
    if file_name_1 != file_name_2:
        if os.path.basename(file_name_1) == os.path.basename(file_name_2):
            if os.path.getsize(file_name_1) == os.path.getsize(file_name_2):
                file_name = os.path.basename(file_name_1)
                if file_name in duplicate_files_dict:
                    duplicate_files_dict[file_name].extend([file_name_1,
                                                            file_name_2])
                else:
                    duplicate_files_dict[file_name] = [file_name_1,
                                                       file_name_2]


def are_files_duplicates(file_path_1, file_path_2):
    duplicate_files_dict = {}
    for file_name_1 in get_full_file_name(file_path_1):
        for file_name_2 in get_full_file_name(file_path_2):
            compare_files(file_name_1, file_name_2, duplicate_files_dict)
    return duplicate_files_dict


def print_compare_files(duplicate_files_dict):
    if duplicate_files_dict:
        print('Found duplicate files!')
        for num_file, file_name in enumerate(duplicate_files_dict.keys(),
                                             start=1):
            print('%s. %s:' % (num_file, file_name))
            file_paths = set(duplicate_files_dict[file_name])
            for num_path, file_path in enumerate(file_paths, start=1):
                print('\t %s) %s' % (num_path, file_path))
    else:
        print('Duplicate files not found.')


def createParser():
    parser = argparse.ArgumentParser(description=
                                     'Script to search for duplicate files.')
    parser.add_argument('-d1', '--dir1', required=True, metavar='DIRECTORY 1',
                        help='Enter path to directory 1.')
    parser.add_argument('-d2', '--dir2', required=True, metavar='DIRECTORY 2',
                        help='Enter path to directory 2.')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    list_valid_dir = validate_enter_dir(namespace.dir1, namespace.dir2)
    if len(list_valid_dir) == 2:
        duplicate_files_dict = are_files_duplicates(list_valid_dir[0],
                                                    list_valid_dir[1])
        print_compare_files(duplicate_files_dict)
