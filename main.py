import os
import sqlite3
import uuid

from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from agent import get_agent_type,generate_reply

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

app = FastAPI()

security = HTTPBearer()

class IncomingMessage(BaseModel):
    event_id: str
    user_id: str
    message: str
    

class SimulateMessage(BaseModel):
    user_id: str
    message: str

def init_db():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
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
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials 
    
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return token

def process_message_logic(payload: IncomingMessage):
    agent = get_agent_type(payload.message)
    reply_text = generate_reply(agent)

    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM sessions WHERE user_id = ?", (payload.user_id,))
        row = cursor.fetchone()

        if row:
            session_id = row[0]
            cursor.execute("UPDATE sessions SET agent=?, last_active=CURRENT_TIMESTAMP WHERE id=?", (agent, session_id))
        else:
            session_id = "sess_" + str(uuid.uuid4())[:8]
            cursor.execute("INSERT INTO sessions (id, user_id, agent) VALUES (?, ?, ?)", (session_id, payload.user_id, agent))
        
        msg_id_user = "msg_" + str(uuid.uuid4())[:8]
        cursor.execute("INSERT INTO messages (id, session_id, role, content, event_id) VALUES (?, ?, ?, ?, ?)",
                       (msg_id_user, session_id, "user", payload.message, payload.event_id))
        
        msg_id_bot = "msg_" + str(uuid.uuid4())[:8]
        cursor.execute("INSERT INTO messages (id, session_id, role, content, event_id) VALUES (?, ?, ?, ?, ?)",
                       (msg_id_bot, session_id, "assistant", reply_text, payload.event_id + "_reply"))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"status": "ignored", "reason": "Duplicated event_id detected"}
    finally:
        conn.close()

    return {"status": "success", "agent": agent, "reply": reply_text}


@app.post("/webhook/whatsapp")
def receive_whatsapp_message(payload: IncomingMessage, token: str = Depends(verify_token)):
    return process_message_logic(payload)

@app.post("/simulate")

def simulate_message(payload: SimulateMessage):
    event_id = "evt_" +str(uuid.uuid4())[:8]
    fake_payload = IncomingMessage(
        event_id = event_id,
        user_id= payload.user_id,
        message=payload.message
    )
    return process_message_logic(fake_payload)

@app.get("/sessions")
def get_sessions():
    conn = sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sessions ORDER BY last_active DESC")

    rows = cursor.fetchall()
    conn.close()

    return[dict(row) for row in rows]

@app.get("/sessions/{session_id}/messages")
def get_session_messages(session_id:str):
    conn=sqlite3.connect('chat.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY id ASC",(session_id,))
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]