#!/usr/bin/env python3

import random
import argparse
import os
import shutil
from collections import defaultdict

from PIL import Image, ImageDraw, ImageFont
import imageio


def create_image(string, filename, wh, font):
        text = string
        img = Image.new('RGB', wh, color='black')
        drawing = ImageDraw.Draw(img)
        drawing.text((10, 10), text, fill='green', font=font)
        filename = '{}.gif'.format(filename)
        img.save(filename)
        return filename


def get_text_size(font, text):
    img = Image.new('RGB', (1, 1), color='black')
    drawing = ImageDraw.Draw(img)
    wh = drawing.textsize(text, font=font)
    return wh[0] + 20, wh[1] + 20


def create_gifv(file_list, output_basename):

    video_writer = imageio.get_writer("{}.gif".format(output_basename), mode='I', loop=0)

    img = ''

    for filename in file_list:
        img = imageio.imread(filename)
        video_writer.append_data(img)

    for _ in range(60):
        video_writer.append_data(img)

    video_writer.close()


def make_images(string, out_dir):
    font = ImageFont.truetype('/System/Library/Fonts/Monaco.dfont', 50)
    wh = get_text_size(font, string)

    previous_misses = defaultdict(list)
    min_char = 32
    max_char = 126
    target = string
    current = [chr(random.randint(min_char, max_char)) for i in range(len(target))]
    files = []
    current_string = ""
    iteration = 1
    while current_string != target:
        current_string = ''.join(current)
        filename = '{}{}'.format(out_dir, iteration)
        image = create_image(current_string, filename, wh, font)
        files.append(image)
        for idx in range(len(current)):
            if current[idx] != target[idx]:
                guess = ""
                while guess in previous_misses[idx]:
                    guess = chr(random.randint(min_char, max_char))

                current[idx] = guess
                previous_misses[idx].append(guess)

        iteration += 1
    return files


def clean_files(out_dir):
    shutil.rmtree(out_dir)


def main(args):
    out_dir = 'output/'
    os.mkdir(out_dir)
    print('Creating Frames')
    file_list = make_images(args.string, out_dir)
    print('Writing gif')
    create_gifv(file_list, args.outfile)
    print('Cleaning up')
    clean_files(out_dir)


if __name__ == "__main__":
    os.environ['IMAGEIO_FFMPEG_EXE'] = '/Users/aricmaddux/bin/ffmpeg'
    parser = argparse.ArgumentParser(prog='decrypt_gif', usage='%(prog)s text string')
    parser.add_argument("string", help="String to animate")
    parser.add_argument("outfile", help="The file to save the gif to", nargs='?')
    args = parser.parse_args()
    if not args.outfile:
        args.outfile = 'output'
    main(args)
