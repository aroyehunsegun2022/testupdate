from crypt import methods
import email
from bson import ObjectId
from flask import Blueprint, render_template, request, jsonify, abort
from mypersonalapp.extensions import mongo
import jwt

from functools import wraps
import datetime

SECRET_KEY= 'MySecretKey'
users = mongo.db


# usersInsert.insert_one({'name': 'John', 'age': '30'})

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return('Hello World')

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, SECRET_KEY)
            
#             current_user = users.find_one({'email': data['email']}).first()
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated


@main.route('/register', methods=['POST'])
def userregister():
    usersInsert = mongo.db.user2
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password =  request.json['password']
    usersInsert.insert_one({'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password})
    return jsonify({'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password})




@main.route('/login', methods=['POST'])
def userlogin():
    usersInsert = mongo.db.user2
    email = request.json['email']
    password = request.json['password']
    user = usersInsert.find_one({'email': (email)})
    if not user:
        return jsonify({'message': 'User does not exist!'})
    if user['password'] != password:
        return jsonify({'message': 'Wrong password!'})
    token = jwt.encode({'email': user['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
    return jsonify({'token': token})


# @main.route('/login', methods=['POST'])
# def userlogin():
#     users = mongo.db.users
#     email = request.json['email']
#     password = request.json['password']
#     user = users.find_one({'email': email})
#     if user:
#         if user['password'] == password:
#             return jsonify({'email': email, 'password': password})
#         else:
#             return jsonify({'message': 'Wrong password!'})
#     else:
#         return jsonify({'message': 'User not found!'})


# @main.route('/login', methods=['POST'])
# def userlogin():
#     users = mongo.db.user2
#     email = request.json['email']
#     password = request.json['password']
#     user = users.find_one({'email': email})
#     if user:
#         if user['password'] == password:
#             token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
#             return jsonify({'token': token})
#         else:
#             return jsonify({'message': 'Wrong password!'})
#     else:
#         return jsonify({'message': 'User not found!'})
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        users = mongo.db.user2
        token=None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "missing token"}), 401
        try:
            data=jwt.decode(token, SECRET_KEY)
            current_user=users.find_one({"email": data["public_id"]}).first()
        except:
            return jsonify({"message": "invalid token"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@main.route('/template', methods=['POST'])
def insert_new_template():
    templates = mongo.db.template2
    id = request.json['id']
    template_name=  request.json['template_name']
    subject = request.json['subject']
    body= request.json['body']
    templates.insert_one({'id':id, 'template_name': template_name, 'subject': subject, 'body': body})
    return jsonify({'id':id,'template_name': template_name, 'subject': subject, 'body': body})


@main.route('/template', methods=['GET'])
def get_all_template():
    templates = mongo.db.template2
    template = templates.find()
    template_list = []
    for i in template:
        template_list.append({'id': i['id'],'template_name': i['template_name'],'subject': i['subject'], 'body': i['body']})
    return jsonify({'template': template_list})


@main.route('/template/<string:id>', methods=['GET'])
def get_single_template(id):
    templates = mongo.db.template2
    template = templates.find_one({'id': id})
    if not template:
        return jsonify({'message': 'Template not found!'})
    return jsonify({'id':id,'template_name': template['template_name'],'subject': template['subject'], 'body': template['body']})

@main.route('/template/<string:id>', methods=['PUT'])
def update_template(id):
    templates = mongo.db.templates2
    template = templates.find_one({'id': id})
    if not template:
        return jsonify({'message': 'Template not found!'})
    templates.update_one({'id': id}, {'$set': {'template_name': request.json['template_name'], 'subject': request.json['subject'], 'body': request.json['body']}})
    return jsonify({'id':id,'template_name': template['template_name'],'subject': template['subject'], 'body': template['body']})


@main.route('/template/<string:id>', methods=['DELETE'])
def delete_template(id):
    templates = mongo.db.templates2
    template = templates.find_one({'id': id})
    if not template:
        return jsonify({'message': 'Template not found!'})
    templates.delete_one({'id': id})
    return jsonify({'message': 'Template deleted!'})



# @main.route('/template/<string:id>', methods=['PUT'])
# def updtate_single_template(id):
#     templates = mongo.db.template2
#     template = templates.find_one({'_id': id})
#     if not templates:
#         return jsonify({'message': 'Template not found!'})
#     template_name = request.json['template_name']
#     subject = request.json['subject']
#     body = request.json['body']
#     templates.update_one({'_id': id}, {'$set': {'template_name': template_name, 'subject': subject, 'body': body}})
#     return jsonify({'id':id,'template_name': template['template_name'],'subject': template['subject'], 'body': template['body']})


# @main.route('/template/<string:id>', methods=['DELETE'])
# def delete_single_template(id):
#     templates = mongo.db.template2
#     template = templates.find_one({'_id': id})
#     if not template:
#         return jsonify({'message': 'Template not found!'})
#     templates.delete_one({'_id': id})
#     return jsonify({'message': 'Template deleted!'})
