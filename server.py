from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import connectToMySQL
import re
from flask_bcrypt import Bcrypt
import datetime
import socket
app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.secret_key = 'DoYouWantToBuildASnowman'
mysql = connectToMySQL('the_wall')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    if 'first_name' not in session.keys():
        session['first_name'] = ""
    if 'last_name' not in session.keys():
        session['last_name'] = ""
    if 'reg_email' not in session.keys():
        session['reg_email'] = ""
    if 'log_email' not in session.keys():
        session['log_email'] = ""
    return render_template('index.html', reg_email=session['reg_email'], log_email=session['log_email'], first_name=session['first_name'], last_name=session['last_name'])

@app.route('/register', methods=['POST'])
def register():
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['reg_email'] = request.form['reg_email']

    if len(request.form['first_name']) < 1:
        flash('First Name cannot be blank!', 'first_name')
    if len(request.form['first_name']) == 1:
        flash('First Name must be 2 or more characters!', 'first_name')
    if request.form['first_name'].isalpha() == False:
        flash('First Name can only contain letters!', 'first_name')
    
    if len(request.form['last_name']) < 1:
        flash('Last Name cannot be blank!', 'last_name')
    if len(request.form['last_name']) == 1:
        flash('Last Name must be 2 or more characters!', 'last_name')
    if request.form['last_name'].isalpha() == False:
        flash('Last Name can only contain letters!', 'last_name')


    if len(request.form['reg_email']) < 1:
        flash('Email cannot be blank!', 'reg_email')
    elif not EMAIL_REGEX.match(request.form['reg_email']):
        flash('Invalid email address!', 'reg_email')
    mysql = connectToMySQL('the_wall')
    registered_emails = mysql.query_db('SELECT email FROM the_wall.users')
    for i in registered_emails:
        if request.form['reg_email'].lower() == i['email'].lower():
            flash('Email address already registered!', 'reg_email')

    if len(request.form['password']) < 1:
        flash('Password cannot be blank!', 'password')
    if len(request.form['password']) > 0 and len(request.form['password']) < 8:
        flash('Password must be 8 or more characters!', 'password')

    if request.form['confirm_password'] != request.form['password']:
        flash('Password does not match!', 'confirm_password')

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        mysql = connectToMySQL("the_wall")
        query = "INSERT INTO the_wall.users (first_name, last_name, email, password, created_at, messages_in_inbox, messages_in_outbox, admin_level) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s, NOW(), 0, 0, 1);"
        data = { "first_name" : request.form['first_name'], "last_name" : request.form['last_name'], "email" : request.form['reg_email'].lower(), "password_hash" : pw_hash}
        mysql.query_db(query, data)
        mysql = connectToMySQL('the_wall')
        result = mysql.query_db('SELECT id FROM the_wall.users WHERE email ="'+session['reg_email']+'"')
        session['user_id'] = result[0]['id']
        print('line 74='+str(session['user_id']))
        session['logged_in'] = True
        return redirect("/inbox")

@app.route('/log_in', methods=['POST'])
def log_in():
    session['log_email'] = request.form['log_email']
    if len(request.form['log_email']) < 1:
        flash('Email cannot be blank!', 'log_email')
    elif not EMAIL_REGEX.match(request.form['log_email']):
        flash('Invalid email address!', 'log_email')

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        mysql = connectToMySQL("the_wall")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { "email" : request.form["log_email"].lower() }
        result = mysql.query_db(query, data)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
                session['user_id'] = result[0]['id']
                session['logged_in'] = True
                session['first_name'] = result[0]['first_name']
                session['admin_level'] = result[0]['admin_level']
                if result[0]['admin_level'] == 9:
                    return redirect("/admin")
                else:
                    return redirect("/inbox")
    flash("You could not be logged in", 'log_email')
    return redirect("/")

@app.route('/inbox')
def inbox():
    if 'logged_in' not in session.keys():
        hostname=socket.gethostname() 
        IPAddr=socket.gethostbyname(hostname)  
        return render_template('error.html', IPAddr=IPAddr)

    #These lines pull a list of users to populate the outbox forms
    mysql = connectToMySQL('the_wall')
    user_list = mysql.query_db('SELECT id, first_name FROM users')
    
    #These lines pull a list of messages to populate the inbox list
    mysql = connectToMySQL('the_wall')
    session['messages_in_inbox'] = mysql.query_db('SELECT messages_in_inbox FROM users WHERE id = '+str(session['user_id'])+';')
    print('line 112='+str(session['messages_in_inbox']))
    if session['messages_in_inbox'][0]['messages_in_inbox'] == 1:
        mysql = connectToMySQL('the_wall')
        message_list = mysql.query_db('SELECT messages.id, messages.message_text, messages.recipient_id, messages.user_id, messages.created_at, users.first_name FROM messages LEFT JOIN users ON messages.user_id = users.id ORDER BY created_at DESC')
    else:
        message_list= []
    
    #These lines pull the count of outbox messages for the outbox counter.
    mysql = connectToMySQL('the_wall')
    session['messages_in_outbox'] = mysql.query_db('SELECT messages_in_outbox FROM users WHERE id = '+str(session['user_id'])+';')
    print('line 122='+str(session['messages_in_outbox']))
    if session['messages_in_outbox'][0]['messages_in_outbox'] == 1:
        mysql = connectToMySQL('the_wall')
        outbox_count = mysql.query_db('SELECT COUNT(user_id) "outbox_count" FROM messages WHERE user_id = '+str(session['user_id'])+';')
        session['outbox_count'] = outbox_count[0]['outbox_count']
    else:
        session['outbox_count'] = 0
    
    #These lines pull the count of inbox messages for the inbox counter.
    if session['messages_in_inbox'][0]['messages_in_inbox'] == 1:
        mysql = connectToMySQL('the_wall')
        inbox_count = mysql.query_db('SELECT COUNT(recipient_id) AS "inbox_count" FROM messages WHERE recipient_id = '+str(session['user_id'])+';')
        session['inbox_count'] = inbox_count[0]['inbox_count']
        print('line 135='+str(session['inbox_count']))
    else:
        session['inbox_count'] = 0
    return render_template('inbox.html', user_list=user_list, message_list=message_list)


@app.route('/send_message', methods=['POST'])
def send_message():
    mysql = connectToMySQL("the_wall")
    query = "INSERT INTO the_wall.messages (message_text, recipient_id, created_at, user_id) VALUES (%(message_text)s, %(recipient_id)s, NOW(), %(user_id)s);"
    data = { "message_text" : request.form['message_text'], "recipient_id" : request.form['recipient_id'], "user_id" : session['user_id']}
    mysql.query_db(query, data)
    # These three lines change the messages_in_inbox flag to 1 for recipient_id
    mysql = connectToMySQL("the_wall")
    query = "UPDATE the_wall.users SET messages_in_inbox = 1 WHERE id = %(recipient_id)s;"
    data = { "recipient_id" : request.form['recipient_id'] }
    mysql.query_db(query, data)
    # These three lines change the messages_in_outbox flag to 1 for user_id
    mysql = connectToMySQL("the_wall")
    query = "UPDATE the_wall.users SET messages_in_outbox = 1 WHERE id = %(user_id)s;"
    data = { "user_id" : session['user_id'] }
    mysql.query_db(query, data)
    return redirect("/inbox")

@app.route('/delete_message', methods=['POST'])
def delete_message():
    mysql = connectToMySQL("the_wall")
    query = "DELETE FROM the_wall.messages WHERE id = %(id)s;"
    data = { "id" : request.form['message_id'] }
    mysql.query_db(query, data)
    return redirect("/inbox")

@app.route('/admin')
def admin():
    if 'logged_in' not in session.keys():
        hostname=socket.gethostname() 
        IPAddr=socket.gethostbyname(hostname)  
        return render_template('error.html', IPAddr=IPAddr)
    mysql = connectToMySQL("the_wall")
    query = "SELECT admin_level FROM users WHERE id = %(id)s;"
    data = { "id" : session["user_id"] }
    result = mysql.query_db(query, data)
    if result[0]['admin_level'] == 9:
        mysql = connectToMySQL("the_wall")
        user_list = mysql.query_db("SELECT * FROM users;")
        return render_template('/admin.html', user_list = user_list)
    else:
        return render_template('nope.html')

@app.route('/remove', methods=['POST'])
def remove():
    mysql = connectToMySQL("the_wall")
    query = "DELETE FROM the_wall.users WHERE id = %(id)s;"
    data = { "id" : request.form['id'] }
    mysql.query_db(query, data)
    mysql = connectToMySQL("the_wall")
    query = "DELETE FROM the_wall.messages WHERE user_id = %(id)s;"
    data = { "id" : request.form['id'] }
    mysql.query_db(query, data)
    mysql = connectToMySQL("the_wall")
    query = "DELETE FROM the_wall.messages WHERE recipient_id = %(id)s;"
    data = { "id" : request.form['id'] }
    mysql.query_db(query, data)
    return redirect('/admin')

@app.route('/remove_admin', methods=['POST'])
def remove_admin():
    mysql = connectToMySQL("the_wall")
    query = "UPDATE the_wall.users SET admin_level = 0 WHERE id = %(id)s;"
    data = { "id" : request.form['id'] }
    mysql.query_db(query, data)
    return redirect('/admin')

@app.route('/make_admin', methods=['POST'])
def make_admin():
    mysql = connectToMySQL("the_wall")
    query = "UPDATE the_wall.users SET admin_level = 9 WHERE id = %(id)s;"
    data = { "id" : request.form['id'] }
    mysql.query_db(query, data)
    return redirect('/admin')


@app.route('/log_out', methods=['POST'])
def log_out():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)