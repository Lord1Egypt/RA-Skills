"""SQLite-backed persistence for the Traveler directory.

Travelers are tenant-owned profiles that can be auto-applied to TravelRequests
to pre-populate preferences and booking info.
"""

from __future__ import annotations

import sqlite3
import threading
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

from zim.core import TravelPreferences


class Traveler(BaseModel):
    """A directory entry for a named traveler within a tenant."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    tenant_id: str = "default"
    name: str
    email: str
    phone: Optional[str] = None
    preferences: TravelPreferences = Field(default_factory=TravelPreferences)
    frequent_flyer: dict[str, str] = Field(
        default_factory=dict,
        description="Airline IATA code → FF number",
    )
    # Subset of TravelerInfo fields stored for auto-population at booking time
    passport_info: dict[str, Any] = Field(
        default_factory=dict,
        description="Pre-filled booking info (first_name, last_name, dob, passport, etc.)",
    )
    is_deleted: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class TravelerStore:
    """SQLite-backed store for Traveler directory entries."""

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS travelers (
        id          TEXT PRIMARY KEY,
        tenant_id   TEXT NOT NULL DEFAULT 'default',
        email       TEXT NOT NULL,
        is_deleted  INTEGER NOT NULL DEFAULT 0,
        data_json   TEXT NOT NULL,
        created_at  REAL NOT NULL,
        updated_at  REAL NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_travelers_tenant ON travelers(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_travelers_email ON travelers(email);
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_travelers.db")
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._lock:
            with self._connect() as conn:
                conn.executescript(self._CREATE_SQL)

    def create(self, traveler: Traveler) -> str:
        """Insert a new Traveler. Returns the traveler id."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO travelers
                       (id, tenant_id, email, is_deleted, data_json, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        traveler.id,
                        traveler.tenant_id,
                        traveler.email,
                        int(traveler.is_deleted),
                        traveler.model_dump_json(),
                        now,
                        now,
                    ),
                )
        return traveler.id

    def get(self, traveler_id: str) -> Traveler | None:
        """Fetch a Traveler by id."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM travelers WHERE id = ?",
                    (traveler_id,),
                ).fetchone()
        if row is None:
            return None
        return Traveler.model_validate_json(row["data_json"])

    def update(self, traveler: Traveler) -> bool:
        """Persist changes to a Traveler. Returns False if not found."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    """UPDATE travelers
                       SET tenant_id = ?, email = ?, is_deleted = ?, data_json = ?, updated_at = ?
                       WHERE id = ?""",
                    (
                        traveler.tenant_id,
                        traveler.email,
                        int(traveler.is_deleted),
                        traveler.model_dump_json(),
                        now,
                        traveler.id,
                    ),
                )
        return cur.rowcount > 0

    def list_travelers(
        self,
        tenant_id: Optional[str] = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Traveler]:
        """List travelers with optional tenant filter."""
        clauses: list[str] = []
        params: list[Any] = []

        if tenant_id is not None:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if not include_deleted:
            clauses.append("is_deleted = 0")

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = (
            f"SELECT data_json FROM travelers{where} "
            "ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])

        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()

        return [Traveler.model_validate_json(r["data_json"]) for r in rows]
