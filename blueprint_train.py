from flask import Blueprint
from flask import request
import jwt
import csv
import json
from functions import*

train = Blueprint('train',__name__)
path_train = r'data\train.csv'
key = "Caesar"

@train.route('/')
def get_train():
    page = request.args.get('page', default=1,type=int)
    li_train = li_dictObject(path_train)
    return json.dumps(li_train[(int(page)-1)*10:(int(page))*10])

@train.route('/create',methods = ['POST'])
def create_train_details():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        id = request.json["id"]
        train_number = request.json["train_number"]
        departure_loc = request.json["departure_loc"]
        arrival_loc = request.json["arrival_loc"]
        journey_duration = request.json["journey_duration"]
        fare = request.json["fare"]
        header = ["id", "train_number", "departure_loc","arrival_loc","journey_duration","fare"]
        value = {"id" : id,"train_number": train_number, "departure_loc" : departure_loc,"arrival_loc" : arrival_loc,"journey_duration" : journey_duration,"fare":fare}
        append_row(path_train,header,value)
        return json.dumps({"message" : "new train details added"})
    else:
        return json.dumps({"message" : "only admin access"})

@train.route('/search',methods = ['POST'])
def search_train():
    train_number = request.json["train_number"]
    file_hand = open(path_train,'r')
    file_hand_reader = csv.DictReader(file_hand)
    for row in file_hand_reader:
        if row["train_number"] == train_number:
            file_hand.close()
            return json.dumps(row)
    return json.dumps({"message" : "invalid train number"})

@train.route('/modify', methods = ['PATCH'])
def train_modify():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        train_number = request.json["train_number"]
        modifying_variable = request.json["modifying_variable"]
        modified_value = request.json["modified_value"]
        li_train = li_dictObject(path_train)
        for row in li_train:
            if row["train_number"] == train_number:
                row[modifying_variable] = modified_value
                overwrite_file(path_train,li_train)
                return json.dumps({"message" : "train detail modified"})
        return json.dumps({"message" : "invalid train number"})
    else:
        return json.dumps({"message" : "only admins access"})

@train.route('/delete',methods = ['DELETE'])
def delete_train():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    if decoded_jwt["role"] == "admin":
        train_number = request.json["train_number"]
        li_train = li_dictObject(path_train)
        for row in li_train:
            if row["train_number"] == train_number:
                li_train.remove(row)
                overwrite_file(path_train,li_train)
                return json.dumps({"message" : "train details deleted"})
        return json.dumps({"message":"invalid train number"})
    else:
        return json.dumps({"message":"only admin access"})