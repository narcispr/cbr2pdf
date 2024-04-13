# CBR to PDF scrip

This script is used to convert CBR files to PDF files. 

## Requirements

* Python 3.6 or higher
* Pilow Image Library
* fpdf library
* argparse library
* tqdm library

To install all the requirements, install firts Python 3.6 or higher and then run the following command:

```bash
pip install -r requirements.txt
```

## Usage

CBR files are compressed files that contain images. Rename first the CBR file to `*.zip` and then descompress it. This script has to be pointed (`path` parameter) to the folder containing the images.

```bash
usage: cbr2pdf.py [-h] [--path PATH] [--bw BW]
                  [--contrast CONTRAST] [--brightness BRIGHTNESS]
                  [--width WIDTH] [--height HEIGHT]
                  [--crop_left CROP_LEFT] [--crop_right CROP_RIGHT]
                  [--crop_top CROP_TOP] [--crop_bottom CROP_BOTTOM]
                  [--output OUTPUT]

```
Example:

```bash
python.exe .\cbr2pdf.py --path '..\Dragon Ball\Dragon Ball 1' --bw True --contrast True --brightness 1.2 --width 1072 --height 1448 --crop_bottom 20 --output dragon_ball_01.pdf
```

Set width and height to the screen size of your device. 


---
Narcís Palomeras
April 2024
