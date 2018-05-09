from flask import Flask, render_template, redirect, request, session
import re
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
# create a regular expression object that we can use run operations on
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = connectToMySQL('friendsdb')

@app.route('/')
def index():
    all_friends = mysql.query_db("SELECT first_name,last_name,occupation FROM friends")
    print("Fetched all friends", all_friends)
    return render_template('code.html', friends = all_friends)

@app.route('/create_friend', methods=['Post'])
def create():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    
    mysql.query_db(query, data) # just pass a string to the flash function
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

