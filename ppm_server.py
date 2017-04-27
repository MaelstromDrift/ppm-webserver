from tables import FollowedProcess, Process, User, Task, ProcessTasks
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request

#load Flask
app = Flask(__name__)

#Connect to our database
engine = create_engine('mysql://root:maninthemiddle@localhost/ppm')
engine.echo = False

#setup a session to query and insert into the DB 
DBSession = sessionmaker()
session = DBSession()

#should probably abstract away constructing json statements for various things
def processToJson(process):
	jsonCollection = []
	for p in process:
		processDict = p.as_dict()
		processTasks = session.query(ProcessTasks).filter(ProcessTasks.processId == p._id).order_by(asc(ProcessTasks.taskOrder)).all()
		taskList = []
		for f in processTasks:
			taskList.append(f.taskId)
		processDict['tasks'] = taskList
		jsonCollection.append(processDict)
	return jsonify(jsonCollection)

@app.route('/all_processes/')
def all_processes():
	all_processes = session.query(Process).all()
	return processToJson(all_processes)

@app.route('/user_processes/<userId>/')
def user_processes(userId):
	processes = session.query(Process).filter(Process.creatorId == userId).all()
	return processToJson(processes)

@app.route('/followed_processes/<userId>/', methods=['GET'])
def followed_processes(userId):
	processes = []
	followed = session.query(FollowedProcess).filter(FollowedProcess.userId == userId).all()
	for f in followed:
		processes.append(session.query(Process).filter(Process._id == f.processId).one())
	return processToJson(processes)

@app.route('/user/<userId>/', methods=['GET'])
def get_user(userId):
	try:
		user = session.query(User).filter(User._id == userId).one()
	except:
		return 'User doesn\'t exist'
	userDict = user.as_dict()
	
	followedProcesses = session.query(FollowedProcess).filter(FollowedProcess.userId == userId).all()
	processList = []
	for f in followedProcesses:
		processList.append(f.processId)
	userDict['followed_processes'] = processList
	return jsonify(userDict)

@app.route('/verify/', methods=['POST'])
def verify_user():
	userInfo = request.get_json(silent=True)
	username = userInfo['username']
	password = userInfo['password']
	try:
		dbEntry = session.query(User).filter(User.username == username).one()
	except:
		return '[]'
	if userInfo['password'] == dbEntry.password:
		return jsonify(dbEntry.as_dict())
	return '[]'
@app.route('/follow/', methods=['POST'])
def follow_process():
	followInfo = request.get_json(silent=True)
	followedProcess = FollowedProcess(**followInfo)
	session.add(followedProcess)
	session.commit()
	return 'followed'

@app.route('/unfollow/', methods=['DELETE'])
def unfollow_process():
	try:
		followInfo = request.get_json(silent=True)
		followed = session.query(FollowedProcess).filter(FollowedProcess.userId==followInfo['userId']).filter(FollowedProcess.processId==followInfo['processId']).one()
		session.delete(followed)
		session.commit()
		return 'deleted'
	except:
		return 'nothing to delete'

@app.route('/task/<taskId>', methods=['GET'])
def get_task(taskId):
	try:
		task = session.query(Task).filter(Task._id == taskId).one()
	except:
		return '[]'
	return jsonify(task.as_dict())

@app.route('/task/', methods=['POST'])
def new_task():
	taskInfo = request.get_json(silent=True)
	task = Task(**taskInfo)
	session.add(task)
	session.commit()
	return str(task._id) 

@app.route('/process/<processId>', methods=['GET'])
def get_process(processId):
	try:
		process = session.query(Process).filter(Process._id == processId).one()
	except:
		return'[]'
	return jsonify(process.as_dict())

def link_tasks(processid, tasks):
	for i in range(0, len(tasks)):
		temp = {}
		temp['processId'] = processid
		temp['taskId'] = tasks[i]
		temp['taskOrder'] = i
		linkTask = ProcessTasks(**temp) 
		session.add(linkTask)

		session.commit()
@app.route('/process/', methods=['POST'])
def new_process():
	processInfo = request.get_json(silent=True)
	processDict = {}
	processDict['title'] = processInfo['title']
	processDict['description'] = processInfo['description']
	processDict['creatorId'] = processInfo['creatorId']
	processDict['categoryId'] = processInfo['categoryId']
	process = Process(**processDict)
	session.add(process)
	session.commit()
	link_tasks(process._id, processInfo['tasks'])
	return str(process._id)

@app.route('/user/', methods=['POST'])
def new_user():
	userInfo = request.get_json(silent=True)
	user = User(**userInfo)
	session.add(user)
	session.commit()
	return str(user._id)
