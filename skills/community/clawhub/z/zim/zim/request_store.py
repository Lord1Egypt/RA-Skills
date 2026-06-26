"""SQLite-backed persistence for TravelRequest objects.

Thread-safe, single-process. Follows the same pattern as state_store.py.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

from zim.request_state import RequestState, TravelRequest, InvalidTransitionError


class _Encoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class RequestStore:
    """SQLite-backed store for TravelRequest objects.

    Args:
        db_path: Path to SQLite file. Defaults to /tmp/zim_requests.db.
    """

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS travel_requests (
        id          TEXT PRIMARY KEY,
        data_json   TEXT NOT NULL,
        state       TEXT NOT NULL,
        tenant_id   TEXT NOT NULL DEFAULT 'default',
        traveler_id TEXT NOT NULL DEFAULT 'default',
        created_at  REAL NOT NULL,
        updated_at  REAL NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_requests_state ON travel_requests(state);
    CREATE INDEX IF NOT EXISTS idx_requests_tenant ON travel_requests(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_requests_traveler ON travel_requests(traveler_id);
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_requests.db")
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

    def create(self, request: TravelRequest) -> str:
        """Insert a new TravelRequest. Returns the request id."""
        now = time.time()
        data = request.model_dump(mode="json")
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO travel_requests
                       (id, data_json, state, tenant_id, traveler_id, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        request.id,
                        json.dumps(data, cls=_Encoder),
                        request.state.value,
                        request.tenant_id,
                        request.traveler_id,
                        now,
                        now,
                    ),
                )
        return request.id

    def get(self, request_id: str) -> TravelRequest | None:
        """Fetch a TravelRequest by id."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM travel_requests WHERE id = ?",
                    (request_id,),
                ).fetchone()
        if row is None:
            return None
        return TravelRequest.model_validate(json.loads(row["data_json"]))

    def update(self, request: TravelRequest) -> bool:
        """Persist the current state of a TravelRequest. Returns False if not found."""
        now = time.time()
        data = request.model_dump(mode="json")
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    """UPDATE travel_requests
                       SET data_json = ?, state = ?, updated_at = ?
                       WHERE id = ?""",
                    (
                        json.dumps(data, cls=_Encoder),
                        request.state.value,
                        now,
                        request.id,
                    ),
                )
        return cur.rowcount > 0

    def transition(
        self, request_id: str, new_state: RequestState
    ) -> TravelRequest:
        """Atomically transition a request to a new state.

        Raises:
            KeyError: If request not found.
            InvalidTransitionError: If transition is invalid.
        """
        req = self.get(request_id)
        if req is None:
            raise KeyError(f"Request {request_id} not found")
        req.transition_to(new_state)
        self.update(req)
        return req

    def get_stats(
        self,
        tenant_id: str | None = None,
        since_7d: float | None = None,
        since_30d: float | None = None,
    ) -> dict[str, Any]:
        """Return aggregate statistics for the admin dashboard."""
        t_clause = "tenant_id = ?" if tenant_id else ""
        t_params = [tenant_id] if tenant_id else []

        def _where(*extra: str) -> tuple[str, list[Any]]:
            parts = [c for c in [t_clause, *extra] if c]
            return (" WHERE " + " AND ".join(parts)) if parts else "", list(t_params)

        with self._lock:
            with self._connect() as conn:
                # Total requests
                w, p = _where()
                total = conn.execute(
                    f"SELECT COUNT(*) FROM travel_requests{w}", p
                ).fetchone()[0]

                # Requests by state
                w, p = _where()
                rows = conn.execute(
                    f"SELECT state, COUNT(*) FROM travel_requests{w} GROUP BY state", p
                ).fetchall()
                by_state = {r[0]: r[1] for r in rows}

                # Last 7 days
                last_7 = 0
                if since_7d is not None:
                    w, p = _where(f"created_at >= {since_7d}")
                    last_7 = conn.execute(
                        f"SELECT COUNT(*) FROM travel_requests{w}", p
                    ).fetchone()[0]

                # Last 30 days
                last_30 = 0
                if since_30d is not None:
                    w, p = _where(f"created_at >= {since_30d}")
                    last_30 = conn.execute(
                        f"SELECT COUNT(*) FROM travel_requests{w}", p
                    ).fetchone()[0]

        return {
            "total_requests": total,
            "requests_by_state": by_state,
            "requests_last_7_days": last_7,
            "requests_last_30_days": last_30,
        }

    def list_requests(
        self,
        tenant_id: str | None = None,
        traveler_id: str | None = None,
        state: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[TravelRequest]:
        """List requests with optional filters."""
        clauses: list[str] = []
        params: list[Any] = []

        if tenant_id:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if traveler_id:
            clauses.append("traveler_id = ?")
            params.append(traveler_id)
        if state:
            clauses.append("state = ?")
            params.append(state)

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"SELECT data_json FROM travel_requests{where} ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()

        return [TravelRequest.model_validate(json.loads(r["data_json"])) for r in rows]
