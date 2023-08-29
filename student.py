
from flask import Flask, render_template, url_for, request, redirect, session
# from main import app
from sql import sql, fetch_sql

import mysql.connector

# ! THE STUDENT CREDENTIALS ARE AUTHINTICATED !

def authenticate_student(id, pw):
    qry = f"SELECT student_id, name, email, password FROM student WHERE student_id = '{id}' and password = '{pw}' "
    tab = fetch_sql(qry)
    # the student user does not exist
    if len(tab) == 0:
        msg = 'Id or Password or both not registered as student.'
        return render_template("show_message.html", title_bar = "Admin Login Failed",  message = msg)
    
    # the student user exists
    else:
        student_id, name, email, password = tab[0][0], tab[0][1], tab[0][2], tab[0][3]
        session['student_id'] = student_id
        session['student_password'] = password
        session['student_name'] = name
        session['student_email'] = email
        return redirect(url_for('student_dashboard' , student_id = student_id))
    
def table_row(s):
    ret = []
    for i in s:
        p = ''

        for k in i:
            p = p + '<td>' + str(k) + '</td>'
        ret.append(p)

    return ret


def add_application(studentID, credit, result, description):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='cse370_project',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO scholarship (student_id, credits, result, description, status)
                                VALUES (%s, %s, %s, %s, %s) """

        record = (session['student_id'], credit, result, description, "NULL")
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Application submitted")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# student_id		credits	result	description	status	