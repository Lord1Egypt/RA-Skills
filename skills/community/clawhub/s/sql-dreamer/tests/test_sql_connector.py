"""
tests/test_sql_connector.py — Unit tests for SQLDreamerConnector
Uses mock DB — no live SQL required.
"""
import pytest
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime, timezone

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.sql_connector import SQLDreamerConnector


MOCK_CONFIG = """
sql:
  server: "test-server"
  database: "test-db"
  username: "test-user"
corpus:
  importance_threshold: 7
  lookback_days: 2
dreaming:
  workspace_dir: "/tmp/test-workspace"
  archive_after_days: 7
"""


@pytest.fixture
def connector():
    conn = SQLDreamerConnector("mock-conn-string")
    mock_db = MagicMock()
    mock_db.cursor.return_value.description = [("id",), ("category",), ("key_name",), ("content",), ("importance",), ("created_at",)]
    mock_db.cursor.return_value.fetchall.return_value = [
        (1, "facts", "test_key", "test content", 8, datetime.now(timezone.utc))
    ]
    conn._conn = mock_db
    return conn


def test_query_returns_list_of_dicts(connector):
    results = connector.query("SELECT TOP 1 id FROM memory.Memories", ())
    assert isinstance(results, list)
    assert isinstance(results[0], dict)


def test_get_corpus_memories_uses_parameterized_query(connector):
    with patch.object(connector, 'query', return_value=[]) as mock_q:
        connector.get_corpus_memories(importance_threshold=7, lookback_days=2)
        call_args = mock_q.call_args
        sql = call_args[0][0]
        params = call_args[0][1]
        # Must not use f-strings or format — check params tuple has values
        assert len(params) == 2
        assert params[0] == 7
        # pyodbc uses qmark (?) not %s
        assert "?" in sql
        assert "%s" not in sql
        # Must use TOP N not LIMIT
        assert "TOP" in sql.upper()
        assert "LIMIT" not in sql.upper()


def test_from_config_reads_yml(tmp_path, monkeypatch):
    # Clear any CI env override so we test actual config parsing
    monkeypatch.delenv("SQL_CONNECTION_STRING", raising=False)
    config_file = tmp_path / "config.yml"
    config_file.write_text(MOCK_CONFIG)
    with patch("pyodbc.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        connector = SQLDreamerConnector.from_config(str(config_file))
        assert "test-server" in connector._conn_str
        assert "test-db" in connector._conn_str


def test_from_config_env_override(tmp_path, monkeypatch):
    config_file = tmp_path / "config.yml"
    config_file.write_text(MOCK_CONFIG)
    monkeypatch.setenv("SQL_CONNECTION_STRING", "Driver=...;Server=override;")
    connector = SQLDreamerConnector.from_config(str(config_file))
    assert "override" in connector._conn_str


def test_write_dream_light_uses_executemany(connector):
    entries = [
        {"key": "k1", "snippet": "test", "confidence": 0.8, "evidence": "memory/test.md:1:1", "recalls": 2, "status": "staged"},
    ]
    with patch.object(connector, 'executemany') as mock_em:
        connector.write_dream_light("2026-04-26", entries)
        assert mock_em.called
        sql = mock_em.call_args[0][0]
        # pyodbc qmark style: ? not %s
        assert "?" in sql
        assert "%s" not in sql
        assert "f'" not in sql  # No f-strings


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
