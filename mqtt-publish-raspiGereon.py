
# Skript zur Sensorenauslesung und Datenübertragung per MQTT
# Sensordaten werden über Funktion get[]() (Zeile 23 - 52) ausgelesen
# Jeder Sensorwert wird in seperater JSON-Mitteilung verschickt => 4 Mitteilungen pro Skriptdurchlauf
#       -> Funktion: publish (Zeile 52)
# Skript Autor: Gereon Pütz

import paho.mqtt.client as mqtt
import time
import datetime
from datetime import timezone
import os
import busio
import digitalio
import RPi.GPIO as GPIO
import json
import board
import adafruit_dht
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

### Funktionen #########################################################################
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline() 
    return(int(float(res.replace("temp=","").replace("'C\n",""))))

def getTemperature():
    temp = None
    while temp == None:
        try:
            temp = dhtDevice.temperature
        except:
            print ("Error - Temperature")
            pass
    return temp

def getHumidity():
    humidity = None
    while humidity is None:
        try:
            humidity = dhtDevice.humidity
        except:
            print ("Error - Humidity")
            pass
    return humidity

def getMoisture():
    moisture = None
    while moisture is None:
        try:
            moisture = int(chan0.value/64) #int((chan0.value / 65535) * 100)
        except:
            print ("Error - Moisture")
            pass
    return moisture

def publish(device, timestamp, sensor, value):
    daten = {
        'device': device,
        'time'  : timestamp,
        'sensor': sensor,
        'value' : value
    }
    print(daten)
    client.publish(topic, json.dumps(daten))

### Setup ##############################################################################
#Konfiguration der  MQTT-Verbindung
host="test.mosquitto.org"
topic="sensordaten"
port=1883
device = "raspiGereon"
client=mqtt.Client()
client.connect(host, port)

### DHT11 Setup ###################
dhtDevice = adafruit_dht.DHT11(board.D24)

### AD-Wandler (MCP3008) Setup#####
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22) #Chip-Select
mcp = MCP.MCP3008(spi, cs)
chan0 = AnalogIn(mcp, MCP.P0)

### Programmcode ########################################################################
client.loop_start()
try:
    while 1:
        # Publish alle 15 Sekunden
        print ("Wait...")
        while (int(time.strftime('%S',time.localtime())))%15 != 0:
            time.sleep(0.5)
        #Zeitstempel (Zeitzone UTC) erstellen
        timestamp = datetime.datetime.now(tz=timezone.utc).isoformat('T')
        publish(device, timestamp, "CPU_Temperature", getCPUtemperature())
        publish(device, timestamp, "Temperature", getTemperature())
        publish(device, timestamp, "Humidity", getHumidity())
        publish(device, timestamp, "Moisture", getMoisture())
        print ("Wait 15s")
        time.sleep(13)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
    print ("Ciao")
