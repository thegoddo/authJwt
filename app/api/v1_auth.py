from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_v1', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filetr_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400
    
    new_user = User(username=data['username'], role=data.get('role', 'user'))
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_passworda(data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role, 'id': user.id})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401