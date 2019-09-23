import warmup4ie
import paho.mqtt.client as mqtt
import threading
import json

import secrets

UPDATE_INTERVAL = 10
TEMPERATURE_COMMAND_TOPIC = "climate/warmup/temperature/set"
MODE_COMMAND_TOPIC = "climate/warmup/mode/set"
DATA_UPDATE_TOPIC = "climate/warmup"

device = warmup4ie.Warmup4IEDevice(secrets.email, secrets.password,
                                   secrets.location, secrets.room, 21)

client = mqtt.Client("WarmupBridge")
client.connect("test.mosquitto.org")

client.subscribe(TEMPERATURE_COMMAND_TOPIC)
client.subscribe(MODE_COMMAND_TOPIC)


def on_message(client, userdata, message):
    if message.topic == TEMPERATURE_COMMAND_TOPIC:
        device.set_new_temperature(int(message.payload))

    if message.topic == MODE_COMMAND_TOPIC:
        if message.payload == "off":
            device.set_location_to_off()

        elif message.payload == "heat":
            device.set_temperature_to_manual()

        elif message.payload == "auto":
            device.set_temperature_to_auto()

    print(message.topic)
    print(message.payload)


def update():
    t = threading.Timer(UPDATE_INTERVAL, update)
    t.start()
    current_temperature = device.get_current_temmperature()
    target_temperature = device.get_target_temmperature()
    run_mode = device.get_run_mode()
    data_out = {"available": "online",
                "current_temperature": current_temperature,
                "target_temperature": target_temperature,
                "run_mode": run_mode}
    client.publish(DATA_UPDATE_TOPIC, json.dumps(data_out))
    print("hello, world")


t = threading.Timer(UPDATE_INTERVAL, update)
t.start()

client.on_message = on_message

while 1:
    client.loop_forever()
