import warmup4ie
import paho.mqtt.client as mqtt
import threading
import json

import secrets

UPDATE_INTERVAL = 1
TEMPERATURE_COMMAND_TOPIC = "climate/warmup/temperature/set"
MODE_COMMAND_TOPIC = "climate/warmup/mode/set"
DATA_UPDATE_TOPIC = "climate/warmup"


device = warmup4ie.Warmup4IEDevice(secrets.email, secrets.password,
                                   secrets.location, secrets.room, 21)

client = mqtt.Client("WarmupBridge")
client.connect(secrets.broker)

client.subscribe(TEMPERATURE_COMMAND_TOPIC)
client.subscribe(MODE_COMMAND_TOPIC)



def on_message(client, userdata, message):
    print(message.topic)
    print(message.payload)
    if message.topic == TEMPERATURE_COMMAND_TOPIC:
        device.set_new_temperature(int(float(message.payload.decode('utf8'))))

    if message.topic == MODE_COMMAND_TOPIC:
        if message.payload == b"off":
            device.set_location_to_frost()

        elif message.payload == b"heat":
            print("Set to manual")
            device.set_temperature_to_manual()

        elif message.payload == b"auto":
            device.set_temperature_to_auto()




def update():
    t = threading.Timer(UPDATE_INTERVAL, update)
    t.start()
    device.update_room()
    current_temperature = device.get_current_temperature()
    target_temperature = device.get_target_temperature()
    run_mode = device.get_run_mode()
    run_mode_ha = run_mode

    if run_mode == "program":
        run_mode_ha = "auto"
    if run_mode == "frost":
        run_mode_ha = "off"
    if run_mode == "override":
        run_mode_ha = "heat"
    if run_mode == "fixed":
        run_mode_ha = "heat"
    if run_mode == "away":
        run_mode_ha = "off"

    data_out = {"available": "online",
                "current_temperature": current_temperature,
                "target_temperature": target_temperature,
                "run_mode": run_mode_ha}
    client.publish(DATA_UPDATE_TOPIC, json.dumps(data_out))
    print("hello, world")


t = threading.Timer(UPDATE_INTERVAL, update)
t.start()

client.on_message = on_message

while 1:
    client.loop_forever()
