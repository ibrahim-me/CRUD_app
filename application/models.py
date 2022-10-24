from .database import *
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager

class Trackers(db.Model):
    __tablename__ = 'tracker'
    tracker_id = db.Column(db.Integer,nullable=False,primary_key=True,unique=True)
    name = db.Column(db.String,nullable=False,unique=True)
    description = db.Column(db.String, nullable=False)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.username')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String,nullable=False,primary_key=True,unique=True)
    name = db.Column(db.String,nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    relation = db.relationship("Trackers", secondary="your_tracker")
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Your_Tracker(db.Model):
    __tablename__ = 'your_tracker'
    relation_id = db.Column(db.Integer,nullable=False,primary_key=True,unique=True)
    rtracker_id = db.Column(db.Integer,db.ForeignKey("tracker.tracker_id"),nullable=False,primary_key=True,unique=True)
    rusername = db.Column(db.String,db.ForeignKey("users.username"),nullable=False,primary_key=True,unique=True)
    #value=db.Column(db.Integer)
    name=db.Column(db.String)

class Tracker_Data(db.Model):
	__tablename__ = 'tracker_data'
	entry_id=db.Column(db.Integer,nullable=False,primary_key=True)
	your_tracker_id=db.Column(db.Integer,db.ForeignKey("your_tracker.relation_id"),nullable=False,primary_key=True, unique=True)
	time= db.Column(db.String, nullable=False)
	value=db.Column(db.String, nullable=False)
