from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Auto-reload templates during development

BOOKINGS_FILE = 'bookingsDetails.json'
USERS_FILE = 'user_details.json'
RESORTS_FILE = 'resorts.json'

# Load initial data
def load_data():
    try:
        with open(RESORTS_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

resorts_data = load_data()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def save_booking(data):
    bookings = []
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'r', encoding='utf-8') as f:
            try:
                bookings = json.load(f)
            except json.JSONDecodeError:
                pass

    bookings.append(data)
    with open(BOOKINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bookings, f, indent=4, ensure_ascii=False)

@app.route('/')
def homepage():
    return render_template('index.html', user_email=session.get('user'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('loginEmail', '').strip()
    password = request.form.get('loginPassword', '').strip()
    users = load_users()

    user = next((u for u in users if u['email'] == email and u['password'] == password), None)

    if user:
        session['user'] = email
        flash('Login successful!', 'success')
    else:
        flash('Invalid email or password.', 'error')

    return redirect(url_for('homepage'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('signupEmail', '').strip()
    password = request.form.get('signupPassword', '').strip()

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('homepage'))

    users = load_users()
    if any(u['email'] == email for u in users):
        flash('Email already registered.', 'error')
        return redirect(url_for('homepage'))

    users.append({'email': email, 'password': password})
    save_users(users)
    flash('Signup successful! You can now log in.', 'success')
    return redirect(url_for('homepage'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('homepage'))

@app.route('/explore')
def explore():
    return render_template('explore.html', resorts=resorts_data) 

@app.route('/destination/<city_name>')
def show_city(city_name):
    with open('resorts.json') as f:
        resorts_data = json.load(f)

    # Normalize city_name for matching keys ignoring case
    city_key = None
    for key in resorts_data.keys():
        if key.lower() == city_name.lower():
            city_key = key
            break

    if not city_key:
        return f"No resorts found for {city_name}", 404

    city_resorts = resorts_data[city_key]

    return render_template('city.html', city=city_key, resorts=city_resorts) 

if __name__ == '__main__':
    app.run(debug=True)