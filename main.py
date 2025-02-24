# SPDX-FileCopyrightText: 2020 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import requests

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

# Create two lines of text to scroll. Besides changing the text, you can also
# customize the color and font (using Adafruit_CircuitPython_Bitmap_Font).
# To keep this demo simple, we just used the built-in font.
# The Y coordinates of the two lines were chosen so that they looked good
# but if you change the font you might find that other values work better.
line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xEB6E1F,
    text="")
line1.x = display.width
line1.y = 8

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,
    text="")
line2.x = display.width
line2.y = 24

line3 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,
    text="")
line3.x = 0
line3.y = 16


# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line1)
g.append(line2)
g.append(line3)
display.root_group = g

# This function will scoot one label a pixel to the left and send it back to
# the far right if it's gone all the way off screen. This goes in a function
# because we'll do exactly the same thing with line1 and line2 below.

def GameUpdate(text):
    print(f'Updating {text}')
    line1.text, line2.text = "", ""
    line3.text = text

    t = 0
    while t != 30:
        scroll(line3)
        t += 0.5
        display.refresh(minimum_frames_per_second=0)
        time.sleep(0.5)
    return None

def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width

# This function scrolls lines backwards.  Try switching which function is
# called for line2 below!


def reverse_scroll(line):
    line.x = line.x + 1
    line_width = line.bounding_box[2]
    if line.x >= display.width:
        line.x = -line_width


def get_astros_scores(data):
    teams = data["game"]["teams"]

    # Determine which team is the Astros
    if teams["away"]["team"]["name"] == "Houston Astros":
        astros = teams["away"]
        other_team = teams["home"]
    else:
        astros = teams["home"]
        other_team = teams["away"]

    astros_score = f'{astros["score"]} {astros["team"]["name"]}'
    other_team_score = f'{other_team["score"]} {other_team["team"]["name"]}'

    return astros_score, other_team_score

# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.


def get_astros_scores():
    response = requests.get('https://neon-code.vercel.app/api/astros-playing')

    data = response.json()
    if data["playing"] == False:
        return None

    teams = data["game"]["teams"]

    # Determine which team is the Astros
    if teams["away"]["team"]["name"] == "Houston Astros":
        astros = teams["away"]
        other_team = teams["home"]
    else:
        astros = teams["home"]
        other_team = teams["away"]

    astros_score = f'{astros["score"]} - {astros["team"]["name"]}'
    other_team_score = f'{other_team["score"]} - {other_team["team"]["name"]}'

    return astros_score, other_team_score

while True:
    game = get_astros_scores()
    if game == None:
        line1.text = f"No game playing"
        line2.text = f"Waiting for a game to start"
    line1.text, line2.text = game
    scroll(line1)
    reverse_scroll(line2)
    display.refresh(minimum_frames_per_second=0)
    time.sleep(0.05)
