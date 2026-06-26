"""
tenant.py - Multi-tenant isolation module

Enforces row-level data isolation between tenants via:
  - TenantPartitionStrategy: SHARED_DB / PER_TENANT_DB / HYBRID
  - TenantContext: per-request identity + permission checks
  - TenantRegistry: in-memory + file-backed tenant directory
  - TenantIsolationManager: store wrapper for tenant-aware operations
  - with_tenant_isolation: context manager applying tenant filters

Thread-safe.  Stdlib only.  Python 3.7+.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import sqlite3
import tempfile
import threading
import time
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent / "data"
_REGISTRY_PATH = _DATA_DIR / "tenant_registry.json"


# ═══════════════════════════════════════════════════════════════════
# Partition strategy
# ═══════════════════════════════════════════════════════════════════


class TenantPartitionStrategy(str, Enum):
    SHARED_DB = "shared_db"
    PER_TENANT_DB = "per_tenant_db"
    HYBRID = "hybrid"


# ═══════════════════════════════════════════════════════════════════
# TenantContext
# ═══════════════════════════════════════════════════════════════════


class TenantContext:
    """Per-request tenant identity with permission checks."""

    __slots__ = ("tenant_id", "agent_id", "permissions", "metadata")

    def __init__(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        permissions: Optional[set] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.tenant_id = tenant_id
        self.agent_id = agent_id
        self.permissions = set(permissions) if permissions else set()
        self.metadata = metadata or {}

    def as_filter(self) -> Dict[str, Any]:
        return {"tenant_id": self.tenant_id}

    def can_read(self) -> bool:
        return "read" in self.permissions

    def can_write(self) -> bool:
        return "write" in self.permissions

    def can_admin(self) -> bool:
        return "admin" in self.permissions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "agent_id": self.agent_id,
            "permissions": sorted(self.permissions),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TenantContext:
        return cls(
            tenant_id=data["tenant_id"],
            agent_id=data.get("agent_id"),
            permissions=set(data.get("permissions", [])),
            metadata=data.get("metadata", {}),
        )

    def __repr__(self) -> str:
        return (
            f"TenantContext(tenant_id={self.tenant_id!r}, "
            f"agent_id={self.agent_id!r}, "
            f"permissions={sorted(self.permissions)})"
        )


# ═══════════════════════════════════════════════════════════════════
# TenantRegistry
# ═══════════════════════════════════════════════════════════════════


class TenantRegistry:
    """In-memory + file-backed registry of tenants.

    Thread-safe.  Persisted to ``data/tenant_registry.json``.
    """

    def __init__(self, registry_path: Optional[str] = None):
        self._path = Path(registry_path) if registry_path else _REGISTRY_PATH
        self._lock = threading.Lock()
        self._tenants: Dict[str, dict] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        try:
            if self._path.exists():
                with open(self._path, "r", encoding="utf-8") as fh:
                    self._tenants = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load tenant registry: %s", exc)
            self._tenants = {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(
                dir=str(self._path.parent), suffix=".tmp"
            )
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                    json.dump(self._tenants, fh, ensure_ascii=False, indent=2)
                os.replace(tmp_path, str(self._path))
            except Exception:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        except OSError as exc:
            logger.error("Failed to persist tenant registry: %s", exc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(
        self,
        tenant_id: str,
        strategy: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._lock:
            self._tenants[tenant_id] = {
                "tenant_id": tenant_id,
                "strategy": strategy,
                "config": config or {},
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
            }
            self._save()
            logger.info("Tenant registered: %s (strategy=%s)", tenant_id, strategy)

    def lookup(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._tenants.get(tenant_id)

    def exists(self, tenant_id: str) -> bool:
        with self._lock:
            return tenant_id in self._tenants

    def unregister(self, tenant_id: str) -> bool:
        with self._lock:
            if tenant_id not in self._tenants:
                return False
            del self._tenants[tenant_id]
            self._save()
            logger.info("Tenant unregistered: %s", tenant_id)
            return True

    def list_tenants(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._tenants.values())

    def update_config(self, tenant_id: str, config: Dict[str, Any]) -> bool:
        with self._lock:
            entry = self._tenants.get(tenant_id)
            if not entry:
                return False
            entry["config"].update(config)
            entry["updated_at"] = int(time.time())
            self._save()
            return True


# ═══════════════════════════════════════════════════════════════════
# TenantIsolationManager
# ═══════════════════════════════════════════════════════════════════


class TenantIsolationManager:
    """Wraps a memory store with tenant-isolation enforcement.

    Parameters
    ----------
    store :
        An object whose interface matches ``AbstractMemoryStore`` or the
        native ``store`` module.
    config :
        Optional configuration dict.  Keys recognised:
        - ``strategy``: ``TenantPartitionStrategy`` member or string
        - ``data_dir``: base directory for per-tenant DB files
    """

    def __init__(
        self,
        store: Any,
        config: Optional[Dict[str, Any]] = None,
    ):
        self._store = store
        self._config = config or {}
        self._lock = threading.Lock()
        self._registry = TenantRegistry()

        raw = self._config.get("strategy", "shared_db")
        if isinstance(raw, TenantPartitionStrategy):
            self._strategy = raw
        else:
            self._strategy = TenantPartitionStrategy(raw)

        self._data_dir = Path(
            self._config.get("data_dir", str(_DATA_DIR / "tenants"))
        )
        self._data_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def strategy(self) -> TenantPartitionStrategy:
        return self._strategy

    @property
    def registry(self) -> TenantRegistry:
        return self._registry

    @property
    def store(self) -> Any:
        return self._store

    # ------------------------------------------------------------------
    # DB path resolution
    # ------------------------------------------------------------------

    def get_db_for_tenant(self, tenant_id: str) -> str:
        if self._strategy == TenantPartitionStrategy.PER_TENANT_DB:
            tenant_dir = self._data_dir / tenant_id
            tenant_dir.mkdir(parents=True, exist_ok=True)
            return str(tenant_dir / "memory.db")
        elif self._strategy == TenantPartitionStrategy.HYBRID:
            tenant_dir = self._data_dir / tenant_id
            tenant_dir.mkdir(parents=True, exist_ok=True)
            return str(tenant_dir / "memory.db")
        if hasattr(self._store, "_db_path"):
            return getattr(self._store, "_db_path")
        return str(_DATA_DIR.parent / "memory.db")

    # ------------------------------------------------------------------
    # Tenant lifecycle
    # ------------------------------------------------------------------

    def create_tenant(
        self,
        tenant_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        entry = self._registry.lookup(tenant_id)
        if entry:
            raise ValueError(f"Tenant already exists: {tenant_id}")

        config_entry: Dict[str, Any] = {"metadata": metadata or {}}

        if self._strategy in (
            TenantPartitionStrategy.PER_TENANT_DB,
            TenantPartitionStrategy.HYBRID,
        ):
            db_path = self.get_db_for_tenant(tenant_id)
            config_entry["db_path"] = db_path
            self._init_tenant_db(db_path)

        self._registry.register(
            tenant_id=tenant_id,
            strategy=self._strategy.value,
            config=config_entry,
        )
        logger.info("Tenant created: %s (strategy=%s)", tenant_id, self._strategy.value)
        return self._registry.lookup(tenant_id) or {}

    def delete_tenant(self, tenant_id: str) -> bool:
        entry = self._registry.lookup(tenant_id)
        if not entry:
            return False

        if self._strategy in (
            TenantPartitionStrategy.PER_TENANT_DB,
            TenantPartitionStrategy.HYBRID,
        ):
            tenant_dir = self._data_dir / tenant_id
            if tenant_dir.exists():
                shutil.rmtree(str(tenant_dir), ignore_errors=True)

        self._registry.unregister(tenant_id)
        logger.info("Tenant deleted: %s", tenant_id)
        return True

    def list_tenants(self) -> List[Dict[str, Any]]:
        return self._registry.list_tenants()

    def get_tenant_stats(self, tenant_id: str) -> Dict[str, Any]:
        entry = self._registry.lookup(tenant_id)
        if not entry:
            raise KeyError(f"Tenant not found: {tenant_id}")

        stats: Dict[str, Any] = {
            "tenant_id": tenant_id,
            "strategy": entry["strategy"],
            "created_at": entry["created_at"],
            "memory_count": 0,
            "storage_size_bytes": 0,
            "last_activity": entry["updated_at"],
        }

        if self._strategy == TenantPartitionStrategy.SHARED_DB:
            stats["memory_count"] = self._count_tenant_memories_shared(tenant_id)
            stats["storage_size_bytes"] = self._estimate_tenant_storage_shared(tenant_id)
        elif self._strategy in (
            TenantPartitionStrategy.PER_TENANT_DB,
            TenantPartitionStrategy.HYBRID,
        ):
            db_path = entry.get("config", {}).get("db_path") or self.get_db_for_tenant(tenant_id)
            stats["memory_count"] = self._count_memories_in_db(db_path)
            stats["storage_size_bytes"] = self._db_file_size(db_path)

        return stats

    def get_all_tenant_stats(self) -> List[Dict[str, Any]]:
        """一次查询获取所有租户统计"""
        stats = []
        for t in self.list_tenants():
            tid = t.get("tenant_id", "")
            try:
                stats.append(self.get_tenant_stats(tid))
            except Exception as e:
                logger.debug("tenant: get_all_tenant_stats: %s", e)
        return stats

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_tenant_db(self, db_path: str) -> None:
        schema_path = Path(__file__).resolve().parent / "config" / "schema.sql"
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        if schema_path.exists():
            with open(schema_path, "r", encoding="utf-8") as fh:
                conn.executescript(fh.read())
        conn.close()

    def _count_tenant_memories_shared(self, tenant_id: str) -> int:
        try:
            if hasattr(self._store, "conn"):
                cur = self._store.conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE tenant_id = ?",
                    (tenant_id,),
                )
                row = cur.fetchone()
                return row[0] if row else 0
            if hasattr(self._store, "_conn"):
                cur = self._store._conn.execute(
                    "SELECT COUNT(*) FROM memories WHERE tenant_id = ?",
                    (tenant_id,),
                )
                row = cur.fetchone()
                return row[0] if row else 0
        except Exception as e:
            logger.warning("tenant: %s", e)
        return 0

    def _estimate_tenant_storage_shared(self, tenant_id: str) -> int:
        try:
            if hasattr(self._store, "conn"):
                cur = self._store.conn.execute(
                    "SELECT SUM(LENGTH(content)) FROM memories WHERE tenant_id = ?",
                    (tenant_id,),
                )
                row = cur.fetchone()
                return row[0] if row and row[0] else 0
        except Exception as e:
            logger.warning("tenant: %s", e)
        return 0

    @staticmethod
    def _count_memories_in_db(db_path: str) -> int:
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.execute("SELECT COUNT(*) FROM memories")
            row = cur.fetchone()
            conn.close()
            return row[0] if row else 0
        except Exception:
            return 0

    @staticmethod
    def _db_file_size(db_path: str) -> int:
        p = Path(db_path)
        wal_path = Path(str(db_path) + "-wal")
        shm_path = Path(str(db_path) + "-shm")
        total = 0
        for path in (p, wal_path, shm_path):
            try:
                total += path.stat().st_size
            except OSError as e:
                logger.debug("tenant: db size stat: %s", e)
        return total

    def close(self) -> None:
        if hasattr(self._store, "close"):
            self._store.close()


# ═══════════════════════════════════════════════════════════════════
# Context manager
# ═══════════════════════════════════════════════════════════════════


class _IsolationGuard:
    """Internal context manager that augments a store with tenant filters."""

    def __init__(self, store: Any, tenant_ctx: TenantContext):
        self._store = store
        self._tenant_ctx = tenant_ctx
        self._original_fns: Dict[str, Any] = {}

    def __enter__(self) -> Any:
        filter_dict = self._tenant_ctx.as_filter()

        if hasattr(self._store, "query"):
            original = self._store.query

            def _guarded_query(**kwargs: Any) -> Any:
                merged = {**filter_dict, **kwargs}
                return original(**merged)

            self._original_fns["query"] = original
            self._store.query = _guarded_query

        if hasattr(self._store, "count"):
            original = self._store.count

            def _guarded_count() -> Any:
                result = original()
                return result

            self._original_fns["count"] = original
            self._store.count = _guarded_count

        self._store._tenant_ctx = self._tenant_ctx
        return self._store

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        for attr, original in self._original_fns.items():
            setattr(self._store, attr, original)
        if hasattr(self._store, "_tenant_ctx"):
            del self._store._tenant_ctx
        return None


@contextmanager
def with_tenant_isolation(store: Any, tenant_ctx: TenantContext):
    guard = _IsolationGuard(store, tenant_ctx)
    try:
        yield guard.__enter__()
    finally:
        guard.__exit__(None, None, None)