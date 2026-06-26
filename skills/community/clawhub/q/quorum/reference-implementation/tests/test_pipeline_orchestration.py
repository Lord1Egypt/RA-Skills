"""Phase 2: Pipeline orchestration tests — phase coordination, gating, integration."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    CriticResult,
    Evidence,
    FileResult,
    Finding,
    FixProposal,
    FixReport,
    Severity,
    Verdict,
    VerdictStatus,
)
from quorum.pipeline import (
    _aggregate_batch,
    _create_run_dir,
    _format_findings_by_severity,
    _select_rubric,
    _write_json,
    _write_report,
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


@pytest.fixture
def config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-model",
        model_tier2="test-model",
        depth_profile="quick",
        enable_prescreen=True,
    )


@pytest.fixture
def rubric():
    from quorum.models import Rubric, RubricCriterion
    return Rubric(
        name="test-rubric",
        domain="test",
        version="1.0",
        criteria=[
            RubricCriterion(
                id="T-001",
                criterion="Test",
                severity=Severity.MEDIUM,
                evidence_required="any",
                why="testing",
            ),
        ],
    )


# ── Create Run Dir ────────────────────────────────────────────────────────────


class TestCreateRunDir:
    def test_creates_directory(self, tmp_path):
        run_dir = _create_run_dir(tmp_path, Path("test.md"))
        assert run_dir.exists()
        assert (run_dir / "critics").exists()

    def test_directory_name_contains_stem(self, tmp_path):
        run_dir = _create_run_dir(tmp_path, Path("my-artifact.md"))
        assert "my-artifact" in run_dir.name

    def test_directory_name_has_timestamp(self, tmp_path):
        run_dir = _create_run_dir(tmp_path, Path("test.md"))
        # Format: YYYYMMDD-HHMMSS-stem
        parts = run_dir.name.split("-")
        assert len(parts[0]) == 8  # YYYYMMDD
        assert parts[0].isdigit()


# ── Select Rubric ─────────────────────────────────────────────────────────────


class TestSelectRubric:
    def test_explicit_rubric_name(self, config):
        from quorum.rubrics.loader import RubricLoader
        loader = RubricLoader()
        builtins = loader.list_builtin()
        if builtins:
            rubric = _select_rubric(loader, builtins[0], Path("test.md"), "text", config)
            assert rubric is not None
            assert rubric.name  # has a non-empty name

    def test_auto_detect_python(self, config):
        from quorum.rubrics.loader import RubricLoader
        loader = RubricLoader()
        # Should try python-code rubric
        try:
            rubric = _select_rubric(loader, None, Path("code.py"), "def foo(): pass", config)
            assert rubric is not None
        except (FileNotFoundError, RuntimeError):
            pytest.skip("No python-code rubric available")

    def test_auto_detect_research(self, config):
        from quorum.rubrics.loader import RubricLoader
        loader = RubricLoader()
        research_text = "abstract methodology findings hypothesis study results"
        try:
            rubric = _select_rubric(loader, None, Path("paper.md"), research_text, config)
            assert rubric is not None
        except (FileNotFoundError, RuntimeError):
            pytest.skip("No research rubric available")

    def test_fallback_to_first_builtin(self, config):
        from quorum.rubrics.loader import RubricLoader
        loader = RubricLoader()
        builtins = loader.list_builtin()
        if not builtins:
            pytest.skip("No built-in rubrics")
        rubric = _select_rubric(loader, None, Path("file.xyz"), "random content", config)
        assert rubric is not None


# ── Aggregate Batch ───────────────────────────────────────────────────────────


class TestAggregateBatch:
    def test_no_results_returns_reject(self):
        batch = _aggregate_batch([], [])
        assert batch.status == VerdictStatus.REJECT
        assert "No files" in batch.reasoning

    def test_all_pass(self):
        fr1 = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.PASS),
            run_dir="/tmp/run1",
        )
        fr2 = FileResult(
            file_path="b.md",
            verdict=make_verdict(VerdictStatus.PASS),
            run_dir="/tmp/run2",
        )
        batch = _aggregate_batch([fr1, fr2], [])
        assert batch.status == VerdictStatus.PASS
        assert batch.files_passed == 2
        assert batch.files_failed == 0

    def test_worst_status_wins(self):
        fr_pass = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.PASS),
            run_dir="/tmp/run1",
        )
        fr_reject = FileResult(
            file_path="b.md",
            verdict=make_verdict(VerdictStatus.REJECT, [make_finding(severity=Severity.CRITICAL)]),
            run_dir="/tmp/run2",
        )
        batch = _aggregate_batch([fr_pass, fr_reject], [])
        assert batch.status == VerdictStatus.REJECT

    def test_total_findings_counted(self):
        findings = [make_finding(), make_finding()]
        fr = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.REVISE, findings),
            run_dir="/tmp/run1",
        )
        batch = _aggregate_batch([fr], [])
        assert batch.total_findings == 2

    def test_errors_in_reasoning(self):
        fr = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.PASS),
            run_dir="/tmp/run1",
        )
        errors = [{"file": "bad.md", "error": "parse error"}]
        batch = _aggregate_batch([fr], errors)
        assert "failed to process" in batch.reasoning

    def test_confidence_averaged(self):
        fr1 = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.PASS, confidence=0.8),
            run_dir="/tmp/run1",
        )
        fr2 = FileResult(
            file_path="b.md",
            verdict=make_verdict(VerdictStatus.PASS, confidence=0.6),
            run_dir="/tmp/run2",
        )
        batch = _aggregate_batch([fr1, fr2], [])
        assert batch.confidence == pytest.approx(0.7, abs=0.01)

    def test_total_files_includes_errors(self):
        fr = FileResult(
            file_path="a.md",
            verdict=make_verdict(VerdictStatus.PASS),
            run_dir="/tmp/run1",
        )
        errors = [{"file": "b.md", "error": "err"}]
        batch = _aggregate_batch([fr], errors)
        assert batch.total_files == 2


# ── Format Findings by Severity ───────────────────────────────────────────────


class TestFormatFindingsBySeverity:
    def test_groups_by_severity(self):
        findings = [
            make_finding(severity=Severity.CRITICAL, description="Critical issue"),
            make_finding(severity=Severity.LOW, description="Low issue"),
        ]
        lines = _format_findings_by_severity(findings)
        text = "\n".join(lines)
        assert "CRITICAL" in text
        assert "LOW" in text

    def test_critical_before_low(self):
        findings = [
            make_finding(severity=Severity.LOW, description="Low issue"),
            make_finding(severity=Severity.CRITICAL, description="Critical issue"),
        ]
        lines = _format_findings_by_severity(findings)
        text = "\n".join(lines)
        crit_pos = text.index("CRITICAL")
        low_pos = text.index("LOW")
        assert crit_pos < low_pos

    def test_empty_findings(self):
        lines = _format_findings_by_severity([])
        assert lines == []

    def test_includes_evidence(self):
        findings = [make_finding(severity=Severity.HIGH, description="Issue")]
        lines = _format_findings_by_severity(findings)
        text = "\n".join(lines)
        assert "Evidence" in text

    def test_includes_loci(self):
        from quorum.models import Locus
        finding = make_finding(severity=Severity.HIGH, description="Cross issue")
        finding.loci = [
            Locus(file="spec.md", start_line=1, end_line=5, role="spec", source_hash="a" * 64),
        ]
        lines = _format_findings_by_severity([finding])
        text = "\n".join(lines)
        assert "spec.md" in text

    def test_includes_remediation(self):
        finding = make_finding(
            severity=Severity.HIGH,
            description="Issue",
            remediation="Fix it like this",
        )
        lines = _format_findings_by_severity([finding])
        text = "\n".join(lines)
        assert "Fix it like this" in text


# ── Write Report ──────────────────────────────────────────────────────────────


class TestWriteReport:
    def test_basic_report(self, tmp_path, config, rubric):
        verdict = make_verdict(VerdictStatus.PASS)
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("test.md"), rubric, config)
        text = path.read_text()
        assert "Quorum Validation Report" in text
        assert "PASS" in text
        assert "test.md" in text

    def test_report_with_findings(self, tmp_path, config, rubric):
        findings = [
            make_finding(severity=Severity.HIGH, description="Important issue"),
        ]
        verdict = make_verdict(VerdictStatus.REVISE, findings)
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("code.py"), rubric, config)
        text = path.read_text()
        assert "REVISE" in text
        assert "Important issue" in text

    def test_report_with_fix_proposals(self, tmp_path, config, rubric):
        verdict = make_verdict(VerdictStatus.REVISE, [make_finding(severity=Severity.HIGH)])
        fix_report = FixReport(
            proposals=[
                FixProposal(
                    finding_id="F-test",
                    finding_description="Bug in code",
                    file_path="test.py",
                    original_text="old code",
                    replacement_text="new code",
                    explanation="Fixes the bug",
                    confidence=0.9,
                ),
            ],
            findings_addressed=1,
            findings_skipped=0,
        )
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("test.py"), rubric, config, fix_report=fix_report)
        text = path.read_text()
        assert "Fix Proposals" in text
        assert "old code" in text
        assert "new code" in text
        assert "90%" in text

    def test_report_no_findings(self, tmp_path, config, rubric):
        verdict = make_verdict(VerdictStatus.PASS)
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("clean.md"), rubric, config)
        text = path.read_text()
        assert "No issues found" in text

    def test_report_summary_table(self, tmp_path, config, rubric):
        findings = [
            make_finding(severity=Severity.HIGH),
            make_finding(severity=Severity.MEDIUM),
        ]
        verdict = make_verdict(VerdictStatus.REVISE, findings)
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("test.md"), rubric, config)
        text = path.read_text()
        assert "Summary" in text
        assert "CRITICAL" in text
        assert "HIGH" in text

    def test_report_uses_relative_path(self, tmp_path, config, rubric):
        verdict = make_verdict(VerdictStatus.PASS)
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("/absolute/path/test.md"), rubric, config)
        text = path.read_text()
        # Should use just the filename for absolute paths
        assert "test.md" in text

    def test_report_fix_skip_reasons(self, tmp_path, config, rubric):
        verdict = make_verdict(VerdictStatus.REVISE, [make_finding(severity=Severity.HIGH)])
        fix_report = FixReport(
            proposals=[
                FixProposal(
                    finding_id="F-1",
                    finding_description="Issue",
                    file_path="test.py",
                    original_text="old",
                    replacement_text="new",
                    explanation="fix",
                    confidence=0.9,
                ),
            ],
            findings_addressed=1,
            findings_skipped=1,
            skip_reasons=["Could not fix architectural issue"],
        )
        path = tmp_path / "report.md"
        _write_report(path, verdict, Path("test.py"), rubric, config, fix_report=fix_report)
        text = path.read_text()
        assert "Skipped" in text
        assert "architectural issue" in text


# ── Pipeline Phase Coordination (mocked end-to-end) ──────────────────────────


class TestPipelinePhaseCoordination:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.RubricLoader")
    def test_prescreen_disabled(self, MockLoader, MockProvider, tmp_path):
        from quorum.pipeline import _run_prescreen

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test", model_tier2="test",
            depth_profile="quick",
            enable_prescreen=False,
        )
        target = tmp_path / "test.md"
        target.write_text("# Hello")
        run_dir = tmp_path / "run"
        run_dir.mkdir()

        result = _run_prescreen(config, target, "# Hello", run_dir)
        assert result is None

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.RubricLoader")
    def test_prescreen_enabled(self, MockLoader, MockProvider, tmp_path):
        from quorum.pipeline import _run_prescreen

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test", model_tier2="test",
            depth_profile="quick",
            enable_prescreen=True,
        )
        target = tmp_path / "test.md"
        target.write_text("# Clean document\n\nNo issues here.\n")
        run_dir = tmp_path / "run"
        run_dir.mkdir()

        result = _run_prescreen(config, target, "# Clean document\n\nNo issues here.\n", run_dir)
        assert result is not None
        assert (run_dir / "prescreen.json").exists()

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.RubricLoader")
    def test_prescreen_failure_non_fatal(self, MockLoader, MockProvider, tmp_path):
        from quorum.pipeline import _run_prescreen
        from unittest.mock import patch as mock_patch

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test", model_tier2="test",
            depth_profile="quick",
            enable_prescreen=True,
        )
        run_dir = tmp_path / "run"
        run_dir.mkdir()

        # Force the prescreen to crash
        with mock_patch("quorum.prescreen.PreScreen", side_effect=RuntimeError("broken")):
            result = _run_prescreen(config, Path("test.md"), "text", run_dir)
        # Should return None, not crash
        assert result is None


# ── Write JSON Edge Cases ─────────────────────────────────────────────────────


class TestWriteJsonExtended:
    def test_datetime_serialized(self, tmp_path):
        path = tmp_path / "test.json"
        now = datetime.now(timezone.utc)
        _write_json(path, {"timestamp": now})
        data = json.loads(path.read_text())
        assert isinstance(data["timestamp"], str)

    def test_path_serialized(self, tmp_path):
        path = tmp_path / "test.json"
        _write_json(path, {"path": Path("/some/path")})
        data = json.loads(path.read_text())
        assert data["path"] == "/some/path"
