from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo

class Registration(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=5,max=20)])
    email=EmailField('email',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=5,max=20)])
    confrim_password =PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField(label='register')

class Login(FlaskForm):
    email=EmailField('email',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired(),Length(min=5,max=20)])
    submit=SubmitField(label='login')

class UpdateAccount(FlaskForm):
    username=StringField('username',validators=[DataRequired(),Length(min=5,max=20)])
    email=EmailField('email',validators=[DataRequired()])
    submit=SubmitField(label='update')

class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField(label='post')
