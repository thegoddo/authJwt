from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

from app.models import db
jwt = JWTManager()

def create_app(config_class=Config):
    app  = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    from app.api.v1_auth import auth_bp
    from app.api.v1_tasks import tasks_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    
    return app