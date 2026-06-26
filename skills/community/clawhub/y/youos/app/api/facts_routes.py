"""Facts CRUD API routes — store and retrieve contextual facts for drafting."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.db.bootstrap import resolve_sqlite_path

router = APIRouter(prefix="/api/facts", tags=["facts"])


def _get_db_path(request: Request) -> Path:
    return resolve_sqlite_path(request.app.state.settings.database_url)


def _row_to_fact(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "type": row["type"],
        "key": row["key"],
        "fact": row["fact"],
        "tags": json.loads(row["tags"]) if row["tags"] else [],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


class FactBody(BaseModel):
    type: str  # 'contact' | 'project' | 'user_pref'
    key: str   # e.g. 'john@acme.com', 'project_alpha', 'sign_off'
    fact: str  # e.g. 'Prefers Tuesday meetings'
    tags: list[str] = []


@router.get("")
def list_facts(request: Request, type: str | None = None) -> dict:
    """Return all facts, optionally filtered by type."""
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        if type:
            rows = conn.execute(
                "SELECT * FROM memory WHERE type = ? ORDER BY type, key, updated_at DESC",
                (type,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM memory ORDER BY type, key, updated_at DESC"
            ).fetchall()
        return {"facts": [_row_to_fact(r) for r in rows]}
    finally:
        conn.close()


@router.post("")
def create_fact(body: FactBody, request: Request) -> dict:
    """Create a new fact (or update if type+key+fact already exists)."""
    if not body.type.strip() or not body.key.strip() or not body.fact.strip():
        raise HTTPException(status_code=400, detail="type, key, and fact are required")
    valid_types = {"contact", "project", "user_pref"}
    if body.type not in valid_types:
        raise HTTPException(status_code=400, detail=f"type must be one of: {', '.join(sorted(valid_types))}")

    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO memory (type, key, fact, tags, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(type, key, fact) DO UPDATE SET
                tags = excluded.tags,
                updated_at = CURRENT_TIMESTAMP
            """,
            (body.type.strip(), body.key.strip(), body.fact.strip(), json.dumps(body.tags)),
        )
        conn.commit()
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM memory WHERE type = ? AND key = ? AND fact = ?",
            (body.type.strip(), body.key.strip(), body.fact.strip()),
        ).fetchone()
        return {"status": "created", "fact": _row_to_fact(row) if row else None}
    finally:
        conn.close()


@router.delete("/{fact_id}")
def delete_fact(fact_id: int, request: Request) -> dict:
    """Delete a fact by ID."""
    db_path = _get_db_path(request)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.execute("DELETE FROM memory WHERE id = ?", (fact_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Fact not found")
        return {"status": "deleted", "id": fact_id}
    finally:
        conn.close()
