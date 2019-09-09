__author__ = 'Maren Luper'

#imports
import sqlite3
from flask import Flask, render_template
from flask import request, redirect, url_for

#instantiate
app = Flask(__name__)
# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

            conn = sqlite3.connect('celebrities.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM credentials WHERE credID=1''')
            row = c.fetchone()
            
            if row:
                if request.form['username'] != row[1] or request.form['password'] != row[2]:
                    error = 'Invalid Credentials. Please try again.'
                else:
                    return redirect(url_for('info'))
            
    return render_template('login.htm', error=error)

@app.route('/info', methods=['GET', 'POST'])
def info():
    memberID = None
    firstname = ''
    lastname = ''
    age = None
    email = ''
    bio = ''
    success = False

    if request.method == 'GET':
        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members WHERE memberID=1''')
        row = c.fetchone()

        if row:
            memberID = row[0]
            firstname = row[1]
            lastname = row[2]
            age = row[3]
            email = row[4]
            bio = row[5]
            
        conn.close()

    if request.method == 'POST':
        memberID=request.form['memberID']
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        age=request.form['age']
        email=request.form['email']
        bio=request.form['bio']
        success = True

        conn = sqlite3.connect('celebrities.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM members''')
        row = c.fetchone()
        if row:
            c.execute('''UPDATE members SET firstname = ?, lastname = ?, age = ?, email = ?, bio = ? WHERE
memberID=?''',
                      (firstname, lastname, age, email, bio, memberID))
        else:
            c.execute('''INSERT INTO members VALUES (?, ?, ?, ?, ?, ?)''',
                      (memberID, firstname, lastname, age, email, bio))
        conn.commit()
        conn.close()
    return render_template('profile.htm', memberID=memberID, firstname=firstname, lastname=lastname, age=age,
                           email=email, bio=bio, success=success)

@app.route('/view_all_celebs')
def view_all():
    celebID=None
    firstname = ''
    lastname = ''
    age = ''
    email = ''
    photo = ''
    bio = ''

    conn = sqlite3.connect('celebrities.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM celebs ORDER BY celebID''')
    rows = c.fetchall()
    conn.close()

    return render_template('view_all_celebs.htm',
rows=rows)


@app.route('/view_one_celeb')
def view():
    celebID=None
    firstname = ''
    lastname = ''
    age = ''
    email = ''
    photo = ''
    bio = ''

    conn = sqlite3.connect('celebrities.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM celebs WHERE celebID=3''')
    row = c.fetchone()

    if row:
            celebID = row[0]
            firstname = row[1]
            lastname = row[2]
            age = row[3]
            email = row[4]
            photo = row[5]
            bio = row[6]
            
    conn.close()

    return render_template('view_one_celeb.htm', celebID=celebID, firstname=firstname, lastname=lastname, age=age,
                           email=email, photo=photo, bio=bio)

def get(request):
    pass

def post(request):
    pass

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    app.run(debug=False)
