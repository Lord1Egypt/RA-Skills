"""Sender profiles API routes."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.core.facts_extractor import extract_and_save
from app.db.bootstrap import resolve_sqlite_path

router = APIRouter(prefix="/senders", tags=["senders"])


def _get_db_path(request: Request) -> Path:
    return resolve_sqlite_path(request.app.state.settings.database_url)


def _row_to_profile(row: sqlite3.Row) -> dict:
    return {
        "email": row["email"],
        "display_name": row["display_name"],
        "domain": row["domain"],
        "company": row["company"],
        "sender_type": row["sender_type"],
        "relationship_note": row["relationship_note"],
        "reply_count": row["reply_count"],
        "avg_reply_words": row["avg_reply_words"],
        "first_seen": row["first_seen"],
        "last_seen": row["last_seen"],
        "topics": json.loads(row["topics_json"]) if row["topics_json"] else [],
    }


def _infer_profile_from_corpus(conn: sqlite3.Connection, email: str) -> dict | None:
    """Build a lightweight profile from reply_pairs without a stored sender_profile."""
    from app.core.sender import classify_sender, extract_domain

    rows = conn.execute(
        "SELECT inbound_author, reply_text, paired_at FROM reply_pairs WHERE inbound_author LIKE ? ORDER BY paired_at DESC",
        (f"%{email}%",),
    ).fetchall()
    if not rows:
        return None

    reply_count = len(rows)
    word_counts = [len((r["reply_text"] or "").split()) for r in rows]
    avg_words = round(sum(word_counts) / len(word_counts), 1) if word_counts else None
    timestamps = [r["paired_at"] for r in rows if r["paired_at"]]
    first_seen = min(timestamps) if timestamps else None
    last_seen = max(timestamps) if timestamps else None

    author_str = rows[0]["inbound_author"] or email
    domain = extract_domain(author_str)
    company = _company_from_domain(domain) if domain else None

    return {
        "email": email,
        "display_name": _extract_display_name(author_str),
        "domain": domain,
        "company": company,
        "sender_type": classify_sender(author_str),
        "relationship_note": None,
        "reply_count": reply_count,
        "avg_reply_words": avg_words,
        "first_seen": first_seen,
        "last_seen": last_seen,
        "topics": [],
    }


def _extract_display_name(author: str) -> str | None:
    """Extract display name from 'Display Name <email>' format."""
    if "<" in author:
        name = author.split("<")[0].strip().strip('"').strip("'")
        return name if name else None
    return None


def _company_from_domain(domain: str) -> str | None:
    """Infer company name from domain."""
    from app.core.sender import _PERSONAL_DOMAINS

    if not domain or domain in _PERSONAL_DOMAINS:
        return None
    parts = domain.split(".")
    if len(parts) >= 2:
        name = parts[-2]
        return name.replace("-", " ").replace("_", " ").title()
    return None


@router.get("/lookup")
def sender_lookup(email: str, request: Request) -> dict:
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute("SELECT * FROM sender_profiles WHERE email = ?", (email.lower(),)).fetchone()
        if row:
            return {"found": True, "profile": _row_to_profile(row)}
        # Try inferring from corpus
        inferred = _infer_profile_from_corpus(conn, email.lower())
        if inferred:
            return {"found": True, "inferred": True, "profile": inferred}
        return {"found": False, "profile": None}
    finally:
        conn.close()


@router.get("/search")
def sender_search(q: str, request: Request) -> dict:
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT * FROM sender_profiles WHERE email LIKE ? OR company LIKE ? LIMIT 5",
            (f"%{q}%", f"%{q}%"),
        ).fetchall()
        return {"results": [_row_to_profile(r) for r in rows]}
    finally:
        conn.close()


class NoteBody(BaseModel):
    relationship_note: str


@router.post("/{email}/note")
def update_note(email: str, body: NoteBody, request: Request) -> dict:
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute(
            "UPDATE sender_profiles SET relationship_note = ?, updated_at = CURRENT_TIMESTAMP WHERE email = ?",
            (body.relationship_note, email.lower()),
        )
        conn.commit()
        if cur.rowcount == 0:
            # Create a minimal profile if it doesn't exist
            conn.execute(
                "INSERT INTO sender_profiles (email, relationship_note) VALUES (?, ?)",
                (email.lower(), body.relationship_note),
            )
            conn.commit()
        # Extract and auto-save facts from the relationship note
        extracted_facts: list[dict] = []
        try:
            extracted_facts = extract_and_save(body.relationship_note, db_path, sender_email=email.lower())
        except Exception:
            pass

        return {"status": "updated", "email": email.lower(), "extracted_facts": extracted_facts}
    finally:
        conn.close()


@router.get("/{email}/history")
def sender_history(email: str, request: Request) -> dict:
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT inbound_text, reply_text, paired_at FROM reply_pairs WHERE inbound_author LIKE ? ORDER BY paired_at DESC LIMIT 5",
            (f"%{email}%",),
        ).fetchall()
        history = [
            {
                "inbound_snippet": (r["inbound_text"] or "")[:200],
                "reply_snippet": (r["reply_text"] or "")[:200],
                "paired_at": r["paired_at"],
            }
            for r in rows
        ]
        return {"email": email, "history": history}
    finally:
        conn.close()
