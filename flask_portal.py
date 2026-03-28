from flask import Flask, render_template_string, request, redirect, url_for, session
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'student',
    'password': 'student123',
    'database': 'unidb'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>UniDB Student Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #16213e; padding: 40px; border-radius: 10px; width: 320px; box-shadow: 0 0 20px rgba(0,150,255,0.2); }
        h2 { text-align: center; color: #00b4d8; }
        input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #444; border-radius: 5px; background: #0f3460; color: #eee; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #00b4d8; border: none; border-radius: 5px; color: white; font-size: 16px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0096c7; }
        .error { color: #ff6b6b; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🎓 UniDB Portal</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Student ID" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
    </div>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>UniDB - Student Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; margin: 0; padding: 20px; }
        h1 { color: #00b4d8; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #16213e; border-radius: 8px; overflow: hidden; }
        th { background: #0f3460; padding: 12px; text-align: left; color: #00b4d8; }
        td { padding: 10px 12px; border-bottom: 1px solid #2a2a4a; }
        tr:hover td { background: #0f3460; }
        .logout { float: right; padding: 8px 16px; background: #e63946; border: none; border-radius: 5px; color: white; cursor: pointer; text-decoration: none; }
        .badge { padding: 3px 8px; border-radius: 12px; font-size: 12px; }
        .active { background: #2d6a4f; color: #95d5b2; }
        .inactive { background: #6b2737; color: #ffb3c1; }
    </style>
</head>
<body>
    <a href="/logout" class="logout">Logout</a>
    <h1>🎓 Student Records</h1>
    <p>Logged in as: <strong>{{ username }}</strong> | {{ now }}</p>
    <table>
        <tr>
            <th>Student ID</th><th>Name</th><th>Email</th><th>Course</th><th>GPA</th><th>Status</th>
        </tr>
        {% for row in students %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
            <td><span class="badge {{ 'active' if row[5] == 'Active' else 'inactive' }}">{{ row[5] }}</span></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            db.close()
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials. Access denied.'
        except Exception as e:
            error = f'Database error: {str(e)}'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT student_id, name, email, course, gpa, status FROM students")
        students = cursor.fetchall()
        db.close()
    except Exception as e:
        students = []
    return render_template_string(DASHBOARD_HTML,
                                   username=session['username'],
                                   students=students,
                                   now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
