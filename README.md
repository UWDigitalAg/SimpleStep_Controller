Step Motor control
==================

For controlling a step motor with command line, you can use linact.py or using MapperGUI.py for a graphical interface.

Pre-requisites for MapperGUI.py
-------------------------------
inact.py and install PySimpleGUI (https://pysimplegui.readthedocs.io/en/latest/)

GUI allow user to control all 3 axis of the step motor (with or without checking the limit), give the current position of the step motor, current speed, control the speed of the step motor and initializes the stepper at its current position.

The "Move" button allows the user to move the step motor. The user can move the step motor in the 3 axis (X, Y and Z) and in the 2 directions (positive and negative).

The "Update x Velocity" button allows the user to set the speed of the step motor. The speed is set in steps per second.

When user click on the "Initialize" button, the stepper is initialized at its current position. The stepper is initialized at the position 0 when the program is launched.

When user click "Shutdown" button, the program is closed and the steppers will return to its initial position.

Pre-requisites for linact.py
----------------------------
periphery.py

Before user can control the step motor, the user must initialize the stepper at its current position.

PDF Manual
----------
Simple Step Product Manual-2.pdf
