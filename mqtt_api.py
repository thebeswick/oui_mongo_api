import json
import os
import sys
import re
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.wifidb
import paho.mqtt.client as mqtt

def mqtt_setup():
    mqttc.on_message = on_message
    mqttc.connect("192.168.1.238", 1883, 60)
    mqttc.subscribe("ouidata/request")
def on_message(mosq, obj, msg):
    macaddr = db.ouidata
    mac_input = str(msg.payload)
    if bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', mac_input.lower())):
        macAddr = re.sub('[:-]', '', msg.payload)
        vendorMACPrefix = macAddr[0:6].upper()
        print vendorMACPrefix
        macquery = macaddr.find_one({"vendorOUI": vendorMACPrefix})
        if macquery:
            print macquery
            new_topic = "ouidata/respond/" + macAddr
            outvalue = str(macquery)
            mqttc.publish(new_topic, outvalue)
        else:
            mqttc.publish("ouidata/respond/unknown", "Error: OUI not found in database")
    else:
        mqttc.publish("ouidata/respond/unknown", "Error: invalid MAC address must be 16 bytes (hex)")
    output = []
#    if macquery:
#        output.append({"vendorOUI" : macquery['vendorOUI'], "VendorName" : macquery['vendorName'] })


if __name__ == '__main__':
    mqttc = mqtt.Client()
    mqtt_setup()
    mqttc.loop_forever()




