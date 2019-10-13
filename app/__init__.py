from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
from app import routes
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)
login = LoginManager(app)
