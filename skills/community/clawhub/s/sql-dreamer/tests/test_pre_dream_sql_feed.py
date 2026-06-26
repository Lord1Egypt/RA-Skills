"""
tests/test_pre_dream_sql_feed.py — Tests for pre_dream_sql_feed.py
"""
import pytest
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pre_dream_sql_feed import build_memory_content, run


SAMPLE_MEMORIES = [
    {"id": 1, "category": "facts", "key_name": "ob342_complete", "content": "Memory palace configured with OB-342.", "importance": 9, "created_at": datetime(2026, 4, 25, 12, 0, tzinfo=timezone.utc)},
    {"id": 2, "category": "facts", "key_name": "crontab_fixed", "content": "Crontab corrected with OB-343.", "importance": 8, "created_at": datetime(2026, 4, 25, 13, 0, tzinfo=timezone.utc)},
    {"id": 3, "category": "lessons_learned", "key_name": "rule2_enforcement", "content": "Always branch before committing.", "importance": 7, "created_at": datetime(2026, 4, 25, 14, 0, tzinfo=timezone.utc)},
    {"id": 4, "category": "facts", "key_name": "low_importance", "content": "Should not appear in corpus.", "importance": 3, "created_at": datetime(2026, 4, 25, 15, 0, tzinfo=timezone.utc)},
]


class TestBuildMemoryContent:
    def test_returns_string(self):
        result = build_memory_content(SAMPLE_MEMORIES[:2])
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_date_header(self):
        result = build_memory_content(SAMPLE_MEMORIES[:2])
        assert "Session Memory" in result

    def test_groups_by_category(self):
        result = build_memory_content(SAMPLE_MEMORIES[:3])
        assert "Facts" in result or "facts" in result.lower()
        assert "Lessons Learned" in result or "lessons_learned" in result.lower()

    def test_higher_importance_appears_first_in_category(self):
        result = build_memory_content(SAMPLE_MEMORIES[:2])
        pos_9 = result.find("ob342_complete")
        pos_8 = result.find("crontab_fixed")
        assert pos_9 < pos_8, "Higher importance (9) should appear before lower (8)"

    def test_content_included(self):
        result = build_memory_content(SAMPLE_MEMORIES[:1])
        assert "Memory palace configured" in result

    def test_empty_memories_returns_header_only(self):
        result = build_memory_content([])
        assert "Session Memory" in result

    def test_no_secrets_in_output(self):
        result = build_memory_content(SAMPLE_MEMORIES)
        assert "ghp_" not in result
        assert "password" not in result.lower()


class TestRunDryRun:
    def test_dry_run_does_not_write_file(self, tmp_path):
        config_content = f"""
sql:
  server: test
  database: test
  username: test
corpus:
  importance_threshold: 7
  lookback_days: 2
dreaming:
  workspace_dir: {tmp_path}
  archive_after_days: 7
"""
        config_file = tmp_path / "config.yml"
        config_file.write_text(config_content)

        mock_conn = MagicMock()
        mock_conn.__enter__ = lambda s: s
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.get_corpus_memories.return_value = SAMPLE_MEMORIES[:2]
        mock_conn.write_dream_corpus_batch = MagicMock()

        with patch("scripts.pre_dream_sql_feed.SQLDreamerConnector.from_config", return_value=mock_conn):
            run(str(config_file), dry_run=True)

        # File should NOT exist after dry run
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        output_path = tmp_path / "memory" / f"{today}.md"
        assert not output_path.exists(), "Dry run must not write files"

    def test_real_run_writes_file(self, tmp_path):
        config_content = f"""
sql:
  server: test
  database: test
  username: test
corpus:
  importance_threshold: 7
  lookback_days: 2
dreaming:
  workspace_dir: {tmp_path}
  archive_after_days: 7
"""
        config_file = tmp_path / "config.yml"
        config_file.write_text(config_content)

        mock_conn = MagicMock()
        mock_conn.__enter__ = lambda s: s
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.get_corpus_memories.return_value = SAMPLE_MEMORIES[:2]
        mock_conn.write_dream_corpus_batch = MagicMock()

        with patch("scripts.pre_dream_sql_feed.SQLDreamerConnector.from_config", return_value=mock_conn):
            run(str(config_file), dry_run=False)

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        output_path = tmp_path / "memory" / f"{today}.md"
        assert output_path.exists(), "Real run must write the memory file"
        content = output_path.read_text()
        assert "Session Memory" in content

    def test_no_memories_skips_write(self, tmp_path):
        config_content = f"""
sql:
  server: test
  database: test
  username: test
corpus:
  importance_threshold: 7
  lookback_days: 2
dreaming:
  workspace_dir: {tmp_path}
  archive_after_days: 7
"""
        config_file = tmp_path / "config.yml"
        config_file.write_text(config_content)

        mock_conn = MagicMock()
        mock_conn.__enter__ = lambda s: s
        mock_conn.__exit__ = MagicMock(return_value=False)
        mock_conn.get_corpus_memories.return_value = []

        with patch("scripts.pre_dream_sql_feed.SQLDreamerConnector.from_config", return_value=mock_conn):
            run(str(config_file), dry_run=False)

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        output_path = tmp_path / "memory" / f"{today}.md"
        assert not output_path.exists(), "No memories = no file written"
