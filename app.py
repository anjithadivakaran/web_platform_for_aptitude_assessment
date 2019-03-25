import pymysql
import random
import string
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
    db='Quiz_Database',
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
        user_password = request.form['password']
        cursor = connection.cursor()
        com = "select * from login where u_email='" + email + "'"
        cursor.execute(com)
        data = cursor.fetchone()[2]
        com = "select * from login where u_email='" + email + "'"
        cursor.execute(com)
        utype = cursor.fetchone()[3]
        cursor.close()
        if utype == "student":
            if sha256_crypt.verify(user_password, data):
                session['logged_in'] = True
                session['username'] = email
                session['id'] = data
                return render_template("/studenthome.html")
        elif utype == "admin":
            if sha256_crypt.verify(user_password, data):
                session['logged_in'] = True
                session['username'] = email
                session['id'] = data
                return render_template("/adminhome.html")
        elif utype == "instructor":
            if sha256_crypt.verify(user_password, data):
                session['logged_in'] = True
                session['username'] = email
                session['id'] = data
                return render_template("/instructorhome.html")
            else:
                flash("problem with password")
        else:
            flash("Invalid Login")
        gc.collect()
        return redirect("/login.html")
    else:
        flash("Invalid login")
        return redirect("/login.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("/login.html")


@app.route('/logoutprofile')  # if not registered
def logoutprofile():
    id = session['username']
    cursor = connection.cursor()
    cmd = "delete from login where u_email = '" + id + "' "
    cursor.execute(cmd)
    connection.commit()
    session.pop('user', None)
    flash("Sorry registration unsuccessful")
    return render_template("/signup.html")


@app.route("/studenthome.html")
def stud_home():
    return render_template("/studenthome.html")


@app.route("/signup.html")
def index():
    return render_template("/signup.html")


@app.route("/instructorhome.html")
def instructorhome():
    return render_template("/instructorhome.html")


@app.route("/question")
def question():
    cursor = connection.cursor()
    command = "select * from question_details"
    result = cursor.execute(command)
    if result > 0:
        question = cursor.fetchall()
        return render_template("/question.html", question=question)
    else:
        flash("Error")
        return redirect("/studenthome.html")


@app.route("/settings.html")
def settings():
    return render_template("/settings.html")


@app.route("/post_question", methods=['POST'])
def post_question():
    cursor = connection.cursor()
    quesid = request.form['id']
    cursor.execute("select user_id from login where u_email= '"+session['username']+"'")
    data = cursor.fetchone()[0]
    stud_id = data
    answer = request.form['optradio']
    qry = "insert into answer_details values (%s,%s,%s) "
    cursor.execute(qry, (quesid, stud_id, answer))
    connection.commit()
    return redirect("/question")


@app.route('/post_user', methods=['POST'])  # sign up function
def post_user():
    if request.method == 'POST':
        cursor = connection.cursor()
        email = request.form['email']
        password = sha256_crypt.encrypt(request.form['password'])
        utype = "student"
        x = cursor.execute("select * from login where u_email='" + email + "'")
        if int(x) > 0:
            flash("That username is already taken, please choose another")
            return redirect("/signup.html")
        else:
            if request.form['password'] == request.form['con_password']:
                sql = """ALTER TABLE login AUTO_INCREMENT = 100"""
                cursor.execute(sql)
                com = """insert into login (u_email,password,user_type) values (%s, %s, %s)"""
                cursor.execute(com, (email, password, utype))
                query = "select * from login where u_email='" + email + "'"
                cursor.execute(query)
                data = cursor.fetchone()[0]
                connection.commit()
                session['logged_in'] = True
                session['username'] = email
                session['id'] = data
                cursor.close()
                return render_template("/profile.html")
            else:
                flash("Password not same")
                return redirect("/signup.html")


@app.route("/profile.html")
def profile():
    return render_template('/profile.html')


@app.route("/adminhome.html")
def adminhome():
    return render_template('/adminhome.html')


@app.route("/adminaddinstructor")
def addinstructor():
    return render_template('/adminaddinstructor.html')


@app.route("/adminaddinst_profile", methods=['POST'])  # admin add instructor profile and login details
def addinst_profile():
    if request.method == 'POST':
        firstnme = request.form['frst_name']
        lst_nme = request.form['lst_name']
        dob = request.form['dob']
        gender = request.form['optradio']
        cntno = request.form['phn_no']
        email = request.form['e_mail']
        qualification = request.form['quali']
        house = request.form['house_name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pin = request.form['pin_code']
        pasw = "instructor"
        p = sha256_crypt.encrypt(pasw)
        utype = "instructor"
        cursor = connection.cursor()
        sql = """ALTER TABLE login AUTO_INCREMENT = 100"""
        cursor.execute(sql)
        cmd = "insert into login (u_email,password,user_type) values (%s, %s, %s)"
        cursor.execute(cmd, (email, p, utype))
        qry = "select user_id from login where u_email = '" + email + "'"
        cursor.execute(qry)
        data = cursor.fetchone()[0]
        insqry = "insert into instructor_details values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        cursor.execute(insqry, (
        data, firstnme, lst_nme, dob, gender, cntno, email, qualification, house, city, state, country, pin))
        connection.commit()
        flash("Instructor Creation successful.... Password is" + pasw)
        return render_template("/adminhome.html")


@app.route('/post_profile', methods=['POST'])  # profile completion function
def post_profile():
    id = session['id']
    if request.method == 'POST':
        cursor = connection.cursor()
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
        com = "insert into student_profile values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(com,
                       (id, firstnme, lst_nme, dob, gender, cntno, email, institute, clas, house, city, country, pin))
        connection.commit()
        flash("Thanks for registering!")
        return redirect("/studenthome.html")
    connection.close()


@app.route('/change_password', methods=['POST'])  # change password
def change_password():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = session['username']
        newpassword = sha256_crypt.encrypt(request.form['password1'])
        if request.form['password1'] == request.form['password2']:
            com = "update login set password ='" + newpassword + "' where u_email = '" + uid + "' "
            cursor.execute(com)
            connection.commit()
            flash("Password updated")
            return redirect("/settings.html")
        else:
            flash("Password Does not Match")
            return redirect("/settings.html")


@app.route('/instchange_password', methods=['POST'])  # instructor change password
def instchange_password():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = session['username']
        newpassword = sha256_crypt.encrypt(request.form['password1'])
        if request.form['password1'] == request.form['password2']:
            com = "update login set password ='" + newpassword + "' where u_email = '" + uid + "' "
            cursor.execute(com)
            connection.commit()
            flash("Password updated")
            return redirect("/instsettings.html")
        else:
            flash("Password Does not Match")
            return redirect("/instsettings.html")


@app.route('/adminchange_password', methods=['POST'])  # admin change password
def adminchange_password():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = session['username']
        newpassword = sha256_crypt.encrypt(request.form['password1'])
        if request.form['password1'] == request.form['password2']:
            com = "update login set password ='" + newpassword + "' where u_email = '" + uid + "' "
            cursor.execute(com)
            connection.commit()
            flash("Password updated")
            return redirect("/adminsettings.html")
        else:
            flash("Password Does not Match")
            return redirect("/adminsettings.html")


@app.route('/delete_user', methods=['POST'])  # Delete Account
def delete_user():
    if request.method == 'POST':
        uid = session['username']
        cursor = connection.cursor()
        command = "delete from student_profile where stud_email = '" + uid + "'"
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


@app.route('/instdelete_user', methods=['POST'])  # instructor Delete Account
def instdelete_user():
    if request.method == 'POST':
        uid = session['username']
        cursor = connection.cursor()
        command = "delete from instructor_details where inst_email = '" + uid + "'"
        cursor.execute(command)
        query = "delete from login where u_email= '" + uid + "'"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        session.pop('user', None)
        flash("user deleted successfully...")
        return redirect("/home.html")

    else:
        flash("Wrong password")
        return redirect("/settings.html")


@app.route("/studeditprofile/<id>")  # student profile edit
def studeditprofile(id):
    cursor = connection.cursor()
    command = "select * from student_profile where stud_id= '" + id + "'"
    cursor.execute(command)
    res = cursor.fetchone()
    return render_template("/studeditprofile.html", data=res)


@app.route("/viewprofile")  # student profile view
def view_user():
    uid = session['username']
    cursor = connection.cursor()
    command = "select * from student_profile where stud_email= '" + uid + "'"
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/viewprofile.html", data=res)


@app.route("/instructorprofileview")  # instructor profile view
def instructorprofileview():
    uid = session['username']
    cursor = connection.cursor()
    command = "select * from instructor_details"
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/instructorprofileview.html", data=res)


@app.route("/editinstructorprofile/<id>")  # instructor profile edit
def editinstructorprofile(id):
    cursor = connection.cursor()
    command = "select * from instructor_details where inst_id= '" + id + "'"
    cursor.execute(command)
    res = cursor.fetchone()
    return render_template("/editinstructorprofile.html", data=res)


@app.route("/update_instr", methods=['POST', 'GET'])  # instructor profile update
def update_instr():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = request.form['id']
        frst_name = request.form['frst_name']
        lst_name = request.form['lst_name']
        phone_no = request.form['phn_no']
        qualification = request.form['quali']
        house = request.form['house_name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pincode = request.form['pin_code']
        qry = "update instructor_details set inst_first_name='" + frst_name + "',inst_last_name='" + lst_name + "',inst_contact_no='" + phone_no + "', inst_qualification='" + qualification + "', inst_state='" + state + "',inst_house='" + house + "',inst_city='" + city + "',inst_country='" + country + "', inst_pin='" + pincode + "' where inst_id='" + uid + "'"
        cursor.execute(qry)
        connection.commit()
        flash("update successful")
        return render_template("/instructorhome.html")
    else:
        return render_template("/instructorhome.html")


@app.route("/instmanagestudent")  # instructor student profile view
def instmanagestudent():
    uid = session['username']
    cursor = connection.cursor()
    command = "select * from student_profile"
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/instmanagestudent.html", data=res)


@app.route("/insteditstudent/<id>")  # instructor editview student profile
def insteditstudent(id):
    cursor = connection.cursor()
    command = "select * from student_profile where stud_id= '" + id + "'"
    cursor.execute(command)
    res = cursor.fetchone()
    return render_template("/insteditstudent.html", data=res)


@app.route("/update_stud", methods=['POST', 'GET'])  # instructor student profile update
def update_stud():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = request.form['id']
        frst_name = request.form['frst_name']
        lst_name = request.form['lst_name']
        phone_no = request.form['phn_no']
        institute = request.form['insti']
        clasnme = request.form['cls']
        house = request.form['house_name']
        city = request.form['city']
        country = request.form['country']
        pincode = request.form['pin_code']
        qry = "update student_profile set stud_first_name='" + frst_name + "',stud_last_name='" + lst_name + "',cnt_number='" + phone_no + "', stud_inst='" + institute + "', stud_class='" + clasnme + "',stud_house='" + house + "',stud_city='" + city + "',stud_country='" + country + "', pin_code='" + pincode + "' where stud_id='" + uid + "'"
        cursor.execute(qry)
        connection.commit()
        flash("update successful")
        return render_template("/instructorhome.html")
    else:
        return render_template("/instructorhome.html")


@app.route("/adminstudentmanage")  # admin view student
def adminstudentmanage():
    cursor = connection.cursor()
    command = "select * from student_profile "
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/adminstudentmanage.html", data=res)


@app.route("/admineditstudent/<id>")  # admin edit view student profile
def admineditstudent(id):
    cursor = connection.cursor()
    command = "select * from student_profile where stud_id= '" + id + "'"
    cursor.execute(command)
    res = cursor.fetchone()
    return render_template("/admineditstudent.html", data=res)


@app.route("/update_studadmin", methods=['POST', 'GET'])  # admin student profile update
def update_studadmin():
    if request.method == 'POST':
        cursor = connection.cursor()
        uid = request.form['id']
        frst_name = request.form['frst_name']
        lst_name = request.form['lst_name']
        phone_no = request.form['phn_no']
        institute = request.form['insti']
        clasnme = request.form['cls']
        house = request.form['house_name']
        city = request.form['city']
        country = request.form['country']
        pincode = request.form['pin_code']
        qry = "update student_profile set stud_first_name='" + frst_name + "',stud_last_name='" + lst_name + "',cnt_number='" + phone_no + "', stud_inst='" + institute + "', stud_class='" + clasnme + "',stud_house='" + house + "',stud_city='" + city + "',stud_country='" + country + "', pin_code='" + pincode + "' where stud_id='" + uid + "'"
        cursor.execute(qry)
        connection.commit()
        flash("update successful")
        return render_template("/adminhome.html")
    else:
        return render_template("/adminhome.html")


@app.route("/questionview")  # instructor view question
def questionview():
    cursor = connection.cursor()
    command = "select * from question_details"
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/questionview.html", data=res)


@app.route("/add_question", methods=['POST'])
def add_question():
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    cursor = connection.cursor()
    commad = "ALTER TABLE question_details AUTO_INCREMENT = 100"
    cursor.execute(commad)
    command = "insert into question_details (question,value1,value2,value3,value4, answer ) values (%s,%s,%s,%s,%s,%s)"
    cursor.execute(command, (question, option1, option2, option3, option4,answer))
    connection.commit()
    flash("Question insertion successful")
    return render_template("/instructorhome.html")


@app.route("/addquestion.html")
def addquestion():
    return render_template("/addquestion.html")


@app.route("/instsettings.html")
def instsettings():
    return render_template("/instsettings.html")


@app.route("/adminsettings.html")
def adminsettings():
    return render_template("/adminsettings.html")


@app.route("/adminviewinstructor")  # admin instructor profile view
def view_instructor():
    cursor = connection.cursor()
    command = "select * from instructor_details "
    cursor.execute(command)
    res = cursor.fetchall()
    return render_template("/adminviewinstructor.html", data=res)


@app.route("/admineditinstructordetails/<id>")  # admin instructor profile edit
def admineditinstructordetails(id):
    cursor = connection.cursor()
    command = "select * from instructor_details where inst_id= '" + id + "'"
    cursor.execute(command)
    res = cursor.fetchone()
    return render_template("/admineditinstructordetails.html", data=res)


@app.route("/updateinst_profile", methods=['post'])  # admin update instructor profile
def updateinst_profile():
    if request.method == 'POST':
        uid = request.form['id']
        firstnme = request.form['frst_name']
        lst_nme = request.form['lst_name']
        dob = request.form['dob']
        gender = request.form['gender']
        cntno = request.form['phn_no']
        email = request.form['e_mail']
        qualification = request.form['quali']
        house = request.form['house_name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        pin = request.form['pin_code']
        cursor = connection.cursor()
        qry = "update instructor_details set inst_first_name = '" + firstnme + "', inst_last_name ='" + lst_nme + "', inst_dob ='" + dob + "', inst_gender='" + gender + "', inst_contact_no= '" + cntno + "', inst_email='" + email + "', inst_qualification= '" + qualification + "', inst_house = '" + house + "', inst_city = '" + city + "', inst_state='" + state + "', inst_country='" + country + "', inst_pin= '" + pin + "' where inst_id = '" + uid + "'"
        cursor.execute(qry)
        connection.commit()
        flash("update successful")
        return render_template("/adminhome.html")
    else:
        return render_template("/adminhome.html")


@app.route("/update_profile", methods=['post'])  # student profile update
def update_user():
    if request.method == 'POST':
        uid = session['username']
        frst_name = request.form['frst_name']
        lst_name = request.form['lst_name']
        phone_no = request.form['phn_no']
        institute = request.form['inst']
        clasnme = request.form['clasnme']
        house = request.form['house_name']
        city = request.form['city']
        country = request.form['country']
        pincode = request.form['pin_code']
        qry = "update student_profile set stud_first_name='" + frst_name + "',stud_last_name='" + lst_name + "',cnt_number='" + phone_no + "', stud_inst='" + institute + "', stud_class='" + clasnme + "',stud_house='" + house + "',stud_city='" + city + "',stud_country='" + country + "', pin_code='" + pincode + "' where stud_email='" + uid + "'"
        cursor = connection.cursor()
        cursor.execute(qry)
        connection.commit()
        flash("update successful")
        return render_template("/studenthome.html")
    else:
        return render_template("/studenthome.html")


if __name__ == "__main__":
    app.run()
