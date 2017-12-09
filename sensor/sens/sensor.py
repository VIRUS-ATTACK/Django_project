#!/usr/bin/python
import sys
import Adafruit_DHT
import requests
import time

sys.path.insert(0,"../reze")
try:
    from receive import *
except ImportError:
    print('No Import')

import datetime
from time import sleep
import mcp3008
import RPi.GPIO as GPIO
import math
from datetime import datetime
GPIO.setmode(GPIO.BCM)                #set the pins to BCM mode
GPIO.setwarnings(False)               #to avoid warnings
TRIG = 21           #set GPIO 21 pin as the trigger pin to send sound wave(ultrasonic)         
ECHO = 20           #set GPIO 20 pin as the echo pin to receive sound wave(ultrasonic)

GPIO.setup(TRIG,GPIO.OUT)             
GPIO.setup(ECHO,GPIO.IN)

class sensor:
    def __init__(self,moisturepin,motorgpiopin):
        self.moisturepin = moisturepin
        self.motorgpiopin = motorgpiopin
        GPIO.setup(self.motorgpiopin,GPIO.OUT)
    def startmotor(self):
        GPIO.output(motorgpiopin, True)
        time.sleep(3)
        GPIO.output(motorgpiopin, False)
    def stopmotor(self):
        GPIO.output(motorgpiopin, False)
    def calculatemoisture(self):
        soil_moisture = mcp3008.readadc(moisturepin)        #taking soilmoisture value from adc pin 5
        soil_moisture = (soil_moisture*100)/1024
        soil_moisture = 100-soil_moisture
        return soil_moisture
    def calculate_tankheight(self):
        GPIO.output(TRIG, False)
        GPIO.output(TRIG, True)                  #sending the sound wave for a time span of 0.00001 sec
        time.sleep(0.00001)               
        GPIO.output(TRIG, False)  
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()            #storing the start time of pulse
        while GPIO.input(ECHO)==1:            
            pulse_end = time.time()              #storing the end time of pulse
        pulse_duration = pulse_end - pulse_start #pulse duration
        
        distance = pulse_duration * 17150        #distance = time * sped
        distance = round(distance, 2)
        return distance
    def mailmessage(self):
        email_subject=readmail()
        return email_subject
        

url="http://192.168.43.94:8094/get/"      #url to which the data is to be sent
plant1 = sensor(5,16)
plant2 = sensor(6,26)#function for calculating all the sensor values
while True:
    status = 0
    email_subject=plant1.mailmessage()
    message = email_subject.split(',')
    Raspmessage = message[0]
    print "Message sent from django server",Raspmessage
    status = int(message[1])
    print "status of the motor",status
    plantid = int(message[2])
    print "plant id:",plantid
        
    if(status == 1 and plantid== 0):
        print 'motor '+str(plantid)+' is on'
        plant1.startmotor()
        plant1.stopmotor()
    elif(status ==1 and plantid == 1):
        print 'motor '+str(plantid)+' is on'
        plant2.startmotor()
        plant2.stopmotor()
    else:
        plant1.stopmotor()
        plant2.stopmotor()
    print Raspmessage
    plant1.stopmotor()      #off the motors initially
    plant2.stopmotor()
    soil_moisture1 = plant1.calculatemoisture()      
    #print "soil moisture1:",soil_moisture1
    soil_moisture2 = plant2.calculatemoisture()      #taking soilmoisture value from adc pin 6
    #print "soil moisture2:",soil_moisture2
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print "humidity:",humidity
    #print "temperature:",temperature
    watersensor_reading = mcp3008.readadc(0)        #taking water sensor reading value from adc pin 0
    #print watersensor_reading
    if(watersensor_reading>=15):
        print("Raining")         
        k=0
    else:
        print("not Raining")
        k=1
    distance = calculate_tankheight()
    print "------------------------------------------------"
    print "humidity: ",humidity,"temperature: ",temperature
    print "soil moisture of plant 0:",soil_moisture1
    print "soil moisture of plant 1:",soil_moisture2
    print "distance:",distance
    print "water sensor:",watersensor_reading
    print "------------------------------------------------" 
    water_level=math.ceil(13-distance)
    condition="motors are being controlled manually"
    condition1="motors are being controlled manually"
    if(k==1 and status==0):
        if(soil_moisture1 <30):            #stop the motor if there is a rainfall
            plant1.startmotor()         #on the motor if soil moisture is less than 30      
            condition = "Motor one is on "
        else:
            plant1.stopmotor()
            condition = "Motor one is off "
        if(soil_moisture2 <30):
            plant2.startmotor()
            condition1 = " Motor two is on "
        else:
            plant2.stopmotor()
            condition1 = " Motor two is off "
        time.sleep(3)
        GPIO.output(16, False)
        GPIO.output(26, False)
    elif(status==0):
        GPIO.output(26,False)
        GPIO.output(16,False)
        condition = "It's raining and all the motors are off"
        condition1 = "It's raining and all the motors are off"
    print condition,condition1
    data = {'condition':condition,'pid':0,'temperature':temperature,'humidity':humidity,'soilmoisture':soil_moisture1 ,'waterlevel':water_level,'watersensor':watersensor_reading}
    requests.get(url,params=data)
    data = {'condition':condition1,'pid':1,'temperature':temperature,'humidity':humidity,'soilmoisture':soil_moisture2 ,'waterlevel':water_level,'watersensor':watersensor_reading}
    requests.get(url,params=data)
    time.sleep(2)