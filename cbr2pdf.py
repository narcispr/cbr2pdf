#!/usr/bin/env python
# coding: utf-8

import os
from PIL import Image, ImageOps, ImageEnhance
from fpdf import FPDF
import argparse
from tqdm import tqdm


def correction(f, bw=False, contrast=True, brightness=1.0, resize=None, crop=(0,0,0,0)):
    "Given a file, open it with PIL and apply a brightness and contrast filter and save it as a new file"
    im = Image.open(f)
    if bw:
        im = ImageOps.grayscale(im)
    if crop != (0,0,0,0):
        im = im.crop((crop[0], crop[1], im.width - crop[2], im.height - crop[3]))

    if contrast:
        im = ImageOps.autocontrast(im, cutoff=3.0)
    if brightness != 1.0:
        # apply brightness filter
        enhancer = ImageEnhance.Brightness(im)
        im = enhancer.enhance(brightness)

    if resize is not None:
        im = im.resize((resize[0], resize[1]), Image.BICUBIC)
    
    return im


def jpg_to_pdf(files, output="output.pdf"):
    "Given a list of files, create a pdf with them"
    pdf = FPDF()
    print("Creating pdf...")
    
    for f in tqdm(files):
        # print progress bar with i out of len(files)
        pdf.add_page()
        pdf.image(f, 0, 0, 210, 297)
    print("Saving pdf...")
    pdf.output(output)

def cbr2pdf(path, bw=False, contrast=True, brightness=1.0, resize=None, crop=(0,0,0,0), output="output.pdf"):
    "Given a folder with image files, process them and convert them to pdf"
    
    # print("current path: ", current_path)
    # print("path: ", path)
    # print("output: ", output)
    # print("bw: ", bw)
    # print("contrast: ", contrast)
    # print("brightness: ", brightness)
    # print("resize: ", resize)
    # print("crop: ", crop)

    # get current folder
    current_path = os.getcwd()
    
    # move to working folder
    os.chdir(path)

    # Get all files in given folder
    files = [f for f in os.listdir() if os.path.isfile(f)]

    print("Processing files...")
    # create tmp folder
    try:
        os.mkdir("tmp")
    except FileExistsError:
        pass
    for f in tqdm(files):
        im = correction(f, bw=bw, contrast=contrast, brightness=brightness, resize=resize, crop=crop)
        im.save(os.path.join("tmp/" + f))

    # move to tmp folder
    os.chdir("tmp")

    # create PDF wth files in tmp folder
    jpg_to_pdf(files, os.path.join(current_path, output))

    # remove files in tmp folder and tmp folder
    for f in files:
        os.remove(f)
    os.chdir("..")
    os.rmdir("tmp")

if __name__ == "__main__":
    # get parameters from command line
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path', type=str, help='Path to the file')
    parser.add_argument('--bw', type=str, default="False", help='Black and white filter')
    parser.add_argument('--contrast', type=str, default="True", help='Automatic contrast filter')
    parser.add_argument('--brightness', type=float, default=1.0, help='Change brightness of the image (e.g., 1.3)')
    parser.add_argument('--width', type=int, default=None, help='Device width in pixels (Kindle 11th: 1072)')
    parser.add_argument('--height', type=int, default=None, help='Device height in pixels (Kindle 11th: 1448)')
    parser.add_argument('--crop_left', type=int, default=0, help='Crop original image left side in pixels')
    parser.add_argument('--crop_right', type=int, default=0, help='Crop original image right side in pixels')
    parser.add_argument('--crop_top', type=int, default=0, help='Crop original image top side in pixels')
    parser.add_argument('--crop_bottom', type=int, default=0, help='Crop original image bottom side in pixels')
    parser.add_argument('--output', type=str, default='output.pdf', help='Output file name')
    args = parser.parse_args()
    if args.width is not None and args.height is not None:
        resize = (args.width, args.height)
    else:
        resize = None
 
    cbr2pdf(args.path, resize=resize, bw=(args.bw=="True"), contrast=(args.contrast=="True"), brightness=args.brightness, 
            crop = (args.crop_left, args.crop_top, args.crop_right, args.crop_bottom), output=args.output)


