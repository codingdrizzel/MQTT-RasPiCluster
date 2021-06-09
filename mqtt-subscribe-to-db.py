import paho.mqtt.client as mqtt
import json
from influxdb import InfluxDBClient
###############################################################
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connected OK - Returned ",rc)
    else:
        print("Bad connection - Returned",rc)

def on_message(client, userdata, message):
    mqtt_message = json.loads(str(message.payload.decode("utf-8")))
    #print(mqtt_message)
    write_to_db(mqtt_message)

def write_to_db(json):
    json_body = [
        {
            "measurement": json["device"],
            "tags": {
                "sensor": json["sensor"] ,
            },
            "time": json["time"],
            "fields": {
                "value": json["value"]
            }
        }
    ]
    print(json_body)
    db_client.write_points(json_body)
    print(json["device"],json["sensor"], "erfolgreich in Database geschoben")

def _init_influxdb_database():
    databases = db_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == db_name, databases))) == 0:
        db_client.create_database(db_name)
    db_client.switch_database(db_name)

###############################################################
# MQTT Konfiguration
host = "test.mosquitto.org"
port = 1883
topic = "sensordaten"
#mqtt_username = "pi"
#mqtt_password = "raspberry"
mqtt_client=mqtt.Client()
################################################################
# InfluxDB Konfiguration
db_adrs = "192.168.0.214" #raspi3
db_user = "mqtt"
db_pswd = "mqtt"
db_name= "sensordaten"
db_client = InfluxDBClient(db_adrs, 8086, db_user, db_pswd, None)
_init_influxdb_database()
################################################################

#mqtt_client.username_pw_set(mqtt_username,mqtt_password)
mqtt_client.connect(host,port)
mqtt_client.on_connect=on_connect #callback
mqtt_client.subscribe(topic)
mqtt_client.on_message=on_message #callback
mqtt_client.loop_forever()