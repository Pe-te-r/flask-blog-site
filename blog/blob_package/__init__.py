from flask import Flask
from flask_bcrypt import Bcrypt

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SECRET_KEY']='123456789'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:peter@127.0.0.1/blob'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db=SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view='login'
login_manager.login_message_category='warning'
login_manager.init_app(app)






from blob_package import routes
