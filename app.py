import pymysql
from flask import Flask, render_template, request, redirect, flash, session
from passlib.hash import sha256_crypt
import gc


app = Flask(__name__)
app.debug = True
app.secret_key = 'some secret key'

connection = pymysql.connect(
    host='localhost',
    user='testuser',
    password='test',
    db='TESTDB',
    port=3307
)


@app.route("/")
def home():
    return render_template("/home.html")


@app.route("/aboutus.html")
def aboutus():
    return render_template("/aboutus.html")


@app.route("/home.html")
def intro():
    return render_template("/home.html")


@app.route("/login.html")
def login():
    return render_template("/login.html")


@app.route("/contactus.html")
def contactus():
    return render_template("/contactus.html")


@app.route('/check_user', methods=['POST'])  # login function
def check_user():
    if request.method == 'POST':
        email = request.form['email']
        user_password = request.form['pass']
        cursor = connection.cursor()
        com = "select * from login where u_email='"+email+"'"
        cursor.execute(com)
        data = cursor.fetchone()[2]
        cursor.close()
        if sha256_crypt.verify(user_password, data):
                session['logged_in'] = True
                session['username'] = email
                return render_template("/studenthome.html")
        else:
                flash("Invalid Login")
        gc.collect()
        return redirect("/login.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("/login.html")


@app.route("/studenthome.html")
def stud_home():
    return render_template("/studenthome.html")


@app.route("/signup.html")
def index():
    return render_template("/signup.html")


@app.route("/question.html")
def quiz():
    return render_template("/question.html")


@app.route('/post_user', methods=['POST'])  # sign up function
def post_user():
    if request.method == 'POST':
        cursor = connection.cursor()
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['pass'])
        x = cursor.execute("select * from login where u_email='"+email+"'")
        if int(x) > 0:
                flash("That username is already taken, please choose another")
                return redirect("/signup.html")
        else:
            sql = """ALTER TABLE login AUTO_INCREMENT = 100"""
            cursor.execute(sql)
            com = """insert into login (u_email,password) values (%s, %s)"""
            cursor.execute(com, (email, password))
            connection.commit()
            flash("Thanks for registering!")
            session['logged_in'] = True
            session['username'] = email
            cursor.close()
            return redirect("/profile.html")


@app.route("/profile.html")
def profile():
    return render_template('/profile.html')


@app.route('/post_profile', methods=['POST'])  # profile completion function
def post_profile():
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute()
        email = request.form['email']
        password = request.form['pass']
        com = """insert into login (uemail,password) values (%s, %s)"""
        cursor.execute(com, (email, password))
        connection.commit()
        return redirect("/profile.html")
    connection.close()


if __name__ == "__main__":
    app.run()
