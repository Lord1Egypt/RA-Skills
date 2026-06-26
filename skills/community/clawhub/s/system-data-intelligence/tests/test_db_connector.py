#!/usr/bin/env python3
"""Unit tests for db_connector."""
import sqlite3
from pathlib import Path
import sys
import pytest
sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)
from scripts.db_connector import DBConnector, build_url

@pytest.fixture
def sqlite_db(tmp_path):
    p = tmp_path / "test.db"
    conn = sqlite3.connect(str(p))
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    conn.executemany("INSERT INTO users VALUES (?,?)", [(1,'A'),(2,'B')])
    conn.commit()
    conn.close()
    return str(p)

def test_query(sqlite_db):
    db = DBConnector(f"sqlite:///{sqlite_db}")
    df = db.query("SELECT * FROM users")
    assert len(df) == 2
    db.close()
