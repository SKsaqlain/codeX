import socket
import pymysql
import os
import thread
import threading
# from _thread import *

lock=threading.Lock()

try:
	conn=pymysql.connect(host="localhost",user="root",password="123",database="code_editor");
except:
	conn=pymysql.connect(host="localhost",user="root",password="123");
	conn.cursor().execute('create database code_editor')
	conn.cursor().execute('create table code_editor.user_data (username varchar(255) PRIMARY KEY,password varchar(255))')
	conn.commit()
	conn=pymysql.connect(host="localhost",user="root",password="123",database="code_editor");
cursor=conn.cursor()



s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=12345
host=socket.gethostname()
print(host)
s.bind(('',port))

s.listen(5)
languages=["python","c","java","cpp"]
available_client=list()

def python_executor(code):
	data=open("code"+"_py.py","w")
	data.write(code)
	data.close()
	os.system("python2 code_py.py 2>code_intermediate.txt 1>code_output.txt")
	inter=open("code_intermediate.txt",'r')
	error=inter.readlines()
	data=None
	if(len(error)==0):
		
		inter=open("code_output.txt",'r')
		data=''.join(inter.readlines())
		print(data)
	else:
		data=''.join(error)
	os.system("rm code_py.py")
	os.system("rm code_intermediate.txt")
	os.system("rm code_output.txt")
	return data


def java_executor(code):
	data=open("code_j.java","w")
	data.write("import java.util.*;\nimport java.lang.*;\n")
	data.write("public class code_j{\n")
	data.write(code)
	data.write("}")
	data.close()
	os.system("javac code_j.java 2>code_intermediate.txt")
	inter=open("code_intermediate.txt",'r')
	error=inter.readlines()
	if(len(error)==0):
		os.system("java code_j > code_intermediate.txt")
		inter=open("code_intermediate.txt",'r')
		data=''.join(inter.readlines())
		print(data)
	else:
		data=''.join(error)	
	os.system("rm code_j.java")
	os.system("code_intermediate.txt")
	os.system("rm *.class")
	return data



def c_executor(code):
	data=open("code_c.c","w")
	data.write(code)
	data.close()
	os.system("gcc code_c.c 2>code_intermediate.txt")
	inter=open("code_intermediate.txt",'r')
	error=inter.readlines()
	if(len(error)==0):
		os.system("./a.out > code_intermediate.txt")
		inter=open("code_intermediate.txt",'r')
		data=''.join(inter.readlines())
		print(data)
	else:
		print("errror")
		data=''.join(error)

	os.system("rm code_c.c")
	os.system("rm code_intermediate.txt")
	return data




def cpp_executor(code):
	data=open("code_cpp.cpp","w")
	data.write(code)
	data.close()
	os.system("g++ code_cpp.cpp 2>code_intermediate.txt")
	inter=open("code_intermediate.txt",'r')
	error=inter.readlines()
	if(len(error)==0):
		os.system("./a.out > code_intermediate.txt")
		inter=open("code_intermediate.txt",'r')
		data=''.join(inter.readlines())
		print(data)
	else:
		print("errror")
		data=''.join(error)

	os.system("rm code_cpp.cpp")
	os.system("rm code_intermediate.txt")
	return data



def client_listener_test(c,addr):
	print("In test")
	print(addr[0])
	while(1):
		print("recv->")
		data=c.recv(1024)
		#print(data)
		c.send("language received")
		try:
			lock.acquire()
			if(data=="python"):
				print("getting python script from the client")
				code=c.recv(1024)
				print(code)
				print("calling python excutor")
				output=python_executor(code)
				#os.system(c)
				os.system("echo '"+output+"'>output.txt")
				os.system("diff -wB output.txt result.txt > diff.txt")
				diff_fd=open("diff.txt","r+")
				l=diff_fd.readline()
				if(len(l)==0):
					print("Done executing")
					c.send("U got perfect score")
				else:
					print("Done executing")
					c.send("Wrong Ouput")
				#print("done executing")
				#print(output)
				#c.send(output)
			elif(data=="c"):

				print("getting c script from clinet")
				code=c.recv(1024)
				print(code)
				print("calling c executor")
				output=c_executor(code)

				print("done executing")
				print(output)
				c.send(output)
			elif(data=="java"):
				print("getting java script from the user")
				code=c.recv(1024)
				print(code)
				print("calling java executor")
				output=java_executor(code)

				print("done executing")
				print(output)
				c.send(output)
			else:
				pass
			lock.release()
		except:
			pass

def client_listener_practice(c,addr):
	print("In practice")
	print(addr[0])
	while(1):
		print("recv->")
		data=c.recv(1024)
		#print(data)
		c.send("language received")
		try:
			lock.acquire()
			if(data=="python"):
				print("getting python script from the client")
				code=c.recv(1024)
				print(code)
				print("calling python excutor")
				output=python_executor(code)
				
				print("done executing")
				print(output)
				c.send(output)
			elif(data=="c"):

				print("getting c script from clinet")
				code=c.recv(1024)
				print(code)
				print("calling c executor")
				output=c_executor(code)

				print("done executing")
				print(output)
				c.send(output)
			elif(data=="java"):
				print("getting java script from the user")
				code=c.recv(1024)
				print(code)
				print("calling java executor")
				output=java_executor(code)

				print("done executing")
				print(output)
				c.send(output)
			else:
				pass
			lock.release()
		except:
			pass


def login(c):
	print("In login function")
	username=c.recv(1024)
	print("username",username)
	c.send("username received")
	password=c.recv(1024)
	c.send("password received")
	user_present=cursor.execute("select * from user_data where username='%s' and password ='%s'"%(username,password))
	if(user_present):
		c.send("pass")
		return 1
	else:
		c.send("fail")
		return 0

def signup(c):
	print("In sign-up function")
	username=c.recv(1024)
	print("username",username)
	c.send("username received")
	password=c.recv(1024)
	c.send("password received")
	user_present=cursor.execute("select * from user_data where username='%s'"%(username))
	print("user_present",user_present)
	if(user_present):
		c.send("fail")
		return 0
	else:
		cursor.execute("insert into user_data values('%s','%s')"%(username,password))
		conn.commit()
		c.send("pass")
		return 1



def server_listener(c,addr):
	print("server listining")
	state=c.recv(1024)
	print(state)
	flag=0
	if(state=='signup'):
		c.send("no-error")
		flag=signup(c)
	elif(state=='login'):
		#print("in login")
		c.send("no-error")
		flag=login(c)
	else:
		c.send("error")
	if(flag):
		#mode=c.recv(1024)
		mode=c.recv(1024)
		print(mode)
		if(mode=="Test"): # Question
			c.send("redirecting to  test")
			print("test")
			thread.start_new_thread(client_listener_test,(c,addr,))
		else:
			c.send("redirecting to practice")
			print('practice')
			thread.start_new_thread(client_listener_practice,(c,addr,))
		
		print("connected client to a thread process")
		return
	else:
		server_listener(c,addr)
		return
def main():
	while(1):
		c,addr=s.accept()
		print(str(addr))
		if addr not in available_client:
			available_client.append(addr)
			thread.start_new_thread(server_listener,(c,addr,))
		
if ('__main__'==__name__):
	main()

	
