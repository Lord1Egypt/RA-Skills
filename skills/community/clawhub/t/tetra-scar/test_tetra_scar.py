#!/usr/bin/env python3
"""Tests for tetra_scar.py — standalone, no external dependencies."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tetra_scar import (
    read_scars, write_scar,
    read_narrative, write_narrative,
    reflex_check, tetra_check,
    schedule_verification, run_pending_verifications,
    write_trace, read_traces, trace_to_training_pair, export_training_data,
    _extract_keywords, _read_jsonl,
)


class TestScarLayer:
    """Scar layer: immutable failure records."""

    def test_write_and_read(self, tmp_path):
        d = str(tmp_path / "mem")
        entry = write_scar("tests broke", "run tests first", memory_dir=d)
        assert entry["what_broke"] == "tests broke"
        assert entry["never_again"] == "run tests first"
        assert entry["id"].startswith("scar_")

        scars = read_scars(memory_dir=d)
        assert len(scars) == 1
        assert scars[0]["never_again"] == "run tests first"

    def test_multiple_scars_order(self, tmp_path):
        d = str(tmp_path / "mem")
        write_scar("first", "never first", memory_dir=d)
        write_scar("second", "never second", memory_dir=d)
        write_scar("third", "never third", memory_dir=d)

        scars = read_scars(n=2, memory_dir=d)
        assert len(scars) == 2
        assert scars[0]["what_broke"] == "second"
        assert scars[1]["what_broke"] == "third"

    def test_read_empty(self, tmp_path):
        d = str(tmp_path / "mem")
        scars = read_scars(memory_dir=d)
        assert scars == []

    def test_scar_immutability(self, tmp_path):
        """Scars append-only — writing new scars doesn't erase old ones."""
        d = str(tmp_path / "mem")
        write_scar("old failure", "never old", memory_dir=d)
        write_scar("new failure", "never new", memory_dir=d)
        scars = read_scars(n=100, memory_dir=d)
        assert len(scars) == 2
        assert scars[0]["what_broke"] == "old failure"


class TestNarrativeLayer:
    """Narrative layer: mutable success records."""

    def test_write_and_read(self, tmp_path):
        d = str(tmp_path / "mem")
        entry = write_narrative("deployed v2", "Users", memory_dir=d)
        assert entry["what"] == "deployed v2"
        assert entry["who_benefited"] == "Users"

        entries = read_narrative(memory_dir=d)
        assert len(entries) == 1

    def test_who_benefited_optional(self, tmp_path):
        d = str(tmp_path / "mem")
        entry = write_narrative("did stuff", memory_dir=d)
        assert entry["who_benefited"] == ""


class TestExtractKeywords:
    """Keyword extraction for reflex arc."""

    def test_english_words(self):
        kws = _extract_keywords("Always run full test suite before deployment")
        assert "Always" in kws
        assert "test" in kws
        assert "suite" in kws
        assert "deployment" in kws

    def test_japanese_words(self):
        kws = _extract_keywords("計画と実行を分離するな")
        assert "計画" in kws
        assert "実行" in kws
        assert "分離" in kws

    def test_mixed_language(self):
        kws = _extract_keywords("CLI呼び出しをONE-SHOTで完結させろ")
        en = [k for k in kws if k.isascii()]
        ja = [k for k in kws if not k.isascii()]
        assert len(en) > 0  # CLI, ONE, SHOT
        assert len(ja) > 0  # 呼び出し, 完結

    def test_short_words_ignored(self):
        kws = _extract_keywords("do it on me at")
        assert kws == []  # all < 3 chars


class TestReflexCheck:
    """Reflex arc: scar collision detection."""

    def test_collision_detected(self):
        scars = [{"never_again": "Always run full test suite before deployment"}]
        result = reflex_check("Deploy latest changes and run test suite", scars)
        assert result is not None
        assert "scar collision" in result

    def test_no_collision(self):
        scars = [{"never_again": "Always run full test suite before deployment"}]
        result = reflex_check("Add a new button to the UI", scars)
        assert result is None

    def test_empty_task(self):
        scars = [{"never_again": "something"}]
        assert reflex_check("", scars) is None
        assert reflex_check(None, scars) is None

    def test_empty_scars(self):
        result = reflex_check("Deploy everything", [])
        assert result is None

    def test_japanese_scar_collision(self):
        scars = [{"never_again": "計画と実行を別々のCLI呼び出しに分離するな"}]
        result = reflex_check("計画を立てて実行を分離して呼び出す", scars)
        assert result is not None

    def test_threshold_just_below(self):
        """Below 40% match should not trigger."""
        scars = [{"never_again": "Always run full test suite before deployment to production server"}]
        # Only 1 keyword matches out of many — below threshold
        result = reflex_check("Check the server status", scars)
        assert result is None

    def test_scar_with_empty_never_again(self):
        scars = [{"never_again": ""}]
        result = reflex_check("Do anything", scars)
        assert result is None


class TestTetraCheck:
    """4-axis validation."""

    def test_all_axes_pass(self, tmp_path):
        d = str(tmp_path / "mem")
        scars = []
        approved, reason = tetra_check("Fix the login button bug", scars)
        assert approved is True
        assert "4 axes passed" in reason

    def test_emotion_axis_empty(self):
        approved, reason = tetra_check("", [])
        assert approved is False
        assert "emotion" in reason

    def test_emotion_axis_too_short(self):
        approved, reason = tetra_check("hi", [])
        assert approved is False
        assert "emotion" in reason

    def test_action_axis_no_verb(self):
        approved, reason = tetra_check("the big red button on the page", [])
        assert approved is False
        assert "action" in reason

    def test_life_axis_scar_collision(self):
        scars = [{"never_again": "Always run full test suite before deployment"}]
        approved, reason = tetra_check("Deploy without running test suite", scars)
        assert approved is False
        assert "life axis" in reason

    def test_ethics_axis_dangerous(self):
        approved, reason = tetra_check("Run rm -rf on the project directory", [])
        assert approved is False
        assert "ethics" in reason
        assert "rm -rf" in reason

    def test_ethics_axis_drop_table(self):
        approved, reason = tetra_check("Execute drop table users", [])
        assert approved is False

    def test_japanese_task_passes(self):
        approved, reason = tetra_check("テストを追加して確認する", [])
        assert approved is True

    def test_force_push_blocked(self):
        approved, reason = tetra_check("Do a force push to main branch", [])
        assert approved is False
        assert "force push" in reason


class TestReadJsonl:
    """JSONL reading robustness."""

    def test_malformed_lines_skipped(self, tmp_path):
        f = tmp_path / "test.jsonl"
        f.write_text('{"good": 1}\nthis is bad\n{"also_good": 2}\n')
        entries = _read_jsonl(f)
        assert len(entries) == 2
        assert entries[0]["good"] == 1
        assert entries[1]["also_good"] == 2

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.jsonl"
        f.write_text("")
        assert _read_jsonl(f) == []

    def test_nonexistent_file(self, tmp_path):
        f = tmp_path / "nope.jsonl"
        assert _read_jsonl(f) == []



class TestDelayedVerification:
    """Delayed verification: schedule and check."""

    def test_schedule_and_run(self, tmp_path):
        d = str(tmp_path / "mem")
        # Schedule with 0 days = immediately due
        entry = schedule_verification("deployed v2", check_after_days=0, memory_dir=d)
        assert entry["what"] == "deployed v2"
        assert not entry["checked"]

        import time
        time.sleep(0.1)
        due = run_pending_verifications(memory_dir=d)
        assert len(due) == 1
        assert due[0]["checked"] is True

    def test_not_yet_due(self, tmp_path):
        d = str(tmp_path / "mem")
        schedule_verification("future check", check_after_days=30, memory_dir=d)
        due = run_pending_verifications(memory_dir=d)
        assert len(due) == 0

    def test_empty_verifications(self, tmp_path):
        d = str(tmp_path / "mem")
        due = run_pending_verifications(memory_dir=d)
        assert due == []



class TestDecisionTrace:
    """Decision trace: judgment path recording."""

    def test_write_and_read(self, tmp_path):
        d = str(tmp_path / "mem")
        entry = write_trace(
            situation="OAuth 1.0a returns 401",
            options=[
                {"option": "debug signature", "chosen": False, "reason": "too slow"},
                {"option": "switch to tweepy", "chosen": True, "reason": "proven library"},
            ],
            outcome="tweepy also 401 — key/permission issue",
            learned="separate implementation bugs from config bugs early",
            tags=["api", "auth"],
            memory_dir=d,
        )
        assert entry["situation"] == "OAuth 1.0a returns 401"
        assert len(entry["options"]) == 2
        assert entry["tags"] == ["api", "auth"]

        traces = read_traces(memory_dir=d)
        assert len(traces) == 1

    def test_filter_by_tags(self, tmp_path):
        d = str(tmp_path / "mem")
        write_trace("s1", [], "o1", "l1", tags=["api"], memory_dir=d)
        write_trace("s2", [], "o2", "l2", tags=["git"], memory_dir=d)
        write_trace("s3", [], "o3", "l3", tags=["api", "git"], memory_dir=d)

        api_traces = read_traces(tags=["api"], memory_dir=d)
        assert len(api_traces) == 2

        git_traces = read_traces(tags=["git"], memory_dir=d)
        assert len(git_traces) == 2

    def test_to_training_pair(self):
        trace = {
            "situation": "deploy failed",
            "options": [
                {"option": "rollback", "chosen": True, "reason": "safe"},
                {"option": "hotfix", "chosen": False, "reason": "risky"},
            ],
            "outcome": "rollback succeeded",
            "learned": "always rollback first",
            "tags": ["deploy"],
        }
        pair = trace_to_training_pair(trace)
        assert "deploy failed" in pair["instruction"]
        assert "rollback" in pair["output"]
        assert "hotfix" in pair["output"]
        assert "always rollback first" in pair["output"]

    def test_export_training_data(self, tmp_path):
        d = str(tmp_path / "mem")
        write_scar("broke prod", "test first", memory_dir=d)
        write_trace("s1", [{"option": "a", "chosen": True, "reason": "r"}],
                     "worked", "lesson1", memory_dir=d)

        out = export_training_data(memory_dir=d)
        assert Path(out).exists()
        lines = Path(out).read_text().strip().split("\n")
        assert len(lines) == 2  # 1 trace + 1 scar

    def test_empty_traces(self, tmp_path):
        d = str(tmp_path / "mem")
        traces = read_traces(memory_dir=d)
        assert traces == []
