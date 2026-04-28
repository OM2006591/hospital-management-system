#  Hospital Management System

A full-stack Hospital Management System developed using Flask (Python), MySQL, and HTML/CSS/JavaScript. The system manages patients, doctors, and appointments with priority scheduling and email notifications.

---

## Features

* Add, view, and delete patients
* Book appointments with priority scheduling
* View appointments (sorted by priority & time)
* Update appointment status (Pending → Completed)
* Email notification on appointment booking
* Admin login system

---

## Tech Stack

* Backend: Python (Flask)
* Database: MySQL
* Frontend: HTML, CSS, JavaScript
* API Testing: Postman

---

## 🔗 API Endpoints

* GET /patients
* GET /patient/<id>
* POST /add_patient
* DELETE /delete_patient/<id>
* GET /doctors
* POST /add_appointment
* GET /appointments
* PUT /update_status/<id>

---

 ▶️ How to Run

1. Install dependencies:
   pip install flask mysql-connector-python

2. Run the server:
   python app.py

3. Open in browser:
   http://127.0.0.1:5000

---

 Login Credentials

Username: admin
Password: 123

---

 Purpose

This project is developed for academic purposes to demonstrate DBMS concepts, REST API development, and full-stack web application design.

---

 Author

**Om Anil Mali**
B.Tech CSE (Core) Student
MIT World Peace University (MIT-WPU), Pune

