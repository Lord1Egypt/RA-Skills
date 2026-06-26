"""
Unified database connection layer for all CH Skills.

Preferred PostgreSQL setup:
    export ALPHA_DB_BACKEND=postgresql
    export ALPHA_PG_URL="postgresql://alpha_user:***@/alpha_data?host=/tmp"

TCP fallback:
    export ALPHA_PG_URL="postgresql://alpha_user:***@localhost:5432/alpha_data"

Offline fallback:
    export ALPHA_DB_BACKEND=sqlite
    export ALPHA_SQLITE_DIR="~/AlphaData/db"
"""

from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from enum import Enum
from typing import Any, Generator
from urllib.parse import urlsplit, urlunsplit

# ---------------------------------------------------------------------------
# Lazy imports (avoid import-time side effects)
# ---------------------------------------------------------------------------
try:
    from psycopg2 import pool as _pg_pool_mod
    from psycopg2.extras import RealDictCursor as _RealDictCursor
except ImportError:  # pragma: no cover
    _pg_pool_mod = None
    _RealDictCursor = None


class Backend(Enum):
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"


# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
DEFAULT_PG_URL = "postgresql://alpha_user:alpha_pass@/alpha_data?host=/tmp"


def _read_backend() -> Backend:
    raw = os.getenv("ALPHA_DB_BACKEND", "postgresql").strip().lower()
    try:
        return Backend(raw)
    except ValueError as exc:
        allowed = ", ".join(backend.value for backend in Backend)
        raise RuntimeError(
            f"Invalid ALPHA_DB_BACKEND={raw!r}; expected one of: {allowed}"
        ) from exc


def _read_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {raw!r}") from exc
    if value <= 0:
        raise RuntimeError(f"{name} must be positive, got {value}")
    return value


def _read_pg_url() -> str:
    # ALPHA_PG_URL is the canonical CH Skills variable. DATABASE_URL is accepted
    # only as a compatibility fallback for generic agent/scheduler runtimes.
    return (
        os.getenv("ALPHA_PG_URL")
        or os.getenv("DATABASE_URL")
        or DEFAULT_PG_URL
    )


BACKEND = _read_backend()
PG_URL = _read_pg_url()
SQLITE_DIR = os.path.expanduser(os.getenv("ALPHA_SQLITE_DIR", "."))
PG_CONNECT_TIMEOUT = _read_int_env("ALPHA_PG_CONNECT_TIMEOUT", 5)
PG_POOL_MAX = _read_int_env("ALPHA_PG_POOL_MAX", 8)


# ---------------------------------------------------------------------------
# PostgreSQL connection pool (module-level singleton)
# ---------------------------------------------------------------------------
_pg_pool = None
_pool_lock = threading.Lock()


def mask_dsn(dsn: str | None = None) -> str:
    """Return a display-safe DSN with the password removed."""
    value = dsn or PG_URL
    try:
        parts = urlsplit(value)
    except ValueError:
        return "<unparseable-dsn>"

    if not parts.password:
        return value

    user = parts.username or ""
    host = parts.hostname or ""
    port = f":{parts.port}" if parts.port else ""
    netloc = f"{user}:***@{host}{port}"
    return urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


def config_snapshot() -> dict[str, Any]:
    """Return non-secret connection settings for diagnostics."""
    return {
        "backend": BACKEND.value,
        "pg_url": mask_dsn(PG_URL) if BACKEND == Backend.POSTGRESQL else None,
        "sqlite_dir": SQLITE_DIR if BACKEND == Backend.SQLITE else None,
        "pg_connect_timeout": PG_CONNECT_TIMEOUT if BACKEND == Backend.POSTGRESQL else None,
        "pg_pool_max": PG_POOL_MAX if BACKEND == Backend.POSTGRESQL else None,
        "pg_url_source": (
            "ALPHA_PG_URL"
            if os.getenv("ALPHA_PG_URL")
            else "DATABASE_URL"
            if os.getenv("DATABASE_URL")
            else "default"
        )
        if BACKEND == Backend.POSTGRESQL
        else None,
    }


def _get_pool() -> Any:
    """Return (creating lazily) the module-level ThreadedConnectionPool."""
    global _pg_pool
    if _pg_pool is not None:
        return _pg_pool
    with _pool_lock:
        if _pg_pool is not None:
            return _pg_pool
        if _pg_pool_mod is None:
            raise RuntimeError(
                "psycopg2 is required for PostgreSQL backend. "
                "Install psycopg2-binary or switch ALPHA_DB_BACKEND=sqlite."
            )
        try:
            _pg_pool = _pg_pool_mod.ThreadedConnectionPool(
                minconn=1,
                maxconn=PG_POOL_MAX,
                dsn=PG_URL,
                connect_timeout=PG_CONNECT_TIMEOUT,
            )
        except Exception as exc:
            raise RuntimeError(
                "Failed to open PostgreSQL pool. "
                f"dsn={mask_dsn(PG_URL)}, timeout={PG_CONNECT_TIMEOUT}s. "
                "Check ALPHA_PG_URL, server status, and init_alpha_data.sql."
            ) from exc
        return _pg_pool


def close_pool() -> None:
    """Close all connections in the pool and reset the singleton.

    Call this at script shutdown or between test cases to release
    PostgreSQL connections immediately.
    """
    global _pg_pool
    with _pool_lock:
        if _pg_pool is not None:
            _pg_pool.closeall()
            _pg_pool = None


# ---------------------------------------------------------------------------
# Connection factory
# ---------------------------------------------------------------------------
@contextmanager
def get_connection(db_path: str | None = None) -> Generator[Any, None, None]:
    """
    Yield a DB connection (sqlite3.Connection or psycopg2 connection).
    Caller receives the connection; commit/rollback is handled on exit.
    """
    if BACKEND == Backend.SQLITE:
        import sqlite3

        path = os.path.expanduser(db_path or os.path.join(SQLITE_DIR, "alpha.db"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    else:
        conn = _get_pool().getconn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            _get_pool().putconn(conn)


# ---------------------------------------------------------------------------
# SQL dialect helpers
# ---------------------------------------------------------------------------
def placeholder() -> str:
    """Return the parameter placeholder for the current backend."""
    return "?" if BACKEND == Backend.SQLITE else "%s"


def adapt_sql(sql: str) -> str:
    """Convert SQLite-flavoured SQL to PostgreSQL dialect.

    Rules applied (idempotent for SQLite):
      1. '?' placeholders -> '%s'
      2. sqlite_master    -> information_schema.tables
      3. ON CONFLICT(...) -> PostgreSQL compatible (same syntax, no change needed)
      4. PRAGMA           -> no-op (returned as empty SELECT)
    """
    if BACKEND == Backend.SQLITE:
        return sql

    # 1. positional placeholders
    sql = sql.replace("?", "%s")

    # 2. sqlite_master → information_schema.tables
    sql = sql.replace(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name =",
        "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name =",
    )

    # 3. PRAGMA → no-op
    if sql.strip().upper().startswith("PRAGMA"):
        return "SELECT 1 WHERE false"

    return sql


def table_exists(conn: Any, table_name: str) -> bool:
    """Return True if *table_name* exists in the current DB."""
    if BACKEND == Backend.SQLITE:
        cur = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (table_name,),
        )
        return cur.fetchone() is not None
    else:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
            (table_name,),
        )
        return cur.fetchone() is not None


# ---------------------------------------------------------------------------
# Row helpers (produce plain dict from any row type)
# ---------------------------------------------------------------------------
def row_to_dict(row: Any) -> dict[str, Any]:
    """Normalise sqlite3.Row / RealDictRow / dict → plain dict."""
    return dict(row)


def rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    """Bulk version of row_to_dict."""
    return [dict(r) for r in rows]


def ping(required_tables: list[str] | None = None) -> dict[str, Any]:
    """Run a lightweight connectivity check and optional table existence check."""
    info = {"config": config_snapshot(), "ok": True, "tables": {}}
    with get_connection() as conn:
        if BACKEND == Backend.SQLITE:
            cur = conn.execute("SELECT 1")
            info["select_1"] = cur.fetchone()[0]
        else:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    current_database() AS database,
                    current_user AS user_name,
                    inet_server_addr()::text AS server_addr,
                    inet_server_port() AS server_port
                """
            )
            row = cur.fetchone()
            info["server"] = {
                "database": row[0],
                "user": row[1],
                "server_addr": row[2],
                "server_port": row[3],
            }

        for table in required_tables or []:
            info["tables"][table] = table_exists(conn, table)

    missing = [name for name, exists in info["tables"].items() if not exists]
    if missing:
        info["ok"] = False
        info["missing_tables"] = missing
    return info
