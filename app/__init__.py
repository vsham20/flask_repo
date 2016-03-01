import os
from flask.ext.login import LoginManager
from flask import Flask


app = Flask(__name__)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
from app import views
