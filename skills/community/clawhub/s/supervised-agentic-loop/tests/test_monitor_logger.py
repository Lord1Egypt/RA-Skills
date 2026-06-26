"""Tests for sal.monitor.logger — JSONL logging with sanitization."""

import json
import os
import tempfile

import pytest

from sal.monitor.logger import ToolCallLogger


@pytest.fixture
def tmp_logger():
    tmpdir = tempfile.mkdtemp()
    return ToolCallLogger(state_dir=tmpdir)


class TestToolCallLogger:
    def test_creates_log_file(self, tmp_logger):
        """should create daily JSONL file on first log."""
        tmp_logger.log("agent-1", "session-1", "exec", {"command": "echo hi"})
        log_files = list(tmp_logger.state_dir.glob("tool-call-log-*.jsonl"))
        assert len(log_files) == 1

    def test_log_entry_structure(self, tmp_logger):
        """should write valid JSONL with required fields."""
        tmp_logger.log("agent-1", "sess-1", "exec", {"command": "ls"}, result_code=0)
        entries = tmp_logger.read_recent(limit=1)
        assert len(entries) == 1
        entry = entries[0]
        assert entry["agent_id"] == "agent-1"
        assert entry["tool"] == "exec"
        assert "ts" in entry

    def test_sanitizes_secrets(self, tmp_logger):
        """should redact secrets in args before writing."""
        tmp_logger.log(
            "agent-1", "sess-1", "exec",
            {"env": "OPENAI_KEY=sk-abc123def456ghi789jkl012mno345"},
        )
        entries = tmp_logger.read_recent()
        assert "sk-abc123" not in json.dumps(entries)
        assert "REDACTED" in json.dumps(entries)

    def test_read_session(self, tmp_logger):
        """should filter by session_id."""
        tmp_logger.log("a1", "sess-A", "exec", {"x": "1"})
        tmp_logger.log("a1", "sess-B", "exec", {"x": "2"})
        tmp_logger.log("a1", "sess-A", "exec", {"x": "3"})

        session_a = tmp_logger.read_session("sess-A")
        assert len(session_a) == 2

    def test_read_recent_limit(self, tmp_logger):
        """should respect limit parameter."""
        for i in range(20):
            tmp_logger.log("a1", "s1", "exec", {"i": str(i)})

        recent = tmp_logger.read_recent(limit=5)
        assert len(recent) == 5

    def test_count_today(self, tmp_logger):
        """should count entries correctly."""
        assert tmp_logger.count_today() == 0
        tmp_logger.log("a1", "s1", "exec", {"x": "1"})
        tmp_logger.log("a1", "s1", "exec", {"x": "2"})
        assert tmp_logger.count_today() == 2
