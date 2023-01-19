# dojocon-micropython
Workshop micropython for Dojocon Belgium

This repo contains the content of a workshop for Dojocon Belgium 2023, a [CoderDojo Belgium](https://www.coderdojobelgium.be) conference for and by the volunteers.

Goals of this workshop:

1. For those new to hardware/electronics, it will be a gentle introduction the this wonderfull world
1. For those having some experience with Arduino, I hope the workshop will provide some hands-on experience to how the interactivity of micropython lowers the learning curve to start with hardware/electronics

# Our Project
In this workshop, we will automate the Chrome dino game using a servo that presses the space bar, and a light dependend resistor. We'll use micropython the do the coding and benefit from the interactivity of the python REPL to figure out the settings for our servo and resistor.

![Automating the chrome dino game](media/dino-game.gif)

# Before we start - your dev environment
Before we can start, we'll need some things to setup.

## Editor
We'll need an editor to write our python code and to interact with our microcontroller.

Feel free to use whatever editor you like, for dojo's I highly recommend (Thonny)[https://thonny.org/], the Python Editor for beginners. You'll find download links for your platform on the home page.

## Hardware
We'll use an ESP32-based board, the ttgo t-display.
![liligo ttgo t-display](media/esp32-ttgo-t-display.jpg)

I like this board because it is inexpensive, has a display, has 2 physical buttons and has a 5V pin. Mind that the ESP32 runs on 3.3V, and all the I/O pins can only deal with 3.3V, 5V might fry your board. The 5V will only work if the ESP32 is powered by USB, and is ideal to power Neopixels or servo's. For steering those, a PWM signal of 3.3V is enough, so driving them with this board is perfectly possible.

You might need to install a specific driver. On Windows I saw little to no problems (caveat, I don't have a windows machine myself, many of our ninja's have...), on Mac, you need to install a specific driver, that can be found at https://github.com/Xinyuan-LilyGO/TTGO-T-Display. 

Once the driver is installed, you might see the microcontroller pop up twice in your list of connected devices as
```
/dev/cu.usbmodem<some numbers and letter here>
```
or as
```
/dev/cu.wchusbserial<letters and numbers>
```
It's the last one you'll need.

## Micropython
We need to install, or *flash* micropython on the microcontroller. You can find ready made binaries on the [Micropython](https://micropython.org/) site in the download section.

If you want to use the display of this board, you'll need a special firmware, since the driver for this display is written in c/c++ with python bindings. (note: In this workshop, we will not be using the display)

So download the firmware at: https://github.com/russhughes/st7789_mpy/blob/master/firmware/T-DISPLAY-ESP32/firmware.bin

Flashing the firmware can be done from within Thonny.

1. Connect the ESP32 via a USB-C cable to your computer
1. Fire up Thonny
1. In the  __Run__ (uitvoeren) menu, choose __Configure Interpreter__
1. Choose MicroPython (ESP32)
1. In the same dialog, click __install or update MicroPython__ at the bottom right of the dialog box
1. Choose the port at which your ESP32 is connected and select the firmware.bin file you just downloaded. Don't forget the choose the right one (see above)
1. Click install. This might take a one to two minutes to complete

Once flashed, you can connect Thonny to the ESP32 by clicking on the lower right hand side corner of Thonny. You should see MicroPython (ESP32) * Port there...

Once clicked, you will get access to a REPL, an interactive Python shell that is actually running on the ESP32. In there, you can import module or run python code interactively.

# Let's start developing

## The Electronics
For this project, we'll need:

- an ESP32
- a simple servo
- an LDR - light dependent resistor - the more light, the lower the resistance
- a 10kΩ resistor
- jumperwires
- some tape

Here's a schema of the entire project. 

![electrical schema](media/dojocon-dino-fun_bb.png)


Don't start building this entire schema just yet, we'll take it one step at the time ;)

## Step 1: Using a servo

```
Important: when fiddling with wires, always disconnect the ESP32!
```

Start with building the servo-related part of the schema.

Servo's typically need 5V (red wire), a ground (black wire) and a PWM signal (yellow wire).

Use pin 2 for the signal.

Once built, connect the ESP32 via USB again.

MicroPython does not have a servo class (it does have a PWM class), feel free to either figure out how servo's and PWM works, or use [servo.py](src/servo.py) ;)

Copy the (src/servo.py) in an empty directory locally and open that directory in Thonny.

Connect the ESP32, make sure Thonny is connected, right-click servo.py and choose ```upload to /```. The file is now uploaded to the ESP32 and can be imported via the REPL

```python
import servo.py
```

Play a bit with the servo, make sure it works correctly

```python
import machine

s = servo.Servo(machine.Pin(2))
s.write_angle(90)
```

Pressing the arrow-up/arrow-down key in Thonny, when in the REPL, brings back earlier commands.

Place the servo on your keyboards, use tape if needed. Find out interactively what angles you need to press and release the space bar.
 
Next, make a new file, call is spel.py, and, based upon the values of the servo, create a function that presses the space bar every few seconds.

Tip:
```python
# the time module has a sleep function
import time

#sleep for 2 seconds
time.sleep(2)
```

Copy over your spel.py file, import it in the REPL and try it out.

If it's not working as you expected, don't worry, you can edit the file and upload again.
```
Changes will not immediately take effect, you have to restart your micropython. Pressing crtl+d will restart the micropython. When you import your file now, you'll see the new code in action.
```

## Step 2: Using an LDR (Light Dependent Resistor)
Next up: sensing if an obstacle is approaching the dino. For that, we'll be using a LDR. This resistor has a low resistance when lit, and a very high one when in the dark.

We can't measure resistance directly, but we can measure voltages. Build the necessary wiring as per our schema. Use pin 32 for measuring the voltage over the LDR. This value will be low in low light, high when lit. Don't forget to disconnect the ESP32 when working on the wiring!

Once wiring is done,  have a look at [ldr.py](src/ldr.py).

This file contains a little class that uses the ADC-class to deal with analogue inputs.

Let's play with our sensor:
```python
import ldr

r = ldr.LDR(32)

print(r.value())
```

Do this a couple of times, cover the ldr and see how the value changes.

Put the print statement in a loop and print out a value every few milliseconds.

## Bringing it all together
Now it's time to get to the real deal.

Open Chrome and go to [chrome://dino](chrome://dino) (or switch of your wifi and surf to any site in chrome ;) )

Look how the sensor readout changes when an obstacle passes by.

Tip: you might want to increase the brightness of your screen to increase contrast.

Once you have a feel of the difference between full brightness and a cactus passing by, you can start changing your spel.py to make the dino jump whenever the sensor detects a passing obstacle.

For the impatient, at [src/spel.py](src/spel.py) you can find some inspiration.

Experiment away with timing, the placeing of the sensor, etc..

And most of all, have fun :)

# Wrapping up

I hope this workshop gave you an idea on how the interactivity of micropython makes hardware and electronics more accessible for coaches and ninja's :)
