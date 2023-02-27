#!/usr/bin/python3
import sys
import os
import time


DUPLICATE_FILE_SEPARATOR = "------------------------------------------------------------------------------------------------------------------------------------------------------"

def parse_duplicate_file(duplicate_file='duplicate.txt'):
    """
    Parse the strings like:
------------------------------------------------------------------------------------------------------------------------------------------------------
IMG_20180902_172045.jpg	D:\VG\Images\Bea	1,09 MB	2018. 09. 02. 15:20:46
IMG_20180902_172045.jpg	D:\VG\Private\Család\Bea\Beus motor	1,09 MB	2018. 09. 02. 15:20:46
------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    print('Parse duplicate file')

    try:
        with open(duplicate_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        err_msg = '[ERRROR] Duplicate file does not exist!'
        sys.exit(err_msg)
    except:
        raise

    new_pack = []
    list_of_duplicated_files = []
    for item in lines:
        if item.strip() == DUPLICATE_FILE_SEPARATOR:
            if new_pack:
                list_of_duplicated_files.append(new_pack)
                new_pack = []
        else:
            new_pack.append(item)
    #print(list_of_duplicated_files)
    processed_duplicate_items = []
    for duplicate_pack in list_of_duplicated_files:
        duplicate_new_pack = []
        for item in duplicate_pack:
            splitted = item.split('\t')
            file_name = splitted[0]
            dir_path = splitted[1]
            size = splitted [2]  # TODO: Use
            datetime = splitted[3]  # TODO: Use
            duplicate_new_pack.append(os.path.join(dir_path, file_name))
        processed_duplicate_items.append(duplicate_new_pack)

    return processed_duplicate_items


def create_symlink(src_path, dst_path):
    os.remove(src_path)
    time.sleep(2)
    os.symlink(src_path, dst_path)


def remove_file(path, dst_path):
    os.remove(path)


def do_nothing():
    print('Do nothing')


def print_cmd(letter, cmd, elem, alternative, method, params):
    print(f'{letter}) {cmd} {elem}')
    if alternative:
        print(f'  to {alternative}')
    return (letter, method, params)


def get_resolves_input(elements):
    print('Please select:')
    range_abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    command_list = []
    index_letter = 0
    for index, elem in enumerate(elements):
        cmd = 'delete'
        method = remove_file
        alternative = None
        command_elem = print_cmd(range_abc[index_letter], cmd, elem, alternative, method, params=elem)
        command_list.append(command_elem)
        index_letter += 1
        cmd = 'symlink'
        method = create_symlink
        alternative = elements[1] if index == 0 else elements[0]
        command_elem = print_cmd(range_abc[index_letter], cmd, elem, alternative, method, params=[elem, alternative])
        command_list.append(command_elem)
        index_letter += 1
    cmd = 'skip'
    command_elem = print_cmd(range_abc[index_letter], cmd, elem=None, alternative=None, method=do_nothing, params=None)
    command_list.append(command_elem)
    #
    cmd_char = input()  # Blocked call
    # Search command
    for item in command_list:
        cmd_expected_char = item[0]
        method = item[1]
        params = item[2]
        if cmd_expected_char == cmd_char:
            method(*params)
            break


def check_list(duplicated_elements):
    print('Check duplicated elements')
    for item in duplicated_elements:
        # Duplicated list
        duplicate_count = len(item)
        new_item = []
        for path in item:
            # One element in the duplicates
            print(path)
            if not os.path.exists(path):
                print(f'File does not exist, maybe there is no TODO: {path}')
                duplicate_count -= 1
            elif os.path.islink(path):
                print(f'File is link, maybe there is no TODO: {path}')
                duplicate_count -= 1
            else:
                new_item.append(path)
                # exists and not symlink
        if duplicate_count <= 1:
            print('There is no TODO, this issue is resolved')
        else:
            get_resolves_input(new_item)


if __name__ == '__main__':
    print('Duplicate resolver')

    duplicated_list = parse_duplicate_file()
    check_list(duplicated_list)


