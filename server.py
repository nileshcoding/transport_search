from flask import Flask
from flask import request
from functions import *
import jwt
import csv
import json
from blueprint_user import user
from blueprint_bus import bus
from blueprint_train import train

app = Flask(__name__)
app.register_blueprint(user,url_prefix= '/user')
app.register_blueprint(bus,url_prefix = '/bus')
app.register_blueprint(train,url_prefix = '/train')

path_user = r'data\user.csv'
path_bus = r'data\bus.csv'
path_train = r'data\train.csv'
path_userpass = r'data\userpass.csv'

@app.route('/login',methods = ['POST'])
def login_page():
    username  = request.json["username"]
    password = request.json["password"]
    file_hand = open(path_userpass,'r')
    file_hand_reader = csv.DictReader(file_hand)
    flag_validUser = False
    flag_validCredential = False
    for row in file_hand_reader:
        if row["username"] == username:
            flag_validUser = True
            if row["password"] == password:
                flag_validCredential = True
                id = row["id"]
                break
    file_hand.close()
    
    if flag_validCredential == True:
        li_user = li_dictObject(path_user)
        for row in li_user:
            if row["id"] == id:
                role = row["role"]
                break
        payload = {"username" : username, "message" : "logged in", "role" : role}
        key = 'Caesar'
        encoded_jwt = jwt.encode(payload,key)
        return json.dumps({"auth_token" : encoded_jwt.decode(),"message" : "logged in"})
    elif flag_validCredential == False and flag_validUser == True:
        return json.dumps({"message" : "password did not match"})
    else:
        return json.dumps({"message" : "invalid user"})