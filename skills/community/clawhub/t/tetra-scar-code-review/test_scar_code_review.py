#!/usr/bin/env python3
"""Tests for scar_code_review.py — at least 20 tests.

Covers: security checks, performance checks, correctness checks,
maintainability checks, reflex arc, scar recording/loading, CLI.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent))
from scar_code_review import (
    _check_correctness,
    _check_maintainability,
    _check_performance,
    _check_security,
    _extract_keywords,
    load_review_scars,
    record_miss,
    reflex_check,
    review,
)


# ============================================================================
# Helpers
# ============================================================================

def _write_temp_file(content: str, suffix: str = ".py") -> str:
    """Write content to a temp file and return its path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w") as f:
        f.write(content)
    return path


def _write_temp_scars(scars: list[dict]) -> str:
    """Write scar dicts to a temp JSONL file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w") as f:
        for s in scars:
            f.write(json.dumps(s) + "\n")
    return path


# ============================================================================
# Security: SQL injection
# ============================================================================

class TestSecuritySQLInjection:
    def test_fstring_sql_injection(self):
        lines = ['cursor.execute(f"SELECT * FROM users WHERE id={user_id}")']
        findings = _check_security(lines)
        assert any("SQL injection" in f["message"] for f in findings)

    def test_format_sql_injection(self):
        lines = ['cursor.execute("SELECT * FROM users WHERE id={}".format(uid))']
        findings = _check_security(lines)
        assert any("SQL injection" in f["message"] for f in findings)

    def test_parameterized_query_safe(self):
        lines = ['cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))']
        findings = _check_security(lines)
        assert not any("SQL injection" in f["message"] for f in findings)


# ============================================================================
# Security: Hardcoded secrets
# ============================================================================

class TestSecuritySecrets:
    def test_hardcoded_password(self):
        lines = ['password = "SuperSecret123"']
        findings = _check_security(lines)
        assert any("secret" in f["message"].lower() or "credential" in f["message"].lower()
                    for f in findings)

    def test_hardcoded_api_key(self):
        lines = ['api_key = "sk-1234567890abcdef"']
        findings = _check_security(lines)
        assert any("secret" in f["message"].lower() or "credential" in f["message"].lower()
                    for f in findings)

    def test_variable_reference_safe(self):
        lines = ['password = os.environ["DB_PASSWORD"]']
        findings = _check_security(lines)
        assert not any("secret" in f["message"].lower() or "credential" in f["message"].lower()
                    for f in findings)


# ============================================================================
# Security: XSS
# ============================================================================

class TestSecurityXSS:
    def test_innerhtml(self):
        lines = ['element.innerHTML = userInput;']
        findings = _check_security(lines)
        assert any("XSS" in f["message"] for f in findings)

    def test_dangerously_set(self):
        lines = ['<div dangerouslySetInnerHTML={{__html: data}} />']
        findings = _check_security(lines)
        assert any("XSS" in f["message"] for f in findings)


# ============================================================================
# Security: eval/exec
# ============================================================================

class TestSecurityEval:
    def test_eval_detected(self):
        lines = ['result = eval(user_input)']
        findings = _check_security(lines)
        assert any("eval" in f["message"].lower() for f in findings)

    def test_subprocess_shell(self):
        lines = ['subprocess.run(cmd, shell=True)']
        findings = _check_security(lines)
        assert any("eval" in f["message"].lower() or "shell" in f["message"].lower()
                    for f in findings)


# ============================================================================
# Performance
# ============================================================================

class TestPerformance:
    def test_query_in_loop(self):
        lines = [
            "for item in items:",
            "    result = db.query(item.id)",
        ]
        findings = _check_performance(lines)
        assert any("N+1" in f["message"] for f in findings)

    def test_unbounded_select(self):
        lines = ['query = "SELECT * FROM users;"']
        findings = _check_performance(lines)
        assert any("Unbounded" in f["message"] for f in findings)

    def test_select_with_limit_safe(self):
        lines = ['query = "SELECT * FROM users LIMIT 100;"']
        findings = _check_performance(lines)
        assert not any("Unbounded" in f["message"] for f in findings)

    def test_missing_pagination(self):
        lines = ["items = Item.objects.filter()"]
        findings = _check_performance(lines)
        assert any("pagination" in f["message"].lower() for f in findings)


# ============================================================================
# Correctness
# ============================================================================

class TestCorrectness:
    def test_off_by_one_lte_len(self):
        lines = ["if i <= len(items):"]
        findings = _check_correctness(lines)
        assert any("off-by-one" in f["message"].lower() for f in findings)

    def test_unhandled_fetch(self):
        lines = ["fetch('/api/data')"]
        findings = _check_correctness(lines)
        assert any("unhandled" in f["message"].lower() for f in findings)

    def test_awaited_fetch_safe(self):
        lines = ["const data = await fetch('/api/data')"]
        findings = _check_correctness(lines)
        assert not any("unhandled" in f["message"].lower() for f in findings)


# ============================================================================
# Maintainability
# ============================================================================

class TestMaintainability:
    def test_long_function(self):
        lines = ["def very_long_function():"]
        lines.extend(["    x = 1"] * 55)
        findings = _check_maintainability(lines)
        assert any("exceeds 50 lines" in f["message"].lower() for f in findings)

    def test_short_function_safe(self):
        lines = ["def short():"]
        lines.extend(["    x = 1"] * 10)
        findings = _check_maintainability(lines)
        assert not any("exceeds 50 lines" in f["message"].lower() for f in findings)

    def test_deep_nesting(self):
        lines = ["                        deeply_nested = True"]  # 24 spaces = 6 levels
        findings = _check_maintainability(lines)
        assert any("deep nesting" in f["message"].lower() for f in findings)


# ============================================================================
# Reflex arc
# ============================================================================

class TestReflexArc:
    def test_regex_pattern_match(self):
        scars = [{
            "id": "rscar_1",
            "what_missed": "SQL injection in format strings",
            "pattern": r"execute.*format",
            "severity": "critical",
        }]
        diff = 'cursor.execute("SELECT {}".format(user_id))'
        blocks = reflex_check(diff, scars)
        assert len(blocks) == 1
        assert "rscar_1" in blocks[0]

    def test_keyword_match(self):
        scars = [{
            "id": "rscar_2",
            "what_missed": "Missed unvalidated redirect in login handler",
            "pattern": "",
            "severity": "high",
        }]
        diff = "redirect to login page based on unvalidated handler input"
        blocks = reflex_check(diff, scars)
        assert len(blocks) >= 1

    def test_no_match_clean(self):
        scars = [{
            "id": "rscar_3",
            "what_missed": "SQL injection in database layer",
            "pattern": r"execute.*format.*user",
            "severity": "critical",
        }]
        diff = "def add(a, b):\n    return a + b\n"
        blocks = reflex_check(diff, scars)
        assert blocks == []

    def test_empty_scars(self):
        blocks = reflex_check("some diff content", [])
        assert blocks == []

    def test_empty_diff(self):
        scars = [{"id": "rscar_4", "what_missed": "something", "pattern": "x"}]
        blocks = reflex_check("", scars)
        assert blocks == []


# ============================================================================
# Scar recording and loading
# ============================================================================

class TestScarStorage:
    def test_record_and_load(self, tmp_path):
        scar_file = str(tmp_path / "review_scars.jsonl")
        entry = record_miss(
            what_missed="Missed buffer overflow",
            pattern=r"strcpy\(",
            severity="critical",
            scar_file=scar_file,
        )
        assert entry["id"].startswith("rscar_")
        assert entry["severity"] == "critical"

        scars = load_review_scars(scar_file)
        assert len(scars) == 1
        assert scars[0]["what_missed"] == "Missed buffer overflow"

    def test_invalid_severity(self, tmp_path):
        scar_file = str(tmp_path / "review_scars.jsonl")
        with pytest.raises(ValueError, match="Invalid severity"):
            record_miss("x", "y", severity="extreme", scar_file=scar_file)

    def test_load_nonexistent_file(self):
        scars = load_review_scars("/tmp/nonexistent_review_scars_xyz.jsonl")
        assert scars == []

    def test_multiple_scars(self, tmp_path):
        scar_file = str(tmp_path / "review_scars.jsonl")
        record_miss("miss1", "pat1", "warning", scar_file)
        record_miss("miss2", "pat2", "critical", scar_file)
        scars = load_review_scars(scar_file)
        assert len(scars) == 2


# ============================================================================
# Integration: review() with scars
# ============================================================================

class TestIntegration:
    def test_review_with_scar_match(self, tmp_path):
        # Create a source file with an eval
        src = _write_temp_file("result = eval(user_input)\n")
        # Create a scar that also matches
        scar_file = str(tmp_path / "review_scars.jsonl")
        record_miss("Missed eval injection", r"\beval\s*\(", "critical", scar_file)

        findings = review(src, scar_file=scar_file)
        dimensions = {f["dimension"] for f in findings}
        assert "security" in dimensions
        assert "scar" in dimensions
        os.unlink(src)

    def test_review_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            review("/tmp/nonexistent_file_xyz.py")


# ============================================================================
# CLI
# ============================================================================

class TestCLI:
    def test_cli_review(self):
        src = _write_temp_file('password = "hunter2"\n')
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "scar_code_review.py"),
             "review", src],
            capture_output=True, text=True,
        )
        assert "secret" in result.stdout.lower() or "credential" in result.stdout.lower()
        os.unlink(src)

    def test_cli_record_miss_and_list(self, tmp_path):
        scar_file = str(tmp_path / "review_scars.jsonl")
        script = str(Path(__file__).parent / "scar_code_review.py")

        # Record
        result = subprocess.run(
            [sys.executable, script, "--scar-file", scar_file,
             "record-miss", "--what-missed", "test miss",
             "--pattern", "test.*pattern", "--severity", "high"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "SCAR RECORDED" in result.stdout

        # List
        result = subprocess.run(
            [sys.executable, script, "--scar-file", scar_file, "list-scars"],
            capture_output=True, text=True,
        )
        assert "test miss" in result.stdout

    def test_cli_no_command(self):
        script = str(Path(__file__).parent / "scar_code_review.py")
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True,
        )
        assert result.returncode == 1


# ============================================================================
# Keyword extraction
# ============================================================================

class TestKeywords:
    def test_english_keywords(self):
        kws = _extract_keywords("Missed SQL injection in user handler")
        assert "Missed" in kws
        assert "SQL" in kws
        assert "injection" in kws

    def test_short_words_excluded(self):
        kws = _extract_keywords("an ok XSS in a db")
        # "an", "ok", "in", "a", "db" are <3 chars
        assert "XSS" in kws
        assert "an" not in kws
