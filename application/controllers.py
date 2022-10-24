from flask import Flask, request
from flask import render_template
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from flask import abort, redirect, url_for
from application.models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .database import *
from flask_security import login_required, roles_accepted, roles_required,current_user


@app.route('/', methods=['GET', 'POST'])
@login_required
def login():
	'''if request.method == 'GET':
					return render_template('login.html')
				elif request.method == 'POST':
					email= request.form['email']
					password= request.form['pass']
					print("login attempt by ",email)
					try:
						users=db.session.query(Users).filter(Users.email==email).one()
						if(users.password==password):
							return redirect("/dashboard/"+email)
						else:
							raise Exception
					except Exception:
						print("error")
						return render_template('try_again.html')'''
	email = current_user.email
	print(current_user)
	return redirect("/dashboard/"+email)	
	
	
@app.route('/add_tracker/<string:email>',methods=['GET', 'POST'])
@login_required
def add_tracker(email):
	if request.method == 'GET':
		trackers= Trackers.query.all()
		users=db.session.query(Users).filter(Users.email==email).one()
		return render_template('add_tracker.html', trackers=trackers,user=users)
	
	elif request.method == 'POST':
		trackers= Trackers.query.all()
		users=db.session.query(Users).filter(Users.email==email).one()
		print("\n\n\n ----------------------------------------post request sent------------------------------------------------- \n \n \n")
		tracker_name=request.form["tracker_name"]
		tracker_type=request.form["tracker_type"]
		print(tracker_name,tracker_type)
		tracker=db.session.query(Trackers).filter(Trackers.tracker_id==tracker_type).one()
		users.relation.append(tracker)
		
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return redirect("/dashboard/"+email)
		else:
			user_tracker=db.session.query(Your_Tracker).filter(Your_Tracker.rtracker_id==tracker_type, Your_Tracker.rusername==users.username).first()
			user_tracker.name=tracker_name
			try:
				db.session.commit()
			except:
				db.session.rollback()
				print("-----------------------something went wrong----------------------------\n\n\n")
				return redirect("/dashboard/"+email)
			else:
				return redirect("/dashboard/"+email)


@app.route('/edit_tracker/<string:username>/<int:tracker_id>',methods=['GET', 'POST'])
def edit_tracker(username, tracker_id):
	if request.method == 'GET':
		users=db.session.query(Users).filter(Users.username==username).one()
		tracker=db.session.query(Your_Tracker).filter(Your_Tracker.rusername==username, Your_Tracker.rtracker_id==tracker_id).one()
		if tracker_id==1:
			return render_template("edit_tracker_mood.html", user=users, tracker=tracker,tracker_id=tracker_id)
		if tracker_id==2:
			return render_template("edit_tracker_sleep.html", user=users, tracker=tracker,tracker_id=tracker_id)
		if tracker_id==3:
			return render_template("edit_tracker_temp.html", user=users, tracker=tracker,tracker_id=tracker_id)
		if tracker_id==4:
			return render_template("edit_tracker_running.html", user=users, tracker=tracker,tracker_id=tracker_id)
		if tracker_id==5:
			return render_template("edit_tracker_custom.html", user=users, tracker=tracker,tracker_id=tracker_id)
		if tracker_id==6:
			return render_template("edit_tracker_custom_mcq.html", user=users, tracker=tracker,tracker_id=tracker_id)


	if request.method == 'POST':
		tracker=db.session.query(Your_Tracker).filter(Your_Tracker.rusername==username, Your_Tracker.rtracker_id==tracker_id).one()
		users=db.session.query(Users).filter(Users.username==username).one()
		email=users.email
		
		if tracker_id==1:
			mood=request.form["flexRadioDefault"]
			time=request.form["timestamp"]
			#print(mood,time,"\n\n\n\n\n\n\n\n\n\n\n")
			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=mood)
			db.session.add(data)
		

		if tracker_id==2:
			sleepDuration=request.form["duration"]
			time=request.form["timestamp"]
			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=sleepDuration)
			db.session.add(data)

		if tracker_id==3:
			temp=request.form["temp"]
			time=request.form["timestamp"]

			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=temp)
			db.session.add(data)

		if tracker_id==4:
			runDuration=request.form["duration"]
			time=request.form["timestamp"]
			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=runDuration)
			db.session.add(data)

		if tracker_id==5:
			num=request.form["num"]
			time=request.form["timestamp"]

			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=num)
			db.session.add(data)

		if tracker_id==6:
			val=request.form["flexRadioDefault"]
			time=request.form["timestamp"]
			#print(mood,time,"\n\n\n\n\n\n\n\n\n\n\n")
			data=Tracker_Data(your_tracker_id=tracker.relation_id, time=time, value=val)
			db.session.add(data)


		try :
			db.session.commit()
			return redirect("/dashboard/"+email)
		except:
			db.session.rollback()
			print("\n\n\n -------------------------------------something went wrong----------------------------\n\n\n\n")
			return redirect("/dashboard/"+email)


@app.route('/delete_tracker/<string:username>/<int:tracker_id>',methods=['GET', 'POST'])
def delete_tracker(username, tracker_id):
	if request.method == 'GET':
		user=db.session.query(Users).filter(Users.username==username).one()
		tracker_to_delete=db.session.query(Your_Tracker).filter(Your_Tracker.rusername==username, Your_Tracker.rtracker_id==tracker_id).one()
		print(tracker_to_delete,"\n\n\n")
		trackers_data_to_del=db.session.query(Tracker_Data).filter(Tracker_Data.your_tracker_id==tracker_to_delete.relation_id).all()
		for i in trackers_data_to_del:
			db.session.delete(i)

		db.session.delete(tracker_to_delete)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return redirect("/dashboard/"+user.email)
		else:
			return redirect("/dashboard/"+user.email) 



@app.route('/tracker_details/<string:relation_id>',methods=['GET', 'POST'])
def tracker_details(relation_id):
	if request.method == 'GET':
		tracker=db.session.query(Your_Tracker).filter(Your_Tracker.relation_id==relation_id).one()
		tracker_data_entries= db.session.query(Tracker_Data).filter(Tracker_Data.your_tracker_id==relation_id).all()
		print(tracker_data_entries)
		list_to_plot=[]
		if(tracker.rtracker_id==2 or tracker.rtracker_id==4):
			list_to_plot=[int(j.value[:2]+j.value[3:]) for j in tracker_data_entries]
		else:
			list_to_plot=[int(j.value) for j in tracker_data_entries]
		#print(list_to_plot,"\n\n\n\n\n\n\n")
		x_axis=[i for i in range(len(list_to_plot))]

		plt.plot(x_axis, (list_to_plot), color='black', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='black', markersize=12)
		plt.xticks([])
		
		plt.savefig('static/plot.jpg')
		plt.clf()
		return render_template('tracker_details.html',tracker=tracker,tracker_data_entries=tracker_data_entries)



@app.route('/edit_data/<int:entry_id>',methods=['GET', 'POST'])
def edit_data(entry_id):
	if request.method=="GET":
		time=db.session.query(Tracker_Data).filter(Tracker_Data.entry_id==entry_id).one().time
		your_tracker_id=db.session.query(Tracker_Data).filter(Tracker_Data.entry_id==entry_id).one().your_tracker_id
		tracker=db.session.query(Your_Tracker).filter(Your_Tracker.relation_id==your_tracker_id).one()
		tracker_id=tracker.rtracker_id
		if tracker_id==1:
			return render_template("edit_data_mood.html",  tracker=tracker,tracker_id=tracker_id, entry_id=entry_id,time=time)
		if tracker_id==2:
			return render_template("edit_data_sleep.html", entry_id=entry_id, tracker=tracker,tracker_id=tracker_id,time=time)
		if tracker_id==3:
			return render_template("edit_data_temp.html", entry_id=entry_id, tracker=tracker,tracker_id=tracker_id,time=time)
		if tracker_id==4:
			return render_template("edit_data_running.html", entry_id=entry_id, tracker=tracker,tracker_id=tracker_id,time=time)	
		if tracker_id==5:
			return render_template("edit_data_custom.html", entry_id=entry_id, tracker=tracker,tracker_id=tracker_id,time=time)
		if tracker_id==6:
			return render_template("edit_data_custom_mcq.html", entry_id=entry_id, tracker=tracker,tracker_id=tracker_id,time=time)



	if request.method=="POST":
		your_tracker=db.session.query(Tracker_Data).filter(Tracker_Data.entry_id==entry_id).one()
		your_tracker_id=your_tracker.your_tracker_id
		tracker=db.session.query(Your_Tracker).filter(Your_Tracker.relation_id==your_tracker_id).one()
		tracker_id=tracker.rtracker_id
		user=db.session.query(Users).filter(Users.username==tracker.rusername).one()
		email=user.email
		if tracker_id==1:
			mood=request.form["flexRadioDefault"]
			time=request.form["timestamp"]
			
			your_tracker.value=mood
			your_tracker.time=time
		

		if tracker_id==2:
			sleepDuration=request.form["duration"]
			time=request.form["timestamp"]
			your_tracker.value=sleepDuration
			your_tracker.time=time

		if tracker_id==3:
			temp=request.form["temp"]
			time=request.form["timestamp"]

			your_tracker.value=temp
			your_tracker.time=time

		if tracker_id==4:
			runDuration=request.form["duration"]
			time=request.form["timestamp"]
			your_tracker.value=runDuration
			your_tracker.time=time

		if tracker_id==5:
			num=request.form["num"]
			time=request.form["timestamp"]

			your_tracker.value=num
			your_tracker.time=time

		if tracker_id==6:
			val=request.form["flexRadioDefault"]
			time=request.form["timestamp"]
			
			your_tracker.value=val
			your_tracker.time=time


		try :
			db.session.commit()
			return redirect("/dashboard/"+email)
		except:
			db.session.rollback()
			print("\n\n\n -------------------------------------something went wrong----------------------------\n\n\n\n")
			return redirect("/dashboard/"+email)



@app.route('/create_account',methods=['GET', 'POST'])
def create_account():
	if request.method=="GET":
		return render_template("create_account.html")
	else:
		name = request.form["name"]
		password = request.form["password"]
		username = request.form["username"]
		email= request.form["email"]
		print(name,password,email,username)
		new_user= Users(username=username, name=name, password=password, email=email)
		db.session.add(new_user)
		try:
			db.session.commit()
			return redirect("/")
		except:
			db.session.rollback()
			return redirect("/")



@app.route('/delete_data/<int:entry_id>',methods=['GET', 'POST'])
def delete_data(entry_id):
	your_tracker=db.session.query(Tracker_Data).filter(Tracker_Data.entry_id==entry_id).one()
	your_tracker=db.session.query(Tracker_Data).filter(Tracker_Data.entry_id==entry_id).one()
	your_tracker_id=your_tracker.your_tracker_id
	tracker=db.session.query(Your_Tracker).filter(Your_Tracker.relation_id==your_tracker_id).one()
	tracker_id=tracker.rtracker_id
	user=db.session.query(Users).filter(Users.username==tracker.rusername).one()
	email=user.email
	db.session.delete(your_tracker)
	try :
		db.session.commit()
		return redirect("/dashboard/"+email)
	except:
		db.session.rollback()
		print("\n\n\n -------------------------------------something went wrong----------------------------\n\n\n\n")
		return redirect("/dashboard/"+email)

@app.route('/change/<int:relation_id>',methods=['GET', 'POST'])
def change_name(relation_id):
	tracker= db.session.query(Your_Tracker).filter(Your_Tracker.relation_id==relation_id).first()
	user=db.session.query(Users).filter(Users.username==tracker.rusername).first()
	email=user.email
	if request.method=="GET":
		return render_template("change_name.html",relation_id=relation_id)
	if request.method=="POST":
		tracker.name= request.form["tracker_name"]
		try:
			db.session.commit()
			return redirect("/dashboard/"+email)
		except:
			db.session.rollback()
			return redirect("/dashboard/"+email)


def last_value(user_trackers):
    last_tracked={}
    for tracker in user_trackers:
            last_tracked[tracker.relation_id]=0
    
    for i in last_tracked.keys():
        trackers=db.session.query(Tracker_Data).filter(Tracker_Data.your_tracker_id==i).all()
        if len(trackers)!=0:
            maxval=int(trackers[0].time[:2]+trackers[0].time[3:])
            for j in trackers:
                if (int(j.time[:2]+j.time[3:]))>=maxval:
                    last_tracked[i]=[j.value,"at"+j.time]


    return(last_tracked)


@app.route('/dashboard/<string:email>',methods=['GET', 'POST'])
@login_required
def dashboard(email):
	print(current_user.username)
	users=db.session.query(Users).filter(Users.email==email).one()
	user_trackers=db.session.query(Your_Tracker).filter(Your_Tracker.rusername==users.username).all()
	print(last_value(user_trackers))
	values=last_value(user_trackers)
	return render_template('index.html',user=users,trackers=user_trackers,values=values)
	if request.method == 'POST':
		return render_template('index.html',user=users)
