from flask import Flask, render_template, request, redirect, g, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5# y2L"F4Q8z\n\xec]/'

DATABASE = 'user_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('user_data.db')
    return db

@app.route('/')
def homepage():
    return render_template("home.html")

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


@app.route("/loggedin")
def loginhompeage():
    if session['loggedin'] == 'true':
        return render_template(login)

@app.route("/accountcreation")
def accountcreated():
    return render_template('account_created.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        cursor = get_db().cursor()
        new_name = request.form["name"]
        new_password = request.form["password"]
        sql1 = "INSERT INTO users(name,password) VALUES (?,?)"
        cursor.execute(sql1,(new_name, new_password))
        get_db().commit()

    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)