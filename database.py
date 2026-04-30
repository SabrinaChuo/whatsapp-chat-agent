import sqlite3

def init_db():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions(
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    agent TEXT,
                    last_active DATETIME DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                   id TEXT PRIMARY KEY,
                   session_id TEXT,
                   role TEXT,
                   content TEXT,
                   event_id TEXT UNIQUE,
                   FOREIGN KEY (session_id) REFERENCES sessions (id))
                   ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()