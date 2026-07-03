"""SQLite driver adapter."""
import sqlite3
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


def get_tables(path: str) -> list:
    """Get all tables in a SQLite database."""
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


def table_exists(path: str, table_name: str) -> bool:
    """Check if a table exists."""
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_row_count(path: str, table_name: str) -> int:
    """Get the row count for a table."""
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
        return cursor.fetchone()[0]
    finally:
        conn.close()
