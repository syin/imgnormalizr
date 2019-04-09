#!/usr/bin/env python

import argparse
import glob
import math
from PIL import Image


def read_files(input_dir, max_image_size):
    image_types = ["*.png", "*.jpg", "*.jpeg"]
    # TODO: recursive
    files = [glob.glob(input_dir + image_type) for image_type in image_types]
    files_flattened = [item for sublist in files for item in sublist]
    for filename in files_flattened:
        transform_image(filename, max_image_size)


def transform_image(in_filename, max_image_size):
    print(in_filename)
    image = Image.open(in_filename)

    image = resize_image(image, max_image_size)
    write_output_image(image, in_filename)


def resize_image(image, max_image_size):
    print('old size', image.size)
    ratio = image.size[0] / image.size[1]

    if (image.size[0] >= image.size[1]):
        new_width = min(max_image_size, image.size[0])
        new_height = math.floor(new_width / ratio)
    else:
        new_height = min(max_image_size, image.size[1])
        new_width = math.floor(new_height * ratio)

    print('new size', (new_width, new_height))
    return image.resize((new_width, new_height))


def write_output_image(image, in_filename):
    filename_base = ".".join(in_filename.split(".")[:-1])
    filename_ext = in_filename.split(".")[-1]
    out_filename = "{filename_base}_resized.{filename_ext}"\
        .format(filename_base=filename_base, filename_ext=filename_ext)
    image.save(out_filename, optimize=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', help='Input directory', required=True)
    parser.add_argument('--max-size', '-s', help='Maximum image dimension (px; default 1200)', type=int)

    args = parser.parse_args()
    input_dir = args.input + ("/" if args.input[-1] else "")
    max_image_size = args.max_size or 1200
    if input_dir:
        read_files(input_dir, max_image_size)


if __name__ == '__main__':
    main()
