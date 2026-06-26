"""SQLite-backed persistence for Tenant objects."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Optional

from zim.tenant import Tenant


class TenantStore:
    """SQLite-backed store for Tenant records."""

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS tenants (
        id          TEXT PRIMARY KEY,
        name        TEXT NOT NULL,
        domain      TEXT NOT NULL DEFAULT '',
        is_deleted  INTEGER NOT NULL DEFAULT 0,
        data_json   TEXT NOT NULL,
        created_at  REAL NOT NULL,
        updated_at  REAL NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_tenants_domain ON tenants(domain);
    CREATE INDEX IF NOT EXISTS idx_tenants_deleted ON tenants(is_deleted);
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_tenants.db")
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

    def create(self, tenant: Tenant) -> str:
        """Insert a new Tenant. Returns the tenant id."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO tenants
                       (id, name, domain, is_deleted, data_json, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        tenant.id,
                        tenant.name,
                        tenant.domain,
                        int(tenant.is_deleted),
                        tenant.model_dump_json(),
                        now,
                        now,
                    ),
                )
        return tenant.id

    def get(self, tenant_id: str) -> Tenant | None:
        """Fetch a Tenant by id (including soft-deleted)."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM tenants WHERE id = ?",
                    (tenant_id,),
                ).fetchone()
        if row is None:
            return None
        return Tenant.model_validate_json(row["data_json"])

    def update(self, tenant: Tenant) -> bool:
        """Persist changes to a Tenant. Returns False if not found."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    """UPDATE tenants
                       SET name = ?, domain = ?, is_deleted = ?, data_json = ?, updated_at = ?
                       WHERE id = ?""",
                    (
                        tenant.name,
                        tenant.domain,
                        int(tenant.is_deleted),
                        tenant.model_dump_json(),
                        now,
                        tenant.id,
                    ),
                )
        return cur.rowcount > 0

    def soft_delete(self, tenant_id: str) -> bool:
        """Mark a tenant as deleted. Returns False if not found."""
        tenant = self.get(tenant_id)
        if tenant is None:
            return False
        tenant.is_deleted = True
        return self.update(tenant)

    def list_tenants(
        self,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Tenant]:
        """List tenants, optionally including soft-deleted ones."""
        clauses: list[str] = []
        params: list[Any] = []

        if not include_deleted:
            clauses.append("is_deleted = 0")

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = (
            f"SELECT data_json FROM tenants{where} "
            "ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])

        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()

        return [Tenant.model_validate_json(r["data_json"]) for r in rows]
