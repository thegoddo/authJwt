from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Task
from app import db

tasks_bp = Blueprint('tasks_v1', __name__, url_prefix='/api/v1/tasks')


@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    data = request.get_json()

    new_task = Task(title=data['title'], content=data.get(
        'content', ''), user_id=current_user['id'])
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


@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_tasks_by_id(id):

    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({"msg": "Task not found"}), 404

    if current_user['role'] != 'admin' and task.user_id != current_user['id']:
        return jsonify({"msg": "Unauthorized access to this task"}), 403

    return jsonify({"id": task.id, "title": task.title, "content": task.content}), 200


@tasks_bp.route("/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_by_id(id):
    current_user = get_jwt_identity()
    task = Task.query.filter_by(id=id).first()

    if not task:
        return jsonify({"msg": "Task not found"}), 404

    if current_user['role'] != 'admin' and task.user_id != current_user['id']:
        return jsonify({"msg": "Unauthorized access to this task"}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": f"Task {id} successfully deleted"}), 200
