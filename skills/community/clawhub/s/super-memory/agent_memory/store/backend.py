"""Abstract storage backend interface.

All storage backends (SQLite, PostgreSQL, etc.) must implement this interface.
This allows swapping storage backends without changing business logic.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Optional

_VALID_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


class StorageBackend(ABC):
    """Abstract base class for memory storage backends."""

    @abstractmethod
    def insert(self, table: str, data: dict) -> str:
        """Insert a record. Returns the record ID."""
        ...

    @abstractmethod
    def get(self, table: str, record_id: str) -> Optional[dict]:
        """Get a single record by ID."""
        ...

    @abstractmethod
    def update(self, table: str, record_id: str, data: dict) -> bool:
        """Update a record. Returns True if successful."""
        ...

    @abstractmethod
    def delete(self, table: str, record_id: str, soft: bool = True) -> bool:
        """Delete a record. Returns True if successful."""
        ...

    @abstractmethod
    def query(self, table: str, filters: dict = None, order_by: str = None,
              limit: int = 100, offset: int = 0) -> list:
        """Query records with optional filters."""
        ...

    @abstractmethod
    def count(self, table: str, filters: dict = None) -> int:
        """Count records matching filters."""
        ...

    @abstractmethod
    def execute(self, sql: str, params: tuple = None) -> Any:
        """Execute raw SQL (backend-specific)."""
        ...

    @abstractmethod
    def transaction(self):
        """Context manager for transactions."""
        ...

    @abstractmethod
    def close(self):
        """Close the backend connection."""
        ...

    @abstractmethod
    def health_check(self) -> dict:
        """Check backend health."""
        ...


class SQLiteBackend(StorageBackend):
    """SQLite implementation of StorageBackend.

    Wraps the existing MemoryStore to implement the abstract interface.
    This is a gradual migration path — MemoryStore still does the heavy lifting,
    but new code should use the StorageBackend interface.
    """

    @staticmethod
    def _validate_identifier(name: str, context: str = "identifier") -> None:
        """Validate SQL identifier (table/column name) to prevent injection."""
        if not _VALID_IDENTIFIER.match(name):
            raise ValueError(f"Invalid SQL {context}: {name!r}")

    @staticmethod
    def _validate_order_by(order_by: str) -> None:
        """Validate ORDER BY clause to prevent injection."""
        for part in order_by.split(','):
            part = part.strip().rsplit(' ', 1)[0]  # Remove ASC/DESC
            if not _VALID_IDENTIFIER.match(part.strip()):
                raise ValueError(f"Invalid ORDER BY column: {part!r}")

    def __init__(self, store):
        """Initialize with an existing MemoryStore instance."""
        self._store = store

    @property
    def store(self):
        """Access the underlying MemoryStore for backward compatibility."""
        return self._store

    def insert(self, table: str, data: dict) -> str:
        self._validate_identifier(table, "table name")
        for key in data:
            self._validate_identifier(key, "column name")
        if table == "memories":
            result = self._store.insert_memory(
                content=data.get("content", ""),
                memory_id=data.get("memory_id"),
                **{k: v for k, v in data.items() if k not in ("content", "memory_id")},
            )
            if isinstance(result, dict):
                return result.get("memory_id", "")
            return str(result)
        # Generic insert for other tables
        return self._store.execute_sql(
            f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join(['?' for _ in data])})",
            params=tuple(data.values()),
        )

    def get(self, table: str, record_id: str) -> Optional[dict]:
        self._validate_identifier(table, "table name")
        if table == "memories":
            return self._store.get_memory(record_id)
        rows = self._store.execute_sql(
            f"SELECT * FROM {table} WHERE id = ? LIMIT 1",
            params=(record_id,),
            fetch=True,
        )
        return rows[0] if rows else None

    def update(self, table: str, record_id: str, data: dict) -> bool:
        self._validate_identifier(table, "table name")
        for key in data:
            self._validate_identifier(key, "column name")
        if table == "memories":
            try:
                self._store.update_memory(record_id, data.get("content", ""), **data)
                return True
            except Exception:
                return False
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        try:
            self._store.execute_sql(
                f"UPDATE {table} SET {set_clause} WHERE id = ?",
                params=tuple(data.values()) + (record_id,),
            )
            return True
        except Exception:
            return False

    def delete(self, table: str, record_id: str, soft: bool = True) -> bool:
        self._validate_identifier(table, "table name")
        if table == "memories":
            try:
                self._store.delete_memory(record_id, permanent=not soft)
                return True
            except Exception:
                return False
        try:
            self._store.execute_sql(f"DELETE FROM {table} WHERE id = ?", params=(record_id,))
            return True
        except Exception:
            return False

    def query(self, table: str, filters: dict = None, order_by: str = None,
              limit: int = 100, offset: int = 0) -> list:
        self._validate_identifier(table, "table name")
        if filters:
            for key in filters:
                self._validate_identifier(key, "filter column name")
        if order_by:
            self._validate_order_by(order_by)
        if table == "memories" and not filters:
            return self._store.query(limit=limit)

        where_parts = []
        params = []
        if filters:
            for k, v in filters.items():
                where_parts.append(f"{k} = ?")
                params.append(v)

        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        order_clause = f"ORDER BY {order_by}" if order_by else ""

        return self._store.execute_sql(
            f"SELECT * FROM {table} WHERE {where_clause} {order_clause} LIMIT ? OFFSET ?",
            params=tuple(params) + (limit, offset),
            fetch=True,
        )

    def count(self, table: str, filters: dict = None) -> int:
        self._validate_identifier(table, "table name")
        if filters:
            for key in filters:
                self._validate_identifier(key, "filter column name")
        if table == "memories" and not filters:
            return self._store.count()

        where_parts = []
        params = []
        if filters:
            for k, v in filters.items():
                where_parts.append(f"{k} = ?")
                params.append(v)

        where_clause = " AND ".join(where_parts) if where_parts else "1=1"
        rows = self._store.execute_sql(
            f"SELECT COUNT(*) as cnt FROM {table} WHERE {where_clause}",
            params=tuple(params),
            fetch=True,
        )
        return rows[0]["cnt"] if rows else 0

    def execute(self, sql: str, params: tuple = None) -> Any:
        return self._store.execute_sql(sql, params=params, fetch=True)

    def transaction(self):
        return self._store.transaction()

    def close(self):
        self._store.close_all()

    def health_check(self) -> dict:
        return {"backend": "sqlite", "healthy": True}
