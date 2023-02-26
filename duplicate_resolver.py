#!/usr/bin/python3
import sys


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
    return list_of_duplicated_files


if __name__ == '__main__':
    print('Duplicate resolver')

    parse_duplicate_file()


