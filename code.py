import time
import board
import usb_hid
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

offset = 5
interval = 180
enabled = False

staticpin = DigitalInOut(board.GP11)
staticpin.direction = Direction.OUTPUT
staticpin.value = True

btn = DigitalInOut(board.GP13)
btn.direction = Direction.INPUT
btn.pull = Pull.DOWN
switch = Debouncer(btn)

mouse = Mouse(usb_hid.devices)

now = time.monotonic()

while True:
    switch.update()

    if switch.rose:
        enabled = not enabled

    if (now + interval) < time.monotonic() and enabled:
        mouse.move(0, offset)
        offset = -offset
        now = time.monotonic()

    time.sleep(0.01)
