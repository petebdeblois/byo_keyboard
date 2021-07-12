
import time
import board
import adafruit_matrixkeypad
import usb_hid
import adafruit_dotstar
from digitalio import DigitalInOut
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# https://learn.adafruit.com/introducing-itsy-bitsy-m0/circuitpython-internal-rgb-led
led = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
led.brightness = 0.1
time.sleep(1)

# https://circuitpython.readthedocs.io/projects/matrixkeypad/en/latest/index.html
cols = [DigitalInOut(x) for x in (board.D11, board.D12, board.D13)]
rows = [DigitalInOut(x) for x in (board.D9, board.D10)]
keys = (
    (0, 1, 2),
    (3, 4, 5),
)

control_key = Keycode.SHIFT
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(kbd)

MEDIA = 1
KEY = 2
STR = 3

KEYMAP = {
    (0): (KEY, (Keycode.CONTROL, Keycode.SHIFT, Keycode.F3)),
    #(1): (STR, ["ahkobs"]),
    (1): (STR, ["ahkobs"]),
    (2): (KEY, (Keycode.WINDOWS, Keycode.L)),
    (3): (KEY, (Keycode.CONTROL, Keycode.SHIFT, Keycode.F2)),
    (4): (KEY, (Keycode.CONTROL, Keycode.SHIFT, Keycode.F1)),
    (5): (MEDIA, ConsumerControlCode.PLAY_PAUSE),
}

while True:
    keys = keypad.pressed_keys
    if keys:
        for key in keys:
            try:
                if KEYMAP[key][0] == KEY:
                    kbd.send(*KEYMAP[key][1])
                    led[0] = (0, 255, 255)
                    time.sleep(0.2)
                    led[0] = (0, 0, 0)
                elif KEYMAP[key][0] == STR:
                    keyboard_layout.write(*KEYMAP[key][1])
                    led[0] = (100, 255, 255)
                    time.sleep(0.2)
                    led[0] = (0, 0, 0)
                else:
                    cc.send(KEYMAP[key][1])
                    led[0] = (255, 255, 255)
                    time.sleep(0.2)
                    led[0] = (0, 0, 0)
            except ValueError:  # deals w six key limit
                pass
    time.sleep(0.1)
