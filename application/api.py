from flask_restful import Resource
from application.models import *
from .database import *
from flask_sqlalchemy import SQLAlchemy
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
from flask_login import current_user


class User_API(Resource):
    #@auth_required("token")
    def get(self):
        return {"username": current_user.username, "email": current_user.email, }
        #requires flask login
    def put(self):
        pass
    def delete(self):
        pass
    def post(self):
        pass



class trackerAPI(Resource):
    def get(self):        
        #should return all trackers of a user 
        user_trackers=db.session.query(Your_Tracker).filter(Your_Tracker.rusername==current_user.username).all()
        trackers={}
        for tracker in user_trackers:
            trackers[tracker.relation_id]=[tracker.rtracker_id, tracker.name]
        return trackers
    def patch(self):
        #should update a tracker 
        
    def delete(self):
        #delete a tracker 
        pass
    def post(self):
        #create a new tracker  
        pass


class logAPI(Resource):
    def get(self):
        #return logs 
        pass
    def put(self):
        #update a log chuck this ig
        pass
    def post(self):
        #create a new log
        pass
    def delete(self):
        #delete a log
        pass