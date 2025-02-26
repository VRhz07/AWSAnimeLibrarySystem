import sqlite3

def promote_to_admin(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_admin = ? WHERE username = ?', (True, username))
    conn.commit()
    conn.close()

# Replace 'admin_username' with the actual username you want to promote to admin
promote_to_admin('harvz')
