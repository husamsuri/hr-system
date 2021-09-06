import os
from flask import Flask, redirect, url_for, request, send_file, render_template
from datetime import datetime, date
import json
import mariadb
from config import dataBaseConfig, UPLOAD_FOLDER, allowed_files

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_files


@app.route('/apply', methods=['POST'])
def apply():
    try:
        conn = mariadb.connect(**dataBaseConfig)
        cur = conn.cursor()
    except:
        return {
            "error": "database error"
        }, 500

    file = request.files['file']
    if not allowed_file(file.filename):
        return {
            "error": "file extension not allowed"
        }, 400

    if not isinstance(request.form['name'], str) or not isinstance(request.form['birthDate'], str) or not isinstance(request.form['ExperienceYears'], str) or not isinstance(request.form['department'], str):
        return {
            "error": "type error"
        }, 400

    department = request.form['department'].capitalize()

    if department != 'IT' and department != 'HR' and department != 'Finance':
        return {
            "error": "department not allowed"
        }, 400

    try:
        int(request.form['ExperienceYears'])
    except ValueError:
        return {
            "error": "ExperienceYears should be number"
        }, 400

    try:
        datetime.fromisoformat(request.form['birthDate'])
    except ValueError:
        return {
            "error": "not a valid date"
        }, 400

    cur.execute(
        f"INSERT INTO applicants (name, DOB, experience_years, department, created_at) VALUES ('{request.form ['name']}', '{request.form['birthDate']}', {request.form['ExperienceYears']}, '{department}', '{datetime.now()}');")
    conn.commit()

    is_dir = os.path.exists(UPLOAD_FOLDER)
    if (not is_dir):
        os.mkdir(UPLOAD_FOLDER)

    file.save(os.path.join(
        UPLOAD_FOLDER, f"{cur.lastrowid}.{file.filename.rsplit('.', 1)[1].lower()}"))

    return {
        "applicantId": cur.lastrowid,
        "status": "success"
    }


@app.route('/list')
def list():
    if not 'X-ADMIN' in request.headers:
        return {"error": "Unauthorized Access"}, 401

    if request.headers['X-ADMIN'] != "1":
        return {"error": "Unauthorized Access"}, 401
    conn = mariadb.connect(**dataBaseConfig)
    cur = conn.cursor()
    cur.execute("select * from applicants ORDER BY created_at DESC")
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    return {"data": json_data}


@app.route('/file/<id>')
def file(id):
    if not 'X-ADMIN' in request.headers:
        return {"error": "Unauthorized Access"}, 401

    if request.headers['X-ADMIN'] != "1":
        return {"error": "Unauthorized Access"}, 401
    try:
        return send_file(f"./Resumes/{id}.pdf", as_attachment=True)
    except:
        try:
            return send_file(f"./Resumes/{id}.docx", as_attachment=True)
        except:
            return {
                "error": "file not found"
            }, 404


if __name__ == '__main__':
    app.run(debug=True)
