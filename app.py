import sys
import pandas as pd
import pymysql
from flask import Flask, request, render_template;
from flaskext.mysql import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))

app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

conn = pymysql.connect(host='localhost',
                        user='root',
                        password='blessings100%',
                        db='people',)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/sign', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        employeeDetails = request.form
        name = employeeDetails['name']
        password = employeeDetails['password']
        cur = conn.cursor()
        cur.execute("INSERT INTO EMPLOYEES(name, password) VALUES(%s, %s)", (name, password))
        conn.commit();
        cur.close();
        return """
        Your information has been successfully uploaded. <br> <p><a href="/sign">Go Back</a></p>
        """
    
    return render_template("sign.html")

@app.route('/roster')
def roster():
    cur = conn.cursor()
    results = cur.execute("SELECT * FROM EMPLOYEES")
    if results > 0: 
        employeeDetails = cur.fetchall()
        return render_template('roster.html', employeeDetails=employeeDetails)
    else:
        return """Nobody works here. <br><p><a href="</sign">Go Back</a></p>"""

@app.route("/login", methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            employeeDetails = request.form
            name = employeeDetails['name']
            password = employeeDetails['password']
            cur = conn.cursor()
            cur.execute("SELECT * FROM EMPLOYEES WHERE name = %s and password = %s", (name, password))
            record = cur.fetchone()
            if record is not None: 
                cur.close();
                msg = ("""
                You have successfully logged in. Welcome, {}<br> <p><a href="/login">Go Back</a></p>""").format(name)
                return msg
            
            else:
                return """
                Incorrect name or password. <br> <p><a href="/login">Go Back</a></p>
                """            

        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')