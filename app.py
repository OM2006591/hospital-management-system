from flask import Flask, jsonify, request, render_template, session, redirect
import mysql.connector
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "secret123"

# =========================
# EMAIL CONFIG
# =========================
SENDER_EMAIL = "your_email@gmail.com"     
APP_PASSWORD = "your_app_password"


# =========================
# HOME
# =========================
@app.route('/')
def home():
    if not session.get("logged_in"):
        return redirect('/login')
    return render_template("index.html")


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data.get("username") == "admin" and data.get("password") == "123":
        session["logged_in"] = True
        return {"message": "Login successful"}
    else:
        return {"error": "Invalid credentials"}, 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# =========================
# DB CONNECTION
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db1"
    )


# =========================
# EMAIL FUNCTION
# =========================
def send_email(to_email, patient_name, date, time):
    subject = "Appointment Confirmation 🏥"

    body = f"""
Hello {patient_name},

Your appointment has been successfully booked.

📅 Date: {date}
⏰ Time: {time}

Please arrive 10 minutes early.

Thank you,
Hospital Management
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", e)


# =========================
# PATIENT APIs
# =========================
@app.route('/patients', methods=['GET'])
def get_patients():
    if not session.get("logged_in"):
        return {"error": "Login required"}, 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Patients")
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)


@app.route('/add_patient', methods=['POST'])
def add_patient():
    if not session.get("logged_in"):
        return {"error": "Login required"}, 401

    data = request.get_json()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Patients (name, age, gender, email)
            VALUES (%s, %s, %s, %s)
        """, (data['name'], data['age'], data['gender'], data['email']))

        conn.commit()
        conn.close()

        return {"message": "Patient added successfully"}

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/delete_patient/<int:id>', methods=['DELETE'])
def delete_patient(id):
    if not session.get("logged_in"):
        return {"error": "Login required"}, 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Patients WHERE patient_id = %s", (id,))
    conn.commit()
    conn.close()

    return {"message": "Patient deleted successfully"}


# =========================
# APPOINTMENTS
# =========================
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    if not session.get("logged_in"):
        return {"error": "Login required"}, 401

    data = request.get_json()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # INSERT APPOINTMENT
        cursor.execute("""
            INSERT INTO Appointments 
            (patient_id, doctor_id, appointment_date, appointment_time, status, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['patient_id'],
            data['doctor_id'],
            data['appointment_date'],
            data['appointment_time'],
            data['status'],
            data['priority']
        ))

        # FETCH PATIENT EMAIL
        cursor.execute("""
            SELECT name, email FROM Patients WHERE patient_id = %s
        """, (data['patient_id'],))

        patient = cursor.fetchone()

        conn.commit()
        conn.close()

        # SEND EMAIL
        if patient and patient['email']:
            send_email(
                patient['email'],
                patient['name'],
                data['appointment_date'],
                data['appointment_time']
            )

        return {"message": "Appointment booked + Email sent ✅"}

    except Exception as e:
        return {"error": str(e)}, 500


@app.route('/appointments', methods=['GET'])
def get_appointments():
    if not session.get("logged_in"):
        return {"error": "Login required"}, 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.appointment_id,
            p.name AS patient_name,
            d.name AS doctor_name,
            a.appointment_date,
            a.appointment_time,
            a.priority,
            a.status
        FROM Appointments a
        JOIN Patients p ON a.patient_id = p.patient_id
        JOIN Doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.priority ASC, a.appointment_time ASC
    """)

    data = cursor.fetchall()

    for row in data:
        row['appointment_time'] = str(row['appointment_time'])
        row['appointment_date'] = str(row['appointment_date'])

    conn.close()
    return jsonify(data)


# =========================
# UPDATE STATUS
# =========================
@app.route('/update_status/<int:id>', methods=['PUT'])
def update_status(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Appointments 
        SET status = 'Completed'
        WHERE appointment_id = %s
    """, (id,))

    conn.commit()
    conn.close()

    return {"message": "Marked as Completed"}


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)
