import os


def enter_directory():
    list_file_path = []
    for num in range(1, 3):
        while True:
            enter_file_path = input('Enter directory %s to scan: ' % num)
            if os.path.exists(enter_file_path):
                if os.path.isdir(enter_file_path):
                    list_file_path.append(os.path.abspath(enter_file_path))
                    break
                else:
                    print('This is not directory!')
            else:
                print('Directory not found!')
    return list_file_path


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


if __name__ == '__main__':
    list_file_path = enter_directory()
    duplicate_files_dict = are_files_duplicates(list_file_path[0],
                                                list_file_path[1])
    print_compare_files(duplicate_files_dict)
