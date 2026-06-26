"""storage/sqlite_store.py — DEPRECATED: use MemoryStore instead.

This module has been archived. SqliteMemoryStore is now an alias
for MemoryStore for backward compatibility.
Will be removed in v13.0.0.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "storage.sqlite_store is deprecated since v12.0.0, "
    "use agent_memory.store.MemoryStore instead. "
    "This module will be removed in v13.0.0.",
    DeprecationWarning,
    stacklevel=2,
)


def __getattr__(name):
    """Lazy import to avoid circular dependency with store.py"""
    if name == "SqliteMemoryStore":
        from ..store import MemoryStore
        return MemoryStore
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["SqliteMemoryStore"]
