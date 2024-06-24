import re
import os
import datetime
from os import listdir
from os.path import isfile, join, isdir, getmtime


# TODO Expand for other formats and deal with problems until everything is perfect!
formats = {'desired': "^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})_\d+.(jpg)$",  # My format yyyymmdd_hhmmss_{unique_number}.jpg
           'samsung': "^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2}).(jpg)$",      # Samsung format yyyymmdd_hhmmss.jpg
           'whatsapp': "^IMG-(\d{4})(\d{2})(\d{2})-WA\d{4}.(jpg)$"}     # Whatsapp format IMG-yyyymmdd-WAnnnn.jpg

root_location = r"E:\Graeme_Files\Graeme_Pictures"

n = 1  # Unique number for every picture


def get_folders(folder_location):
    return [f for f in listdir(folder_location) if isdir(join(folder_location, f))]


def get_file_names(folder_location):
    return [f for f in listdir(folder_location) if isfile(join(folder_location, f))]


def return_formatted_name(year, month, day, hour, minute, second, number, extension):
    # Keep time in format to keep in a good order within same day
    return f"{year}{month}{day}_{hour}{minute}{second}_{number}.{extension}"


def rename_files_in_folder(folder_location, unique_number):
    file_names = get_file_names(folder_location)

    for file_name in file_names:
        y, mo, d, h, mi, s, ext = None, None, None, None, None, None, None

        # Check known formats to get from file name
        for format_name, format_ in formats.items():
            match = re.match(format_, file_name)
            if match is not None:
                if format_name in ['desired', 'samsung']:
                    y, mo, d, h, mi, s, ext = match.groups()
                elif format_name in ['whatsapp']:
                    y, mo, d, ext = match.groups()
                    m_time = getmtime(join(folder_location, file_name))
                    date_time = datetime.datetime.fromtimestamp(m_time)
                    h = datetime.datetime.strftime(date_time, '%H')
                    mi = datetime.datetime.strftime(date_time, '%M')
                    s = datetime.datetime.strftime(date_time, '%S')
                break

        if None not in [y, mo, d, h, mi, s, ext]:
            new_file_name = return_formatted_name(y, mo, d, h, mi, s, unique_number, ext)
            os.rename(join(folder_location, file_name), join(folder_location, new_file_name))
            unique_number += 1
            print(f"Renamed a file in {folder_location}")

    return unique_number


# Get all folders to rename
all_folders = []


def parse_folder_for_folders(folder_location):
    folders = get_folders(folder_location)

    if len(folders) != 0:
        for folder_name in folders:
            full_path = join(folder_location, folder_name)
            all_folders.append(full_path)
            parse_folder_for_folders(full_path)


parse_folder_for_folders(root_location)

for folder_path in all_folders:
    n = rename_files_in_folder(folder_path, n)

print('Done')
