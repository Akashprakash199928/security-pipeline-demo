from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret
SECRET_API_KEY = "DEMO_FAKE_sk_test_key_not_real_12345"

# VULNERABILITY 2: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return str(cursor.fetchall())

# VULNERABILITY 3: Command Injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    result = os.popen(f'ping -c 1 {host}').read()
    return f"<pre>{result}</pre>"

@app.route('/')
def home():
    return """
    <html>
        <body>
            <h1>Vulnerable Demo Application</h1>
            <p>This app has security vulnerabilities for testing.</p>
            <ul>
                <li><a href="/user/admin">User Lookup</a></li>
                <li><a href="/ping?host=google.com">Ping Tool</a></li>
            </ul>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)