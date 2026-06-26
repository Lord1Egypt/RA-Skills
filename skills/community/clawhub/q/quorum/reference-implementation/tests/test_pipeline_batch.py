"""Layer 2b: Integration tests for batch/multi-file validation (mocked LLM)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    CriticResult,
    FileResult,
    Verdict,
    VerdictStatus,
)
from quorum.pipeline import (
    _aggregate_batch,
    resolve_targets,
    run_batch_validation,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def quick_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="m1",
        model_tier2="m2",
        depth_profile="quick",
        enable_prescreen=True,
    )


def _make_file_result(path: str, status: VerdictStatus, n_findings: int = 0) -> FileResult:
    from quorum.models import Evidence, Finding, Severity
    findings = [
        Finding(severity=Severity.MEDIUM, description=f"f{i}", evidence=Evidence(tool="t", result="r"))
        for i in range(n_findings)
    ]
    report = AggregatedReport(findings=findings, confidence=0.8)
    verdict = Verdict(status=status, reasoning="test", confidence=0.8, report=report)
    return FileResult(file_path=path, verdict=verdict, run_dir="/tmp/run")


# ── Batch aggregation ────────────────────────────────────────────────────────


class TestBatchAggregation:
    def test_all_pass(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS),
            _make_file_result("b.md", VerdictStatus.PASS),
        ]
        bv = _aggregate_batch(results, [])
        assert bv.status == VerdictStatus.PASS
        assert bv.files_passed == 2
        assert bv.files_failed == 0

    def test_worst_case_wins(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS),
            _make_file_result("b.md", VerdictStatus.REVISE, n_findings=2),
        ]
        bv = _aggregate_batch(results, [])
        assert bv.status == VerdictStatus.REVISE

    def test_reject_worst(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS),
            _make_file_result("b.md", VerdictStatus.REJECT, n_findings=3),
        ]
        bv = _aggregate_batch(results, [])
        assert bv.status == VerdictStatus.REJECT

    def test_empty_results_reject(self):
        bv = _aggregate_batch([], [])
        assert bv.status == VerdictStatus.REJECT

    def test_total_findings_summed(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS, n_findings=2),
            _make_file_result("b.md", VerdictStatus.PASS, n_findings=3),
        ]
        bv = _aggregate_batch(results, [])
        assert bv.total_findings == 5

    def test_confidence_averaged(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS),
            _make_file_result("b.md", VerdictStatus.PASS),
        ]
        bv = _aggregate_batch(results, [])
        assert 0.0 <= bv.confidence <= 1.0

    def test_errors_counted(self):
        results = [_make_file_result("a.md", VerdictStatus.PASS)]
        errors = [{"file": "b.md", "error": "Failed to load"}]
        bv = _aggregate_batch(results, errors)
        assert bv.total_files == 2
        assert "failed to process" in bv.reasoning.lower()

    def test_reasoning_summary(self):
        results = [
            _make_file_result("a.md", VerdictStatus.PASS),
            _make_file_result("b.md", VerdictStatus.REVISE, n_findings=1),
        ]
        bv = _aggregate_batch(results, [])
        assert "2 files validated" in bv.reasoning
        assert "1 need work" in bv.reasoning


# ── Resolve targets for batch ────────────────────────────────────────────────


class TestBatchResolveTargets:
    def test_resolve_directory(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        (tmp_path / "b.md").write_text("b")
        result = resolve_targets(tmp_path)
        assert len(result) == 2

    def test_resolve_with_pattern(self, tmp_path):
        (tmp_path / "a.md").write_text("a")
        (tmp_path / "b.py").write_text("b")
        result = resolve_targets(tmp_path, pattern="*.md")
        assert len(result) == 1

    def test_empty_dir_returns_empty(self, tmp_path):
        result = resolve_targets(tmp_path)
        assert result == []


# ── Batch validation end-to-end (mocked) ─────────────────────────────────────


class TestBatchValidation:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_batch_two_files(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        mock_provider = MagicMock()
        MockProvider.return_value = mock_provider

        cr = CriticResult(critic_name="correctness", findings=[], confidence=0.9, runtime_ms=50)
        MockSupervisor.return_value.run = MagicMock(return_value=[cr])

        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="OK",
            confidence=0.9,
            report=AggregatedReport(findings=[], confidence=0.9),
        )
        MockAggregator.return_value.run = MagicMock(return_value=verdict)

        # Create test files
        test_dir = tmp_path / "input"
        test_dir.mkdir()
        (test_dir / "a.md").write_text("# File A\n\nContent.\n")
        (test_dir / "b.md").write_text("# File B\n\nContent.\n")

        batch_verdict, batch_dir = run_batch_validation(
            target=test_dir,
            pattern="*.md",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert isinstance(batch_verdict, BatchVerdict)
        assert batch_verdict.total_files >= 2

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_batch_single_file_delegates(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        mock_provider = MagicMock()
        MockProvider.return_value = mock_provider

        cr = CriticResult(critic_name="correctness", findings=[], confidence=0.9, runtime_ms=50)
        MockSupervisor.return_value.run = MagicMock(return_value=[cr])

        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="OK",
            confidence=0.9,
            report=AggregatedReport(findings=[], confidence=0.9),
        )
        MockAggregator.return_value.run = MagicMock(return_value=verdict)

        target = tmp_path / "single.md"
        target.write_text("# Single\n")

        batch_verdict, _ = run_batch_validation(
            target=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert batch_verdict.total_files == 1

    def test_batch_no_files_raises(self, quick_config, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(FileNotFoundError, match="No validatable files"):
            run_batch_validation(
                target=empty_dir,
                pattern="*.xyz",
                config=quick_config,
                runs_dir=tmp_path / "runs",
            )
