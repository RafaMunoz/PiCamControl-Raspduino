PiCamControl-Raspduino
===================
System to control the position through 2 servos and monitoring of a Pi camera with a low latency through a graphical interface. In this repository is the code base of the systems and how to implement it.

![PiCamControl graphical interface](https://github.com/RafaMunoz/PiCamControl-Raspduino/blob/master/images/vista_previa.png)

----------

Materials
-------------
We used the following components::

 - 1x Raspberry 2. 
 - 1x Arduino Uno rev. 2. 
 - 2x Servo.
 - 1x Pi Camera.
 - 1x Power supply.

----------
System design
-------------
In the following image we can see how the different elements will be interconnected.

We have a PC in which we will have the graphical interface to visualize the Pi camera and control the positioning of the servos. The software that we will have in this device we can install also in the Raspberry Pi.

> For the preview it will be necessary that we have MPlayer installed.

Then on the Raspberry Pi we will connect the Pi Camera and the Arduino through a serial connection.

Finally in the Arduino we will connect the 2 servos for the horizontal and vertical positioning of the camera.

![PiCamControl General Connection](https://github.com/RafaMunoz/PiCamControl-Raspduino/blob/master/images/conexion_general.png)



In the next image we see the way to connect the Servos to the Arduino. The servo connected to the PIN 9 will take care of the horizontal positioning and the servo connected to the PIN 10 will take care of the vertical positioning.

> It is advisable to connect an external power supply for the servos and connect the GND of the power supply and the Arduino.

![PiCamControl Connection Arduino](https://github.com/RafaMunoz/PiCamControl-Raspduino/blob/master/images/conexion_arduino.png)

----------
Installation
-------------
For installation the first thing we are going to do is to download or clone this repository on a PC or Raspberry Pi.

> `$ git clone https://github.com/RafaMunoz/PiCamControl-Raspduino.git`

In the folder called raspberry we will find two files.

 - PiCamControl.py 
 - picam_server.py 
 
**PiCamControl.py** is the graphical interface with which we are going to control the positioning of the servos and will be in charge to start MPlayer for the preview of the camera.
This file will need to be copied to the PC or the Raspberry Pi.

**picam_server.py** will have to be copied to the Raspberry Pi. This socket will receive the commands that we send from the graphic interface and the Arduino will be communicated to them.


In the Arduino folder we will find the software that we need to compile in our Arduino.

 - aruduino.ino

----------
Settings
-------------
At the beginning of the python scripts we will find a series of settings that we must configure. The most important is the **PORT** settings found in the picam_server.py file. In the indicated to which serial port of the Raspberry Pi is connected our Arduino.
To see in which port we have connected our Arduino we can execute the following command:

    ls /dev/tty*
 And we'll see that it gives us a list of different devices. Then we simply connect the Arduino, we execute the command again and we will see how an additional device will appear. In my case my Arduino appears as: **/dev/ttyUSB0**.
 

    # Values for connection with Arduino
    PORT = "/dev/ttyUSB0"
    BAUDRATE = 9600
    
    # Values for connection with Client Socket
    # By default it allows all computers
    HOST = ""
    SOCKET_PORT = 9999
    
    # Values for Netcat
    PORTNETCAT = 2222
    
    # Values for PiCamera
    WIDTH = 800
    HEIGTH = 600
    FPS = 20


In case we need to invert the rotation of the servos we can put the settings **REVERSE_X** and **REVERSE_Y** to 1 in the file PiCamControl.py

    # Values for Netcat
    PORTNETCAT = 2222
    
    # This configuration reverses the direction of rotation of the servos. Values ​​0 or 1
    REVERSE_X = 0
    REVERSE_Y = 0

----------
Service
-------------
To run our control and preview system we must execute the following commands.

First:

    $ python picam_server.py


Second:

    $ python PiCamControl.py

In raspberry we can also create a service so that it starts automatically every time it boots. To do this we can execute the following commands:


> The following service is created for the case where we have
> picam_control.py in the path: **/home/pi**.
>  
> In case you have the file in another route you only have to change the settings:

We create the file picamcontrol.service.

    $ sudo nano /etc/systemd/system/picamcontrol.service

Copy the following code and save the file using <kbd>Ctrl+O</kbd> and <kbd>Ctrl+X</kbd>.

    [Unit]
    Description=PiCamControl Service
    After=network.target
   
    [Service]
    Type=simple
    ExecStart=/usr/bin/python /home/pi/picam_server.py
    WorkingDirectory=/home/pi
    Restart=always
    RestartSec=3
    
    [Install]
    WantedBy=multi-user.target


We give executable permissions to the service and the script.

    $ sudo chmod +x /etc/systemd/system/picamcontrol.service
    $ sudo chmod +x /home/pi/picam_server.py

And finally we execute:

    $ sudo systemctl enable picamcontrol.service
    $ sudo systemctl daemon-reload

Now we can start / stop the service with the following commands:

    $ sudo systemctl start picamcontrol
    $ sudo systemctl stop picamcontrol