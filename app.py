from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = '****'  # Change this to a secure key

# Dummy user database (replace with a proper database in real-world applications)
users = []

# Dummy data logs (replace with actual data storage mechanism)
sleep_log = []
weight_tracker = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if the email is already registered
        if any(user['email'] == email for user in users):
            flash('Email is already registered!', 'error')
        else:
            users.append({'email': email, 'password': password})
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if the email and password match
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['email'] = email
                flash('Login successful!', 'success')
                return redirect(url_for('profile'))
        flash('Invalid email or password!', 'error')
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'email' in session:
        user = next((user for user in users if user['email'] == session['email']), None)
        if user:
            return render_template('profile.html', user=user)
        else:
            flash('User not found!', 'error')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'email' in session:
        user_email = session['email']
        user_settings = {}  # Replace with actual user settings retrieval mechanism
        if request.method == 'POST':
            # Handle form submission to update settings
            user_settings['setting1'] = request.form.get('setting1', '')
            user_settings['setting2'] = request.form.get('setting2', '')
            # Add more settings as needed
            flash('Settings updated!', 'success')
            return redirect(url_for('profile'))
        return render_template('settings.html', settings=user_settings)  # Pass user settings to the template
    return redirect(url_for('login'))

@app.route('/sleep_log')
def view_sleep_log():
    if 'email' in session:
        user_email = session['email']
        return render_template('sleep_log.html', sleep_log=sleep_log)
    return redirect(url_for('login'))

@app.route('/weight_tracker')
def view_weight_tracker():
    if 'email' in session:
        user_email = session['email']
        return render_template('weight_tracker.html', weight_tracker=weight_tracker)
    return redirect(url_for('login'))

@app.route('/bmi_calculator', methods=['GET', 'POST'])
def bmi_calculator():
    if 'email' in session:
        if request.method == 'POST':
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            bmi = calculate_bmi(weight, height)
            bmi_category = get_bmi_category(bmi)
            diet_plan = get_diet_plan(bmi_category)
            return render_template('bmi_result.html', bmi=bmi, category=bmi_category, diet=diet_plan)
        return render_template('bmi_calculator.html')
    return redirect(url_for('login'))

def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obesity'

def get_diet_plan(category):
    if category == 'Underweight':
        return 'Increase your calorie intake with balanced meals.'
    elif category == 'Normal weight':
        return 'Maintain your current calorie intake with balanced meals.'
    elif category == 'Overweight':
        return 'Reduce your calorie intake and increase physical activity.'
    else:
        return 'Seek professional advice for weight management.'

@app.route('/sos')
def sos():
    # Implement SOS functionality here
    flash('SOS alert sent to ambulance and family members!', 'info')
    return redirect(url_for('profile'))

@app.route('./exercise_log')
def view_exercise_log():
    if 'email' in session:
        user_email = session['email']
        # Assuming you have a function to fetch exercise log data for the logged-in user
        exercise_log_data = fetch_exercise_log_data(user_email)
        return render_template('exercise_log.html', exercise_log=exercise_log_data)
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
