#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import serial
import socket
import subprocess

# *******************************************
# ************** CONFIGURATION **************
# *******************************************

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


# *******************************************
# *******************************************


# Send coordinates to the servos
def posicion(px, py):
    coordinates = "px" + str(px) + ":py" + str(py)
    arduino.write(coordinates + "\n")
    return coordinates


# Send reply to socket client
def cs_response(msgsend):
    clientsocket.send(msgsend)
    clientsocket.close()
    print(msgsend)


# Others parameters
y = 90
x = 90
speed = 5
video = 0
statusmpl = 0
pid = 0

msg = ""

# Connection with Arduino
arduino = serial.Serial(PORT, BAUDRATE, timeout=1)

# Connection with Client Socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, SOCKET_PORT))
serversocket.listen(5)

# Send default position (90,90)
posicion(x, y)

while True:

    clientsocket, addr = serversocket.accept()
    key = clientsocket.recv(1024)

    try:

        if re.search("^x[0-9]{1,3}:y[0-9]{1,3}$", key):
            arduino.write(key + "\n")
            msg = key

        elif key == "mpl":
            if statusmpl == 0:
                command = "/opt/vc/bin/raspivid -t 0 -w " + str(WIDTH) + " -h " + str(HEIGTH) + " -hf -fps " + str(FPS) + " -o - | nc " + str(addr[0]) + " " + str(PORTNETCAT)
                proc = subprocess.Popen(command, shell=True)
                pid = proc.pid
                statusmpl = 1
                msg = "MP Start"
            else:
                command = "pkill -P " + str(pid)
                subprocess.Popen(command, shell=True)
                statusmpl = 0
                msg = "MP Close"

        else:
            msg = "Incorrect: " + str(key)

        cs_response(msg)


    except:
        msg = "ERROR"
        cs_response(msg)
