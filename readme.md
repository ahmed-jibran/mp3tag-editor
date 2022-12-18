# Overview
A utility python script to modify ID3 tags of mp3 files in a bulk using an input CSV files which contains new tag information.
# Setup Environment

```commandline
# Verify if virtualenv is installed
which virtualenv

# In case virtualenv is not installed, install it using pip

python -m pip install --upgrade pip
pip install virtualenv

# Setup virtual environment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
# Updating ID3 Tags
Script intake directory for mp3 files and corresponding ID3 csv file
ID3 CSV file has filename column to match corresponding ID3 tag information from the CSV file.
Example ID3 CSV files are provided in id3-csv folder.
```
python id3-csv-edit.py --help
usage: ID3 Tag Editor [-h] -d <MP3_DIR> -i <ID3_CSV.csv> [-r]

Edit ID3 Tags for MP3 files using a CSV file

optional arguments:
  -h, --help            show this help message and exit
  -d <MP3_DIR>, --dir <MP3_DIR>
                        Directory with MP3 files
  -i <ID3_CSV.csv>, --id3 <ID3_CSV.csv>
                        Input CSV file with ID3 Tags
  -r, --rename          Rename MP3 file with title value

# Example
python id3-csv-edit.py --dir=$HOME/mp3files/ --id3=id3-tags.csv
```
