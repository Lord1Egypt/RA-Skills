# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""Tests for re-validation loops: fix application, loop termination, and delta calculation."""

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
    FixProposal,
    FixReport,
    Rubric,
    RubricCriterion,
    Severity,
    Verdict,
    VerdictStatus,
)
from quorum.pipeline import apply_fix_proposals, _revalidate_with_critics, run_validation

FIXTURES = Path(__file__).parent / "fixtures"

# ─── Helpers ──────────────────────────────────────────────────────────────────


def make_finding(
    severity: Severity = Severity.HIGH,
    description: str = "Test issue",
    critic: str = "correctness",
    **kwargs,
) -> Finding:
    defaults = dict(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result="matched text"),
        critic=critic,
    )
    defaults.update(kwargs)
    return Finding(**defaults)


def make_proposal(
    finding_id: str = "F-001",
    original: str = "bad code",
    replacement: str = "good code",
    confidence: float = 0.9,
) -> FixProposal:
    return FixProposal(
        finding_id=finding_id,
        finding_description="A bug",
        file_path="test.py",
        original_text=original,
        replacement_text=replacement,
        explanation="Fixes the issue",
        confidence=confidence,
    )


def make_fix_config(max_fix_loops: int = 1) -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-model",
        model_tier2="test-model",
        depth_profile="quick",
        max_fix_loops=max_fix_loops,
        enable_prescreen=False,
    )


def make_rubric() -> Rubric:
    return Rubric(
        name="test-rubric",
        domain="test",
        version="1.0",
        criteria=[
            RubricCriterion(
                id="T-001",
                criterion="Test criterion",
                severity=Severity.HIGH,
                evidence_required="any",
                why="testing",
            )
        ],
    )


# ─── apply_fix_proposals ──────────────────────────────────────────────────────


class TestApplyFixProposals:
    def test_exact_match_applies(self):
        artifact = "line one\nbad code\nline three\n"
        proposal = make_proposal(original="bad code", replacement="good code")
        modified, applied, skipped = apply_fix_proposals([proposal], artifact)
        assert "good code" in modified
        assert "bad code" not in modified
        assert len(applied) == 1
        assert len(skipped) == 0

    def test_original_not_found_is_skipped(self):
        artifact = "line one\nline two\nline three\n"
        proposal = make_proposal(original="text not in artifact", replacement="x")
        modified, applied, skipped = apply_fix_proposals([proposal], artifact)
        assert modified == artifact  # unchanged
        assert len(applied) == 0
        assert len(skipped) == 1

    def test_multiple_proposals_applied_in_order(self):
        artifact = "aaa bbb ccc"
        p1 = make_proposal(original="aaa", replacement="AAA")
        p2 = make_proposal(original="bbb", replacement="BBB")
        modified, applied, skipped = apply_fix_proposals([p1, p2], artifact)
        assert modified == "AAA BBB ccc"
        assert len(applied) == 2
        assert len(skipped) == 0

    def test_second_proposal_may_be_skipped_if_first_consumed_it(self):
        # Both proposals try to replace the same text; second one gets skipped
        artifact = "foo bar"
        p1 = make_proposal(original="foo", replacement="FOO")
        p2 = make_proposal(original="foo", replacement="baz")  # already replaced
        modified, applied, skipped = apply_fix_proposals([p1, p2], artifact)
        assert modified == "FOO bar"
        assert len(applied) == 1
        assert len(skipped) == 1

    def test_empty_proposals_returns_unchanged(self):
        artifact = "original text"
        modified, applied, skipped = apply_fix_proposals([], artifact)
        assert modified == artifact
        assert applied == []
        assert skipped == []

    def test_empty_original_text_proposal_is_skipped(self):
        artifact = "some text"
        proposal = make_proposal(original="", replacement="something")
        modified, applied, skipped = apply_fix_proposals([proposal], artifact)
        assert modified == artifact
        assert len(applied) == 0
        assert len(skipped) == 1

    def test_only_replaces_first_occurrence(self):
        artifact = "foo foo foo"
        proposal = make_proposal(original="foo", replacement="bar")
        modified, applied, skipped = apply_fix_proposals([proposal], artifact)
        assert modified == "bar foo foo"
        assert len(applied) == 1


# ─── _revalidate_with_critics ─────────────────────────────────────────────────


class TestRevalidateWithCritics:
    def _make_mock_critic_cls(self, findings: list[Finding]) -> type:
        """Return a critic class whose evaluate() returns the given findings."""
        result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.8,
            runtime_ms=10,
        )
        mock_cls = MagicMock()
        mock_instance = MagicMock()
        mock_instance.evaluate.return_value = result
        mock_cls.return_value = mock_instance
        return mock_cls

    def test_improved_when_fewer_findings(self):
        original_findings = [
            make_finding(severity=Severity.CRITICAL, critic="correctness"),
            make_finding(severity=Severity.HIGH, critic="correctness"),
        ]
        provider = MagicMock()
        config = make_fix_config()
        rubric = make_rubric()
        after_findings = [make_finding(severity=Severity.LOW, critic="correctness")]
        mock_cls = self._make_mock_critic_cls(after_findings)

        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", {"correctness": mock_cls}):
            results, verdict, delta = _revalidate_with_critics(
                modified_text="fixed artifact",
                blocking_findings=original_findings,
                provider=provider,
                config=config,
                rubric=rubric,
            )

        assert verdict == "improved"
        assert "improved" in delta
        assert "2 →" in delta

    def test_unchanged_when_same_count(self):
        original_findings = [make_finding(severity=Severity.HIGH, critic="correctness")]
        provider = MagicMock()
        config = make_fix_config()
        rubric = make_rubric()
        after_findings = [make_finding(severity=Severity.HIGH, critic="correctness")]
        mock_cls = self._make_mock_critic_cls(after_findings)

        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", {"correctness": mock_cls}):
            results, verdict, delta = _revalidate_with_critics(
                modified_text="text",
                blocking_findings=original_findings,
                provider=provider,
                config=config,
                rubric=rubric,
            )

        assert verdict == "unchanged"

    def test_regressed_when_more_findings(self):
        original_findings = [make_finding(severity=Severity.HIGH, critic="correctness")]
        provider = MagicMock()
        config = make_fix_config()
        rubric = make_rubric()
        after_findings = [
            make_finding(severity=Severity.CRITICAL, critic="correctness"),
            make_finding(severity=Severity.HIGH, critic="correctness"),
            make_finding(severity=Severity.HIGH, critic="correctness"),
        ]
        mock_cls = self._make_mock_critic_cls(after_findings)

        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", {"correctness": mock_cls}):
            results, verdict, delta = _revalidate_with_critics(
                modified_text="text",
                blocking_findings=original_findings,
                provider=provider,
                config=config,
                rubric=rubric,
            )

        assert verdict == "regressed"
        assert "regressed" in delta

    def test_unknown_critic_skipped_gracefully(self):
        original_findings = [
            make_finding(severity=Severity.HIGH, critic="nonexistent_critic")
        ]
        provider = MagicMock()
        config = make_fix_config()
        rubric = make_rubric()

        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", {}):
            results, verdict, delta = _revalidate_with_critics(
                modified_text="text",
                blocking_findings=original_findings,
                provider=provider,
                config=config,
                rubric=rubric,
            )

        # No critic ran → 0 after findings → improved (from 1 to 0)
        assert verdict == "improved"
        assert results == []

    def test_only_reruns_critics_from_blocking_findings(self):
        """Only critics that produced blocking findings should be re-run."""
        blocking_findings = [
            make_finding(severity=Severity.HIGH, critic="correctness"),
        ]
        provider = MagicMock()
        config = make_fix_config()
        rubric = make_rubric()

        correctness_cls = self._make_mock_critic_cls([])
        security_cls = self._make_mock_critic_cls(
            [make_finding(severity=Severity.HIGH, critic="security")]
        )

        registry = {"correctness": correctness_cls, "security": security_cls}
        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", registry):
            results, verdict, delta = _revalidate_with_critics(
                modified_text="text",
                blocking_findings=blocking_findings,
                provider=provider,
                config=config,
                rubric=rubric,
            )

        # Only correctness was in blocking findings → only correctness ran
        correctness_cls.assert_called_once()
        security_cls.assert_not_called()


# ─── Loop termination ─────────────────────────────────────────────────────────


class TestLoopTermination:
    """Test that the re-validation loop terminates correctly."""

    def _make_pipeline_mocks(
        self,
        critic_findings: list[Finding],
        fixer_proposals: list[dict],
        revalidation_findings: list[Finding] | None = None,
    ):
        """
        Build mock objects for a pipeline run:
          - supervisor returns critic_findings
          - fixer returns fixer_proposals
          - revalidation critic returns revalidation_findings
        """
        critic_result = CriticResult(
            critic_name="correctness",
            findings=critic_findings,
            confidence=0.8,
            runtime_ms=10,
        )
        reval_result = CriticResult(
            critic_name="correctness",
            findings=revalidation_findings or [],
            confidence=0.8,
            runtime_ms=10,
        )

        mock_provider = MagicMock()
        mock_provider.complete_json.side_effect = [
            {"fixes": fixer_proposals},  # first fixer call
            {"fixes": []},               # subsequent fixer calls (no more proposals)
            {"findings": [f.model_dump() for f in (revalidation_findings or [])]},
        ]

        return mock_provider, critic_result, reval_result

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_loop_stops_when_no_blocking_findings(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """If there are no CRITICAL/HIGH findings, fixer is never called."""
        config = make_fix_config(max_fix_loops=2)
        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        # Supervisor returns only LOW findings
        low_finding = make_finding(severity=Severity.LOW, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[low_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        report = AggregatedReport(findings=[low_finding], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS_WITH_NOTES,
            reasoning="Only low findings",
            confidence=0.9,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        target = FIXTURES / "good" / "code-clean.py"
        _, run_dir = run_validation(
            target_path=target,
            config=config,
            runs_dir=tmp_path / "runs",
        )

        # No loop files should be written
        loop_files = list(run_dir.glob("fix-proposals-loop-*.json"))
        assert loop_files == []
        assert not (run_dir / "artifact-fixed.txt").exists()

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_max_loops_not_exceeded(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """Loop must terminate at max_fix_loops even if findings persist."""
        config = make_fix_config(max_fix_loops=2)

        high_finding = make_finding(severity=Severity.HIGH, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[high_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        report = AggregatedReport(findings=[high_finding], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.REVISE,
            reasoning="Issues remain",
            confidence=0.8,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        target = FIXTURES / "good" / "code-clean.py"
        artifact_text = target.read_text()

        # Fixer always returns proposals, revalidation always returns same findings
        fixer_fix_return = {
            "fixes": [{
                "finding_id": high_finding.id,
                "original_text": "def clean_function",
                "replacement_text": "def clean_function_fixed",
                "explanation": "fix",
                "confidence": 0.9,
            }]
        }
        revalidation_finding_dict = {
            "findings": [{
                "severity": "HIGH",
                "description": "Still an issue",
                "evidence_tool": "grep",
                "evidence_result": "found it",
            }]
        }

        # Each loop calls: fixer (complete_json once), then revalidation critic (complete_json once)
        mock_prov.complete_json.side_effect = [
            fixer_fix_return,            # loop 1 fixer
            revalidation_finding_dict,   # loop 1 revalidation
            fixer_fix_return,            # loop 2 fixer
            revalidation_finding_dict,   # loop 2 revalidation
        ]

        with patch(
            "quorum.agents.supervisor.CRITIC_REGISTRY",
            {"correctness": _make_passthrough_critic_cls(mock_prov)},
        ):
            _, run_dir = run_validation(
                target_path=target,
                config=config,
                runs_dir=tmp_path / "runs",
            )

        loop_files = sorted(run_dir.glob("fix-proposals-loop-*.json"))
        # Must not exceed max_fix_loops
        assert len(loop_files) <= config.max_fix_loops

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_loop_stops_early_when_no_proposals_applied(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """If fixer proposals cannot be applied, loop stops after one iteration."""
        config = make_fix_config(max_fix_loops=3)

        high_finding = make_finding(severity=Severity.HIGH, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[high_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        report = AggregatedReport(findings=[high_finding], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.REVISE,
            reasoning="Issues remain",
            confidence=0.8,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        # Fixer proposes text that is NOT in the artifact
        mock_prov.complete_json.return_value = {
            "fixes": [{
                "finding_id": high_finding.id,
                "original_text": "THIS TEXT DOES NOT EXIST IN ARTIFACT",
                "replacement_text": "replacement",
                "explanation": "fix",
                "confidence": 0.9,
            }]
        }

        target = FIXTURES / "good" / "code-clean.py"
        _, run_dir = run_validation(
            target_path=target,
            config=config,
            runs_dir=tmp_path / "runs",
        )

        # Loop should stop after first iteration (no proposals applied)
        loop_files = sorted(run_dir.glob("fix-proposals-loop-*.json"))
        assert len(loop_files) == 1
        data = json.loads(loop_files[0].read_text())
        assert data["revalidation_verdict"] == "unchanged"
        assert not (run_dir / "artifact-fixed.txt").exists()


# ─── Original artifact not modified ───────────────────────────────────────────


class TestOriginalArtifactNotModified:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_original_file_unchanged_after_fix(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """The original artifact file must never be written to."""
        config = make_fix_config(max_fix_loops=1)

        # Write a temp artifact so we can check its content later
        artifact_file = tmp_path / "test_artifact.py"
        original_content = "def bad_function():\n    pass\n"
        artifact_file.write_text(original_content)

        high_finding = make_finding(severity=Severity.HIGH, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[high_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        report = AggregatedReport(findings=[], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Fixed",
            confidence=0.9,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        # Fixer returns a valid proposal
        mock_prov.complete_json.return_value = {
            "fixes": [{
                "finding_id": high_finding.id,
                "original_text": "def bad_function",
                "replacement_text": "def good_function",
                "explanation": "rename",
                "confidence": 0.95,
            }]
        }

        with patch(
            "quorum.agents.supervisor.CRITIC_REGISTRY",
            {"correctness": _make_passthrough_critic_cls(mock_prov, findings=[])},
        ):
            _, run_dir = run_validation(
                target_path=artifact_file,
                config=config,
                runs_dir=tmp_path / "runs",
            )

        # Original file must be unchanged
        assert artifact_file.read_text() == original_content

        # Fixed artifact saved only in run dir
        fixed = run_dir / "artifact-fixed.txt"
        if fixed.exists():
            assert "good_function" in fixed.read_text()


# ─── Delta calculation ────────────────────────────────────────────────────────


class TestDeltaCalculation:
    def _run_delta(
        self, before_count: int, after_count: int, critic: str = "correctness"
    ) -> tuple[str, str]:
        before_findings = [
            make_finding(severity=Severity.HIGH, critic=critic)
            for _ in range(before_count)
        ]
        after_findings = [
            make_finding(severity=Severity.HIGH, critic=critic)
            for _ in range(after_count)
        ]
        mock_cls = MagicMock()
        mock_instance = MagicMock()
        after_result = CriticResult(
            critic_name=critic,
            findings=after_findings,
            confidence=0.8,
            runtime_ms=10,
        )
        mock_instance.evaluate.return_value = after_result
        mock_cls.return_value = mock_instance

        with patch("quorum.agents.supervisor.CRITIC_REGISTRY", {critic: mock_cls}):
            _, verdict, delta = _revalidate_with_critics(
                modified_text="artifact",
                blocking_findings=before_findings,
                provider=MagicMock(),
                config=make_fix_config(),
                rubric=make_rubric(),
            )
        return verdict, delta

    def test_improved_verdict(self):
        verdict, delta = self._run_delta(before_count=3, after_count=1)
        assert verdict == "improved"
        assert "3 →" in delta
        assert "improved" in delta

    def test_unchanged_verdict(self):
        verdict, delta = self._run_delta(before_count=2, after_count=2)
        assert verdict == "unchanged"
        assert "unchanged" in delta

    def test_regressed_verdict(self):
        verdict, delta = self._run_delta(before_count=1, after_count=3)
        assert verdict == "regressed"
        assert "regressed" in delta

    def test_all_cleared_is_improved(self):
        verdict, delta = self._run_delta(before_count=2, after_count=0)
        assert verdict == "improved"
        assert "2 → 0" in delta


# ─── Integration: loop files written to run directory ─────────────────────────


class TestLoopFilesWritten:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_loop_file_written_per_loop(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """Each executed loop writes fix-proposals-loop-N.json."""
        config = make_fix_config(max_fix_loops=1)

        high_finding = make_finding(severity=Severity.HIGH, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[high_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        report = AggregatedReport(findings=[], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Passed",
            confidence=0.9,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        target = FIXTURES / "good" / "code-clean.py"
        artifact_content = target.read_text()

        mock_prov.complete_json.return_value = {
            "fixes": [{
                "finding_id": high_finding.id,
                "original_text": "def clean_function",
                "replacement_text": "def clean_function_v2",
                "explanation": "rename",
                "confidence": 0.9,
            }]
        }

        with patch(
            "quorum.agents.supervisor.CRITIC_REGISTRY",
            {"correctness": _make_passthrough_critic_cls(mock_prov, findings=[])},
        ):
            _, run_dir = run_validation(
                target_path=target,
                config=config,
                runs_dir=tmp_path / "runs",
            )

        loop1 = run_dir / "fix-proposals-loop-1.json"
        assert loop1.exists(), "fix-proposals-loop-1.json should exist"
        data = json.loads(loop1.read_text())
        assert data["loop_number"] == 1
        assert data["revalidation_verdict"] in ("improved", "unchanged", "regressed")
        assert data["revalidation_delta"] is not None

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_fix_proposals_json_backward_compat(
        self, MockSupervisor, MockAggregator, MockProvider, tmp_path
    ):
        """fix-proposals.json should still be written for backward compatibility."""
        config = make_fix_config(max_fix_loops=1)

        high_finding = make_finding(severity=Severity.HIGH, critic="correctness")
        critic_result = CriticResult(
            critic_name="correctness",
            findings=[high_finding],
            confidence=0.8,
            runtime_ms=10,
        )
        MockSupervisor.return_value.run.return_value = [critic_result]

        mock_prov = MagicMock()
        MockProvider.return_value = mock_prov

        report = AggregatedReport(findings=[], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Passed",
            confidence=0.9,
            report=report,
        )
        MockAggregator.return_value.run.return_value = verdict

        target = FIXTURES / "good" / "code-clean.py"
        # Fixer can't match — no proposals applied, early stop
        mock_prov.complete_json.return_value = {"fixes": []}

        _, run_dir = run_validation(
            target_path=target,
            config=config,
            runs_dir=tmp_path / "runs",
        )

        assert (run_dir / "fix-proposals.json").exists()


# ─── Helpers for integration tests ────────────────────────────────────────────


def _make_passthrough_critic_cls(
    provider: MagicMock,
    findings: list[Finding] | None = None,
) -> type:
    """
    Return a mock critic class that returns a fixed CriticResult.
    Used to simulate re-validation critic execution without real LLM calls.
    """
    result = CriticResult(
        critic_name="correctness",
        findings=findings if findings is not None else [],
        confidence=0.8,
        runtime_ms=10,
    )

    class MockCritic:
        name = "correctness"

        def __init__(self, provider, config):
            pass

        def evaluate(self, artifact_text, rubric, **kwargs):
            return result

    return MockCritic
