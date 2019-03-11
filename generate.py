#!/usr/bin/env python3

import random
import argparse
import os
import shutil

from PIL import Image, ImageDraw, ImageFont
import imageio

FONT_FILE = '/System/Library/Fonts/Monaco.dfont'
# FONT_FILE = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
FONT_SIZE = 50
TEXT_COLOR = 'green'
BACKGROUND_COLOR='black'

TEMP_DIR = 'output/'

import string
# chars = tuple(chr(c) for c in range(ord(" "), ord("~") + 1))
chars = string.ascii_letters + string.digits + string.punctuation + " "
chars_set = set(chars)


def create_image(string, filename, size, font):
    img = Image.new('RGB', size, color=BACKGROUND_COLOR)
    drawing = ImageDraw.Draw(img)
    drawing.text((10, 10), string, fill=TEXT_COLOR, font=font)
    img.save(filename)
    return filename


def get_text_size(font, text, padding=20):
    img = Image.new('RGB', (1, 1), color='black')
    drawing = ImageDraw.Draw(img)
    size = drawing.textsize(text, font=font)
    return size[0] + padding, size[1] + padding


def assemble_gifv(image_filenames, output_filename, end_frames=60):
    video_writer = imageio.get_writer(output_filename, mode='I', loop=0)
    for filename in image_filenames:
        img = imageio.imread(filename)
        video_writer.append_data(img)
    for _ in range(end_frames):
        video_writer.append_data(img)
    video_writer.close()


def make_images(string, out_dir):
    font = ImageFont.truetype(font=FONT_FILE, size=FONT_SIZE)
    size = get_text_size(font, string)
    filenames = []
    for i, guess in enumerate(crypt_strings(string)):
        filename = out_dir + str(i) + ".gif"
        filenames.append(filename)
        create_image(guess, filename, size, font)
    return filenames


def crypt_strings(string):
    previous_guesses = tuple(set() for _ in string)
    current_chars = random.sample(chars, len(string))
    current_string = "".join(current_chars)
    yield current_string
    while current_string != string:
        for idx, target_char in enumerate(string):
            if current_chars[idx] != target_char:
                guess = random.choice(tuple(chars_set - previous_guesses[idx]))
                previous_guesses[idx].add(guess)
                current_chars[idx] = guess
        current_string = "".join(current_chars)
        yield current_string


def create_gif(string, filename):
    try:
        os.mkdir(TEMP_DIR)
        print("Creating Frames for string '{}'...".format(string))
        image_files = make_images(string, TEMP_DIR)
        print("Writing gif at '{}' ...".format(filename))
        assemble_gifv(image_files, filename)
    finally:
        print("Cleaning up temporary files ...")
        shutil.rmtree(TEMP_DIR)


def main():
    parser = argparse.ArgumentParser(prog='decrypt_gif', usage='%(prog)s text string')
    parser.add_argument("string", help="String to animate")
    parser.add_argument("outfile", help="The file to save the gif to",
                         nargs='?', default='output.gif')
    args = parser.parse_args()
    create_gif(args.string, args.outfile)


if __name__ == "__main__":
    main()
