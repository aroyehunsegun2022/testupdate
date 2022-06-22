# from mypersonalapp import app
from flask import Flask, Blueprint, request, jsonify, abort
import config       #(this is the config in the root) this is how to import things that are on the same level
from mypersonalapp.myroutes import main
from mypersonalapp.extensions import mongo
import certifi 
import jwt
from functools import wraps
import datetime

app = Flask(__name__,instance_relative_config=True)                 #config in instance folder
app.config['MONGO_URI'] = 'mongodb+srv://root:root@cluster0.3xybp1e.mongodb.net/db2?retryWrites=true&w=majority'
# app.config['SECRET_KEY'] = 'MySecretKey'
app.config.from_object(config)                                     #config in root folder
mongo.init_app(app, tlsCAFile=certifi.where())
app.register_blueprint(main)

users = mongo.db.users


if __name__=='__main__':
    app.run(port=5000, debug=True)
