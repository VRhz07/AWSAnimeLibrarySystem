import sqlite3
import bcrypt

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')

    # Add is_admin column if it doesn't exist (to handle existing databases)
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        # Column already exists, do nothing
        pass

    # Insert admin user if not already present
    hashed_password = bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)
    ''', ('admin', hashed_password, 1))  # Setting admin user with is_admin = 1
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database setup completed successfully.")
