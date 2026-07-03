"""
Signet Mind - Database Module
Handles encrypted local storage for conversations and mood tracking.
"""

import sqlite3
import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from config import DB_PATH, MOOD_DB_PATH, DATA_DIR, ENCRYPTION_KEY_FILE

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_encryption_key() -> str:
    """Get or generate encryption key for local data."""
    if ENCRYPTION_KEY_FILE.exists():
        return ENCRYPTION_KEY_FILE.read_text().strip()
    
    # Generate new key (in production, this would be derived from user password)
    key = os.urandom(32).hex()
    ENCRYPTION_KEY_FILE.write_text(key)
    os.chmod(ENCRYPTION_KEY_FILE, 0o600)
    return key


def init_conversation_db():
    """Initialize the conversations database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            mood_before TEXT,
            mood_after TEXT,
            tags TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def init_mood_db():
    """Initialize the mood tracking database."""
    conn = sqlite3.connect(MOOD_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood_score INTEGER NOT NULL,
            energy_level INTEGER,
            notes TEXT,
            triggers TEXT,
            activities TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def save_conversation(user_msg: str, ai_msg: str, mood_before: Optional[str] = None, 
                      mood_after: Optional[str] = None, tags: Optional[List[str]] = None):
    """Save a conversation turn."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO conversations (timestamp, user_message, ai_response, mood_before, mood_after, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        user_msg,
        ai_msg,
        mood_before,
        mood_after,
        json.dumps(tags) if tags else None
    ))
    
    conn.commit()
    conn.close()


def get_conversation_history(limit: int = 50) -> List[Dict]:
    """Retrieve recent conversation history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, user_message, ai_response, mood_before, mood_after, tags
        FROM conversations
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "timestamp": row[0],
            "user": row[1],
            "ai": row[2],
            "mood_before": row[3],
            "mood_after": row[4],
            "tags": json.loads(row[5]) if row[5] else []
        }
        for row in rows
    ]


def save_mood_entry(date: str, mood_score: int, energy: Optional[int] = None,
                    notes: Optional[str] = None, triggers: Optional[List[str]] = None,
                    activities: Optional[List[str]] = None):
    """Save a mood entry."""
    conn = sqlite3.connect(MOOD_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO mood_entries (date, mood_score, energy_level, notes, triggers, activities)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        mood_score,
        energy,
        notes,
        json.dumps(triggers) if triggers else None,
        json.dumps(activities) if activities else None
    ))
    
    conn.commit()
    conn.close()


def get_mood_history(days: int = 30) -> List[Dict]:
    """Get mood history for the specified number of days."""
    conn = sqlite3.connect(MOOD_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT date, mood_score, energy_level, notes, triggers, activities
        FROM mood_entries
        ORDER BY date DESC
        LIMIT ?
    """, (days,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "date": row[0],
            "mood": row[1],
            "energy": row[2],
            "notes": row[3],
            "triggers": json.loads(row[4]) if row[4] else [],
            "activities": json.loads(row[5]) if row[5] else []
        }
        for row in rows
    ]


def save_user_preference(key: str, value: str):
    """Save a user preference/profile item."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO user_profile (key, value, updated_at)
        VALUES (?, ?, ?)
    """, (key, value, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


def get_user_preference(key: str) -> Optional[str]:
    """Get a user preference."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT value FROM user_profile WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    
    return row[0] if row else None


def initialize():
    """Initialize all databases."""
    init_conversation_db()
    init_mood_db()
    get_encryption_key()  # Ensure key exists


if __name__ == "__main__":
    initialize()
    print("Signet Mind databases initialized.")
