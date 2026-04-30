import sqlite3

conn  = sqlite3.connect('chat.db')
cursor = conn.cursor()

print("Checking sessions table")
cursor.execute("SELECT * FROM sessions")
print(cursor.fetchall())

print("Checking messages table")
cursor.execute("SELECT * FROM messages")
print(cursor.fetchall())

conn.close()