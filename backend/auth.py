from flask import session

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_user(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session["logged_in"] = True
        session["username"] = username
        return True
    return False

def logout_user():
    session.clear()

def is_logged_in():
    return session.get("logged_in", False)
