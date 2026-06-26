"""SQLite-backed persistence for admin-managed travel policies.

Wraps the core Policy model with tenant ownership, naming, and lifecycle fields.
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

from zim.core import Policy


class StoredPolicy(BaseModel):
    """A named, tenant-owned travel policy stored in the admin plane."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    tenant_id: str = "default"
    name: str
    is_default: bool = False
    is_deleted: bool = False
    policy: Policy = Field(default_factory=Policy)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class PolicyStore:
    """SQLite-backed store for StoredPolicy objects."""

    _CREATE_SQL = """
    CREATE TABLE IF NOT EXISTS stored_policies (
        id          TEXT PRIMARY KEY,
        tenant_id   TEXT NOT NULL DEFAULT 'default',
        name        TEXT NOT NULL,
        is_default  INTEGER NOT NULL DEFAULT 0,
        is_deleted  INTEGER NOT NULL DEFAULT 0,
        data_json   TEXT NOT NULL,
        created_at  REAL NOT NULL,
        updated_at  REAL NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_policies_tenant ON stored_policies(tenant_id);
    CREATE INDEX IF NOT EXISTS idx_policies_default ON stored_policies(is_default);
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = str(db_path or "/tmp/zim_policies.db")
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

    def create(self, policy: StoredPolicy) -> str:
        """Insert a new StoredPolicy. Returns the policy id."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """INSERT INTO stored_policies
                       (id, tenant_id, name, is_default, is_deleted, data_json, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        policy.id,
                        policy.tenant_id,
                        policy.name,
                        int(policy.is_default),
                        int(policy.is_deleted),
                        policy.model_dump_json(),
                        now,
                        now,
                    ),
                )
        return policy.id

    def get(self, policy_id: str) -> StoredPolicy | None:
        """Fetch a StoredPolicy by id."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT data_json FROM stored_policies WHERE id = ?",
                    (policy_id,),
                ).fetchone()
        if row is None:
            return None
        return StoredPolicy.model_validate_json(row["data_json"])

    def update(self, policy: StoredPolicy) -> bool:
        """Persist changes to a StoredPolicy. Returns False if not found."""
        now = time.time()
        with self._lock:
            with self._connect() as conn:
                cur = conn.execute(
                    """UPDATE stored_policies
                       SET tenant_id = ?, name = ?, is_default = ?, is_deleted = ?,
                           data_json = ?, updated_at = ?
                       WHERE id = ?""",
                    (
                        policy.tenant_id,
                        policy.name,
                        int(policy.is_default),
                        int(policy.is_deleted),
                        policy.model_dump_json(),
                        now,
                        policy.id,
                    ),
                )
        return cur.rowcount > 0

    def soft_delete(self, policy_id: str) -> bool:
        """Mark a policy as deleted. Returns False if not found."""
        policy = self.get(policy_id)
        if policy is None:
            return False
        policy.is_deleted = True
        return self.update(policy)

    def get_default_for_tenant(self, tenant_id: str) -> StoredPolicy | None:
        """Return the default (non-deleted) policy for a tenant, if any."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    """SELECT data_json FROM stored_policies
                       WHERE tenant_id = ? AND is_default = 1 AND is_deleted = 0
                       LIMIT 1""",
                    (tenant_id,),
                ).fetchone()
        if row is None:
            return None
        return StoredPolicy.model_validate_json(row["data_json"])

    def list_policies(
        self,
        tenant_id: Optional[str] = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[StoredPolicy]:
        """List policies with optional tenant filter."""
        clauses: list[str] = []
        params: list[Any] = []

        if tenant_id is not None:
            clauses.append("tenant_id = ?")
            params.append(tenant_id)
        if not include_deleted:
            clauses.append("is_deleted = 0")

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = (
            f"SELECT data_json FROM stored_policies{where} "
            "ORDER BY updated_at DESC LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])

        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(sql, params).fetchall()

        return [StoredPolicy.model_validate_json(r["data_json"]) for r in rows]
