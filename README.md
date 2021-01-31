# Warcraft Helper for Linux #

## What does it do ##

It sends Mouse and Keyboard Events to improve Warcraft: Orcs & Humans:

* Mark multiple units without pressing CTRL on your keyboard
* Scroll at the border of the screen
* Use mouse button 4 to move units
* Use mouse button 5 to harvest or attack

## Requirements ##

* Python 3
* python-evdev (Install with "pip install evdev")
* DOSBox
* Warcraft: Orcs and Humans
* Access to the Input Event Devices in /dev/input/ (Add your user to the group "input")

## How to use ##

1. Download warcraft-helper.py
2. Open warcraft-helper.py in a text editor
    1. Change MOUSE_DEVICE to your mouse. It should be the file in /dev/input/by-id/ thats ends with "-event-mouse"
    2. Change DOSBOX_ARGS to the way you start Warcraft inside DOSBox. eg.:
        * ["dosbox", "~/games/warcraft/WAR.EXE", "-exit"]
        * ["dosbox", "-c", "cd WARCRAFT", "-c", "WAR", "-c", "exit"]
3. Make warcraft-helper.py executable: "chmod +x warcraft-helper.py"
4. Run warcraft-helper.py: "./warcraft-helper.py"
