#!/usr/bin/env python3

from os import environ
from struct import pack
from sys import exit
from time import sleep

from rak811 import Mode, Rak811

from serial.serialutil import SerialException

# Get environment data
# Application EUI and Key are required parameters
app_eui = environ.get('APP_EUI')
app_key = environ.get('APP_KEY')

# LoRaWan band
band = environ.get('BAND', 'EU868')

# Serial port may change depending on the RPi and its configuration:
#   - mini UART: /dev/ttyS0
#   - PL011: /dev/ttyAMA0
# The rak811 library uses by default /dev/serial0 symlink which is not present in the balena container
port = environ.get('SERIAL_PORT', '/dev/ttyS0')
# The /sys path exposing CPU temperature:
path_cpu_temp = environ.get('PATH_CPU_TEMP',
                            '/sys/class/thermal/thermal_zone0/temp')

print('*******************')
print('*** Configuration')
print('*******************')
print('Band   : ', band)
print('App Key: ', app_key)
print('App EUI: ', app_eui)
print('Port   : ', port)
print('Path   : ', path_cpu_temp)
print()

try:
    lora = Rak811(port=port)
except SerialException as e:
    print('Cannot instantiate Rak811 class.')
    print('This is most probably an issue with the serial port.')
    print('Check your device configuration and the SERIAL_PORT variable')
    print('Error:')
    print(e)
    sleep(600)
    exit(0)

print('Initialise RAK811 module...')
lora.hard_reset()
lora.mode = Mode.LoRaWan
lora.band = band
print('Device EUI is:', lora.get_config('dev_eui'))

print('Setup RAK811 module...')
if app_key is None or app_eui is None:
    print('App Key and EUI are required...')
    print('Set APP_KEY and APP_EUI in balenaCloud console')
    sleep(600)
    exit(0)

lora.set_config(app_eui=app_eui,
                app_key=app_key)

print('Joining TTN...')
lora.join_otaa()
lora.dr = 4

print('Entering application loop')
print('You can send downlinks from the TTN console')
try:
    while True:
        # Read temperature
        with open(path_cpu_temp, 'rb') as f:
            temp = f.read().strip()
        temp = float(int(temp)) / 1000
        print('Sending CPU temperature: {0:.1f}'.format(temp))

        # Cayenne LPP temperature (Code 103) is stored as 0.1 °C Signed MSB
        lora.send(pack('>BBh', 1, 103, int(temp * 10 + 0.5)))

        while lora.nb_downlinks:
            print('Received:', lora.get_downlink()['data'].hex())

        sleep(300)
except:  # noqa: E722
    pass

print('Cleaning up')
lora.close()
exit(0)
