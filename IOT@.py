import time
from bmp280 import BMP280
from smbus2 import SMBus, i2c_msg
import wiringpi
import requests
from time import sleep
import sys

write_api_key = '4OOZVKEQL8VQL2JW'

base_url = 'https://api.thingspeak.com/update'

bus = SMBus(0)
address = 0x76
pin = 3
pin2 = 4
pin3 = 6
pin4 = 16
pinSwitch = 13
pinSwitch2 = 10
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin, 1)
wiringpi.pinMode(pin2, 1)
wiringpi.pinMode(pin3, 1)
wiringpi.pinMode(pin4, 1)
wiringpi.pinMode(pinSwitch, 0)
wiringpi.pinMode(pinSwitch2, 0)

bus1 = SMBus(0)
address1 = 0x23

bmp280 = BMP280(i2c_addr=address, i2c_dev=bus)
interval = 15

bus1.write_byte(address1, 0x10)
bytes_read = bytearray(2)

def one ():
    wiringpi.digitalWrite(pin, 1)




def get_value(bus1, address1):
    write = i2c_msg.write(address1, [0x10])
    read = i2c_msg.read(address1, 2)
    bus.i2c_rdwr(write, read)
    bytes_read = list(read)
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2


data = {
    'api_key': write_api_key,
    'field1': 0,
    'field2': 0,
    'field3': 0,
    'field4': 0,
    'field5': 0,
    'field6': 0,
}

deffault_temp= 20
deffault_light= 600
deffault_pressure = 1000

while True:
    lux = get_value(bus1, address1)
    bmp280_temperature = bmp280.get_temperature()
    bmp280_pressure = bmp280.get_pressure()
    if(wiringpi.digitalRead(pinSwitch) == 0):
        print("Default values increased!")
        time.sleep(0.5)
        deffault_pressure += 100
        deffault_light+= 50
        deffault_temp += 5
    if (wiringpi.digitalRead(pinSwitch2) == 0):
        print("DEfault values decreased!")
        time.sleep(0.5)
        deffault_pressure -= 100
        deffault_light -= 50
        deffault_temp -= 5

    print("Temperature: ", (bmp280_temperature))
    if bmp280_temperature < 0:
        wiringpi.digitalWrite(pin, 1)
    elif bmp280_temperature > 0 and bmp280_temperature < 10:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
    elif bmp280_temperature > 10 and bmp280_temperature < 20:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
    else:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
        wiringpi.digitalWrite(pin4, 1)

    time.sleep(2)

    wiringpi.digitalWrite(pin, 0)
    wiringpi.digitalWrite(pin2, 0)
    wiringpi.digitalWrite(pin3, 0)
    wiringpi.digitalWrite(pin4, 0)

    print("Pressure: ", (bmp280_pressure))
    if bmp280_pressure < 1000:
        wiringpi.digitalWrite(pin, 1)
    elif bmp280_pressure > 1000 and bmp280_pressure < 2000:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
    elif bmp280_pressure > 2000 and bmp280_pressure < 3000:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
    else:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
        wiringpi.digitalWrite(pin4, 1)

    time.sleep(2)


    wiringpi.digitalWrite(pin, 0)
    wiringpi.digitalWrite(pin2, 0)
    wiringpi.digitalWrite(pin3, 0)
    wiringpi.digitalWrite(pin4, 0)


    print("Light: ", lux)
    if lux < 200:
        wiringpi.digitalWrite(pin, 1)
    elif lux > 200 and lux < 400:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
    elif lux > 400 and lux < 800:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
    else:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
        wiringpi.digitalWrite(pin4, 1)

    time.sleep(2)

    wiringpi.digitalWrite(pin, 0)
    wiringpi.digitalWrite(pin2, 0)
    wiringpi.digitalWrite(pin3, 0)
    wiringpi.digitalWrite(pin4, 0)

    if bmp280_temperature > deffault_temp and bmp280_pressure > deffault_pressure and lux > deffault_light:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        wiringpi.digitalWrite(pin3, 1)
        wiringpi.digitalWrite(pin4, 1)
        print("ALl values are above default!")
    else:
        wiringpi.digitalWrite(pin, 1)
        wiringpi.digitalWrite(pin2, 1)
        print("Not all values are above!")

    wiringpi.digitalWrite(pin, 0)
    wiringpi.digitalWrite(pin2, 0)
    wiringpi.digitalWrite(pin3, 0)
    wiringpi.digitalWrite(pin4, 0)

    print("ALL     Temperature: %4.1f, Pressure: %4.1f" % (bmp280_temperature, bmp280_pressure), "{:.2f} Lux".format(lux))
    print(deffault_light,"-light  ",deffault_pressure,"-pressure  ",deffault_temp,"-temp")
    data['field1'] = lux
    data['field2'] = bmp280_temperature
    data['field3'] = bmp280_pressure
    data['field4'] = deffault_light
    data['field5'] = deffault_temp
    data['field6'] = deffault_pressure
    response = requests.get(base_url, params=data)
    time.sleep(1)

    if response.status_code == 200:
        print('Data successfully sent to ThingSpeak.')
        # Print the entry ID of the update
        print('Entry ID:', response.text)
    else:
        print('Failed to send data to ThingSpeak. Status code:', response.status_code)



