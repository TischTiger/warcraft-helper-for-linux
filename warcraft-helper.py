#!/usr/bin/env python
from evdev import InputDevice, UInput
from evdev.ecodes import *
from subprocess import Popen
from time import sleep


MOUSE_DEVICE = '/dev/input/by-id/usb-PixArt_OpticalMouse-event-mouse'
DOSBOX_ARGS = ['/usr/bin/dosbox', '-c', 'cd WARCRAFT', '-c', 'WAR', '-c', 'exit']
SCROLL_SENSITIVITY = 1
SCROLL_SCREEN_SIZE = (640, 480)


keyboard = UInput()
mouse = InputDevice(MOUSE_DEVICE)

dosbox = Popen(DOSBOX_ARGS)

button_left = False
button_ctrl = False
ignore_count = 0

x = SCROLL_SCREEN_SIZE[0] // 2
y = SCROLL_SCREEN_SIZE[1] // 2


for mouse_event in mouse.read_loop():
    
    # check if dosbox is still running
    if not dosbox.poll() is None:
        break

    # set x, y and button_left
    if mouse_event.type == EV_REL and mouse_event.code == REL_X:
        x += mouse_event.value
    elif mouse_event.type == EV_REL and mouse_event.code == REL_Y:
        y += mouse_event.value
    elif mouse_event.type == EV_KEY and mouse_event.code == BTN_LEFT:
        if ignore_count == 0:
            button_left = bool(mouse_event.value)
        else:
            ignore_count -= 1
    elif mouse_event.type != EV_KEY:
        continue

    # hold ctrl to mark multiple units
    if mouse_event.type == EV_REL and button_left and not button_ctrl:
        button_ctrl = True
        keyboard.write(EV_KEY, KEY_LEFTCTRL, 1)
        keyboard.syn()
        mouse.write(EV_KEY, BTN_LEFT, 0)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        sleep(0.05)
        mouse.write(EV_KEY, BTN_LEFT, 1)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        ignore_count = 2
    elif not button_left and button_ctrl:
        button_ctrl = False
        keyboard.write(EV_KEY, KEY_LEFTCTRL, 0)
        keyboard.syn()

    # scroll screen
    while x < 0:
        keyboard.write(EV_KEY, KEY_LEFT, 1)
        keyboard.write(EV_KEY, KEY_LEFT, 0)
        keyboard.syn()
        x += SCROLL_SENSITIVITY
    while x > SCROLL_SCREEN_SIZE[0]:
        keyboard.write(EV_KEY, KEY_RIGHT, 1)
        keyboard.write(EV_KEY, KEY_RIGHT, 0)
        keyboard.syn()
        x -= SCROLL_SENSITIVITY
    while y < 0:
        keyboard.write(EV_KEY, KEY_UP, 1)
        keyboard.write(EV_KEY, KEY_UP, 0)
        keyboard.syn()
        y += SCROLL_SENSITIVITY
    while y > SCROLL_SCREEN_SIZE[1]:
        keyboard.write(EV_KEY, KEY_DOWN, 1)
        keyboard.write(EV_KEY, KEY_DOWN, 0)
        keyboard.syn()
        y -= SCROLL_SENSITIVITY

    # mouse button 4 and 5
    if mouse_event.type == EV_KEY and mouse_event.code == BTN_SIDE and mouse_event.value == 1:
        keyboard.write(EV_KEY, KEY_M, 1)
        keyboard.write(EV_KEY, KEY_M, 0)
        keyboard.syn()
        sleep(0.05)
        mouse.write(EV_KEY, BTN_LEFT, 1)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        sleep(0.05)
        mouse.write(EV_KEY, BTN_LEFT, 0)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        ignore_count = 2
    elif mouse_event.type == EV_KEY and mouse_event.code == BTN_EXTRA and mouse_event.value == 1:
        keyboard.write(EV_KEY, KEY_H, 1)
        keyboard.write(EV_KEY, KEY_H, 0)
        keyboard.write(EV_KEY, KEY_A, 1)
        keyboard.write(EV_KEY, KEY_A, 0)
        keyboard.syn()
        sleep(0.05)
        mouse.write(EV_KEY, BTN_LEFT, 1)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        sleep(0.05)
        mouse.write(EV_KEY, BTN_LEFT, 0)
        mouse.write(EV_SYN, SYN_REPORT, 0)
        ignore_count = 2


keyboard.close()
mouse.close()
