import board
import displayio
import os
import gc
import pulseio
import random
import time
import microcontroller

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.text_area import TextArea

backlight = pulseio.PWMOut(microcontroller.pin.PB21)

max_brightness = 2 ** 15

fonts = list(filter(lambda x: x.endswith("bdf") and not x.startswith("."), os.listdir("/")))
fonts = [bitmap_font.load_font(x) for x in fonts]


print("fade up")
# Fade up the backlight
for b in range(100):
    backlight.duty_cycle = b * max_brightness // 100
    time.sleep(0.01)  # default (0.01)

demos = ["CircuitPython = Code + Community", "accents - üàêùéáçãÍóí", "others - αψ◌"]

splash = displayio.Group(max_size=len(fonts) * len(demos))
board.DISPLAY.show(splash)
max_y = 0
y = 2
for demo_text in demos:
    for font in fonts:
        print("Font load {}".format(font.name))
        area = TextArea(font, text=demo_text)
        area.y = y
        splash.append(area.group)

        y += area.height

        # Wait for the image to load.
        board.DISPLAY.wait_for_frame()
        gc.collect()
        print("mem free:", gc.mem_free())

# Wait forever
time.sleep(600)

# Fade down the backlight
for b in range(50, -1, -1):
    backlight.duty_cycle = b * max_brightness // 100
    time.sleep(0.005)  # default (0.005)

print("fade down")

    # splash.pop()
