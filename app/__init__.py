import os
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask import Flask


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "bookmark_database"}
app.config['SECRET_KEY'] = 'vaishali20'

app.config.from_object('config')
db = MongoEngine(app)
lm = LoginManager()
lm.init_app(app)
from app import views
