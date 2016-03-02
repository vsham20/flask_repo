from datetime import datetime
import hashlib
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
#from app.exceptions import ValidationError
from flask.ext.mongoengine.wtf import model_form
from . import db

class User(UserMixin, db.Document):
    email = db.StringField( unique=True, required=True)
    
    password = db.StringField(max_length=128)
    """@password.setter
                def verify_password(self, password):
                    return check_password_hash(self.password_hash, password)
            """

    def __init__(self  ,password , email):
        self.password = password
        self.email = email
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.username

