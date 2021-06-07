import paho.mqtt.client as mqtt
import time
import os
import RPi.GPIO as GPIO
import json
import board
import adafruit_dht


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline() 
    return(int(float(res.replace("temp=","").replace("'C\n",""))))

def getTemperature():
    temp = None
    while temp == None:
        try:
            temp = dhtDevice.temperature
        except:
            pass
    return temp

def getHumidity():
    humidity = None
    while humidity is None:
        try:
            humidity = dhtDevice.humidity
        except:
            pass
    return humidity



################################
#Konfiguration der Verbindung
host="test.mosquitto.org"
topic="sensordaten"
port=1883
device = "raspi4Gereon"
################################
#Konfiguration DHT11-Sensor an Pin 24
dhtDevice = adafruit_dht.DHT11(board.D24)
################################
#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
################################
client = mqtt.Client()
client.connect(host, port)
client.loop_start()

while 1:
    #Warte auf volle Minute
    while (int(time.strftime('%S',time.localtime()))) != 0:
        time.sleep(0.5)
    daten={
        'device' : device, 
        'date': time.strftime('%d.%m.%y',time.localtime()),
        'time': time.strftime('%H:%M:%S',time.localtime()),
        'cpu-temp': getCPUtemperature(),
        'temperature': getTemperature(),
        'humidity': getHumidity()
    }
    client.publish(topic,json.dumps(daten))
    time.sleep(30)
client.loop_stop()
