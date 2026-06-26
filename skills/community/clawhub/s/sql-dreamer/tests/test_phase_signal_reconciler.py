"""
tests/test_phase_signal_reconciler.py — Tests for phase_signal_reconciler.py
"""
import pytest
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.phase_signal_reconciler import parse_phase_signals, parse_daily_ingestion, upsert_phase_signals, _parse_ts


SAMPLE_PHASE_SIGNALS = {
    "version": 1,
    "updatedAt": "2026-04-26T07:00:00.000Z",
    "entries": {
        "memory:memory/2026-04-26.md:3:3": {
            "key": "memory:memory/2026-04-26.md:3:3",
            "lightHits": 2,
            "remHits": 0,
            "lastLightAt": "2026-04-26T07:00:00.000Z"
        },
        "memory:memory/2026-04-26.md:10:15": {
            "key": "memory:memory/2026-04-26.md:10:15",
            "lightHits": 1,
            "remHits": 1,
            "lastLightAt": "2026-04-26T07:00:00.000Z",
            "lastRemAt": "2026-04-25T07:00:00.000Z"
        },
        "memory:memory/2026-04-25.md:5:8": {
            "key": "memory:memory/2026-04-25.md:5:8",
            "lightHits": 0,
            "remHits": 3,
            "lastRemAt": "2026-04-25T07:00:00.000Z"
        }
    }
}

SAMPLE_DAILY_INGESTION = {
    "version": 1,
    "files": {
        "memory/2026-04-26.md": {"mtimeMs": 1777100000000, "size": 5200},
        "memory/2026-04-25.md": {"mtimeMs": 1777000000000, "size": 14659}
    }
}


class TestParsePhaseSignals:
    def test_returns_list(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps(SAMPLE_PHASE_SIGNALS))

        result = parse_phase_signals(tmp_path)
        assert isinstance(result, list)

    def test_parses_three_entries(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps(SAMPLE_PHASE_SIGNALS))

        result = parse_phase_signals(tmp_path)
        assert len(result) == 3

    def test_light_hits_populated(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps(SAMPLE_PHASE_SIGNALS))

        result = parse_phase_signals(tmp_path)
        keys = {r["signal_key"]: r for r in result}
        assert keys["memory:memory/2026-04-26.md:3:3"]["light_hits"] == 2
        assert keys["memory:memory/2026-04-26.md:3:3"]["rem_hits"] == 0

    def test_rem_hits_populated(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps(SAMPLE_PHASE_SIGNALS))

        result = parse_phase_signals(tmp_path)
        keys = {r["signal_key"]: r for r in result}
        assert keys["memory:memory/2026-04-25.md:5:8"]["rem_hits"] == 3
        assert keys["memory:memory/2026-04-25.md:5:8"]["light_hits"] == 0

    def test_missing_file_returns_empty(self, tmp_path):
        result = parse_phase_signals(tmp_path)
        assert result == []

    def test_signal_key_is_original_key(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps(SAMPLE_PHASE_SIGNALS))

        result = parse_phase_signals(tmp_path)
        keys = [r["signal_key"] for r in result]
        assert "memory:memory/2026-04-26.md:3:3" in keys

    def test_empty_entries_returns_empty(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "phase-signals.json").write_text(json.dumps({
            "version": 1, "updatedAt": "2026-04-26T00:00:00Z", "entries": {}
        }))
        result = parse_phase_signals(tmp_path)
        assert result == []


class TestParseDailyIngestion:
    def test_parses_two_files(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "daily-ingestion.json").write_text(json.dumps(SAMPLE_DAILY_INGESTION))

        result = parse_daily_ingestion(tmp_path)
        assert len(result) == 2

    def test_file_path_present(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "daily-ingestion.json").write_text(json.dumps(SAMPLE_DAILY_INGESTION))

        result = parse_daily_ingestion(tmp_path)
        paths = [r["file_path"] for r in result]
        assert "memory/2026-04-26.md" in paths

    def test_size_populated(self, tmp_path):
        dreams_dir = tmp_path / "memory" / ".dreams"
        dreams_dir.mkdir(parents=True)
        (dreams_dir / "daily-ingestion.json").write_text(json.dumps(SAMPLE_DAILY_INGESTION))

        result = parse_daily_ingestion(tmp_path)
        entry = next(r for r in result if r["file_path"] == "memory/2026-04-26.md")
        assert entry["size"] == 5200

    def test_missing_file_returns_empty(self, tmp_path):
        result = parse_daily_ingestion(tmp_path)
        assert result == []


class TestUpsertPhaseSignals:
    def _make_rows(self):
        return [
            {
                "signal_key": "memory:memory/2026-04-26.md:3:3",
                "light_hits": 2,
                "rem_hits": 0,
                "last_light_at": "2026-04-26T07:00:00.000Z",
                "last_rem_at": None,
                "updated_at": "2026-04-26T07:00:00.000Z",
            }
        ]

    def test_dry_run_does_not_call_execute(self):
        conn = MagicMock()
        result = upsert_phase_signals(conn, self._make_rows(), dry_run=True)
        conn.execute.assert_not_called()
        assert result == 1

    def test_real_run_calls_execute(self):
        conn = MagicMock()
        conn.execute = MagicMock(return_value=1)
        result = upsert_phase_signals(conn, self._make_rows(), dry_run=False)
        conn.execute.assert_called_once()
        assert result == 1

    def test_sql_uses_qmark_placeholders(self):
        conn = MagicMock()
        conn.execute = MagicMock(return_value=1)
        upsert_phase_signals(conn, self._make_rows(), dry_run=False)
        sql = conn.execute.call_args[0][0]
        assert "?" in sql
        assert "%s" not in sql

    def test_sql_is_merge_statement(self):
        conn = MagicMock()
        conn.execute = MagicMock(return_value=1)
        upsert_phase_signals(conn, self._make_rows(), dry_run=False)
        sql = conn.execute.call_args[0][0]
        assert "MERGE" in sql.upper()

    def test_empty_rows_returns_zero(self):
        conn = MagicMock()
        result = upsert_phase_signals(conn, [], dry_run=False)
        conn.execute.assert_not_called()
        assert result == 0

    def test_multiple_rows_processed(self):
        conn = MagicMock()
        conn.execute = MagicMock(return_value=1)
        rows = self._make_rows() * 5
        result = upsert_phase_signals(conn, rows, dry_run=False)
        assert conn.execute.call_count == 5
        assert result == 5


class TestParseTs:
    def test_iso_with_z(self):
        result = _parse_ts("2026-04-26T07:00:00.000Z")
        assert result is not None
        assert result.tzinfo is not None

    def test_iso_with_offset(self):
        result = _parse_ts("2026-04-26T07:00:00+00:00")
        assert result is not None

    def test_none_returns_none(self):
        assert _parse_ts(None) is None

    def test_empty_string_returns_none(self):
        assert _parse_ts("") is None

    def test_invalid_returns_none(self):
        assert _parse_ts("not-a-date") is None
