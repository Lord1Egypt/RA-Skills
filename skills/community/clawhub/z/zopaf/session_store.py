"""SQLite-backed session persistence for NegotiationCoach instances.

Serializes coach state to JSON so sessions survive server restarts.
"""
from __future__ import annotations

import json
import os
import sqlite3
from typing import Any

from coach import NegotiationCoach

# Railway volumes mount at /data by default
DB_PATH = os.environ.get("SESSION_DB_PATH", "/data/sessions.db" if os.path.isdir("/data") else "sessions.db")


def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            unlocked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def _serialize_messages(messages: list[dict]) -> list[dict]:
    """Convert Anthropic API message objects to JSON-serializable dicts."""
    serialized = []
    for msg in messages:
        if msg["role"] == "assistant" and isinstance(msg.get("content"), list):
            # Content blocks from Anthropic API — convert to dicts
            blocks = []
            for block in msg["content"]:
                if hasattr(block, "type"):
                    if block.type == "text":
                        blocks.append({"type": "text", "text": block.text})
                    elif block.type == "tool_use":
                        blocks.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input,
                        })
                elif isinstance(block, dict):
                    blocks.append(block)
            serialized.append({"role": "assistant", "content": blocks})
        else:
            serialized.append(msg)
    return serialized


def _coach_to_dict(coach: NegotiationCoach) -> dict:
    """Serialize coach state to a JSON-compatible dict."""
    return {
        "messages": _serialize_messages(coach.messages),
        "issues": coach.issues,
        "elicitation_choices": coach.elicitation_choices,
        "learned_weights": coach.learned_weights,
        "pending_elicitation": coach.pending_elicitation,
        "batna": coach.batna,
        "chat_history": coach.chat_history,
        "counterpart_weights": coach.counterpart_weights,
        "last_offers": coach.last_offers,
        "negotiation_round": coach.negotiation_round,
    }


def _dict_to_coach(data: dict) -> NegotiationCoach:
    """Restore coach state from a dict."""
    coach = NegotiationCoach()
    coach.messages = data.get("messages", [])
    coach.issues = data.get("issues", [])
    coach.elicitation_choices = data.get("elicitation_choices", [])
    coach.learned_weights = data.get("learned_weights", {})
    coach.pending_elicitation = data.get("pending_elicitation")
    coach.batna = data.get("batna")
    coach.chat_history = data.get("chat_history", [])
    coach.counterpart_weights = data.get("counterpart_weights", {})
    coach.last_offers = data.get("last_offers", [])
    coach.negotiation_round = data.get("negotiation_round", 0)
    return coach


def save_session(session_id: str, coach: NegotiationCoach) -> None:
    """Save coach state to SQLite."""
    db = _get_db()
    state = json.dumps(_coach_to_dict(coach))
    db.execute(
        """INSERT INTO sessions (session_id, state, updated_at)
           VALUES (?, ?, CURRENT_TIMESTAMP)
           ON CONFLICT(session_id)
           DO UPDATE SET state = ?, updated_at = CURRENT_TIMESTAMP""",
        (session_id, state, state),
    )
    db.commit()
    db.close()


def load_session(session_id: str) -> NegotiationCoach | None:
    """Load coach state from SQLite. Returns None if not found."""
    db = _get_db()
    row = db.execute(
        "SELECT state FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    db.close()
    if row is None:
        return None
    data = json.loads(row[0])
    return _dict_to_coach(data)


def session_exists(session_id: str) -> bool:
    db = _get_db()
    row = db.execute(
        "SELECT 1 FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    db.close()
    return row is not None


def set_unlocked(session_id: str) -> None:
    db = _get_db()
    db.execute(
        "UPDATE sessions SET unlocked = 1 WHERE session_id = ?", (session_id,)
    )
    # Also insert if session doesn't exist yet (edge case: server redeployed)
    if db.execute("SELECT changes()").fetchone()[0] == 0:
        db.execute(
            "INSERT OR IGNORE INTO sessions (session_id, state, unlocked) VALUES (?, '{}', 1)",
            (session_id,),
        )
    db.commit()
    db.close()


def is_unlocked(session_id: str) -> bool:
    db = _get_db()
    row = db.execute(
        "SELECT unlocked FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    db.close()
    return row is not None and row[0] == 1
