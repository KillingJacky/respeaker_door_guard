#!/usr/bin/env python

import os
import signal
import mraa
import time
import sys
import random
import paho.mqtt.client as mqtt
from monotonic import monotonic
#from websocket import *


class MQTTMessager(object):
    def __init__(self):
        self.connected = False


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    userdata.connected = True

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("seeed-office-2016")

def on_disconnect(client, userdata, rc):
    userdata.connected = False

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

msgr = MQTTMessager()

client = mqtt.Client(userdata=msgr)
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

#########################
#ws = WebSocketServer()
#ws.start()

#########################
script_dir = os.path.dirname(os.path.realpath(__file__))

mission_completed = False
intr_happened = False
last_time_broadcast = monotonic()

def handle_int(sig, frame):
    global mission_completed

    print "Terminating..."
    mission_completed = True
    #ws.terminate()


signal.signal(signal.SIGINT, handle_int)


def isr1(gpip):
    global intr_happened
    intr_happened = True

def playWav(filepath):
    os.system('aplay -M %s' % (filepath,))
    pass


pin = 14
x = mraa.Gpio(pin)
x.dir(mraa.DIR_IN)
x.isr(mraa.EDGE_RISING, isr1, x)

while not mission_completed:
    if intr_happened:
        print 'interrupt happened!'
        intr_happened = False

        n = random.randint(1, 10)

        filepath = os.path.join(script_dir, 'audio/%d.wav' % (n,))

        playWav(filepath)

    now = monotonic()
    if now - last_time_broadcast > 5 and msgr.connected:
        last_time_broadcast = now
        client.publish('seeed-office-2016/well-known', payload='sub topic: seeed-office-2016/events payload: door-income')





x.isrExit()
client.loop_stop(force=True)
#ws.join()
