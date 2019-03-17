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
        com = "select * from login where u_email='" + email + "'"
        cursor.execute(com)
        data = cursor.fetchone()[2]
        cursor.close()
        if sha256_crypt.verify(user_password, data):
            session['logged_in'] = True
            session['username'] = email
            session['id'] = data
            return render_template("/studenthome.html")
        else:
            flash("Invalid Login")
        gc.collect()
        return redirect("/login.html")


@app.route('/editprofile.html')
def editprofile():
    session.pop('user', None)
    return render_template("/editprofile.html")


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


@app.route("/settings.html")
def settings():
    return render_template("/settings.html")


@app.route('/post_user', methods=['POST'])  # sign up function
def post_user():
    if request.method == 'POST':
        cursor = connection.cursor()
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['pass'])
        confirm= sha256_crypt.encrypt(request.form['passw'])
        x = cursor.execute("select * from login where u_email='" + email + "'")
        if int(x) > 0:
            flash("That username is already taken, please choose another")
            return redirect("/signup.html")
        else:
            if request.form['pass'] == request.form['passw']:
                sql = """ALTER TABLE login AUTO_INCREMENT = 100"""
                cursor.execute(sql)
                com = """insert into login (u_email,password) values (%s, %s)"""
                cursor.execute(com, (email, password))
                query = "select * from login where u_email='" + email + "'"
                cursor.execute(query)
                data = cursor.fetchone()[0]
                connection.commit()
                flash("Thanks for registering!")
                session['logged_in'] = True
                session['username'] = email
                session['id'] = data
                cursor.close()
                return redirect("/profile.html")
            else:
                flash("Password not same")
                return redirect("/signup.html")


@app.route("/profile.html")
def profile():
    return render_template('/profile.html')


@app.route('/post_profile', methods=['POST'])  # profile completion function
def post_profile():
    if request.method == 'POST':
        cursor = connection.cursor()
        id = session['id']
        firstnme = request.form['frst_name']
        lst_nme = request.form['lst_name']
        dob = request.form['dob']
        gender = request.form['optradio']
        cntno = request.form['phn_no']
        email = session['username']
        institute = request.form['inst']
        clas = request.form['clasnme']
        house = request.form['house_name']
        city = request.form['city']
        country = request.form['country']
        pin = request.form['pin_code']
        # img= request.file['file']
        com = "insert into user_profile values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(com,
                       (id, firstnme, lst_nme, dob, gender, cntno, email, institute, clas, house, city, country, pin))
        connection.commit()
        return redirect("/studenthome.html")
    connection.close()


@app.route('/change_password', methods=['POST'])  # change password
def change_password():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = session['username']
        newpassword = sha256_crypt.encrypt(request.form['password1'])
        com = "update login set password ='"+newpassword+"' where u_email = '"+uid+"' "
        cursor.execute(com)
        connection.commit()
        flash("Password updated")
        return redirect("/settings.html")


@app.route('/delete_user', methods=['POST'])        # Delete Account
def delete_user():
    if request.method == 'POST':
        uid = session['username']
        cursor = connection.cursor()
        command = "delete from user_profile where stud_email = '" + uid + "'"
        cursor.execute(command)
        query = "delete from login where u_email= '" + uid + "'"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        session.pop('user', None)
        return redirect("/home.html")

    else:
        flash("Wrong password")
        return redirect("/settings.html")


if __name__ == "__main__":
    app.run()


