from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        #This query is to search the database for the entred name and password by the user
        query = "SELECT name,password FROM users where name= '"+name+"' and password='"+password+"'"
        cursor.execute(query)

        results = cursor.fetchall()
        print(results)

        #This states that if the user and/or password is not found in user_data.db, then print this text.
        if len(results) == 0:
            print("no such user exists, please try again")
        #This states that if the username and/or password is found in the user_data.db, take the user to the logged in page.
        else:
            print("user found, successfully logged in")
            return render_template("logged_in.html")           
    
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)