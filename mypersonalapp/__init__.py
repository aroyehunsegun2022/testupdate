# from flask import Flask
# import config       #(this is the config in the root) this is how to import things that are on the same level
# from mypersonalapp.myroutes import main
# from .extensions import mongo
# import certifi 


# app = Flask(__name__,instance_relative_config=True)                 #config in instance folder
# app.config['MONGO_URI'] = 'mongodb+srv://root:root@cluster0.3xybp1e.mongodb.net/db2?retryWrites=true&w=majority'
# app.config['SECRET_KEY'] = 'MySecretKey'
# app.config.from_object(config)                                     #config in root folder
# mongo.init_app(app, tlsCAFile=certifi.where())
# app.register_blueprint(main)

