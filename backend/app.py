from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from similarity import rank_resumes

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# ---------------- FLASK APP ----------------
app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "frontend", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "frontend", "static")
)

app.secret_key = "super_secret_key_123"

# ---------------- UPLOAD FOLDER ----------------
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, "resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- ALLOWED EXTENSIONS ----------------
ALLOWED_EXTENSIONS = {".pdf", ".docx"}

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ---------------- VIEW RESUME ----------------
@app.route("/resumes/<filename>")
def view_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------- DOWNLOAD RESUME ----------------
@app.route("/download/<filename>")
def download_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["user"] = "admin"
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ---------------- UPLOAD & RANK ----------------
@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))

    job_description = request.form["job_description"]
    resumes = request.files.getlist("resumes")

    # -------- CLEAR OLD FILES --------
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # -------- SAVE ONLY PDF & DOCX --------
    for resume in resumes:
        if resume.filename == "":
            continue

        ext = os.path.splitext(resume.filename)[1].lower()

        if ext in ALLOWED_EXTENSIONS:
            save_path = os.path.join(UPLOAD_FOLDER, resume.filename)
            resume.save(save_path)

    # -------- RANK RESUMES --------
    results = rank_resumes(job_description, UPLOAD_FOLDER)

    return render_template("results.html", results=results)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
