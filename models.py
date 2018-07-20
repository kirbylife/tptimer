from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25),unique=True)
    wcaId = db.Column(db.String(10),nullable=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(93))
    create_at = db.Column(db.DateTime,default=datetime.datetime.now)

    times=db.relationship("Time")

    def __init__(self,username,wcaId,email,password):
        self.username=username
        self.wcaId=wcaId
        self.email=email
        self.password=self.__createPassword(password)

    def __createPassword(self, password):
        return generate_password_hash(password)

    def verifyPassword(self,password):
        return check_password_hash(self.password,password)

class Time(db.Model):
    __tablename__="times"
    id=db.Column(db.Integer,primary_key=True)
    user=db.Column(db.Integer,db.ForeignKey("users.id"))
    cube=db.Column(db.String(20))
    time=db.Column(db.Integer)
    displayTime=db.Column(db.String(15))
    scramble=db.Column(db.String(320))

    def __init__(self,user,cube,time,displayTime,scramble):
        self.user=user
        self.cube=cube
        self.time=time
        self.displayTime=displayTime
        self.scramble=scramble