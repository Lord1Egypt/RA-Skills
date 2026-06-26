"""v8.6 — 存储后端抽象层

支持 SQLite（默认）和 PostgreSQL 两种后端，通过环境变量切换:
    MEMORY_STORE_BACKEND=sqlite  (默认)
    MEMORY_STORE_BACKEND=postgres
"""

from __future__ import annotations

from .base import AbstractMemoryStore

# Lazy imports to avoid circular dependency with store.py
def __getattr__(name):
    if name == "SqliteMemoryStore":
        from ..store import MemoryStore
        return MemoryStore
    if name == "PostgresMemoryStore":
        try:
            from .pg_store import PostgresMemoryStore
            return PostgresMemoryStore
        except ImportError:
            return None
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["AbstractMemoryStore", "SqliteMemoryStore", "PostgresMemoryStore"]
