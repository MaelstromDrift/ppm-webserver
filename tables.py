from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 

Base = declarative_base()
engine = create_engine('mysql://root:password@localhost/ppm')
engine.echo = False

Base.metadata.bind = engine

class User(Base):
	__tablename__ = 'ppm_user'

	_id = Column(Integer, primary_key = True)
	username = Column(String(30), unique = True)
	firstName = Column(String(255))
	lastName = Column(String(255))
	password = Column(String(255))
	email = Column(String(255))
	def __init__(self, username, firstName, lastName, password, email):
		self.username = username
		self.firstName = firstName
		self.lastName = lastName
		self.password = password
		self.email = email

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}	
	
class Process(Base):
	__tablename__ = 'ppm_process'
	
	_id = Column(Integer, primary_key = True)
	title = Column(String(255))
	description = Column(String(500))
	creatorId = Column(Integer, ForeignKey(User._id))
	categoryId = Column(Integer)
	def __init__(self, title, description, creatorId, categoryId):
		self.title = title
		self.description = description
		self.creatorId = creatorId
		self.categoryId = categoryId

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}	

class FollowedProcess(Base):
	__tablename__ = 'ppm_follower'
	
	_id = Column(Integer, primary_key = True)
	userId = Column(Integer, ForeignKey(User._id))
	processId = Column(Integer, ForeignKey(Process._id))

class Category(Base):
	__tablename__ = 'ppm_process_category'
	
	categoryId = Column(Integer, primary_key = True)
	categoryName = Column(String(30), unique = True)

class Task(Base):
	__tablename__ = 'ppm_task'

	_id = Column(Integer, primary_key = True)
	title = Column(String(50))
	description = Column(String(500))
	creatorId = Column(Integer, ForeignKey(User._id))
	def __init__(self, title, description, creatorId):
		self.title = title
		self.description = description
		self.creatorId = creatorId
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns }

class ProcessTasks(Base):
	__tablename__ = 'ppm_process_followed_tasks'

	_id = Column(Integer, primary_key = True)	
	processId = Column(Integer, ForeignKey(Process._id))
	taskId = Column(Integer, ForeignKey(Task._id))
	taskOrder = Column(Integer)
	def __init__(self, processId, taskId, taskOrder):
		self.processId = processId
		self.taskId = taskId
		self.taskOrder = taskOrder
