import flask
from flask import Flask,jsonify,flash
import pymysql
import os
import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=12345
host_ip=socket.gethostname()

s.connect(("127.0.0.1",port))
#import socket
#ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)



app=Flask(__name__)

app.secret_key='12345'
@app.route('/')
def home():
	return flask.render_template("homepage.html",user_image= "static/index.gif")
@app.route("/login",methods=['POST','GET'])
def login():
	return flask.render_template('/login.html')

@app.route("/signup",methods=['POST','GET'])
def signup():
	return flask.render_template('/signup.html')

#@app.route('/editor')
#def editor():
#	return flask.render_template('/editor.html')

@app.route('/test',methods=['POST','GET'])
def test():
	print("test")
	s.send("Test")
	#print(s.recv(1024))
	return flask.render_template('test.html')




@app.route('/practice',methods=['POST','GET'])
def practice():
	print("practice")
	s.send("PRACTICE")
	#print(s.recv(1024))
	return flask.render_template('practice.html')

	

	

@app.route('/login_process',methods=['POST','GET'])
def login_process():
	global s
	if(flask.request.method=='POST'):
		username=flask.request.form['username']
		print(username)
		password=flask.request.form['password']
	else:
		username=flask.request.args.get('username',0,type=str)
		password=flask.request.args.get('password',0,type=str)

		print('login')

		s.send('login')
		state=s.recv(1024)
		print(state)
		if(state=='error'):
			return flask.render_template('login.html',error="PLEASE TRY AGAIN!")
		print("login username",username)
		s.send(username)
		print(s.recv(1024))

		print("login password",password)
		s.send(password)
		print(s.recv(1024))

		confirmation=s.recv(1024)
		print(confirmation)

		if(confirmation=="pass"):
			flask.session['username']=username
			return flask.render_template('mode.html')
		else:
			return flask.render_template('login.html',error="INVALID USERNAME OR PASSWORD")



@app.route('/signup_process',methods=['POST','GET'])
def signup_process():
	global s
	if(flask.request.method=='POST'):
		username=flask.request.form['username']
		print(username)
		password=flask.request.form['password']
	else:
		username=flask.request.args.get('username',0,type=str)
		password=flask.request.args.get('password',0,type=str)
		
		s.send('signup')
		state=s.recv(1024)
		print(state)
		if(state=='error'):
			return flask.render_template('signup.html',error="PLEASE TRY AGAIN!")

		s.send(username)
		print(s.recv(1024))
		s.send(password)
		print(s.recv(1024))
		confirmation=s.recv(1024)
		print(confirmation)
		if(confirmation=="pass"):
			flask.session['username']=username

			return flask.render_template('mode.html')
		else:
			return flask.render_template('signup.html',error="UNABLE TO REGISTER USER.USERNAME ALREADY EXISTS, PLEASE TRY AGAIN")


@app.route("/background_process",methods=['POST','GET'])
def background_process():
	global s
	if flask.request.method=='POST':
		code=flask.request.form["code"]
		print(code)
	else:

		code=flask.request.args.get('code',0,type=str)
		language=flask.request.args.get('language',0,type=str)
		#print(type(code))
		#print(code)
		#print(s.recv(1024).decode())
		#print("sending->",language)
		#language="python"
		s.send(language)
		print(s.recv(1024))
		s.send(code)
		data=s.recv(1024)
		print("recv->",data)
		
		
		
	return jsonify(result=data)



if __name__=='__main__':
	app.run()
