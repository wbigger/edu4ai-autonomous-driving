# EDU4AI - Autonomous Driving Cars

This tutorial is part of the following EU funded project:

Edu4AI - Artificial Intelligence and Machine Learning to Foster 21st Century Skills in Secondary Education, in the framework of Erasmus+, Grant Agreement VG-IN-BY-20-25-077366


# Final result
![Robot, complete](robot.jpg)

# Get the parts
For our project we used the following parts
- [ ] Raspberry Pi version 4
- [ ] MicroSD card minimum size 16 GB
- [ ] Two wheels with rubber tires
- [ ] L298N Motor Drive Controller
- [ ] USB 5V power bank, with at least a good quality [2.5A power output](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/) (USB-C)
- [ ] 9V battery with clip
- [ ] USB webcam with hole for tripod
- [ ] Jumper wires F/F and F/M, to connect everything
- [ ] M2.5 and M3 screws, assorted lengths
- [ ] double-sided tape or Patafix
- [ ] 1/4" slotted screw (for camera)
- [ ] ball castor (we used a two-holes ball castor, with distance of 38mm between them)
- [ ] a micro-HDMI to HDMI cable or adapter to connect your Raspberry to a monitor

Optional:
- [ ] Raspberry case

Just as reference, you can see the list part [here](https://www.amazon.it/hz/wishlist/ls/2XP57TFXQNB8H?ref_=wl_share).

## Chassis
More information on how we created the chassis in the [dedicated page](./chassis).

## Power
In this project, we use two separated power source:
- a power bank for the Raspberry PI
- a 9V battery for motors

We cannot use the Raspberry Pi, since its output are not suitable for supporting loads, so we need an additional power supply, and a 9V battery is a good solution. 

According to [official documentation](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/), we can use a good quality 2.5A power bank to power the board if the downstream USB peripherals consume less than 500mA in total. We have only one peripheral, the webcam, that should stay inside this limit.


# L298N <-> Raspberry Pi GPIO pins

| L298N | Raspberry PI GPIO PIN | Raspberry Pi pin description |
|---|---|---|
| IN1 | 29 | GPIO5 |
| IN2 | 31 | GPIO6 |
| IN3 | 37 | GPIO26 |
| IN4 | 36 | GPIO16 |
| GND | 39 | GND |

![Robot rear with connections](connections.jpg)
![Robot top](robot-top.jpg)

# Prepare the SD Card
We used the official [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/).

We tested the project with:
- Raspberry Pi OS with desktop
- Release date: April 4th 2022
- System: 32-bit
- Kernel version: 5.15
- Debian version: 11 (bullseye)

# Set up the Raspberry Pi

Connect a mouse, keyboard and monitor to your Raspberry Pi and power it. Follow configuration and initialisation instructions if any.

To upgrade the Operating System, open a Terminal window and execute:

```sh
sudo apt update
sudo apt -y dist-upgrade
```

Answer 'yes' to any prompts.

Now we should install VNC (Virtual Network Computing) to access the Robot remotely using our Windows laptop.

Install VNC server on the Raspberry Pi

```sh
sudo apt update
sudo apt install realvnc-vnc-server
```

Then from the Pi menu enable the VNC by:
Raspberry Pi Menu->Preferences->Raspberry Pi Configuration->Interface tab->Enable VNC and click OK.

After that you should install a VNC viewer on your Windows laptop; you can download it [here](https://www.realvnc.com/en/connect/download/viewer/).

Get the IP from the Raspberry using:

```sh
hostname -I
```

Put this IP into the VNC viewer on your laptop.


# Move the motors
We are now almost ready to actually move the motors.

On the Raspberry PI, click on the menu on the top right->Programming->Thonny Python IDE.

```py
from gpiozero import Robot
myRobot = Robot(right=(26,16), left=(5,6))

# Argument is the speed, from 0 (stop) to 1 (max speed, default),
# leave empty for default.
# I suggest to start with 0.6, and eventually change it.
# Use these commands on the intearctive console.

myRobot.forward(0.6)  # go forward
myRobot.backward(0.6) # go backward
myRobot.left(0.6) # turn left
myRobot.right(0.6) # turn right
myRobot.stop() # turn right
```

# Train your model
Go to [Teachable Machine](https://teachablemachine.withgoogle.com/train).

Use "Standard Image Model"

After training, export as Tensorflow Lite -> Quantized

# Test trained model with your car

Open a terminal on Raspberry Pi and install dependencies.

```sh
sudo apt update
sudo apt -y install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt -y install libxvidcore-dev libx264-dev
sudo apt -y install libatlas-base-dev

pip3 install opencv-python

pip3 install tflite-runtime

pip3 install numpy --upgrade
```

Create a folder on Raspberry, unzip the Tensorflow model and download the [classify_webcam.py](classify_webcam.py) example inside it.

Inside a terminal, test that everything works:

```sh
python3 classify_webcam.py --model myModel/model.tflite -–labels myModel/labels.txt
```










