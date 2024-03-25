import time
#Importing the time module
from bmp280 import BMP280
#Importing the BMP280 class
from smbus2 import SMBus, i2c_msg
#Importing the SMBus class and i2c_msg
import wiringpi
#Importing the wiringpi module
import requests
#Importing the requests module
from time import sleep
#Importing the sleep function
import sys
#Importing the sys module

write_api_key = '4OOZVKEQL8VQL2JW'
#The Api key i will use to transfer the data to thhingspeak

base_url = 'https://api.thingspeak.com/update'
#URL of thingspeak

bus = SMBus(0)
#Creating an instance of the SMBus class
address = 0x76
#Define the I2C address of the device connected to the bus
pin = 3
pin2 = 4
pin3 = 6
pin4 = 16
pinSwitch = 13
pinSwitch2 = 10
#Assigning all the pins i will use for input and output
wiringpi.wiringPiSetup()
#Initializing the wiringPi library for GPIO pin access
wiringpi.pinMode(pin, 1)
wiringpi.pinMode(pin2, 1)
wiringpi.pinMode(pin3, 1)
wiringpi.pinMode(pin4, 1)
wiringpi.pinMode(pinSwitch, 0)
wiringpi.pinMode(pinSwitch2, 0)
#Seting the modes of the GPIO pin to output

bus1 = SMBus(0)
#Creating an instance of the SMBus class for the second bus
address1 = 0x23
#Define the I2C address of the device connected to the second bus

bmp280 = BMP280(i2c_addr=address, i2c_dev=bus)
#Creating an instance of the BMP280 class for sensor communication
interval = 15
#Defining the interval for sensor readings

bus1.write_byte(address1, 0x10)
# Writing a byte with value 0x10 to the device with address address1
bytes_read = bytearray(2)
#Creating a bytearrray object with legth 2 bytes

def get_value(bus1, address1):
#creating a function for getting the vallue
    write = i2c_msg.write(address1, [0x10])
#Preparing a write message to send the command 0x10 to the device
    read = i2c_msg.read(address1, 2)
#Preparing a read message to read 2 bytes from the device
    bus.i2c_rdwr(write, read)
#Perform a I2C read/write operation
    bytes_read = list(read)
#Converting the received data into a list of bytes
    return (((bytes_read[0] & 3) << 8) + bytes_read[1]) / 1.2
#Processing  the received bytes and calculate the final value


data = {
    'api_key': write_api_key,
    'field1': 0,
    'field2': 0,
    'field3': 0,
    'field4': 0,
    'field5': 0,
    'field6': 0,
}
#Defining the default values that will be send to thingspeak, for the
#6 fields i have

deffault_temp= 20
deffault_light= 600
deffault_pressure = 1000
#Assigning the deffault values for the the three measurements
#those will be used to compare to the actual values
# and will be changed trough the buttons


def one_light(pin):
    wiringpi.digitalWrite(pin, 1)
#Assigning a function that will turn only one light on


def two_lights(pin,pin2):
    wiringpi.digitalWrite(pin, 1)
    wiringpi.digitalWrite(pin2, 1)
#Assigning a function that will turn two lights on

def three_lights(pin,pin2,pin3):
    wiringpi.digitalWrite(pin, 1)
    wiringpi.digitalWrite(pin2, 1)
    wiringpi.digitalWrite(pin3, 1)
#Assigning a function that will turn two lights on


def four_lights(pin,pin2,pin3,pin4):
    wiringpi.digitalWrite(pin, 1)
    wiringpi.digitalWrite(pin2, 1)
    wiringpi.digitalWrite(pin3, 1)
    wiringpi.digitalWrite(pin4, 1)
#Assigning a function that will turn two lights on

def turn_lights_off(pin,pin2,pin3,pin4):
    wiringpi.digitalWrite(pin, 0)
    wiringpi.digitalWrite(pin2, 0)
    wiringpi.digitalWrite(pin3, 0)
    wiringpi.digitalWrite(pin4, 0)
#Assigning a function that will turn all the light off


while True:
    lux = get_value(bus1, address1)
    bmp280_temperature = bmp280.get_temperature()
    bmp280_pressure = bmp280.get_pressure()
    #Assigning variables for the data from the sensors
    #this will be changed in every iteration
    if(wiringpi.digitalRead(pinSwitch) == 0):
        print("Default values increased!")
        time.sleep(0.5)
        deffault_pressure += 100
        deffault_light+= 50
        deffault_temp += 5
        #Checking if the first button is pressed
        #If it is, it increases the default value
    if (wiringpi.digitalRead(pinSwitch2) == 0):
        print("DEfault values decreased!")
        time.sleep(0.5)
        deffault_pressure -= 100
        deffault_light -= 50
        deffault_temp -= 5
        #Checking if the second button is pressed
        #If it is, it decreases the default values

    print("Temperature: ", (bmp280_temperature))
    if bmp280_temperature < 0:
        one_light(pin)
    elif bmp280_temperature > 0 and bmp280_temperature < 10:
        two_lights(pin,pin2)
    elif bmp280_temperature > 10 and bmp280_temperature < 20:
        three_lights(pin,pin2,pin3)
    else:
        four_lights(pin,pin2,pin3,pin4)

    time.sleep(2)

    turn_lights_off(pin,pin2,pin3,pin4)
    #Checking the value for temperature
    #Prints the value on the terminall
    #Depending on the value, it will turn of specific amount of lights
    #I use the functions taht I created a bit earlier
    #Time sleep for a bit of time to see the light

    print("Pressure: ", (bmp280_pressure))
    if bmp280_pressure < 1000:
        one_light(pin)
    elif bmp280_pressure > 1000 and bmp280_pressure < 2000:
        two_lights(pin,pin2)
    elif bmp280_pressure > 2000 and bmp280_pressure < 3000:
        three_lights(pin,pin2,pin3)
    else:
        four_lights(pin,pin2,pin3,pin4)

    time.sleep(2)

    turn_lights_off(pin,pin2,pin3,pin4)
    #The same as above,but for pressure


    print("Light: ", lux)
    if lux < 200:
        one_light(pin)
    elif lux > 200 and lux < 400:
        two_lights(pin,pin2)
    elif lux > 400 and lux < 800:
        three_lights(pin,pin2,pin3)
    else:
        four_lights(pin,pin2,pin3,pin4)

    time.sleep(2)

    turn_lights_off(pin,pin2,pin3,pin4)
    # The same as above,but for light

    if bmp280_temperature > deffault_temp and bmp280_pressure > deffault_pressure and lux > deffault_light:
        four_lights(pin,pin2,pin3,pin4)
        print("ALl values are above default!")
    elif bmp280_temperature > deffault_temp or bmp280_pressure > deffault_pressure or lux > deffault_light:
        two_lights(pin,pin2)
        print("Not all values are above default!")
    else:
        print("No value are above default!")
    time.sleep(2)

    turn_lights_off(pin,pin2,pin3,pin4)
    #Here I compare the actual values to the default ones
    #Depending of the value it will turn on a specific amount of lights
    #It prints it on the terminal as well

    print("ALL     Temperature: %4.1f, Pressure: %4.1f" % (bmp280_temperature, bmp280_pressure), "{:.2f} Lux".format(lux))
    #Here I print all data combined in one line
    print(deffault_light,"-light  ",deffault_pressure,"-pressure  ",deffault_temp,"-temp")
    #Here I print the default values
    data['field1'] = lux
    data['field2'] = bmp280_temperature
    data['field3'] = bmp280_pressure
    data['field4'] = deffault_light
    data['field5'] = deffault_temp
    data['field6'] = deffault_pressure
    #Here the values that will be send to thingspeak are assigned for every field
    response = requests.get(base_url, params=data)
    #here i recieve the response from thingspeak
    time.sleep(1)

    if response.status_code == 200:
        print('Data successfully sent to ThingSpeak.')
        # Print the entry ID of the update
        print('Entry ID:', response.text)
    else:
        print('Failed to send data to ThingSpeak. Status code:', response.status_code)
    #Here I am checking the return value from thingspeak
    #If it is 200, it means that it is send sucessfully




