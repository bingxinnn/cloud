# from curses import flash
# from flask_wtf.csrf import CSRFProtect, CSRFError
from io import BytesIO
from flask import Flask, render_template, session, request, redirect, flash, jsonify, url_for
from pymysql import connections
import os
import boto3
import botocore
from flask import send_file
# import pdfplumber
# Use BytesIO to handle the binary content
# from werkzeug.utils import secure_filename
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompwd,
    db=customdb
)

output = {}
table = 'Student'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/homepage", methods=['GET', 'POST'])
def homepage():
    return render_template('home.html')

@app.route("/searchStudentPage", methods=['GET', 'POST'])
def searchStudentPage():
    return render_template('search_student.html')

@app.route("/aboutpage", methods=['GET', 'POST'])
def aboutpage():
    return render_template('about.html')

@app.route("/featurepage", methods=['GET', 'POST'])
def featurepage():
    return render_template('feature.html')

@app.route("/contactpage", methods=['GET', 'POST'])
def contactpage():
    return render_template('contact.html')

@app.route("/coursepage", methods=['GET', 'POST'])
def coursepage():
    return render_template('course.html')

@app.route("/indexpage", methods=['GET', 'POST'])
def indexpage():
    return render_template('index.html')

@app.route("/teampage", methods=['GET', 'POST'])
def teampage():
    return render_template('team.html')

@app.route("/testimonialpage", methods=['GET', 'POST'])
def testimonialpage():
    return render_template('testimonial.html')

@app.route("/ziyuPortfolio", methods=['GET', 'POST'])
def ziyuPortfolio():
    return render_template('ziyu_portfolio.html')

@app.route("/bingxinPortfolio", methods=['GET', 'POST'])
def bingxinPortfolio():
    return render_template('bingxin_portfolio.html')

@app.route("/justinPortfolio", methods=['GET', 'POST'])
def justinPortfolio():
    return render_template('justin_portfolio.html')

@app.route("/junxianPortfolio", methods=['GET', 'POST'])
def junxianPortfolio():
    return render_template('junxian_portfolio.html')

@app.route("/jianyongPortfolio", methods=['GET', 'POST'])
def jianyongPortfolio():
    return render_template('jianyong_portfolio.html')

@app.route("/xinyiPortfolio", methods=['GET', 'POST'])
def xinyiPortfolio():
    return render_template('xinyi_portfolio.html')

@app.route("/companyform", methods=['GET'])
def companyform():
    #if request.method == "POST":

        com_name = request.form['com_name']
        com_address = request.form['com_address']
        com_HP = request.form['com_hp']
        com_email = request.form['com_mail']
        com_description = request.form['com_description']
        com_website = request.form['com_website']
        com_logo_file = request.files['company_logo_file']
        job_title = request.form['job_title']
        job_type = request.form['job_type']
        job_description = request.form['job_description']
    


        insert_sql = "INSERT INTO company VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if com_logo_file.filename == "":
            return "Please select an image file"

        try:

            cursor.execute(insert_sql, (com_name, com_address, com_HP,com_email,com_description,com_website,job_title,job_type,job_description))
            db_conn.commit()
            # Uplaod image file in S3 #
            comp_image_file_name_in_s3 = str(com_name) + "_logo_image_file"
            s3 = boto3.resource('s3')

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(Key=com_image_file_name_in_s3, Body=com_logo_file)
                bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                s3_location = (bucket_location['LocationConstraint'])

                if s3_location is None:
                    s3_location = ''
                else:
                    s3_location = '-' + s3_location

                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    com_image_file_name_in_s3)

            except Exception as e:
                return str(e)

        finally:
            cursor.close()

        print("all modification done...")
        return render_template('AddComOutput.html', name=com_name)
            #return to company profile page

@app.route("/searchStudentProcess", methods=['GET', 'POST'])
def searchStudProcess():
    stud_id = request.form['stud_id']

    search_sql = "SELECT * FROM student WHERE stud_id = %s"
    cursor = db_conn.cursor()

    cursor.execute(search_sql, (stud_id))
    rows = cursor.fetchall()

    if rows:
        return render_template('display_searchStudInfo.html', rows=rows)
    else:
        return "Student does not exist."

    cursor.close()


def authenticate_user(username, password):
    try:
        # Connection is db_conn !!!
        
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_pass, upper(user_role) FROM users WHERE user_id = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            db_pass, user_role = user_data
            
            # Check if password correct
            if password == db_pass:
                # Redirect users based on their roles
                if user_role == 'ADMIN':
                    return 'admin.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'LECTURER':
                    return 'lecturer.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'STUDENT':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'COMPANY':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
                elif user_role == 'MASTER':
                    return 'home.html' # CHANGE BASED ON IMPLEMENTATION
                else:
                    return None  # Invalid user_role, access denied
        
        return None  # User not found or passwords don't match, access denied
    
    except Exception as e:
        print("Database error:", str(e))
        return None  # Access denied in case of an error
    
    finally:
        # Close the database connection
        if cursor:
            cursor.close()


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username'] #From index.html
    password = request.form['password'] #From index.html
    
    # Use your authenticate_user function here
    redirect_page = authenticate_user(username, password)
    
    if redirect_page:
        # Store the username in the Flask session
        session['username'] = username
        
        # Redirect to the appropriate page based on user role
        return render_template(redirect_page)
    else:
        return "Access denied"
    
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form['signUpUsername'] #From index.html
    password = request.form['signUpPassword'] #From index.html
    roles    = request.form['roles'] #From index.html
    
    insert_sql = "INSERT INTO users VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (username, password, roles))
    db_conn.commit()
    cursor.close()

    return render_template('index.html')

# @app.route("/displayStudInfo", methods=['GET', 'POST'])
# def viewStudentInfo():
#     statement = "SELECT s.* FROM student s JOIN company c ON s.com_id = c.com_id WHERE s.com_id = 'C0001';"
#     cursor = db_conn.cursor()
#     cursor.execute(statement)
#     result = cursor.fetchall()
#     cursor.close()
    
#     return render_template('display_studInfo.html', data=result)

@app.route("/displayStudInfo", methods=['GET', 'POST'])
def viewStudentInfo():
    username = session.get('username')

    if username:
        # statement = "SELECT s.* FROM student s JOIN company c ON s.com_email = c.com_email WHERE s.com_email = %s;"
        statement = "SELECT s.* FROM student s JOIN company c ON s.com_id = c.com_id WHERE s.com_id = %s;"

        cursor = db_conn.cursor()
        cursor.execute(statement, (username,))
        result = cursor.fetchall()
        cursor.close()

        return render_template('display_studInfo.html', data=result)
    
    else:
        return "Nothing found"

@app.route('/displayStudInfoDetails/<stud_id>')
def viewStudentInfoDetails(stud_id):
    statement = "SELECT * FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    result = cursor.fetchone()
            
    return render_template('display_studInfoDetails.html', student=result)


@app.route('/displayStudResume/<stud_id>')
def displayStudentResume(stud_id):
    statement = "SELECT stud_id, stud_resume FROM student s WHERE stud_id = %s"
    cursor = db_conn.cursor()
    cursor.execute(statement, (stud_id,))
    results = cursor.fetchone()
    
    if results: 
        studID, resume = results
        resume = "https://" + bucket + ".s3.amazonaws.com/stud_id-" + studID + "_pdf.pdf"
        return render_template('display_resume.html', results=results, resume=resume)
        
    else: 
        return "Invalid student."
        
    return render_template('display_studInfo.html')

@app.route("/lecturerDisplayStudInfo", methods=['GET', 'POST'])
def lecturerViewStudentInfo():
    statement = "SELECT s.* FROM student s JOIN lecturer l ON s.lec_id = l.lec_id WHERE s.lec_id = 'L0001';"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('lec_displayStudInfo.html', data=result)


@app.route("/studProfile/", methods=['GET', 'POST'])
def GetStudInfo():
    username = session.get('username')

    if username:
        # Fetch student information from the database
        statement = "SELECT * FROM student WHERE stud_id = %s;"
        cursor = db_conn.cursor()
        cursor.execute(statement, (username,))
        student_data = cursor.fetchone()
        cursor.close()
        
        return render_template('studProfile.html', student=student_data)
    else:
        return "Student not found"

@app.route("/preview/<stud_id>")
def preview_file(stud_id):
    # Fetch the resume BLOB from the database
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT stud_resume FROM Student WHERE stud_id = {stud_id}")
    resume_data = cursor.fetchone()
    cursor.close()

    if resume_data:
        # Save the resume to a temporary file
        resume_blob = resume_data[0]
        temp_file_path = f"temp_resume_{stud_id}.pdf"

        with open(temp_file_path, 'wb') as file:
            file.write(resume_blob)

        # Send the file for download
        return send_file(temp_file_path, as_attachment=True)
    else:
        return "Resume not found"


@app.route("/displayComInfo", methods=['GET', 'POST'])
def viewCompanyInfo():
    statement = "SELECT * FROM company WHERE status = 0;"
    cursor = db_conn.cursor()
    cursor.execute(statement)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('admin.html', data=result)


if __name__ == '__main__':
    app.secret_key = 'cc_key'
    app.run(host='0.0.0.0', port=80, debug=True)
