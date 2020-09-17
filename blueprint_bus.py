from flask import request
from functions import *
import csv
import json
import jwt
from flask import Blueprint

bus = Blueprint('bus',__name__)
path_bus = r'data\bus.csv'
key = "Caesar"

@bus.route('/')
def get_bus():
    page = request.args.get('page', default=1,type=int)
    li_bus = li_dictObject(path_bus)
    return json.dumps(li_bus[(int(page)-1)*10:(int(page))*10])

@bus.route('/create',methods = ['POST'])
def create_bus_details():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        id = request.json["id"]
        bus_number = request.json["bus_number"]
        departure_loc = request.json["departure_loc"]
        arrival_loc = request.json["arrival_loc"]
        journey_duration = request.json["journey_duration"]
        fare = request.json["fare"]
        header = ["id", "bus_number", "departure_loc","arrival_loc","journey_duration","fare"]
        value = {"id" : id,"bus_number": bus_number, "departure_loc" : departure_loc,"arrival_loc" : arrival_loc,"journey_duration" : journey_duration,"fare":fare}
        append_row(path_bus,header,value)
        return json.dumps({"message" : "new bus details added"})
    else:
        return json.dumps({"message" : "only admin access"})

@bus.route('/search',methods = ['POST'])
def search_bus():
    bus_number = request.json["bus_number"]
    file_hand = open(path_bus,'r')
    file_hand_reader = csv.DictReader(file_hand)
    for row in file_hand_reader:
        if row["bus_number"] == bus_number:
            file_hand.close()
            return json.dumps(row)
    return json.dumps({"message" : "invalid bus number"})

@bus.route('/modify', methods = ['PATCH'])
def bus_modify():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        bus_number = request.json["bus_number"]
        modifying_variable = request.json["modifying_variable"]
        modified_value = request.json["modified_value"]
        li_bus = li_dictObject(path_bus)
        for row in li_bus:
            if row["bus_number"] == bus_number:
                row[modifying_variable] = modified_value
                overwrite_file(path_bus,li_bus)
                return json.dumps({"message" : "bus detail modified"})
        return json.dumps({"message" : "invalid bus number"})
    else:
        return json.dumps({"message" : "only admins access"})

@bus.route('/delete',methods = ['DELETE'])
def delete_bus():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        bus_number = request.json["bus_number"]
        li_bus = li_dictObject(path_bus)
        for row in li_bus:
            if row["bus_number"] == bus_number:
                li_bus.remove(row)
                overwrite_file(path_bus,li_bus)
                return json.dumps({"message" : "bus details deleted"})
        return json.dumps({"message":"invalid bus number"})
    else:
        return json.dumps({"message":"only admin access"})