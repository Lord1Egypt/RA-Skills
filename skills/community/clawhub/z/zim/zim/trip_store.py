"""SQLite-backed persistence for TripRecord objects.

A TripRecord is created when a TravelRequest reaches COMPLETED state.
It summarises the full journey: destination, dates, cost, booking links,
and confirmation numbers.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field


class TripRecord(BaseModel):
    """Completed trip summary created when a request reaches COMPLETED state."""

    trip_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    request_id: str
    traveler_id: str = "default"
    tenant_id: str = "default"
    destination: str = ""
    dates: dict[str, Any] = Field(default_factory=dict)
    total_cost: float = 0.0
    booking_links: list[str] = Field(default_factory=list)
    confirmation_numbers: list[str] = Field(default_factory=list)
    fulfillment_details: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class TripStore:
    """SQLite-backed store for TripRecord objects."""

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS trip_records (
        trip_id     TEXT PRIMARY KEY,
        request_id  TEXT NOT NULL,
        tenant_id   TEXT NOT NULL DEFAULT 'default',
        traveler_id TEXT NOT NULL DEFAULT 'default',
        data_json   TEXT NOT NULL,
        created_at  REAL NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_trips_request ON trip_records(request_id);
    CREATE INDEX IF NOT EXISTS idx_trips_tenant ON trip_records(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_trips_traveler ON trip_records(traveler_id);
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_trips.db")
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

    def create(self, record: TripRecord) -> str:
        """Insert a TripRecord. Returns the trip_id."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO trip_records
                       (trip_id, request_id, tenant_id, traveler_id, data_json, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        record.trip_id,
                        record.request_id,
                        record.tenant_id,
                        record.traveler_id,
                        record.model_dump_json(),
                        now,
                    ),
                )
        return record.trip_id

    def get(self, trip_id: str) -> TripRecord | None:
        """Fetch a TripRecord by trip_id."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM trip_records WHERE trip_id = ?",
                    (trip_id,),
                ).fetchone()
        if row is None:
            return None
        return TripRecord.model_validate_json(row["data_json"])

    def get_by_request(self, request_id: str) -> TripRecord | None:
        """Fetch the TripRecord created for a given request_id."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM trip_records WHERE request_id = ? LIMIT 1",
                    (request_id,),
                ).fetchone()
        if row is None:
            return None
        return TripRecord.model_validate_json(row["data_json"])

    def list_trips(
        self,
        tenant_id: Optional[str] = None,
        traveler_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TripRecord]:
        """List TripRecords with optional filters."""
        clauses: list[str] = []
        params: list[Any] = []

        if tenant_id:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if traveler_id:
            clauses.append("traveler_id = ?")
            params.append(traveler_id)
        if created_after:
            # Convert ISO string to unix timestamp for comparison
            ts = datetime.fromisoformat(created_after).timestamp()
            clauses.append("created_at >= ?")
            params.append(ts)
        if created_before:
            ts = datetime.fromisoformat(created_before).timestamp()
            clauses.append("created_at <= ?")
            params.append(ts)

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = (
            f"SELECT data_json FROM trip_records{where} "
            "ORDER BY created_at DESC LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])

        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()

        return [TripRecord.model_validate_json(r["data_json"]) for r in rows]

    def get_stats(self, tenant_id: str | None = None) -> dict[str, Any]:
        """Return aggregate trip statistics for the admin dashboard."""
        t_clause = "tenant_id = ?" if tenant_id else ""
        t_params: list[Any] = [tenant_id] if tenant_id else []
        where = (" WHERE " + t_clause) if t_clause else ""

        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    f"SELECT COUNT(*), SUM(json_extract(data_json, '$.total_cost')) "
                    f"FROM trip_records{where}",
                    t_params,
                ).fetchone()
                total = row[0] or 0
                spend = round(row[1] or 0.0, 2)

                dest_rows = conn.execute(
                    f"SELECT json_extract(data_json, '$.destination') as dest, COUNT(*) as cnt "
                    f"FROM trip_records{where} "
                    "GROUP BY dest ORDER BY cnt DESC LIMIT 5",
                    t_params,
                ).fetchall()
                top_destinations = [
                    {"destination": r[0], "count": r[1]}
                    for r in dest_rows
                    if r[0]
                ]

        return {
            "total_trips_completed": total,
            "total_spend_usd": spend,
            "top_destinations": top_destinations,
        }

    def update_fulfillment(self, trip_id: str, fulfillment_details: dict[str, Any]) -> bool:
        """Update the fulfillment_details on a TripRecord."""
        record = self.get(trip_id)
        if record is None:
            return False
        record.fulfillment_details.update(fulfillment_details)
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "UPDATE trip_records SET data_json = ? WHERE trip_id = ?",
                    (record.model_dump_json(), trip_id),
                )
        return True
