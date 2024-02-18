from uuid import uuid4
from flask_login import UserMixin
from datetime import datetime
from blob_package import db,login_manager

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)



class User(db.Model ,UserMixin):
    __tablename__='users'
    id =db.Column(db.UUID(as_uuid=True),primary_key= True,default=uuid4())
    username=db.Column(db.String(30),nullable=False,unique=True)
    email=db.Column(db.String(35),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)


class Post(db.Model):
    id =db.Column(db.UUID(as_uuid=True),primary_key= True,default=uuid4())
    title=db.Column(db.String(120),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.UUID(as_uuid=True),db.ForeignKey('users.id'),nullable=False)

