from flask import Flask, request, render_template, redirect, url_for, session, jsonify, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to display admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (session['username'],))
        user = cursor.fetchone()
        conn.close()

        if user and user['is_admin']:  # Assuming 'is_admin' is a field in your users table
            # Render admin dashboard
            return render_template('admin_dashboard.html', username=session['username'])
        else:
            flash('You are not authorized to access this page as an admin.')
            return redirect(url_for('main1'))  # Redirect to regular main page
    else:
        return redirect(url_for('login_form'))

# Route to delete bookmark
@app.route('/delete_bookmark/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    if 'username' not in session:
        return jsonify({"message": "User not logged in"}), 401

    username = session['username']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM bookmarks WHERE id = ? AND username = ?', (bookmark_id, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Bookmark deleted successfully"}), 200

# Route to add bookmark
@app.route('/add_bookmark', methods=['POST'])
def add_bookmark():
    if 'username' in session:
        username = session['username']
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookmarks (username, name, site, video, link) VALUES (?, ?, ?, ?, ?)',
                       (username, data['name'], data['site'], data['video'], data['link']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/signup')
def signup_form():
    return render_template('signup.html')

@app.route('/main1')
def main1():
    return render_template('main1.html')

@app.route('/main2')
def main2():
    return render_template('main2.html')

@app.route('/main3')
def main3():
    return render_template('main3.html')
@app.route('/admin_user')
def admin_user():
    return render_template('admin_user.html')
    
@app.route('/usersettings')
def usersettings():
    if 'username' not in session:
        return redirect(url_for('login_form'))
    return render_template('usersettings.html', username=session['username'])

@app.route('/userprofile')
def userprofile():
    if 'username' not in session:
        return redirect(url_for('login_form'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookmarks WHERE username = ?', (session['username'],))
    bookmarks = cursor.fetchall()
    conn.close()
    return render_template('userprofile.html', bookmarks=bookmarks)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    confirm_password = request.form['confirm_password'].encode('utf-8')

    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('signup_form'))
    
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        flash('Account created successfully', 'success')
    except sqlite3.IntegrityError:
        flash('Username already taken', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('login_form'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user and bcrypt.checkpw(password, user['password']):
        session['username'] = username
        flash('Logged in successfully', 'success')
        
        if user['is_admin'] == 1:
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        else:
            return redirect(url_for('main1'))  # Redirect to regular user page
        
    else:
        flash('Invalid Credentials', 'error')
        return redirect(url_for('login_form'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('login.html')

# Route to handle user settings update
@app.route('/update_settings', methods=['POST'])
def update_settings():
    if 'username' in session:
        current_username = session['username']
        new_username = request.form['username']
        new_password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update username
        if new_username and new_username != current_username:
            try:
                cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, current_username))
                # Update bookmarks to reflect new username
                cursor.execute('UPDATE bookmarks SET username = ? WHERE username = ?', (new_username, current_username))
                session['username'] = new_username
            except sqlite3.IntegrityError:
                conn.close()
                flash('Username already taken')
                return redirect(url_for('usersettings'))

        # Update password
        if new_password:
            hashed_password = bcrypt.hashpw(new_password, bcrypt.gensalt())
            cursor.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, session['username']))

        conn.commit()
        conn.close()
        flash('Settings updated successfully')
        return redirect(url_for('userprofile'))
    else:
        flash('User not logged in')
        return redirect(url_for('login_form'))
    
@app.route('/delete_account')
def delete_account():
    if 'username' in session:
        username = session['username']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete user from users table
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        
        # Delete user's bookmarks
        cursor.execute('DELETE FROM bookmarks WHERE username = ?', (username,))
        
        conn.commit()
        conn.close()
        
        # Remove user session
        session.pop('username', None)
        
        flash('Your account has been deleted successfully.')
        return redirect(url_for('main1_non_logged_in'))
    else:
        flash('User not logged in')
        return redirect(url_for('login_form'))

# Non-logged-in main pages
@app.route('/main1_non_logged_in')
def main1_non_logged_in():
    return render_template('main1.html')

@app.route('/main2_non_logged_in')
def main2_non_logged_in():
    return render_template('main2.html')

@app.route('/main3_non_logged_in')
def main3_non_logged_in():
    return render_template('main3.html')


if __name__ == '__main__':
    app.run(debug=True)
