import os
import argparse


def validate_dir(dir1, dir2):
    validate_dir_ok = True
    for validation_dir in dir1, dir2:
        if not os.path.exists(validation_dir):
            print('Directory \"%s\" not found!' % validation_dir)
            validate_dir_ok = False
        else:
            if not os.path.isdir(validation_dir):
                print('Enter path \"%s\" is not directory!' % validation_dir)
                validate_dir_ok = False
    return validate_dir_ok


def get_list_file_names(directory):
    for root, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            yield os.path.join(root, file_name)


def compare_files(file_name_1, file_name_2):
    if file_name_1 != file_name_2:
        if os.path.basename(file_name_1) == os.path.basename(file_name_2):
            if os.path.getsize(file_name_1) == os.path.getsize(file_name_2):
                return True
    return False


def search_duplicate_files(dir1, dir2):
    duplicate_files_dict = {}
    for file_name_1 in get_list_file_names(dir1):
        for file_name_2 in get_list_file_names(dir2):
            if compare_files(file_name_1, file_name_2):
                file_name = os.path.basename(file_name_1)
                if file_name in duplicate_files_dict:
                    duplicate_files_dict[file_name].extend([file_name_1,
                                                            file_name_2])
                else:
                    duplicate_files_dict[file_name] = [file_name_1,
                                                       file_name_2]
    return duplicate_files_dict


def print_duplicate_files(duplicate_files):
    if duplicate_files:
        print('Found duplicate files!')
        for num_file, file_name in enumerate(duplicate_files.keys(),
                                             start=1):
            print('%s. %s:' % (num_file, file_name))
            file_paths = set(duplicate_files[file_name])
            for num_path, file_path in enumerate(file_paths, start=1):
                print('\t %s) %s' % (num_path, file_path))
    else:
        print('Duplicate files not found.')


def createParser():
    parser = argparse.ArgumentParser(description='Script to search \
                                     for duplicate files.')
    parser.add_argument('-d1', '--dir1', required=True, metavar='DIRECTORY 1',
                        help='Enter path to directory 1.')
    parser.add_argument('-d2', '--dir2', required=True, metavar='DIRECTORY 2',
                        help='Enter path to directory 2.')
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    if validate_dir(namespace.dir1, namespace.dir2):
        print_duplicate_files(
            search_duplicate_files(os.path.abspath(namespace.dir1),
                                   os.path.abspath(namespace.dir2)))
