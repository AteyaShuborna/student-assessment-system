from flask import Flask, render_template, url_for, request, redirect, session, json
from flask_mysqldb import MySQL,MySQLdb
# User defined module imports
import admin, teacher, student
from sql import insert_into_marks, insert_into_teacher,  insert_into_assesment
from sql import fetch_all_marks, insert_into_enroll, fetch_all_assesment, delete_enroll
from sql import sql, fetch_sql, del_student_db, del_teacher_db, del_assessment_db
from sql import insert_into_student

# Creating and Configuring Flask app Variable
app = Flask(__name__)
app.secret_key = "team-2"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cse370_project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


# ! HOMEPAGE
@app.route('/')
@app.route('/home')
@app.route('/homepage')
def homepage():
    return render_template('home.html', title_bar = "Homepage")

# SIGN UP FOR STUDENT
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', title_bar="Signup")


@app.route('/student_sign_up', methods=['GET', 'POST'])
def student_sign_up():
    student_id = request.form["student_id"]
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    admin = 'Null'
    status='Null'
    chq = f'select * from student where student_id = "{student_id}";'
    chq = fetch_sql(chq)
    if len(chq) > 0:
        return render_template('show_message.html', message='Student Already Exists')

    else:

        qry = f"INSERT into student values('{student_id}','{name}','{email}','{password}','{admin}','{status}');"
        sql(qry)

        return render_template('show_message.html', message='SUCCESSFULLY JOINED')


# ! ADMIN LOGIN REQUEST
@app.route('/admin_login')
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard', admin_id =  session['admin_id']))
    return render_template('admin_login.html', title_bar = "Admin Login")


# ! ADMIN AUTHINTICATOR
@app.route('/admin_authinticate', methods = ['GET', 'POST'])
def admin_authinticate():
    if request.method == "POST":
        adminID = request.form["adminid"]
        password = request.form["password"]
        return admin.authenticate_admin(adminID, password)
    if request.method == "GET":
        if 'adminID' in request.args:
            adminID = request.args["adminid"]
            password = request.args["password"]
            return render_template('show_message.html', message = adminID+' '+password)




# ! ADMIN DASHBOARD AFTER AUTHINTICATION
@app.route('/admin_dashboard/<admin_id>')
def admin_dashboard(admin_id):
    if 'admin_id' in session:
        user = session['admin_id']
        password = session['admin_password']
        return render_template('admin_dashboard.html',
                               title_bar = 'Admin Dashboard: '+user,
                               admin_id = user,
                               admin_name = session['admin_name']
                               )
    else:
        return render_template('show_message.html', message = 'The session ended')


### admin approve scholarship

@app.route('/admin_approve_scholarship')
def admin_approve_scholarship():
    return render_template('admin_approve_scholarship.html')


@app.route('/commit_scholarship_update', methods=['POST'])
def commit_scholarship_update():
    if 'admin_id' in session:
        student_id = request.form['student_id']
        status = request.form['status']

        chq1 = f"select * from scholarship where student_id ='{student_id}';"
        chq2 = fetch_sql(chq1)
        if len(chq2) > 0:

            qry = f"UPDATE scholarship SET status = '{status}' where student_id='{student_id}';"
            sql(qry)

            qry1 = f"UPDATE student SET status = '{status}' where student_id='{student_id}';"
            sql(qry1)

            return render_template('show_message.html', message='SCHOLARSHIP  ' + str(status))
        else:
            return render_template('show_message.html', message='STUDENT NOT FOUND')

    else:
        return render_template('show_message.html', message='SORRY TRY AGAIN')



# ! ADMIN LOGOUT AND CLEAR SESSION
@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_password', None)
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    return redirect(url_for('admin_login'))


# ! ADMIN EDITS OWN PROFILE
@app.route('/admin_profile_edit_request')
def admin_profile_edit_request():
    return render_template('admin_edit_profile.html')

@app.route('/commit_admin_update', methods = ['POST'])
def commit_admin_update():
    if 'admin_id' in session:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name != '':
            qry = f"UPDATE admin SET name = '{name}' WHERE id = '{session['admin_id']}';"
            sql(qry)
            session['admin_name'] = name
        if email != '':
            qry = f"UPDATE admin SET email = '{email}' WHERE id = '{session['admin_id']}';"
            sql(qry)
            session['admin_email'] = email
        if password != '':
            qry = f"UPDATE admin SET password = '{password}' WHERE id = '{session['admin_id']}';"
            sql(qry)
            session['admin_password'] = password
        return redirect(url_for('admin_dashboard', admin_id = session['admin_id']))
    else:
        return render_template('show_message.html', message = 'The session ended Please login again')



# ! ADMIN EDITS STUDENTS
@app.route('/admin_dashboard/edit_student')
def edit_student():
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        return render_template('admin_edit_student.html',
                               students=students,
                               title_bar = 'Student editorial',
                               admin_id = session['admin_id']
                               )

@app.route('/updatesutdent', methods=['POST'])
def updatesutdent():
        pk = request.form['pk']
        name = request.form['name']
        value = request.form['value']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if name == 'name':
           cur.execute("UPDATE student SET name = %s WHERE student_id = %s ", (value, pk))
        elif name == 'email':
           cur.execute("UPDATE student SET email = %s WHERE student_id = %s ", (value, pk))
        elif name == 'password':
           cur.execute("UPDATE student SET password = %s WHERE student_id = %s ", (value, pk))
        elif name == 'administer':
           cur.execute("UPDATE student SET administer = %s WHERE student_id = %s ", (value, pk))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})


# ADMIN ADD STUDENT
@app.route('/admin_dashboard/add_student')
def add_student():
    return render_template('admin_add_student.html')


@app.route('/createstudent', methods=['POST'])
def createstudent():
    if 'admin_id' in session:
        id = request.form['student_id']
        name = request.form['student_name']
        email = request.form['student_email']
        password = request.form['student_password']
        administer = session['admin_id']
        status='Null'
        chq = f'select * from student where student_id = "{id}";'
        chq = fetch_sql(chq)
        if len(chq) > 0:
            return render_template('show_message.html', message='Student Already Exists')
        else:
            insert_into_student(id, name, email, password, administer,status)
            return render_template('show_message.html', message='Student created')
    else:
        return render_template('show_message.html', message='The session ended')



# ! ADMIN DELETES STUDENT
@app.route('/delete_student', methods = ['POST','GET'])
def delete_student():
    student_id = request.form['student_id']
    if 'admin_id' in session:
        del_student_db(student_id)
        return redirect(url_for('edit_student'))
    else:
        return render_template('show_message.html', message = 'The session ended Please login again')


# ! ADMIN DELETES TEACHER
@app.route('/delete_teacher', methods = ['POST','GET'])
def delete_teacher():
    teacher_id = request.form['teacher_id']
    if 'admin_id' in session:
        del_teacher_db(teacher_id)
        return redirect(url_for('edit_teacher'))
    else:
        return render_template('show_message.html', message = 'The session ended. Please login again.')


# ! ADMIN EDITS TEACHER
@app.route('/admin_dashboard/edit_teacher')
def edit_teacher():
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cur.execute("SELECT * FROM teacher")
        teachers = cur.fetchall()

        return render_template('admin_edit_teacher.html',
                               teachers=teachers,
                               title_bar = 'Teacher editorial',
                               admin_id = session['admin_id']
                               )

@app.route('/updateteacher', methods=['POST'])
def updateteacher():
    pk = request.form['pk']
    name = request.form['name']
    value = request.form['value']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if name == 'name':
        cur.execute("UPDATE teacher SET name = %s WHERE teacher_id = %s ", (value, pk))
    elif name == 'email':
        cur.execute("UPDATE teacher SET email = %s WHERE teacher_id = %s ", (value, pk))
    elif name == 'password':
        cur.execute("UPDATE teacher SET password = %s WHERE teacher_id = %s ", (value, pk))
    elif name == 'administer':
        cur.execute("UPDATE teacher SET appointed_by = %s WHERE teacher_id = %s ", (value, pk))
    mysql.connection.commit()
    cur.close()
    return json.dumps({'status':'OK'})



# ! ADMIN APPOINTS TEACHER
@app.route('/admin_dashboard/appoint_teacher')
def appoint_teacher():
    return render_template('admin_assign_teacher.html')

@app.route('/createteacher', methods=['POST'])
def createteacher():
    if 'admin_id' in session:
        id = request.form['teacher_id']
        name = request.form['teacher_name']
        email = request.form['teacher_email']
        password = request.form['teacher_password']
        appointed_by = session['admin_id']
        chq = f'select * from teacher where teacher_id = "{id}";'
        chq = fetch_sql(chq)
        if len(chq) > 0:
            return render_template('show_message.html', message = 'Teacher Already Exists')
        else:
            insert_into_teacher(id, name, email, password, appointed_by)
            return render_template('show_message.html', message = 'Teacher created')

    else:
        return render_template('show_message.html', message = 'The session ended')






# ! STUDENT EDITS OWN PROFILE
@app.route('/student_profile_edit_request')
def student_profile_edit_request():
    return render_template('student_edit_profile.html')

@app.route('/commit_student_update', methods = ['POST'])
def commit_student_update():
    if 'student_id' in session:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name != '':
            qry = f"UPDATE student SET name = '{name}' WHERE student_id = '{session['student_id']}';"
            session['student_name']  = name
            sql(qry)
        if email != '':
            qry = f"UPDATE student SET email = '{email}' WHERE student_id = '{session['student_id']}';"
            session['student_email']  = email
            sql(qry)
        if password != '':
            qry = f"UPDATE student SET password = '{password}' WHERE student_id = '{session['student_id']}';"
            session['student_password']  = password
            sql(qry)
        return redirect(url_for('student_dashboard', student_id = session['student_id']))
    else:
        return render_template('show_message.html', message = 'The session ended. Please login again')


# ! ALL LOGIN PAGES
@app.route('/student_login')
def student_login():
    if 'student_id' in session:
        return redirect(url_for('student_dashboard', student_id = session['student_id']))
    return render_template('student_login.html', title_bar = "Student Login")


@app.route('/student_authinticate', methods = ['GET', 'POST'])
def student_authinticate():
    if request.method == "POST":
        studentID= request.form["studentid"]
        password = request.form["password"]
        return student.authenticate_student(studentID, password)

    if request.method == "GET":
        if 'studentid' in request.args:
            studentID = request.args["studentid"]
            password = request.args["password"]
            return render_template('show_message.html', message = 'Studnet getting ready')


# ! STUDENT DASHBOARD AFTER AUTHINTICATION
@app.route('/student_dashboard/<student_id>')
def student_dashboard(student_id):
    if 'student_id' in session:
        user = str(session['student_id'])
        password = str(session['student_password'])
        return render_template('student_dashboard.html',
                               title_bar = 'Student Dashboard: '+user,
                               student_id = user,
                               student_name = session['student_name']
                               )
    else:
        return render_template('show_message.html', message = 'The session ended')

#STUDENT LOG OUT AND SESSION
@app.route('/logout_student')
def logout_student():
    session.pop('student_id', None)
    session.pop('student_name', None)
    session.pop('student_email', None)
    session.pop('student_password', None)
    return redirect('/student_login')

#STUDENT ADD COURSE

@app.route('/add_course')
def add_course():
    return render_template('student_add_course.html')

@app.route('/add_course_request', methods = ["POST"])
def add_course_request():
    if 'student_id' in session:
        user = str(session['student_id'])
        course = request.form['course']
        semester = request.form['semester']

        chq = fetch_sql(f"select * from assesment where course = '{course}' and semester = '{semester}';")
        if len(chq)>0:
            insert_into_enroll(user, course, semester)
            return render_template('show_message.html', message = 'Course added')

        else:
            return render_template('show_message.html', message = 'The course Does not exist')
    else:
        return render_template('show_message.html', message = 'The session ended')

#STUDENT DROP COURSE

@app.route('/drop_course')
def drop_course():
    return render_template('student_drop_course.html')

@app.route('/drop_course_request',methods = ['POST','GET'])
def drop_course_request():
    if 'student_id' in session:
        user = str(session['student_id'])
        course = request.form.get('course')
        semester = request.form.get('semester', False)
        delete_enroll(user, course, semester)
        return render_template('show_message.html', message='Course dropped')
    else:
        return render_template('show_message.html', message='The session ended')


#SHOWS ALL ASSESSMENT OF A STUDENT

@app.route('/show_all_courses')
def show_all_courses():
    if 'student_id' in session:

        assesment = fetch_all_assesment(session['student_id'])

        if len(assesment)>0:
            user = str(session['student_id'])
            assesments = fetch_all_assesment(user)
            return render_template('student_all_assesment.html', assesments = assesments, title_bar = "All Courses", student_id = user, student_name = session['student_name'])
        else:
            return render_template('show_message.html', message = 'The course Does not exist')

    return render_template('show_message.html', message = 'The session ended')


#SHOWS ALL MARKS OF A STUDENT

@app.route('/show_all_marks')
def show_all_marks():
    if 'student_id' in session:

        marks = fetch_all_assesment(session['student_id'])

        if len(marks)>0:
            user = str(session['student_id'])
            assesments = fetch_all_marks(user)
            return render_template('student_show_marks.html', assesments = assesments, title_bar = "All Marks", student_id = user, student_name = session['student_name'])
        else:
            return render_template('show_message.html', message = 'The course Does not exist')

    return render_template('show_message.html', message = 'The session ended')

#STUDENT APPLY SCHOLARSHIP

@app.route("/scholarship_application")
def scholarship_application():
    return render_template("scholarship.html")



@app.route('/add_application', methods = ['POST'])
def add_application():
    if request.method == "POST":
        studentID= request.form["student_id"]
        credit = request.form["credit"]
        result = request.form["result"]
        description = request.form["description"]
        student.add_application(studentID, credit, result, description)

        return render_template('show_message.html', message = 'Application Submitted')


## STUDENT VIEW SCHOLARSHIP STATUS

@app.route('/view_scholarship', methods = ['POST','GET'])
def view_scholarship():
    if 'student_id' in session:
        user=str(session['student_id'])
        qry = f'select status from student where student_id = "{user}";'
        ret=fetch_sql(qry)
        for i in ret:
            for j in i:
                ret=j
        return render_template('show_message.html', message = 'Your scholarship status is " '+str(ret)+ ' "')
    else:
        return render_template('show_message.html', message = 'NOT FOUND')




# ! TEACHER DASHBOARD AFTER AUTHINTICATION

# TEACHER DASHBOARD
@app.route('/teacher_login')
def teacher_login():
    if 'teacher_id' in session:
        return render_template('teacher_login.html', title_bar = "Teacher Login")
    return render_template('teacher_login.html', title_bar = "Teacher Login")

@app.route('/teacher_authinticate', methods = ['GET', 'POST'])
def teacher_authinticate():
    if request.method == "POST":
        teacherID= request.form["teacherid"]
        password = request.form["password"]
        return teacher.authenticate_teacher(teacherID, password)

    if request.method == "GET":
        if 'teacherid' in request.args:
            teacherID = request.args["teacherid"]
            password = request.args["password"]
            return render_template('show_message.html', message = 'Teacher getting ready')


@app.route('/teacher_dashboard/<teacher_id>')
def teacher_dashboard(teacher_id):
    if 'teacher_id' in session:
        user = session['teacher_id']
        password = session['teacher_password']
        return render_template('teacher_dashboard.html',
                               title_bar = 'Teacher Dashboard: '+ user,
                               teacher_id = user,
                               teacher_name = session['teacher_name']
                               )
    else:
        return render_template('show_message.html', message = 'The session ended')


# teacher logout
@app.route('/teacherlogout')
def teacherlogout():
    session.pop('teacher_id', None)
    session.pop('teacher_password', None)
    session.pop('teacher_name', None)
    session.pop('teacher_email', None)
    return redirect(url_for('teacher_login'))


# teacher edit profile
@app.route('/teacher_profile_edit_request')
def teacher_profile_edit_request():
    return render_template('teacher_edit_profile.html')

@app.route('/commit_teacher_update', methods = ['POST'])
def commit_teacher_update():
    if 'teacher_id' in session:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name != '':
            qry = f"UPDATE teacher SET name = '{name}' WHERE teacher_id = '{session['teacher_id']}';"
            sql(qry)
        if email != '':
            qry = f"UPDATE teacher SET email = '{email}' WHERE teacher_id = '{session['teacher_id']}';"
            sql(qry)
        if password != '':
            qry = f"UPDATE teacher SET password = '{password}' WHERE teacher_id = '{session['teacher_id']}';"
            sql(qry)

        id, name, email, password, x  = fetch_sql(f"SELECT * FROM teacher WHERE teacher_id = '{session['teacher_id']}';")[0]
        session['teacher_id'] = id
        session['teacher_password'] = password
        session['teacher_name'] = name
        session['teacher_email'] = email

        return redirect(url_for('teacher_dashboard', teacher_id = session['teacher_id']))
    else:
        return render_template('show_message.html', message = 'The session ended Please login again')




# teacher creates task
@app.route('/createtask')
def createtask():
    return render_template('teacher_create_task.html')

@app.route('/assesmentcreation', methods=['POST'])
def assesmentcreation():
    if 'teacher_id' in session:
        course = request.form['course']
        semester = request.form['semester']
        type = request.form['type']
        deadline = request.form['deadline']
        description = request.form['description']
        chq = f'select * from assesment where course = "{course}" and semester = "{semester}" and type = "{type}";'
        chq = fetch_sql(chq)
        if len(chq) > 0:
            return render_template('show_message.html', message = 'Task Already Exists')
        else:
            insert_into_assesment(course, semester, type, deadline, description, session['teacher_id'])
            return render_template('show_message.html', message = 'Assesment created')

    else:
        return redirect(url_for('teacher_dashboard', teacher_id = session['teacher_id']))




#teacher Drop Assessment

@app.route('/drop_assessment')
def drop_assessment():
    return render_template('drop_assessment.html')


@app.route('/drop', methods=['POST','GET'])
def drop():
    if 'teacher_id' in session:
        course = request.form.get('course')
        semester = request.form.get('semester')
        type = request.form.get('type')
        chq = f'select * from assesment where course = "{course}" and semester = "{semester}" and type = "{type}";'
        chq = fetch_sql(chq)
        if len(chq) > 0:
            del_assessment_db(course, semester, type)
            return render_template('show_message.html', message='DROPPED')
        else:
            return render_template('show_message.html', message='COURSE DOES NOT EXIST')
    else:
        return render_template('show_message.html', message='PLEASE LOG IN')

### teacher modify assessment
@app.route('/teacher_modify_assessment')
def teacher_modify_assessment():
    return render_template('teacher_modify_assessment.html')

@app.route('/modify_assessment', methods=['POST'])
def modify_assessment():
    if 'teacher_id' in session:
        course = request.form['course']
        semester = request.form['semester']
        type = request.form['type']
        deadline = request.form['deadline']
        description = request.form['description']
        chq = f'select * from assesment where course = "{course}" and semester = "{semester}" and type = "{type}";'
        chq = fetch_sql(chq)
        if len(chq) > 0:
            if deadline!='':
                qry = f"UPDATE assesment SET deadline = '{deadline}' WHERE course = '{course}' and semester = '{semester}' and type = '{type}';"
                sql(qry)
            if description!='':
                qry1 = f"UPDATE assesment SET description = '{description}' WHERE course = '{course}' and semester = '{semester}' and type = '{type}';"
                sql(qry1)
            return render_template('show_message.html', message='MODIFYED')
            
        else:
            return render_template('show_message.html', message='ASSESSMENT DOES NOT EXIST')

    else:
        return render_template('show_message.html', message='LOGIN AGAIN')




#update marks

@app.route('/teacher_update_marks')
def teacher_update_marks():
    return render_template('teacher_update_marks.html')


@app.route('/commit_marks_update', methods=['POST'])
def commit_marks_update():
    if 'teacher_id' in session:
        student_id = request.form['student_id']
        course = request.form['course']
        semester = request.form['semester']
        type = request.form['type']
        achieved_marks = request.form['achieved_marks']

        chq2 = f"select * from marks where student_id ='{student_id}' AND course='{course}' AND semester='{semester}' AND type='{type}';"
        chq2 = fetch_sql(chq2)
        if len(chq2) > 0:

            qry = f"UPDATE marks SET achieved_marks = '{achieved_marks}',updated_by = '{session['teacher_id']}' WHERE student_id = '{student_id}' AND course='{course}' AND semester='{semester}' AND type='{type}';"
            sql(qry)

            return render_template('show_message.html', message='MARKS UPDATES')
        else:
            return render_template('show_message.html', message='FAILED TO UPDATE')

    else:
        return render_template('show_message.html', message='FAILED TO UPDATE')


# TEACHER ASSIGN MARKS


@app.route('/update_marks')
def update_marks():
    return render_template('marks_update.html')


@app.route('/assignmarks', methods=['POST'])
def assignmarks():
    student_id = request.form['student_id']
    course = request.form['course']
    semester = request.form['semester']
    type = request.form['type']
    total_marks = request.form['total_marks']
    achieved_marks = request.form['achieved_marks']
    updated_by = request.form['updated_by']

    chq = f'select * from student where student_id = "{student_id}";'
    chq = fetch_sql(chq)

    chq1 = f'select * from assesment where course = "{course}" and semester ="{semester}" and type = "{type}";'
    chq1 = fetch_sql(chq1)

    chq2 = f'select * from enrolled_courses where student_id="{student_id}" and course = "{course}" and semester = "{semester}" ;'
    chq2 = fetch_sql(chq2)
    if len(chq) > 0 and len(chq1) > 0 and len(chq2) > 0:
        insert_into_marks(student_id, course, semester, type, total_marks, achieved_marks, updated_by)
        return render_template('show_message.html', message='Marks Submitted')
    else:
        return render_template('show_message.html', message='Course or Student does not exist')


if __name__ == '__main__':
    app.run(debug = True)
