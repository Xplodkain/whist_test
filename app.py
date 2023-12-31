from flask import Flask, request, make_response
import mysql.connector
import socket
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)

#logging.basicConfig(filename='./logs/flask.log',level=logging.DEBUG)

def db_connect(): 
    db = mysql.connector.connect(
        host="database-1.cyascaiadbtj.eu-west-2.rds.amazonaws.com",
        user="root", 
        port=3306,
        password="12345678",
        database="mydb"
    )
    return db

# 172.21.0.1

db=db_connect()
print(db)
access_log = ('CREATE TABLE IF NOT EXISTS access_log ('
                     'id INT AUTO_INCREMENT PRIMARY KEY,'
                     'date_time DATETIME NOT NULL,'
                     'client_ip VARCHAR(15) NOT NULL,'
                     'server_ip VARCHAR(15) NOT NULL'
                     ')')
cursor = db.cursor()
cursor.execute(access_log)
cursor.close()



@app.route('/')
def counter():

    cursor = db.cursor()
    
   
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    server_ip = socket.gethostbyname(socket.gethostname())
    response = make_response(f"The server's internal IP address is: {server_ip}")
    expiration = datetime.now() + timedelta(minutes=5)
    response.set_cookie('internal_ip', server_ip, expires=expiration)
    client_ip = request.remote_addr
    log_entry = (date_time, client_ip, server_ip)
    cursor.execute('INSERT INTO access_log (date_time, client_ip, server_ip) VALUES (%s, %s, %s)', log_entry )

    db.commit()
    cursor.close()

    return  response
        
@app.route('/showcount')
def show_count():
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM access_log')
    result = cursor.fetchone()
    
        
    return f'The count is: {result[0]}'
 
    

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
