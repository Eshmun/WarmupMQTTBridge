import warmup4ie
import paho.mqtt.client as mqtt
import threading
import json

import secrets

updateTime = 10

device = warmup4ie.Warmup4IEDevice(secrets.email, secrets.password,
                                   secrets.location, secrets.room, 21)

client = mqtt.Client("WarmupBridge")
client.connect("test.mosquitto.org")

client.subscribe("climate/warmup/temperature/set")
client.subscribe("climate/warmup/mode/set")


def on_message(client, userdata, message):
    if message.topic == "climate/warmup/temperature/set":
        device.set_new_temperature(int(message.payload))

    if message.topic == "climate/warmup/mode/set":
        if message.payload == "off":
            device.set_location_to_off()

        elif message.payload == "heat":
            device.set_temperature_to_manual()

        elif message.payload == "auto":
            device.set_temperature_to_auto()

    print(message.payload)


def update():
    t = threading.Timer(updateTime, update)
    t.start()
    current_temperature = device.get_current_temmperature()
    target_temperature = device.get_target_temmperature()
    run_mode = device.get_run_mode()
    data_out = {"available":            "online",
                "current_temperature":  current_temperature,
                "target_temperature":   target_temperature,
                "run_mode":             run_mode}
    client.publish("climate/warmup", json.dumps(data_out))
    print("hello, world")


t = threading.Timer(updateTime, update)
t.start()

client.on_message = on_message


while 1:
    client.loop_forever()
