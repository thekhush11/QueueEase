# QueueEase 🚀

_A Modern Token Management System for Hospitals and Clinics_

---

## 📌 Overview

QueueEase is a **role-based token management system** built with Python Flask.  
It simplifies patient–doctor queues by allowing:

- Patients to generate and track their tokens.
- Doctors to call the next patient in real time.

The system has a **modern UI**, a **modular codebase**, and is designed for scalability.

---

## ✨ Features

- 🔑 **User Authentication** – Register & Login (Patient/Doctor roles)
- 🎟️ **Token Generation** – Patients can generate tokens instantly
- 🧑‍⚕️ **Doctor Dashboard** – Call next patient, view all tokens
- 👩‍⚕️ **Patient Dashboard** – Track token status live
- 🔔 **Notification Service** (extensible)
- ⚡ **Real-time Updates** – Socket-based token refresh
- 🎨 **Modern Responsive UI** – Clean, intuitive design
- 🧪 **Testing Support** – Unit tests for authentication

---

## 🏗️ Project Structure

QueueEase/

│

├── app.py # Main Flask entry point

├── config.py # App configuration (DB URI, secret keys, etc.)

├── requirements.txt # Dependencies

├── README.md # Documentation

│

├── instance/ # Runtime files

│ └── queueease.db # SQLite database (local dev only)

│

├── models/ # Database models

│ ├── init.py

│ ├── token.py # Token model

│ └── user.py # User model

│

├── routes/ # Flask blueprints (routes)

│ ├── init.py

│ ├── auth.py # Login & Registration

│ ├── doctor.py # Doctor dashboard routes

│ └── patient.py # Patient dashboard routes

│

├── services/ # Business logic & services

│ ├── init.py

│ ├── notification_service.py

│ └── token_service.py

│

├── static/ # Static assets

│ ├── css/

│ │ ├── auth.css # Styles for login/register

│ │ └── style.css # Global styles

│ ├── images/ # Images & icons

│ └── js/

│ ├── main.js # General frontend scripts

│ └── socket.js # Real-time updates with SocketIO

│

├── templates/ # HTML templates (Jinja2)

│ ├── base.html # Common layout

│ ├── index.html # Home page

│ ├── login.html # Login page

│ ├── register.html # Registration page

│ ├── patient_dashboard.html

│ └── doctor_dashboard.html

│

└── tests/ # Unit tests

└── test_auth.py

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/thekhush11/QueueEase
cd QueueEase
```

### 2. Create Virtual Environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Access in Browser

```bash
http://127.0.0.1:5000/
```

### 👩‍💻 Tech Stack

- Backend: Python Flask
- Frontend: HTML, CSS, JavaScript
- Real-time: Flask-SocketIO
- Database: SQLite (local) → future scope: MySQL/PostgreSQL
- Testing: Pytest
- Deployment: Localhost → future scope: Heroku/AWS/GCP

### 🚀 Future Enhancements

- 📱 Mobile-friendly PWA version
- 📊 Analytics dashboard for hospital admins
- 📩 SMS/Email token notifications
- 🔒 JWT-based authentication
- ☁️ Cloud deployment with scalable DB

### 📜 License

This project is licensed under the MIT License.
