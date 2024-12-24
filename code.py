import time
import board
import usb_hid
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer
import neopixel

offset = 5
interval = 180
counter = 0
enabled = False

green = (10, 0, 0)
red = (0, 10, 0)
colors = [red, green]

staticpin = DigitalInOut(board.GP11)
staticpin.direction = Direction.OUTPUT
staticpin.value = True

btn = DigitalInOut(board.GP13)
btn.direction = Direction.INPUT
btn.pull = Pull.DOWN
switch = Debouncer(btn)

mouse = Mouse(usb_hid.devices)
pixels = neopixel.NeoPixel(board.GP16, 1)
pixels[0] = red

now = time.monotonic()

while True:
    switch.update()

    if switch.rose:
        enabled = not enabled
        counter += 1
        if counter > 1:
            counter = 0
        pixels[0] = colors[counter]

    if (now + interval) < time.monotonic() and enabled:
        mouse.move(0, offset)
        offset = -offset
        now = time.monotonic()

    time.sleep(0.01)
