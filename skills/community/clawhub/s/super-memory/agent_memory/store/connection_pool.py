"""Connection pool for SQLite — replaces thread-local connections.

Benefits:
- Bounded connection count (default max 20)
- Better resource management under high concurrency
- Automatic connection health checks
"""

import sqlite3
import threading
import time
import logging
from queue import Queue, Empty, Full
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class SQLiteConnectionPool:
    """Thread-safe SQLite connection pool."""

    def __init__(self, db_path, max_connections=20, **conn_kwargs):
        self._db_path = db_path
        self._max_connections = max_connections
        self._conn_kwargs = conn_kwargs
        self._pool = Queue(maxsize=max_connections)
        self._created = 0
        self._created_lock = threading.Lock()
        self._closed = False

    def _create_connection(self):
        """Create a new SQLite connection with proper PRAGMAs."""
        conn = sqlite3.connect(self._db_path, check_same_thread=False, **self._conn_kwargs)
        conn.row_factory = sqlite3.Row
        # Apply standard PRAGMAs
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    @contextmanager
    def connection(self, timeout=30):
        """Get a connection from the pool.

        Usage:
            with pool.connection() as conn:
                conn.execute(...)
        """
        if self._closed:
            raise RuntimeError("Connection pool is closed")

        conn = self._get_connection(timeout)
        try:
            yield conn
        finally:
            self._return_connection(conn)

    def _get_connection(self, timeout=30):
        """Get a connection from pool or create new one."""
        # Try to get from pool first
        try:
            conn = self._pool.get_nowait()
            # Health check
            try:
                conn.execute("SELECT 1")
                return conn
            except Exception:
                # Connection is stale, create new one
                try:
                    conn.close()
                except Exception:
                    pass
                with self._created_lock:
                    self._created -= 1
        except Empty:
            pass

        # Create new connection if under limit
        with self._created_lock:
            if self._created < self._max_connections:
                self._created += 1
                try:
                    return self._create_connection()
                except Exception:
                    self._created -= 1
                    raise

        # Pool full, wait for a connection to be returned
        try:
            conn = self._pool.get(timeout=timeout)
            try:
                conn.execute("SELECT 1")
                return conn
            except Exception:
                try:
                    conn.close()
                except Exception:
                    pass
                with self._created_lock:
                    self._created -= 1
                    if self._created < self._max_connections:
                        self._created += 1
                        try:
                            return self._create_connection()
                        except Exception:
                            self._created -= 1
                            raise
                raise TimeoutError("Failed to create replacement connection")
        except Empty:
            raise TimeoutError(f"No connection available after {timeout}s")

    def _return_connection(self, conn):
        """Return a connection to the pool."""
        if self._closed:
            try:
                conn.close()
            except Exception:
                pass
            with self._created_lock:
                self._created -= 1
            return

        try:
            self._pool.put_nowait(conn)
        except Full:
            # Pool is full, close the connection
            try:
                conn.close()
            except Exception:
                pass
            with self._created_lock:
                self._created -= 1

    def close_all(self):
        """Close all connections in the pool."""
        self._closed = True
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                try:
                    conn.close()
                except Exception:
                    pass
            except Empty:
                break
        with self._created_lock:
            self._created = 0

    @property
    def stats(self):
        """Return pool statistics."""
        with self._created_lock:
            return {
                "created": self._created,
                "available": self._pool.qsize(),
                "max": self._max_connections,
            }
