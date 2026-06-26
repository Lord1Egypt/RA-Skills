"""Unit tests for the output formatter module."""

from __future__ import annotations

from io import StringIO
from unittest.mock import patch

import pytest

from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    Evidence,
    FileResult,
    Finding,
    PreScreenCheck,
    PreScreenResult,
    Severity,
    Verdict,
    VerdictStatus,
)
from quorum.output import (
    print_error,
    print_prescreen_summary,
    print_rubric_list,
    print_verdict,
    print_warning,
)


def _make_verdict(status=VerdictStatus.PASS, findings=None):
    report = AggregatedReport(
        findings=findings or [],
        confidence=0.9,
    )
    return Verdict(
        status=status,
        reasoning="Test verdict reasoning",
        confidence=0.9,
        report=report,
    )


def _make_finding(severity=Severity.MEDIUM, description="Test finding"):
    return Finding(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result="found match"),
        critic="correctness",
    )


# ── print_verdict ────────────────────────────────────────────────────────────


class TestPrintVerdict:
    def test_print_pass_verdict(self, capsys):
        v = _make_verdict(VerdictStatus.PASS)
        print_verdict(v)
        captured = capsys.readouterr()
        assert "PASS" in captured.out

    def test_print_reject_verdict(self, capsys):
        v = _make_verdict(VerdictStatus.REJECT, findings=[_make_finding(Severity.CRITICAL)])
        print_verdict(v)
        captured = capsys.readouterr()
        assert "REJECT" in captured.out

    def test_verbose_mode(self, capsys):
        findings = [_make_finding(Severity.LOW, "Low severity issue")]
        v = _make_verdict(VerdictStatus.PASS_WITH_NOTES, findings=findings)
        print_verdict(v, verbose=True)
        captured = capsys.readouterr()
        assert "Low severity issue" in captured.out or "PASS_WITH_NOTES" in captured.out


# ── print_prescreen_summary ──────────────────────────────────────────────────


class TestPrintPrescreenSummary:
    def test_print_summary(self, capsys):
        result = PreScreenResult(
            checks=[
                PreScreenCheck(
                    id="PS-001", name="hardcoded_paths", category="security",
                    severity=Severity.HIGH, description="Found paths", result="FAIL",
                    evidence="L1: /Users/x", locations=["line 1"],
                ),
                PreScreenCheck(
                    id="PS-008", name="todo_markers", category="structure",
                    severity=Severity.INFO, description="No TODOs", result="PASS",
                ),
            ],
            total_checks=2, passed=1, failed=1, skipped=0, runtime_ms=5,
        )
        print_prescreen_summary(result)
        captured = capsys.readouterr()
        assert "PS-001" in captured.out or "prescreen" in captured.out.lower()


# ── print_rubric_list ────────────────────────────────────────────────────────


class TestPrintRubricList:
    def test_print_list(self, capsys):
        print_rubric_list(["research-synthesis", "agent-config", "python-code"])
        captured = capsys.readouterr()
        assert "research-synthesis" in captured.out

    def test_print_empty(self, capsys):
        print_rubric_list([])
        # Should not crash


# ── print_error / print_warning ──────────────────────────────────────────────


class TestPrintMessages:
    def test_print_error(self, capsys):
        print_error("Something went wrong")
        captured = capsys.readouterr()
        assert "Something went wrong" in captured.err

    def test_print_warning(self, capsys):
        print_warning("Watch out")
        captured = capsys.readouterr()
        assert "Watch out" in captured.err or "Watch out" in captured.out
