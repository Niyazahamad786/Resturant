from flask_wtf import FlaskForm
#from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,DateField,TimeField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
#import sqlite3
#conn =sqlite3.connect('dite.db',check_same_thread=False)
#c=conn.cursor()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
  
    
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Reserve(FlaskForm):
    title=SelectField('Title*',validators=[DataRequired()], choices=[('Miss.','Miss.'),('Mr.','Mr.'),('Mrs.','Mrs.')])
    first=StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    last=StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])    
    phone=StringField('Phone Number',
                        validators=[DataRequired(), Length(min=10, max=10)])  
    city = SelectField('City*', choices=[('Bengluru','Bengluru'),('California','California'),('NewDelhi','New Delhi'),('Mumbai','Mumbai'),('CapeTown','Cape Town'),('SanFrancisco','San Francisco'),('Texas','Texas'),('Miami','Miami'),('Rio','Rio'),('Berlin','Berlin'),('France','France'),('NewYork','New York')])
    table=SelectField('Type Of Table',validators=[DataRequired()], choices=[('2','Table for 2'),('3','Table for 3'),('4','Table for 4'),('5','Table for 5'),('6','Table for 6')])
    purpose=SelectField('Purpose',validators=[DataRequired()], choices=[('Meeting','Meeting'),('Casual','Casual'),('Celebration','Celebration')])
    meal=SelectField('Meal Plan',validators=[DataRequired()], choices=[('Breakfast','Breakfast'),('Lunch','Lunch'),('Dinner','Dinner')])
    date=DateField('Date',format='%Y-%m-%d')
    time=StringField('Time')
    submit = SubmitField('Reserve')