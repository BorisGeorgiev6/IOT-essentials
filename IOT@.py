import time
from bmp280 import BMP280
from smbus2 import SMBus, i2c_msg
import wiringpi
import requests

# Your ThingSpeak channel's Write API Key
write_api_key = 'ZL61CTS6YTV81QMV'

# The base URL for updating a ThingSpeak channel
base_url = 'https://api.thingspeak.com/update'


bus = SMBus(0)
address = 0x76
pin = 3
pin2 = 4
pin3 = 6
pin4 = 16
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin, 1)
wiringpi.pinMode(pin2, 1)
wiringpi.pinMode(pin3, 1)
wiringpi.pinMode(pin4, 1)

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
    'field3': 0
}


while True:
    lux = get_value(bus1, address1)
    bmp280_temperature = bmp280.get_temperature()
    bmp280_pressure = bmp280.get_pressure()

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
    print("ALL     Temperature: %4.1f, Pressure: %4.1f" % (bmp280_temperature, bmp280_pressure), "{:.2f} Lux".format(lux))
    data['field1'] = lux;
    data['field2'] = bmp280_temperature
    data['field3'] = bmp280_pressure
    response = requests.get(base_url, params=data)
    time.sleep(1)

    if response.status_code == 200:
        print('Data successfully sent to ThingSpeak.')
        # Print the entry ID of the update
        print('Entry ID:', response.text)
    else:
        print('Failed to send data to ThingSpeak. Status code:', response.status_code)



