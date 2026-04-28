const BASE_URL = "http://127.0.0.1:5000";

// =========================
// ADD PATIENT
// =========================
function addPatient() {
    let name = document.getElementById("name").value;
    let age = document.getElementById("age").value;
    let gender = document.getElementById("gender").value;
    let email = document.getElementById("email").value;

    fetch(`${BASE_URL}/add_patient`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, age, gender, email })
    })
    .then(res => res.json())
    .then(data => {
        alert("✅ " + (data.message || data.error));
        getPatients();

        // clear fields
        document.getElementById("name").value = "";
        document.getElementById("age").value = "";
        document.getElementById("gender").value = "";
        document.getElementById("email").value = "";
    })
    .catch(err => {
        console.error(err);
        alert("❌ Error adding patient");
    });
}


// =========================
// GET PATIENTS
// =========================
function getPatients() {
    fetch(`${BASE_URL}/patients`)
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("patientsList");
        list.innerHTML = "";

        data.forEach(p => {
            let item = document.createElement("li");
            item.innerText = `ID: ${p.patient_id} | ${p.name} | ${p.gender} | ${p.email}`;
            list.appendChild(item);
        });
    })
    .catch(err => console.error(err));
}


// =========================
// DELETE PATIENT
// =========================
function deletePatient() {
    let id = document.getElementById("deleteId").value;

    fetch(`${BASE_URL}/delete_patient/${id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert("🗑️ " + (data.message || data.error));
        getPatients();
        document.getElementById("deleteId").value = "";
    })
    .catch(err => console.error(err));
}


// =========================
// BOOK APPOINTMENT
// =========================
function bookAppointment() {
    let patient_id = document.getElementById("patient_id").value;
    let doctor_id = document.getElementById("doctor_id").value;
    let appointment_date = document.getElementById("appointment_date").value;
    let appointment_time = document.getElementById("appointment_time").value;
    let condition = document.getElementById("condition").value;

    // 🔥 PRIORITY LOGIC
    let priority;
    if (condition === "critical") priority = 1;
    else if (condition === "moderate") priority = 2;
    else priority = 3;

    fetch(`${BASE_URL}/add_appointment`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            status: "Pending",
            priority
        })
    })
    .then(res => res.json())
    .then(data => {
        alert("📅 " + (data.message || data.error));
        getAppointments();

        // clear fields
        document.getElementById("patient_id").value = "";
        document.getElementById("doctor_id").value = "";
        document.getElementById("appointment_date").value = "";
        document.getElementById("appointment_time").value = "";
    })
    .catch(err => console.error(err));
}


// =========================
// GET APPOINTMENTS (WITH COLORS)
// =========================
function getAppointments() {
    fetch(`${BASE_URL}/appointments`)
    .then(res => res.json())
    .then(data => {
        let table = document.getElementById("appointmentsTable");

        table.innerHTML = `
            <tr>
                <th>ID</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Date</th>
                <th>Time</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        `;

        data.forEach(a => {
            let row = table.insertRow();

            row.insertCell(0).innerText = a.appointment_id;
            row.insertCell(1).innerText = a.patient_name;
            row.insertCell(2).innerText = a.doctor_name;
            row.insertCell(3).innerText = a.appointment_date;
            row.insertCell(4).innerText = a.appointment_time;
            row.insertCell(5).innerText = a.priority;

            // STATUS
            let statusCell = row.insertCell(6);
            statusCell.innerText = a.status;

            if (a.status === "Pending") {
                statusCell.style.color = "orange";
                statusCell.style.fontWeight = "bold";
            } else {
                statusCell.style.color = "green";
                statusCell.style.fontWeight = "bold";
            }

            // ACTION BUTTON
            let actionCell = row.insertCell(7);

            if (a.status === "Pending") {
                let btn = document.createElement("button");
                btn.innerText = "Mark Completed";
                btn.style.background = "#3498db";
                btn.style.color = "white";
                btn.style.border = "none";
                btn.style.padding = "5px 10px";
                btn.style.borderRadius = "5px";
                btn.style.cursor = "pointer";

                btn.onclick = () => updateStatus(a.appointment_id);
                actionCell.appendChild(btn);
            } else {
                actionCell.innerHTML = "✔ Done";
            }

            // 🎨 PRIORITY COLORS
            if (a.priority == 1) {
                row.style.backgroundColor = "#f8d7da"; // RED
            }
            else if (a.priority == 2) {
                row.style.backgroundColor = "#fff3cd"; // YELLOW
            }
            else {
                row.style.backgroundColor = "#d4edda"; // GREEN
            }
        });

        document.getElementById("totalAppointments").innerText =
            "Total Appointments: " + data.length;

    })
    .catch(err => console.error(err));
}


// =========================
// UPDATE STATUS
// =========================
function updateStatus(id) {
    fetch(`${BASE_URL}/update_status/${id}`, {
        method: "PUT"
    })
    .then(res => res.json())
    .then(data => {
        alert("✅ " + (data.message || data.error));
        getAppointments();
    })
    .catch(err => console.error(err));
}
