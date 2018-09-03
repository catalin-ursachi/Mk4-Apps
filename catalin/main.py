""" Catalin's App
"""
___title___         = "Catalin's App"
___license___      = "MIT"
___dependencies___ = ["ugfx_helper", "sleep", "dialogs", "database"]
___categories___   = ["Other"]
___bootstrapped___ = False

import dialogs, ugfx_helper, ugfx, app, sleep
from tilda import Buttons

# initialize screen
ugfx_helper.init()
ugfx.clear()

# show text
ugfx.text(5, 5, "Hello World :)", ugfx.BLACK)

# waiting until a button has been pressed
while (not Buttons.is_pressed(Buttons.BTN_A)) and (not Buttons.is_pressed(Buttons.BTN_B)) and (not Buttons.is_pressed(Buttons.BTN_Menu)):
    sleep.wfi()

# closing
ugfx.clear()

dialogs.prompt_boolean("Is this a great device Y/N? :D")

app.restart_to_default()
