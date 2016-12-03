"""image utils

Functions for creating ASCII art

"""

from bisect import bisect
import os
import random
from PIL import Image

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# greyscale.. the following strings represent
# 7 tonal ranges, from lighter to darker.
# for a given pixel tonal level, choose a character
# at random from that range.

GREYSCALE = [
    " ",
    " ",
    ".,-",
    "_ivc=!/|\\~",
    "gjez2]/(YL)t[+T7Vf",
    "mdK4ZGbNDXY5P*Q",
    "W8KMA",
    "#%$"
]

# using the bisect class to put luminosity values
# in various ranges.
# these are the luminosity cut-off points for each
# of the 7 tonal levels. At the moment, these are 7 bands
# of even width, but they could be changed to boost
# contrast or change gamma, for example.

ZONEBOUNDS = [36, 72, 108, 144, 180, 216, 252]


# open image and resize
# experiment with aspect ratios according to font
# Constants
VERBOSE = True


def draw_ascii(num):
    """Creates ascii string of a Pokemon.

    Retrieves a PNG Pokemon sprite and creates ASCII art using the Python Image
    Library (PIL).

    Args:
        num: An integer value for Pokemon number

    Returns:
        A string with the ASCII art.
    """
    img_file = os.path.join(DIRECTORY, 'sprites', '{:03d}.png'.format(num))
    image = Image.open(img_file)
    image = image.resize((104, 70), Image.BILINEAR)
    image = image.convert('L')  # convert to mono

    # now, work our way over the pixels
    # build up str

    build_string = ""
    for pos_y in range(0, image.size[1]):
        for pos_x in range(0, image.size[0]):
            lum = 255 - image.getpixel((pos_x, pos_y))
            row = bisect(ZONEBOUNDS, lum)
            possibles = GREYSCALE[row]
            build_string += possibles[random.randint(0, len(possibles) - 1)]
        build_string = build_string + '\n'

    check_string = build_string.split('\n')
    for string in check_string:
        if string.isspace():
            check_string.pop(check_string.index(string))
    return '\n'.join(check_string)
