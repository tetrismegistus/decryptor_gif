#!/usr/bin/env python3

import random
import argparse
import string

from PIL import Image, ImageDraw, ImageFont

from Animation import Animation


CHARS = string.ascii_letters + string.digits + string.punctuation + " "
CHARSET_CHARS = set(CHARS)


class DecryptorGif:
    def __init__(self, message, fontfile="C:\\WINDOWS\\FONTS\\CONSOLA.TTF", fontsize=50, textcolor="green",
                 background="black", outputfile="decryptor.gif", margin=20):
        # FONT_FILE = '/System/Library/Fonts/Monaco.dfont'
        # FONT_FILE = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
        self.font = ImageFont.truetype(font=fontfile, size=fontsize)
        self.textcolor = textcolor
        self.background = background
        self.margin = margin
        self.animation = Animation(filename=outputfile, duration=.1)
        self.make_images(message)
        self.animation.save_gif()

    def create_frame(self, size, message_string):
        img = Image.new('RGB', size, color=self.background)
        drawing = ImageDraw.Draw(img)
        drawing.text((10, 10), message_string, fill=self.textcolor, font=self.font)
        self.animation.frames = img

    def get_text_size(self, text):
        img = Image.new('RGB', (1, 1), color='black')
        drawing = ImageDraw.Draw(img)
        size = drawing.textsize(text, font=self.font)
        return size[0] + self.margin, size[1] + self.margin

    def make_images(self, message_string):
        size = self.get_text_size(message_string)
        for i, guess in enumerate(self.crypt_strings(message_string)):
            self.create_frame(size, guess)

    @staticmethod
    def crypt_strings(message_string):
        previous_guesses = tuple(set() for _ in message_string)
        current_chars = random.choices(CHARS, k=len(message_string))
        current_string = "".join(current_chars)
        yield current_string
        while current_string != message_string:
            for idx, target_char in enumerate(message_string):
                if current_chars[idx] != target_char:
                    guess = random.choice(tuple(CHARSET_CHARS - previous_guesses[idx]))
                    previous_guesses[idx].add(guess)
                    current_chars[idx] = guess
            current_string = "".join(current_chars)
            yield current_string


def main():
    parser = argparse.ArgumentParser(prog='decrypt_gif', usage='%(prog)s text string')
    parser.add_argument("string", help="String to animate")
    parser.add_argument("outfile", help="The file to save the gif to",
                         nargs='?', default='output.gif')
    parser.add_argument("fontsize", help="The size of the font to use",
                        nargs='?', default=50)
    parser.add_argument("textcolor", help="The",
                        nargs='?', default="green")
    args = parser.parse_args()
    DecryptorGif(args.string, outputfile=args.outfile, fontsize=args.fontsize)


if __name__ == "__main__":
    main()
