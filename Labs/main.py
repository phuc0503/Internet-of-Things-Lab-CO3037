import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *
from uart import *


AIO_FEED_IDs = ["bbc-led", "bbc-tv", "fan-speed"]
AIO_USERNAME = "phucle"
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed thanh cong")

def disconnected(client):
    print("Ngat ket noi")
    sys.exit (1)

def message(client, feed_id, payload):
    print("Nhan du lieu: " + payload, "feed id: " + feed_id)
    if feed_id == "bbc-led":
        if payload == "0":
            writeData("1")
        else:
            writeData("2")
    if feed_id == "bbc-tv":
        if payload == "0":
            writeData("3")
        else:
            writeData("4")

client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 5
ai_result = ""
prev_result = ""

while True:

    # counter = counter - 1
    # if counter <= 0:
    #     counter = 10
    #     # TODO
    #     if sensor_type == 0:
    #         temperature = random.randint(15, 50)
    #         print("Temperature: " + str(temperature) + "oC")
    #         client.publish("bbc-temp", temperature)
    #         sensor_type = 1
    #     elif sensor_type == 1:
    #         humidity = random.randint(30, 90)
    #         print("Humidity: " + str(humidity) + "%")
    #         client.publish("bbc-humid", humidity)
    #         sensor_type = 2
    #     elif sensor_type == 2:
    #         light = random.randint(0, 2000)
    #         print("Light: " + str(light) + "lx")
    #         client.publish("bbc-lux", light)
    #         sensor_type = 0

    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        prev_result = ai_result
        ai_result = image_detector()
        print("AI output: ", ai_result)
        if prev_result != ai_result:
            client.publish("assistant", ai_result)

    readSerial(client)
    time.sleep(1)