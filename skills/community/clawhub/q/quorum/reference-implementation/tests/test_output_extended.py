"""Phase 2: Extended output/report tests — color, formatting, batch, prescreen display."""

from __future__ import annotations

import os
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    CriticResult,
    Evidence,
    FileResult,
    Finding,
    Locus,
    PreScreenCheck,
    PreScreenResult,
    Severity,
    Verdict,
    VerdictStatus,
)
from quorum.output import (
    Color,
    _c,
    _print_finding,
    _severity_color,
    _supports_color,
    _verdict_color,
    print_batch_verdict,
    print_error,
    print_prescreen_summary,
    print_rubric_list,
    print_verdict,
    print_warning,
)


def make_finding(severity=Severity.MEDIUM, description="Test finding", critic="correctness", **kwargs):
    defaults = dict(
        severity=severity, description=description,
        evidence=Evidence(tool="grep", result="matched line 42"), critic=critic,
    )
    defaults.update(kwargs)
    return Finding(**defaults)


def make_verdict(status=VerdictStatus.PASS, findings=None, confidence=0.9):
    report = AggregatedReport(findings=findings or [], confidence=confidence, critic_results=[])
    return Verdict(status=status, reasoning="Test verdict", confidence=confidence, report=report)


# ── Supports Color ────────────────────────────────────────────────────────────


class TestSupportsColor:
    def test_non_tty_no_color(self):
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert _supports_color() is False

    def test_dumb_terminal_no_color(self):
        with patch.object(sys.stdout, "isatty", return_value=True):
            with patch.dict(os.environ, {"TERM": "dumb"}):
                assert _supports_color() is False

    def test_empty_term_no_color(self):
        with patch.object(sys.stdout, "isatty", return_value=True):
            with patch.dict(os.environ, {"TERM": ""}):
                assert _supports_color() is False

    def test_xterm_supports_color(self):
        with patch.object(sys.stdout, "isatty", return_value=True):
            with patch.dict(os.environ, {"TERM": "xterm-256color"}):
                assert _supports_color() is True


# ── Color Helper ──────────────────────────────────────────────────────────────


class TestColorHelper:
    def test_plain_text_when_no_color(self):
        with patch("quorum.output._supports_color", return_value=False):
            result = _c("hello", Color.RED)
            assert result == "hello"
            assert "\033" not in result

    def test_colored_text_when_supported(self):
        with patch("quorum.output._supports_color", return_value=True):
            result = _c("hello", Color.RED)
            assert Color.RED in result
            assert Color.RESET in result
            assert "hello" in result

    def test_multiple_codes(self):
        with patch("quorum.output._supports_color", return_value=True):
            result = _c("text", Color.BOLD, Color.RED)
            assert Color.BOLD in result
            assert Color.RED in result


# ── Severity Color ────────────────────────────────────────────────────────────


class TestSeverityColor:
    def test_critical(self):
        c = _severity_color(Severity.CRITICAL)
        assert Color.RED in c
        assert Color.BOLD in c

    def test_high(self):
        assert Color.RED in _severity_color(Severity.HIGH)

    def test_medium(self):
        assert Color.YELLOW in _severity_color(Severity.MEDIUM)

    def test_low(self):
        assert Color.CYAN in _severity_color(Severity.LOW)

    def test_info(self):
        assert Color.DIM in _severity_color(Severity.INFO)


# ── Verdict Color ─────────────────────────────────────────────────────────────


class TestVerdictColor:
    def test_pass(self):
        c = _verdict_color(VerdictStatus.PASS)
        assert Color.GREEN in c

    def test_pass_with_notes(self):
        c = _verdict_color(VerdictStatus.PASS_WITH_NOTES)
        assert Color.CYAN in c

    def test_revise(self):
        c = _verdict_color(VerdictStatus.REVISE)
        assert Color.YELLOW in c

    def test_reject(self):
        c = _verdict_color(VerdictStatus.REJECT)
        assert Color.RED in c


# ── Print Finding ─────────────────────────────────────────────────────────────


class TestPrintFinding:
    def test_basic_finding(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.HIGH,
                description="Important issue found",
            )
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "Important issue found" in output
            assert "HIGH" in output

    def test_finding_with_location(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.MEDIUM,
                description="Issue",
                location="line 42",
            )
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "line 42" in output

    def test_finding_with_loci(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(severity=Severity.HIGH, description="Cross issue")
            finding.loci = [
                Locus(file="spec.md", start_line=5, end_line=10, role="spec", source_hash="a" * 64),
                Locus(file="impl.py", start_line=20, end_line=30, role="impl", source_hash="b" * 64),
            ]
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "spec.md" in output
            assert "impl.py" in output

    def test_critical_always_shows_evidence(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.CRITICAL,
                description="Critical bug",
            )
            _print_finding(1, finding, verbose=False)
            output = capsys.readouterr().out
            assert "Evidence" in output

    def test_medium_hides_evidence_without_verbose(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.MEDIUM,
                description="Minor issue",
            )
            _print_finding(1, finding, verbose=False)
            output = capsys.readouterr().out
            assert "Evidence" not in output

    def test_medium_shows_evidence_with_verbose(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.MEDIUM,
                description="Minor issue",
            )
            _print_finding(1, finding, verbose=True)
            output = capsys.readouterr().out
            assert "Evidence" in output

    def test_finding_with_remediation(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.HIGH,
                description="Issue",
                remediation="Fix it like this",
            )
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "Fix" in output

    def test_finding_with_framework_refs(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = make_finding(
                severity=Severity.HIGH,
                description="Security issue",
            )
            finding.framework_refs = ["CWE-79", "OWASP-A7"]
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "CWE-79" in output

    def test_long_evidence_truncated(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            finding = Finding(
                severity=Severity.CRITICAL,
                description="Issue",
                evidence=Evidence(tool="grep", result="x" * 200),
                critic="test",
            )
            _print_finding(1, finding)
            output = capsys.readouterr().out
            assert "..." in output


# ── Print Verdict ─────────────────────────────────────────────────────────────


class TestPrintVerdict:
    def test_pass_verdict(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            verdict = make_verdict(VerdictStatus.PASS)
            print_verdict(verdict)
            output = capsys.readouterr().out
            assert "PASS" in output
            assert "No issues found" in output

    def test_reject_verdict_with_findings(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            findings = [
                make_finding(severity=Severity.CRITICAL, description="Fatal bug"),
                make_finding(severity=Severity.HIGH, description="Bad bug"),
            ]
            verdict = make_verdict(VerdictStatus.REJECT, findings)
            print_verdict(verdict)
            output = capsys.readouterr().out
            assert "REJECT" in output
            assert "Fatal bug" in output

    def test_verdict_with_run_dir(self, capsys, tmp_path):
        with patch("quorum.output._supports_color", return_value=False):
            verdict = make_verdict(VerdictStatus.PASS)
            print_verdict(verdict, run_dir=tmp_path)
            output = capsys.readouterr().out
            assert "Run directory" in output
            assert str(tmp_path) in output

    def test_verdict_no_report(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            verdict = Verdict(
                status=VerdictStatus.REJECT,
                reasoning="Aggregator failed",
                confidence=0.0,
                report=None,
            )
            print_verdict(verdict)
            output = capsys.readouterr().out
            assert "no report data" in output

    def test_verdict_with_prescreen(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            verdict = make_verdict(VerdictStatus.PASS)
            prescreen = PreScreenResult(
                checks=[
                    PreScreenCheck(
                        id="PS-001", name="hardcoded_paths", category="security",
                        severity=Severity.HIGH, description="No paths found",
                        result="PASS",
                    ),
                ],
                total_checks=1, passed=1, failed=0, skipped=0, runtime_ms=3,
            )
            print_verdict(verdict, prescreen=prescreen)
            output = capsys.readouterr().out
            assert "Pre-screen" in output

    def test_verdict_shows_conflicts_resolved(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            report = AggregatedReport(
                findings=[make_finding()],
                confidence=0.8,
                conflicts_resolved=3,
                critic_results=[],
            )
            verdict = Verdict(
                status=VerdictStatus.PASS_WITH_NOTES,
                reasoning="Notes",
                confidence=0.8,
                report=report,
            )
            print_verdict(verdict)
            output = capsys.readouterr().out
            assert "3 duplicate findings merged" in output

    def test_verdict_verbose_mode(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            findings = [
                make_finding(severity=Severity.LOW, description="Minor thing"),
            ]
            verdict = make_verdict(VerdictStatus.PASS_WITH_NOTES, findings)
            print_verdict(verdict, verbose=True)
            output = capsys.readouterr().out
            assert "Evidence" in output


# ── Print Pre-Screen Summary ──────────────────────────────────────────────────


class TestPrintPrescreenSummary:
    def test_all_pass(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            prescreen = PreScreenResult(
                checks=[
                    PreScreenCheck(
                        id="PS-001", name="paths", category="security",
                        severity=Severity.HIGH, description="No paths",
                        result="PASS",
                    ),
                ],
                total_checks=1, passed=1, failed=0, skipped=0, runtime_ms=2,
            )
            print_prescreen_summary(prescreen)
            output = capsys.readouterr().out
            assert "1/1 passed" in output

    def test_with_failures(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            prescreen = PreScreenResult(
                checks=[
                    PreScreenCheck(
                        id="PS-001", name="paths", category="security",
                        severity=Severity.HIGH, description="Found hardcoded paths",
                        result="FAIL", locations=["L5", "L10"],
                    ),
                    PreScreenCheck(
                        id="PS-002", name="creds", category="security",
                        severity=Severity.CRITICAL, description="No credentials",
                        result="PASS",
                    ),
                ],
                total_checks=2, passed=1, failed=1, skipped=0, runtime_ms=5,
            )
            print_prescreen_summary(prescreen)
            output = capsys.readouterr().out
            assert "1 failed" in output
            assert "PS-001" in output
            assert "L5" in output

    def test_with_skipped(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            prescreen = PreScreenResult(
                checks=[
                    PreScreenCheck(
                        id="PS-006", name="json_syntax", category="syntax",
                        severity=Severity.HIGH, description="Not JSON file",
                        result="SKIP",
                    ),
                ],
                total_checks=1, passed=0, failed=0, skipped=1, runtime_ms=1,
            )
            print_prescreen_summary(prescreen)
            output = capsys.readouterr().out
            assert "1 skipped" in output

    def test_many_locations_truncated(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            locs = [f"L{i}" for i in range(10)]
            prescreen = PreScreenResult(
                checks=[
                    PreScreenCheck(
                        id="PS-001", name="paths", category="security",
                        severity=Severity.HIGH, description="Many paths",
                        result="FAIL", locations=locs,
                    ),
                ],
                total_checks=1, passed=0, failed=1, skipped=0, runtime_ms=3,
            )
            print_prescreen_summary(prescreen)
            output = capsys.readouterr().out
            assert "L0" in output
            assert "L4" in output
            # More than 5 should show +more
            assert "+5 more" in output


# ── Print Batch Verdict ───────────────────────────────────────────────────────


class TestPrintBatchVerdict:
    def test_batch_pass(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            batch = BatchVerdict(
                status=VerdictStatus.PASS,
                file_results=[
                    FileResult(
                        file_path="a.md",
                        verdict=make_verdict(VerdictStatus.PASS),
                        run_dir="/tmp/run1",
                    ),
                ],
                total_files=1,
                confidence=0.9,
                reasoning="All good",
            )
            print_batch_verdict(batch)
            output = capsys.readouterr().out
            assert "BATCH VERDICT" in output
            assert "PASS" in output

    def test_batch_with_findings(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            findings = [make_finding(severity=Severity.HIGH, description="Important")]
            batch = BatchVerdict(
                status=VerdictStatus.REVISE,
                file_results=[
                    FileResult(
                        file_path="code.py",
                        verdict=make_verdict(VerdictStatus.REVISE, findings),
                        run_dir="/tmp/run1",
                    ),
                ],
                total_files=1,
                total_findings=1,
                confidence=0.8,
                reasoning="Needs work",
            )
            print_batch_verdict(batch)
            output = capsys.readouterr().out
            assert "Important" in output

    def test_batch_with_dir(self, capsys, tmp_path):
        with patch("quorum.output._supports_color", return_value=False):
            batch = BatchVerdict(
                status=VerdictStatus.PASS,
                file_results=[],
                total_files=0,
                confidence=0.0,
                reasoning="Empty",
            )
            print_batch_verdict(batch, batch_dir=tmp_path)
            output = capsys.readouterr().out
            assert "Batch directory" in output

    def test_batch_hidden_findings_note(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            findings = [
                make_finding(severity=Severity.LOW, description="Minor"),
            ]
            batch = BatchVerdict(
                status=VerdictStatus.PASS_WITH_NOTES,
                file_results=[
                    FileResult(
                        file_path="a.md",
                        verdict=make_verdict(VerdictStatus.PASS_WITH_NOTES, findings),
                        run_dir="/tmp/run1",
                    ),
                ],
                total_files=1,
                total_findings=1,
                confidence=0.8,
                reasoning="Notes",
            )
            print_batch_verdict(batch, verbose=False)
            output = capsys.readouterr().out
            assert "hidden" in output or "verbose" in output.lower()


# ── Print Rubric List ─────────────────────────────────────────────────────────


class TestPrintRubricList:
    def test_prints_names(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            print_rubric_list(["research-synthesis", "python-code"])
            output = capsys.readouterr().out
            assert "research-synthesis" in output
            assert "python-code" in output


# ── Print Error / Warning ─────────────────────────────────────────────────────


class TestPrintErrorWarning:
    def test_error_to_stderr(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            print_error("Something broke")
            output = capsys.readouterr().err
            assert "Something broke" in output

    def test_warning_to_stdout(self, capsys):
        with patch("quorum.output._supports_color", return_value=False):
            print_warning("Watch out")
            output = capsys.readouterr().out
            assert "Watch out" in output
