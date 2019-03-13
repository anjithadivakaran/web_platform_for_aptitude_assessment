import pymysql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.debug = True

connection = pymysql.connect(
    host='localhost',
    user='testuser',
    password='test',
    db='TESTDB',
    port=3307
)


@app.route("/")
def login():
    return render_template("/login.html")


@app.route('/check_user', methods=['POST'])  # login function
def check_user():
    cursor = connection.cursor()
    email = request.form['email']
    password = request.form['pass']
    com = "select * from user where uemail='"+email+"' and password= '"+password+"'"
    cursor.execute(com)
    connection.commit()
    return redirect('/profile.html')
    connection.close()


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
        sql = """ALTER TABLE user AUTO_INCREMENT = 100"""
        cursor.execute(sql)
        email = request.form['email']
        password = request.form['pass']
        com = """insert into user (uemail,password) values (%s, %s)"""
        cursor.execute(com, (email, password))
        connection.commit()
        return redirect("/profile.html")
    connection.close()


@app.route("/login.html")
def logout():
    return render_template("/login.html")


@app.route("/profile.html")
def profile():
    return render_template('/profile.html')


if __name__ == "__main__":
    app.run()
