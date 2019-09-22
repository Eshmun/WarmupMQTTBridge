import warmup4ie
import paho.mqtt.client as mqtt

import secrets

device = warmup4ie.Warmup4IEDevice(secrets.email, secrets.password,
                                   secrets.location, secrets.room, 21)



print(device.get_current_temmperature())
print(device.get_target_temmperature())
# device.set_new_temperature(17.5)
# device.set_temperature_to_auto()
# device.set_location_to_frost()
print(device.get_all_devices())
