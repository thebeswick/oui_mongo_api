# This is a script to download the IEEE OUI text file and import it into MongoDB
# If you already have a copy of the oui.txt file you can comment out get_mac_table_file()
# to save time. The script is dependent on MongoDB

import os
import sys
import urllib2
import json
import re
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.wifidb
ven_arr = []


def get_mac_table_file(filename="oui.txt"):
    request = urllib2.urlopen("http://standards.ieee.org/develop/regauth/oui/oui.txt")
    with open(filename, "w") as f:
        for line in request:
            f.write(line)


def import_oui_data():
    db.ouidata.drop()
    filename = "./oui.txt"
    with open(filename, "r") as f:
        for line in f:
            if "(base 16)" not in line:
                continue
            ven = tuple(re.sub("\s*([0-9a-zA-Z]+)[\s\t]*\(base 16\)[\s\t]*(.*)\n", r"\1;;\2", line).split(";;"))
            ven_arr.append(ven)
    arr_length = len(ven_arr)
    pos = 0
    while pos < len(ven_arr):
        vendorPrefixMAC = ven_arr[pos][0]
        vendorName = ven_arr[pos][1].rstrip()
        db.ouidata.insert({"vendorOUI": vendorPrefixMAC, "vendorName": vendorName})
        pos += 1


if __name__ == '__main__':
#    get_mac_table_file()
    import_oui_data()
