# Small Flask program to pull OUI (Original Unique Identifier) data
# There is an accompanying script that needs to be executed first
# to download the IEEE OUI text file and import it into MongoDB

import re
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'wifidb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/wifidb'

mongo = PyMongo(app)

@app.route('/api/all', methods=['GET'])
def get_all_mac_addresses():
    macaddr = mongo.db.ouidata
    output = []
    for macquery in macaddr.find():
        output.append({"vendorOUI" : macquery['vendorOUI'], "VendorName" : macquery['vendorName'] })
    return jsonify({'result' : output})

@app.route('/api/<macaddress>', methods=['GET'])
def get_one_mac(macaddress=None):
    macaddr = mongo.db.ouidata
    output = []
    if bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})'] * 6) + '$', macaddress.lower())):
        macAddr = re.sub('[:-]', '', macaddress)
        vendorMACPrefix = macAddr[0:6].upper()
        print vendorMACPrefix
        macquery = macaddr.find_one({"vendorOUI": vendorMACPrefix})

        if macquery:
            output.append({"vendorOUI" : macquery['vendorOUI'], "VendorName" : macquery['vendorName'] })
        else:
            output = "unknown OUI"
    else:
        output = "Not a valid MAC address"

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
