#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import socket
import subprocess
from tkinter import *

# *******************************************
# ************** CONFIGURATION **************
# *******************************************

# Values for Netcat
PORTNETCAT = 2222

# This configuration reverses the direction of rotation of the servos. Values ​​0 or 1
REVERSE_X = 0
REVERSE_Y = 0

# *******************************************
# *******************************************


# Send position to Raspberry Pi
def send_position():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        msg = "x" + str(positionX.get()) + ":y" + str(positionY.get())
        s.connect((host.get(), port.get()))
        s.send(msg)
        s.recv(1024)
        s.close()
        cnx.set("OK")
        color.set("#05c905")
        conexion.configure(fg=color.get())

    except:
        cnx.set("ERROR")
        color.set('red')
        conexion.configure(fg=color.get())


# Send info to Raspberry Pi
def send(parameter):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host.get(), port.get()))
        s.send(parameter)
        s.recv(1024)
        s.close()
        cnx.set("OK")
        color.set("#05c905")
        conexion.configure(fg=color.get())

    except:
        cnx.set("ERROR")
        color.set("red")
        conexion.configure(fg=color.get())


# Reset postion servos
def reset_position():
    positionX.set(90)
    positionY.set(90)
    send_position()


# Calculate position
def px_max():
    if positionX.get() + speed.get() > 180:
        positionX.set(180)
    else:
        positionX.set(positionX.get() + speed.get())

    send_position()


def px_men():
    if positionX.get() - speed.get() < 0:
        positionX.set(0)
    else:
        positionX.set(positionX.get() - speed.get())

    send_position()


def py_max():
    if positionY.get() + speed.get() > 180:
        positionY.set(180)
    else:
        positionY.set(positionY.get() + speed.get())

    send_position()


def py_men():
    if positionY.get() - speed.get() < 0:
        positionY.set(0)
    else:
        positionY.set(positionY.get() - speed.get())

    send_position()


# Start/Stop MPlayer
def mpl():
    command = "nc -l " + str(PORTNETCAT) + " | mplayer -fps 200 -demuxer h264es -"
    try:
        subprocess.Popen(command, shell=True)
        time.sleep(0.5)
        send("mpl")
        cnx.set("MP OK")
        color.set("#05c905")
        conexion.configure(fg=color.get())

    except:
        cnx.set("MP ERROR")
        color.set('red')
        conexion.configure(fg=color.get())


raiz = Tk()
raiz.title("PiCam Control")
raiz.geometry("280x210")

# Default values
positionX = IntVar(value=90)
positionY = IntVar(value=90)
speed = IntVar(value=10)
cnx = StringVar(value="Status")
color = StringVar(value="blue")
host = StringVar(value="192.168.1.220")
port = IntVar(value=9999)

# Panel Coordinates
panelposition = LabelFrame(raiz, text="Position", padx=0, pady=0, labelanchor="n")
panelposition.place(x=20, y=50, height=50, width=105)

etiqX = Label(panelposition, text="X:")
etiqX.place(height=20, width=20, x=2)
valueX = Label(panelposition, textvariable=positionX)
valueX.place(height=20, width=30, x=20)

etiqY = Label(panelposition, text="Y:")
etiqY.place(height=20, width=20, x=55)
valueY = Label(panelposition, textvariable=positionY)
valueY.place(height=20, width=30, x=70)

# Label IP and Port
ip = Label(raiz, text="IP:")
ip.place(height=25, width=40, y=10)
cnxentry = Entry(raiz, textvariable=host)
cnxentry.place(height=25, width=110, x=30, y=10)

prtlabel = Label(raiz, text="Port:")
prtlabel.place(height=25, width=60, x=145, y=10)
prtentry = Entry(raiz, textvariable=port)
prtentry.place(height=25, width=70, x=195, y=10)

# Label Speed
etiqSpeed = Label(raiz, text="Speed:")
etiqSpeed.place(height=20, width=60, x=145, y=70)
comboSpeed = Spinbox(raiz, from_=1, to=20, textvariable=speed)
comboSpeed.place(height=20, width=70, x=200, y=70)

# Buttons control
if REVERSE_X == 0:
    xmas = Button(raiz, text="Left", command=px_max)
    xmas.place(height=30, width=60, x=20, y=140)
    xmenos = Button(raiz, text="Right", command=px_men)
    xmenos.place(height=30, width=60, x=80, y=140)
else:
    xmas = Button(raiz, text="Left", command=px_men)
    xmas.place(height=30, width=60, x=20, y=140)
    xmenos = Button(raiz, text="Right", command=px_max)
    xmenos.place(height=30, width=60, x=80, y=140)

if REVERSE_Y == 0:
    ymenos = Button(raiz, text="Down", command=py_max)
    ymenos.place(height=30, width=60, x=50, y=170)
    ymas = Button(raiz, text="Up", command=py_men)
    ymas.place(height=30, width=60, x=50, y=110)
else:
    ymenos = Button(raiz, text="Down", command=py_men)
    ymenos.place(height=30, width=60, x=50, y=170)
    ymas = Button(raiz, text="Up", command=py_max)
    ymas.place(height=30, width=60, x=50, y=110)

# Button reset position
reset = Button(raiz, text="Reset", command=reset_position)
reset.place(height=30, width=90, x=180, y=110)

# Button MPlayer
mplayer = Button(raiz, text="MPlayer", command=mpl)
mplayer.place(height=30, width=90, x=180, y=140)

# Label info conexion
conexion = Label(raiz, textvariable=cnx, fg=color.get())
conexion.place(height=30, width=90, x=180, y=175)

raiz.mainloop()
