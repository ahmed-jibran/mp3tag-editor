#!/usr/bin/python
import os
import sys
import csv
import argparse
from datetime import datetime
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def update_tag(filepath: str, tag: dict):
    """
    Update tag of a give MP3 file with new tag info provided as key/pair value.
    :param filepath: MP3 file path
    :param tag: tag dictionary to create a new tag
    :return: None
    """
    print(f"Processing file {filepath}")
    audio = MP3(filepath, ID3=EasyID3)
    audio.delete()
    for key, item in tag.items():
        if key != "filename":
            audio[key] = item
    iso_date = datetime.now().isoformat()
    audio['date'] = iso_date
    audio.save()


if __name__ == "__main__":
    # Argument parser the script
    parser = argparse.ArgumentParser(
        prog='ID3 Tag Editor',
        description='Edit ID3 Tags for MP3 files using a CSV file'
    )
    parser.add_argument('-d', '--dir', metavar="<MP3_DIR>",
                        type=str, dest='mp3_dir', required=True,
                        help='Directory with MP3 files')
    parser.add_argument("-i", "--id3", metavar="<ID3_CSV.csv>",
                        type=str, dest="id3_csv", required=True,
                        help="Input CSV file with ID3 Tags")

    parser.add_argument("-r", "--rename",
                        dest="rename_mp3", action='store_true', default=False,
                        help="Rename MP3 file with title value")

    args = parser.parse_args()

    id3_csv = args.id3_csv
    mp3_dir = args.mp3_dir
    rename_mp3 = args.rename_mp3

    files = dict()
    # Populate file paths and filenames
    for filename in os.listdir(mp3_dir):
        f = os.path.join(mp3_dir, filename)
        if os.path.isfile(f):
            files[filename] = f

    # mutagen EasyID3 interface does not contain comments ID3 tag
    EasyID3.RegisterTextKey('comment', 'COMM')

    # Create a new ID3 CSV in case filenames has to be updated with the titles
    # from ID3 csv file
    if rename_mp3:
        d, f = os.path.split(id3_csv)
        csv_filename, _ = os.path.splitext(f)
        csv_filename = f"{csv_filename}_new.csv"
        # noinspection PyBroadException
        try:
            new_id3_csv_file = open(f"{os.path.join(d, csv_filename)}", mode='w')
        except (OSError, IOError) as e:
            print(f"error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Unexpected error:{sys.exc_info()[0]}")

    # Parse ID3 CSV
    with open(id3_csv, newline='') as csvfile:
        id3reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        if rename_mp3:
            # noinspection PyUnboundLocalVariable
            new_id3_csv = csv.DictWriter(new_id3_csv_file, fieldnames=id3reader.fieldnames)
            new_id3_csv.writeheader()

        for mp3info in id3reader:
            if mp3info['filename'] in files:
                mp3path = files[mp3info['filename']]
                # Update tag information with the new information
                update_tag(mp3path, mp3info)
                # Rename files to titles if needed and update new
                # ID3 csv file
                if rename_mp3:
                    d, _ = os.path.split(mp3path)
                    new_filename = f"{mp3info['title']}.mp3"
                    new_filepath = os.path.join(d, new_filename)
                    mp3info['filename'] = f"{mp3info['title']}.mp3"
                    new_id3_csv.writerow(mp3info)
                    os.rename(mp3path, new_filepath)

    if rename_mp3:
        new_id3_csv_file.close()
