#imports
from flask import Flask, render_template, request, redirect, g, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5# y2L"F4Q8z\n\xec]/'

#Database accessing shazam
DATABASE = 'user_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('user_data.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#basic homepage route
@app.route('/')
def homepage():
    return render_template("home.html")

#login route that takes user input and checks if the input is the same as an account found in the user database, if not then it declines.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        # This query is to search the database for the entred name and password by the user
        query = "SELECT name,password FROM users where name= '" + \
            name+"' and password='"+password+"'"
        cursor.execute(query)

        results = cursor.fetchall()
        print(results)

        # This states that if the user and/or password is not found in user_data.db, then print this text.
        if len(results) == 0:
            print("no such user exists, please try again")
        # This states that if the username and/or password is found in the user_data.db, take the user to the logged in page.
        else:
            print("user found, successfully logged in")
            session['loggedin'] = 'true'
            return render_template("logged_in.html")

    return render_template('index.html')

#logged in route, where if the user succesfully logs in they are redirected here.
@app.route("/loggedin")
def loginhompeage():
    if session['loggedin'] == 'true':
        return render_template(login)

#issues resulting me to remove this feature
'''@app.route("/accountcreation")
def accountcreated():
    return render_template('account_created.html')'''

#sign up page asks for input and adds the input into the user database where the user can then log in with afterwards.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    #try and except statements for when the null or unique constraints activate so it doesnt just error the site and rather returns them to the page.
    try:
        if request.method == "POST":
            cursor = get_db().cursor()
            new_name = request.form["name"]
            new_password = request.form["password"]
            sql1 = "INSERT INTO users(name,password) VALUES (?,?)"
            cursor.execute(sql1,(new_name, new_password))
            get_db().commit()
    except:
        return render_template('signup.html')

    return render_template('signup.html')

#The actual display of the homework data and all the connected users assigned to which homework and subjects.
@app.route("/database")
def databasepage():
    cursor = get_db().cursor()
    sql = "SELECT * FROM subject_data"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template('database.html', results=results)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["item_name"]
        new_subject = request.form["item_subject"]
        new_homework = request.form["item_homework"]
        new_due = request.form["item_due"]
        sql = "INSERT INTO subject_data(user,subject,homework,due) VALUES(?,?,?,?)"
        cursor.execute(sql,(new_name,new_subject,new_homework,new_due))
        get_db().commit()
    return redirect('/database')

@app.route('/delete', methods=["GET","POST"])
def delete():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["item_name"])
        sql = "DELETE FROM subject_data WHERE id=?"
        cursor.execute(sql,(id,))
        get_db().commit()
    return redirect('/database')


if __name__ == "__main__":
    app.run(debug=True)