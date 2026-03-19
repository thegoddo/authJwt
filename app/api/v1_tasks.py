from flask import Blueprint, request, jsonify
from app.models import Task
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

tasks_bp = Blueprint('tasks_v1', __name__, url_prefix='/api/v1/tasks')

@tasks_bp.route('/', methods=['POST'])
@jwt_required
def create_task():
    current_user = get_jwt_identitiy()
    data = request.get_json()
    
    new_task = Task(title=data['title'], content=data.get('content', ''), user_id=current_user['id'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Task created", "id": new_task.id}), 201

@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    # Role-based access logic: Admins see all, users see their own
    if current_user['role'] == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=current_user['id']).all()
        
    return jsonify([{"id": t.id, "title": t.title, "content": t.content} for t in tasks]), 200

