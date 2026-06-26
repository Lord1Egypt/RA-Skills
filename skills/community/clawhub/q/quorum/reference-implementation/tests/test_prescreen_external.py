"""Tests for external tool integrations in PreScreen: Ruff, Bandit, PSScriptAnalyzer."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.models import Severity
from quorum.prescreen import PreScreen


@pytest.fixture
def ps() -> PreScreen:
    return PreScreen()


# ── Sample JSON payloads ────────────────────────────────────────────────────

RUFF_JSON_ONE_FINDING = json.dumps([
    {
        "code": "S101",
        "message": "Use of `assert` detected",
        "location": {"row": 10, "column": 4},
        "filename": "test.py",
        "url": "https://docs.astral.sh/ruff/rules/assert/",
    }
])

RUFF_JSON_HIGH_SEVERITY = json.dumps([
    {
        "code": "S301",
        "message": "Use of `pickle` detected",
        "location": {"row": 5, "column": 0},
        "filename": "test.py",
        "url": "https://docs.astral.sh/ruff/rules/suspicious-pickle-usage/",
    }
])

RUFF_JSON_EMPTY = "[]"

BANDIT_JSON_ONE_FINDING = json.dumps({
    "errors": [],
    "generated_at": "2026-01-01T00:00:00Z",
    "metrics": {},
    "results": [
        {
            "code": "subprocess.call(cmd, shell=True)\n",
            "col_offset": 0,
            "filename": "test.py",
            "issue_confidence": "HIGH",
            "issue_cwe": {"id": 78, "link": "https://cwe.mitre.org/data/definitions/78.html"},
            "issue_severity": "HIGH",
            "issue_text": "Use of subprocess.call with shell=True",
            "line_number": 15,
            "line_range": [15],
            "more_info": "https://bandit.readthedocs.io/en/latest/plugins/b602.html",
            "test_id": "B602",
            "test_name": "subprocess_popen_with_shell_equals_true",
        }
    ],
})

BANDIT_JSON_MEDIUM = json.dumps({
    "errors": [],
    "generated_at": "2026-01-01T00:00:00Z",
    "metrics": {},
    "results": [
        {
            "col_offset": 0,
            "filename": "test.py",
            "issue_confidence": "MEDIUM",
            "issue_cwe": {},
            "issue_severity": "MEDIUM",
            "issue_text": "Possible hardcoded password",
            "line_number": 3,
            "line_range": [3],
            "more_info": "",
            "test_id": "B105",
            "test_name": "hardcoded_password_string",
        }
    ],
})

BANDIT_JSON_LOW = json.dumps({
    "errors": [],
    "generated_at": "2026-01-01T00:00:00Z",
    "metrics": {},
    "results": [
        {
            "col_offset": 0,
            "filename": "test.py",
            "issue_confidence": "LOW",
            "issue_cwe": {},
            "issue_severity": "LOW",
            "issue_text": "Consider using assert_called_with",
            "line_number": 7,
            "line_range": [7],
            "more_info": "",
            "test_id": "B101",
            "test_name": "assert_used",
        }
    ],
})

BANDIT_JSON_EMPTY = json.dumps({
    "errors": [],
    "generated_at": "2026-01-01T00:00:00Z",
    "metrics": {},
    "results": [],
})

PSSA_JSON_ONE_FINDING = json.dumps([
    {
        "RuleName": "AvoidUsingInvokeExpression",
        "Severity": "Warning",
        "ScriptName": "test.ps1",
        "Line": 12,
        "Column": 1,
        "Message": "The use of Invoke-Expression is limited to avoid script injection attacks.",
    }
])

PSSA_JSON_ERROR_SEVERITY = json.dumps([
    {
        "RuleName": "AvoidUsingConvertToSecureStringWithPlainText",
        "Severity": "Error",
        "ScriptName": "test.ps1",
        "Line": 8,
        "Column": 1,
        "Message": "Plain text is used in a parameter of type SecureString.",
    }
])

PSSA_JSON_NON_SECURITY_RULE = json.dumps([
    {
        "RuleName": "PSAlignAssignmentStatement",
        "Severity": "Warning",
        "ScriptName": "test.ps1",
        "Line": 3,
        "Column": 1,
        "Message": "Align assignment statements in a hashtable.",
    }
])

PSSA_JSON_EMPTY = "[]"

PSSA_JSON_SINGLE_OBJECT = json.dumps({
    "RuleName": "AvoidUsingPlainTextForPassword",
    "Severity": "Warning",
    "ScriptName": "test.ps1",
    "Line": 6,
    "Column": 1,
    "Message": "Parameter '...' should use SecureString.",
})


# ── _run_ruff unit tests ─────────────────────────────────────────────────────


class TestRunRuff:
    def test_ruff_finding_converted_to_finding_object(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("assert True\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = RUFF_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
            findings = ps._run_ruff(f, f.read_text())
        assert len(findings) == 1
        assert findings[0].critic == "ruff"
        assert findings[0].location == "line 10"
        assert "S101" in findings[0].description

    def test_ruff_uses_select_s_flag(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = RUFF_JSON_EMPTY
        mock_result.stderr = ""
        with patch("quorum.prescreen.subprocess.run", return_value=mock_result) as mock_run:
            ps._run_ruff(f, f.read_text())
        call_args = mock_run.call_args[0][0]
        assert "--select" in call_args
        assert "S" in call_args

    def test_ruff_s1xx_maps_to_medium(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("assert True\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = RUFF_JSON_ONE_FINDING  # code S101
        mock_result.stderr = ""
        with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
            findings = ps._run_ruff(f, f.read_text())
        assert findings[0].severity == Severity.MEDIUM

    def test_ruff_s2xx_maps_to_high(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("import pickle\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = RUFF_JSON_HIGH_SEVERITY  # code S301
        mock_result.stderr = ""
        with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
            findings = ps._run_ruff(f, f.read_text())
        assert findings[0].severity == Severity.HIGH

    def test_ruff_skips_non_py_files(self, ps, tmp_path):
        f = tmp_path / "t.js"
        f.write_text("const x = 1;\n")
        findings = ps._run_ruff(f, f.read_text())
        assert findings == []

    def test_ruff_graceful_degradation_not_installed(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        with patch("quorum.prescreen.subprocess.run", side_effect=FileNotFoundError):
            findings = ps._run_ruff(f, f.read_text())
        assert findings == []

    def test_ruff_returns_empty_on_clean_file(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = RUFF_JSON_EMPTY
        mock_result.stderr = ""
        with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
            findings = ps._run_ruff(f, f.read_text())
        assert findings == []


# ── _run_bandit unit tests ───────────────────────────────────────────────────


class TestRunBandit:
    def test_bandit_high_severity_finding(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("import subprocess\nsubprocess.call(cmd, shell=True)\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = BANDIT_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert len(findings) == 1
        assert findings[0].severity == Severity.HIGH
        assert findings[0].critic == "bandit"
        assert "B602" in findings[0].description
        assert findings[0].location == "line 15"

    def test_bandit_medium_severity(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("password = 'secret'\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = BANDIT_JSON_MEDIUM
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert findings[0].severity == Severity.MEDIUM

    def test_bandit_low_severity(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("assert True\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = BANDIT_JSON_LOW
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert findings[0].severity == Severity.LOW

    def test_bandit_confidence_in_evidence(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("import subprocess\nsubprocess.call(cmd, shell=True)\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = BANDIT_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert "HIGH" in findings[0].evidence.result  # confidence is HIGH

    def test_bandit_cwe_in_framework_refs(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("import subprocess\nsubprocess.call(cmd, shell=True)\n")
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = BANDIT_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert "CWE-78" in findings[0].framework_refs

    def test_bandit_empty_results(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = BANDIT_JSON_EMPTY
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/local/bin/bandit"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_bandit(f, f.read_text())
        assert findings == []

    def test_bandit_skips_non_py_files(self, ps, tmp_path):
        f = tmp_path / "t.js"
        f.write_text("const x = 1;\n")
        findings = ps._run_bandit(f, f.read_text())
        assert findings == []

    def test_bandit_graceful_degradation_not_installed(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        with patch("quorum.prescreen.shutil.which", return_value=None):
            findings = ps._run_bandit(f, f.read_text())
        assert findings == []


# ── _run_pssa unit tests ─────────────────────────────────────────────────────


class TestRunPssa:
    def test_pssa_finding_converted_correctly(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Invoke-Expression $userInput\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert len(findings) == 1
        assert findings[0].critic == "pssa"
        assert findings[0].severity == Severity.MEDIUM
        assert findings[0].location == "line 12"
        assert "AvoidUsingInvokeExpression" in findings[0].description

    def test_pssa_error_severity_maps_to_high(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("$ss = ConvertTo-SecureString 'plaintext'\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_ERROR_SEVERITY
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert findings[0].severity == Severity.HIGH

    def test_pssa_filters_non_security_rules(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("$x = 1\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_NON_SECURITY_RULE
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert findings == []

    def test_pssa_handles_single_object_output(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("param([string]$password)\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_SINGLE_OBJECT
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert len(findings) == 1
        assert "AvoidUsingPlainTextForPassword" in findings[0].description

    def test_pssa_empty_results(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Write-Host 'hello'\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_EMPTY
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert findings == []

    def test_pssa_skips_non_ps1_files(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        findings = ps._run_pssa(f, f.read_text())
        assert findings == []

    def test_pssa_graceful_degradation_not_installed(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Write-Host 'hello'\n")
        with patch("quorum.prescreen.shutil.which", return_value=None):
            findings = ps._run_pssa(f, f.read_text())
        assert findings == []

    def test_pssa_framework_refs_contain_rule_name(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Invoke-Expression $userInput\n")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = PSSA_JSON_ONE_FINDING
        mock_result.stderr = ""
        with patch("quorum.prescreen.shutil.which", return_value="/usr/bin/pwsh"):
            with patch("quorum.prescreen.subprocess.run", return_value=mock_result):
                findings = ps._run_pssa(f, f.read_text())
        assert any("AvoidUsingInvokeExpression" in ref for ref in findings[0].framework_refs)


# ── Deduplication tests ───────────────────────────────────────────────────────


class TestDeduplication:
    def test_bandit_skipped_when_ruff_installed(self, ps, tmp_path):
        """When ruff is available, Bandit should not run for .py files."""
        f = tmp_path / "t.py"
        f.write_text("assert True\n")
        ruff_result = MagicMock()
        ruff_result.returncode = 1
        ruff_result.stdout = RUFF_JSON_ONE_FINDING
        ruff_result.stderr = ""

        def mock_which(cmd):
            return "/usr/local/bin/ruff" if cmd == "ruff" else None

        with patch("quorum.prescreen.shutil.which", side_effect=mock_which):
            with patch("quorum.prescreen.subprocess.run", return_value=ruff_result) as mock_run:
                result = ps.run(f, f.read_text())

        # Bandit should not have been invoked
        for call in mock_run.call_args_list:
            cmd = call[0][0]
            assert "bandit" not in cmd[0], "Bandit should not run when Ruff is available"

        # Ruff findings should appear
        ruff_check_ids = [c.id for c in result.checks if "RUFF" in c.id]
        assert ruff_check_ids

    def test_bandit_runs_when_ruff_not_installed(self, ps, tmp_path):
        """When ruff is not available, Bandit should run for .py files."""
        f = tmp_path / "t.py"
        f.write_text("import subprocess\nsubprocess.call(cmd, shell=True)\n")
        bandit_result = MagicMock()
        bandit_result.returncode = 1
        bandit_result.stdout = BANDIT_JSON_ONE_FINDING
        bandit_result.stderr = ""

        def mock_which(cmd):
            if cmd == "ruff":
                return None  # ruff not installed
            if cmd == "bandit":
                return "/usr/local/bin/bandit"
            return None

        # _run_ruff raises FileNotFoundError when ruff is not found (subprocess)
        def side_effect_subprocess(*args, **kwargs):
            cmd = args[0]
            if cmd[0] == "ruff":
                raise FileNotFoundError
            return bandit_result

        with patch("quorum.prescreen.shutil.which", side_effect=mock_which):
            with patch("quorum.prescreen.subprocess.run", side_effect=side_effect_subprocess):
                result = ps.run(f, f.read_text())

        bandit_check_ids = [c.id for c in result.checks if "BANDIT" in c.id]
        assert bandit_check_ids


# ── File extension filtering integration tests ───────────────────────────────


class TestFileExtensionFiltering:
    def test_ruff_and_bandit_skip_ps1_files(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Write-Host 'hello'\n")

        def mock_which(cmd):
            return None  # no tools installed

        with patch("quorum.prescreen.shutil.which", side_effect=mock_which):
            result = ps.run(f, f.read_text())

        # Ruff/Bandit checks for .ps1 should be PASS (skipped due to extension), never FAIL
        for c in result.checks:
            if "RUFF" in c.id or "BANDIT" in c.id:
                assert c.result in ("PASS", "SKIP"), (
                    f"Expected PASS/SKIP for {c.id} on non-py file, got {c.result}"
                )

    def test_pssa_skips_py_files(self, ps, tmp_path):
        f = tmp_path / "t.py"
        f.write_text("x = 1\n")
        ruff_result = MagicMock()
        ruff_result.returncode = 0
        ruff_result.stdout = RUFF_JSON_EMPTY
        ruff_result.stderr = ""

        def mock_which(cmd):
            if cmd == "ruff":
                return "/usr/local/bin/ruff"
            return None

        with patch("quorum.prescreen.shutil.which", side_effect=mock_which):
            with patch("quorum.prescreen.subprocess.run", return_value=ruff_result):
                result = ps.run(f, f.read_text())

        # No PSSA checks for .py files
        for c in result.checks:
            assert "PSSA" not in c.id

    def test_pssa_runs_for_ps1_files(self, ps, tmp_path):
        f = tmp_path / "t.ps1"
        f.write_text("Invoke-Expression $userInput\n")
        pssa_result = MagicMock()
        pssa_result.returncode = 0
        pssa_result.stdout = PSSA_JSON_ONE_FINDING
        pssa_result.stderr = ""

        def mock_which(cmd):
            return "/usr/bin/pwsh" if cmd == "pwsh" else None

        with patch("quorum.prescreen.shutil.which", side_effect=mock_which):
            with patch("quorum.prescreen.subprocess.run", return_value=pssa_result):
                result = ps.run(f, f.read_text())

        pssa_check_ids = [c.id for c in result.checks if "PSSA" in c.id]
        assert pssa_check_ids
