from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE CONFIG ---------------- #
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///queueease.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)

# ---------------- MODELS ---------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "doctor" or "patient"

    def __init__(self, username, age, gender, password, role):
        self.username = username
        self.age = age
        self.gender = gender
        self.password = password
        self.role = role


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default="waiting")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="tokens")

    def __init__(self, token, user_id, status="waiting"):
        self.token = token
        self.user_id = user_id
        self.status = status

# Create tables if not exist
with app.app_context():
    db.create_all()

# ---------------- ROUTES ---------------- #
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ---------------- #
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        age = request.form["age"]
        gender = request.form["gender"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        captcha = request.form["captcha"]
        role = request.form["role"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("User already exists!", "error")
        elif password != confirm_password:
            flash("Passwords do not match!", "error")
        elif captcha.lower() != "abcd":
            flash("Invalid CAPTCHA!", "error")
        else:
            new_user = User(username, age, gender, password, role)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ---------------- #
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            session["user"] = user.username
            session["role"] = user.role
            flash("Login successful!", "success")
            if user.role == "doctor":
                return redirect(url_for("doctor_dashboard"))
            else:
                return redirect(url_for("patient_dashboard"))
        else:
            flash("Invalid credentials!", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

# ---------------- TOKEN SYSTEM ---------------- #
@app.route("/generate_token")
def generate_token():
    if "user" not in session or session["role"] != "patient":
        return redirect(url_for("login"))

    # Generate next token number
    last_token = Token.query.order_by(Token.id.desc()).first()
    next_number = 1 if not last_token else last_token.id + 1
    token_id = f"T{next_number:03d}"

    new_token = Token(token_id, session["user_id"])
    db.session.add(new_token)
    db.session.commit()

    flash(f"Your token is {token_id}", "success")
    socketio.emit("update_tokens", serialize_tokens())
    return redirect(url_for("patient_dashboard"))

@app.route("/patient")
def patient_dashboard():
    if "user" not in session or session["role"] != "patient":
        return redirect(url_for("login"))
    
    my_tokens = Token.query.filter_by(user_id=session["user_id"]).all()
    return render_template("patient_dashboard.html", user=session["user"], my_tokens=my_tokens)

@app.route("/doctor")
def doctor_dashboard():
    if "user" not in session or session["role"] != "doctor":
        return redirect(url_for("login"))
    
    all_tokens = Token.query.all()
    return render_template("doctor_dashboard.html", user=session["user"], tokens=all_tokens)

@app.route("/call_next")
def call_next():
    if "user" not in session or session["role"] != "doctor":
        return redirect(url_for("login"))

    next_token = Token.query.filter_by(status="waiting").first()
    if next_token:
        next_token.status = "called"
        db.session.commit()
        flash(f"Now calling {next_token.token} ({next_token.user.username})", "success")

    socketio.emit("update_tokens", serialize_tokens())
    return redirect(url_for("doctor_dashboard"))

# ---------------- HELPERS ---------------- #
def serialize_tokens():
    tokens = Token.query.all()
    return [
        {"token": t.token, "status": t.status, "user": t.user.username}
        for t in tokens
    ]

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    socketio.run(app, debug=True)