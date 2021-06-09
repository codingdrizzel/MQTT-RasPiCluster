import paho.mqtt.client as mqtt
import json

###############################################################
def on_message(client, userdata, message):
    ausgabe = json.loads(str(message.payload.decode("utf-8")))
    print(json.dumps(ausgabe, indent=4))
    #file = open("daten.csv", "a")
    #file.write(ausgabe+"\n")
    #file.close()

def on_connect(client, userdata, flags, rc):
    if rc!=0:
        #print("connected OK Returned code =",rc)
    #else:
        print("Bad connection Returned code=",rc)
###############################################################
host="test.mosquitto.org"
port=1883
topic="sensordaten"
#username="pi"
#password="raspberry"
################################################################

file = open("daten.csv", "w")
file.write("Geraet,Datum,Zeit,CPU,Sensor1,Sensor2\n\t,TT:MM:YYYY,HH:MM:SS,degC,\t,\t")
file.close()


client=mqtt.Client()
#client.username_pw_set(username,password)
client.connect(host,port)
client.on_connect=on_connect #callback
client.subscribe(topic)
client.on_message=on_message #callback
client.loop_forever()




