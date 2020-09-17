from flask import Blueprint
from flask import request
from flask import Flask
from functions import *
import jwt
import csv
import json

user = Blueprint('user',__name__)
path_user = r'data\user.csv'
path_userpass = r'data\userpass.csv'
key = "Caesar" #key for encoded payload

#route to get all the users
@user.route('/')
def user_home():
    li_user = li_dictObject(path_user)
    return json.dumps(li_user)

#route to register new users
@user.route('/register',methods = ['POST'])
def user_register():
    id = request.json["id"]
    name = request.json["name"]
    contact_number = request.json["contact_number"]
    address = request.json["address"]
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    header = ["id" , "name", "contact_number", "address","role"]
    value = {"id" : id,"name":name,"contact_number":contact_number,"address":address,"role":role}
    append_row(path_user,header,value)
    header = ["id","username","password"]
    value = {"id":id,"username":username,"password":password}
    append_row(path_userpass,header,value)
    return json.dumps({"message" : "user registered"})

#this route can't modify password
@user.route('/modify',methods = ['PATCH'])
def modify_user():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    username = decoded_jwt["username"]
    modifying_variable = request.json["modifying_variable"]
    modified_value = request.json["modified_value"]
    li_userpass = li_dictObject(path_userpass)
    flag =  False
    for row in li_userpass:
        if row["username"] == username:
            flag = True
            id = row["id"]
            if modifying_variable == "id":
                row["id"] = modified_value
                overwrite_file(path_userpass,li_userpass)
            break
    li_user = li_dictObject(path_user)
    if flag == True:
        for row in li_user:
            if row["id"] == id:
                row[modifying_variable] = modified_value
                break
        overwrite_file(path_user,li_user)
        return json.dumps({"message" : "details modified"})
    else:
        return json.dumps({"message" : "user does not exist or already deleted"})

#route to delete a user
@user.route('/delete',methods = ['DELETE'])
def delete_user():
    auth_token = request.json["auth_token"]
    decoded_jwt = jwt.decode(auth_token,key)
    username = decoded_jwt["username"]
    li_userpass = li_dictObject(path_userpass)
    flag = False
    for row in li_userpass:
        if row["username"] == username:
            flag = True
            id = row["id"]
            li_userpass.remove(row)
            break
    li_user = li_dictObject(path_user)
    if flag:
        for row in li_user:
            if row["id"] == id:
                li_user.remove(row)
                break
        overwrite_file(path_user,li_user)
        overwrite_file(path_userpass,li_userpass)
        return json.dumps({"message" : "user deleted"})
    else:
        return json.dumps({"message" : "user does not exist or already deleted"})