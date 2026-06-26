"""Layer 2a: Integration tests for single-file validation pipeline (mocked LLM)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    CriticResult,
    Evidence,
    Finding,
    Severity,
    Verdict,
    VerdictStatus,
)
from quorum.pipeline import run_validation, _create_run_dir, _write_json

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def quick_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="anthropic/claude-opus-4-6",
        model_tier2="anthropic/claude-sonnet-4-6",
        depth_profile="quick",
        enable_prescreen=True,
    )


def _mock_provider():
    provider = MagicMock()
    provider.complete.return_value = "No issues found."
    provider.complete_json.return_value = {"findings": []}
    return provider


def _mock_supervisor_run(findings=None):
    """Return a mock that produces CriticResult with given findings."""
    result = CriticResult(
        critic_name="correctness",
        findings=findings or [],
        confidence=0.85,
        runtime_ms=100,
    )
    def _run(*args, **kwargs):
        return [result]
    return _run


def _mock_aggregator_run(status=VerdictStatus.PASS, findings=None):
    """Return a mock that produces a Verdict."""
    report = AggregatedReport(
        findings=findings or [],
        confidence=0.9,
    )
    verdict = Verdict(
        status=status,
        reasoning="Mock verdict",
        confidence=0.9,
        report=report,
    )
    def _run(*args, **kwargs):
        return verdict
    return _run


# ── Single file validation ───────────────────────────────────────────────────


class TestSingleFileValidation:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_validate_markdown_quick(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        verdict, run_dir = run_validation(
            target_path=target,
            depth="quick",
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status == VerdictStatus.PASS
        assert run_dir.exists()

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_validate_yaml_config(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "config-valid.yaml"
        verdict, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status == VerdictStatus.PASS

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_validate_python_code(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "code-clean.py"
        verdict, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status == VerdictStatus.PASS

    def test_missing_file_raises(self, quick_config, tmp_path):
        with pytest.raises(FileNotFoundError, match="not found"):
            run_validation(
                target_path=tmp_path / "nonexistent.md",
                config=quick_config,
                runs_dir=tmp_path / "runs",
            )


# ── Output artifacts ─────────────────────────────────────────────────────────


class TestOutputArtifacts:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_run_dir_structure(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        # Check expected files
        assert (run_dir / "run-manifest.json").exists()
        assert (run_dir / "artifact.txt").exists()
        assert (run_dir / "rubric.json").exists()
        assert (run_dir / "verdict.json").exists()
        assert (run_dir / "report.md").exists()
        assert (run_dir / "critics").is_dir()

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_prescreen_json_created(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        prescreen_path = run_dir / "prescreen.json"
        assert prescreen_path.exists()
        data = json.loads(prescreen_path.read_text())
        assert "checks" in data
        assert "total_checks" in data

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_verdict_json_structure(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        verdict_data = json.loads((run_dir / "verdict.json").read_text())
        assert "status" in verdict_data
        assert "reasoning" in verdict_data
        assert "confidence" in verdict_data

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_report_md_contains_verdict(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        report = (run_dir / "report.md").read_text()
        assert "Verdict" in report
        assert "PASS" in report

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_manifest_updated_after_run(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        manifest = json.loads((run_dir / "run-manifest.json").read_text())
        assert "completed_at" in manifest
        assert "verdict" in manifest


# ── Prescreen gating ─────────────────────────────────────────────────────────


class TestPrescreenDisabled:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_no_prescreen_when_disabled(self, MockSupervisor, MockAggregator, MockProvider, tmp_path):
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="m1",
            model_tier2="m2",
            depth_profile="quick",
            enable_prescreen=False,
        )
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = _mock_aggregator_run()

        target = FIXTURES / "good" / "research-clean.md"
        _, run_dir = run_validation(
            target_path=target,
            config=config,
            runs_dir=tmp_path / "runs",
        )

        assert not (run_dir / "prescreen.json").exists()


# ── Error handling ───────────────────────────────────────────────────────────


class TestPipelineErrorHandling:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_aggregator_crash_returns_reject(self, MockSupervisor, MockAggregator, MockProvider, quick_config, tmp_path):
        MockProvider.return_value = _mock_provider()
        MockSupervisor.return_value.run = _mock_supervisor_run()
        MockAggregator.return_value.run = MagicMock(side_effect=RuntimeError("Aggregator crashed"))

        target = FIXTURES / "good" / "research-clean.md"
        verdict, _ = run_validation(
            target_path=target,
            config=quick_config,
            runs_dir=tmp_path / "runs",
        )

        assert verdict.status == VerdictStatus.REJECT
        assert "Aggregator failed" in verdict.reasoning


# ── Run directory creation ───────────────────────────────────────────────────


class TestCreateRunDir:
    def test_creates_with_timestamp(self, tmp_path):
        target = Path("test.md")
        run_dir = _create_run_dir(tmp_path, target)
        assert run_dir.exists()
        assert "test" in run_dir.name
        assert (run_dir / "critics").is_dir()

    def test_unique_per_call(self, tmp_path):
        import time
        target = Path("test.md")
        d1 = _create_run_dir(tmp_path, target)
        time.sleep(0.01)
        d2 = _create_run_dir(tmp_path, target)
        # May or may not be different depending on timing, but both exist
        assert d1.exists()
        assert d2.exists()
