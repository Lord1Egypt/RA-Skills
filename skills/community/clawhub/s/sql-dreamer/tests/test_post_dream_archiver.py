"""
tests/test_post_dream_archiver.py — Tests for post_dream_archiver.py
"""
import pytest
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.post_dream_archiver import parse_light_file, parse_rem_file, parse_deep_file, cleanup_old_files


# ─────────────────────────────────────────────
# Fixtures: realistic dream output content
# ─────────────────────────────────────────────

LIGHT_CONTENT = """# Light Sleep

- Candidate: Memory palace configuration complete with OB-342
  - confidence: 0.85
  - evidence: memory/2026-04-26.md:10-12
  - recalls: 3
  - status: staged
- Candidate: Crontab fixed with correct UTC offsets
  - confidence: 0.72
  - evidence: memory/2026-04-26.md:25-27
  - recalls: 1
  - status: staged
- Candidate: live_sync now includes scripts/ directory
  - confidence: 0.68
  - evidence: memory/2026-04-26.md:40-42
  - recalls: 0
  - status: staged
"""

REM_CONTENT = """# REM Sleep

### Reflections
- Theme: `rules.md` kept surfacing across 187 memories.
  - confidence: 0.72
  - evidence: memory/2026-04-16.md:36-87
  - note: reflection
- Theme: `workflow` kept surfacing across 95 memories.
  - confidence: 0.65
  - evidence: memory/2026-04-25.md:1-5
  - note: reflection

### Possible Lasting Truths
- RULE #2: Branch → PR → Merge. Never commit directly to main. Real ticket IDs only.
- SQL memory is the canonical store. No .md files in memory/ directory.
"""

DEEP_CONTENT = """# Deep Sleep

- Repaired recall artifacts: rewrote recall store.
- Ranked 5 candidate(s) for durable promotion.
- Promoted 2 candidate(s) into MEMORY.md.
"""


# ─────────────────────────────────────────────
# parse_light_file
# ─────────────────────────────────────────────

class TestParseLightFile:
    def test_returns_list(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert isinstance(result, list)

    def test_parses_three_candidates(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert len(result) == 3

    def test_parses_confidence(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert result[0]["confidence"] == pytest.approx(0.85)
        assert result[1]["confidence"] == pytest.approx(0.72)

    def test_parses_recall_count(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert result[0]["recalls"] == 3
        assert result[2]["recalls"] == 0

    def test_parses_status(self):
        result = parse_light_file(LIGHT_CONTENT)
        for entry in result:
            assert entry["status"] == "staged"

    def test_parses_evidence_path(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert "2026-04-26.md:10-12" in result[0]["evidence"]

    def test_snippet_populated(self):
        result = parse_light_file(LIGHT_CONTENT)
        assert "Memory palace" in result[0]["snippet"]

    def test_key_generated(self):
        result = parse_light_file(LIGHT_CONTENT)
        for entry in result:
            assert "key" in entry and len(entry["key"]) > 0

    def test_empty_content_returns_empty(self):
        result = parse_light_file("# Light Sleep\n")
        assert result == []


# ─────────────────────────────────────────────
# parse_rem_file
# ─────────────────────────────────────────────

class TestParseRemFile:
    def test_returns_tuple(self):
        themes, truths = parse_rem_file(REM_CONTENT)
        assert isinstance(themes, list)
        assert isinstance(truths, list)

    def test_parses_two_themes(self):
        themes, _ = parse_rem_file(REM_CONTENT)
        assert len(themes) == 2

    def test_theme_text(self):
        themes, _ = parse_rem_file(REM_CONTENT)
        theme_texts = [t["theme"] for t in themes]
        assert "rules.md" in theme_texts or any("rules" in t for t in theme_texts)

    def test_theme_frequency(self):
        themes, _ = parse_rem_file(REM_CONTENT)
        freqs = [t["frequency"] for t in themes]
        assert 187 in freqs

    def test_parses_two_lasting_truths(self):
        _, truths = parse_rem_file(REM_CONTENT)
        assert len(truths) == 2

    def test_lasting_truth_content(self):
        _, truths = parse_rem_file(REM_CONTENT)
        combined = " ".join(truths)
        assert "RULE #2" in combined or "Branch" in combined

    def test_empty_content(self):
        themes, truths = parse_rem_file("# REM Sleep\n")
        assert themes == []
        assert truths == []


# ─────────────────────────────────────────────
# parse_deep_file
# ─────────────────────────────────────────────

class TestParseDeepFile:
    def test_returns_list(self):
        result = parse_deep_file(DEEP_CONTENT)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_ranked_count(self):
        result = parse_deep_file(DEEP_CONTENT)
        assert result[0]["recallCount"] == 5

    def test_promoted_true(self):
        result = parse_deep_file(DEEP_CONTENT)
        assert result[0]["promoted"] is True

    def test_snippet_populated(self):
        result = parse_deep_file(DEEP_CONTENT)
        assert len(result[0]["snippet"]) > 0


# ─────────────────────────────────────────────
# cleanup_old_files
# ─────────────────────────────────────────────

class TestCleanupOldFiles:
    def _make_dream_dir(self, tmp_path, dates: list) -> Path:
        workspace = tmp_path / "workspace"
        for phase in ("light", "rem", "deep"):
            phase_dir = workspace / "memory" / "dreaming" / phase
            phase_dir.mkdir(parents=True)
            for date_str in dates:
                f = phase_dir / f"{date_str}.md"
                f.write_text(f"# {phase} sleep {date_str}")
        return workspace

    def test_deletes_old_files(self, tmp_path):
        old_date = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%d")
        recent_date = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
        workspace = self._make_dream_dir(tmp_path, [old_date, recent_date])

        cleanup_old_files(workspace, archive_after_days=7, dry_run=False)

        for phase in ("light", "rem", "deep"):
            old_path = workspace / "memory" / "dreaming" / phase / f"{old_date}.md"
            recent_path = workspace / "memory" / "dreaming" / phase / f"{recent_date}.md"
            assert not old_path.exists(), f"Old file should be deleted: {old_path}"
            assert recent_path.exists(), f"Recent file should be kept: {recent_path}"

    def test_dry_run_keeps_all_files(self, tmp_path):
        old_date = (datetime.now(timezone.utc) - timedelta(days=10)).strftime("%Y-%m-%d")
        workspace = self._make_dream_dir(tmp_path, [old_date])

        cleanup_old_files(workspace, archive_after_days=7, dry_run=True)

        for phase in ("light", "rem", "deep"):
            old_path = workspace / "memory" / "dreaming" / phase / f"{old_date}.md"
            assert old_path.exists(), f"Dry run must not delete: {old_path}"

    def test_keeps_files_within_window(self, tmp_path):
        recent_date = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
        workspace = self._make_dream_dir(tmp_path, [recent_date])

        cleanup_old_files(workspace, archive_after_days=7, dry_run=False)

        for phase in ("light", "rem", "deep"):
            recent_path = workspace / "memory" / "dreaming" / phase / f"{recent_date}.md"
            assert recent_path.exists(), f"Recent file should be kept: {recent_path}"
