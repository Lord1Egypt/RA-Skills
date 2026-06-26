# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""Phase 3: Tester pipeline integration tests — DEC-020, depth activation, report/manifest."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.agents.aggregator import AggregatorAgent
from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    CriticResult,
    Evidence,
    Finding,
    Severity,
    TesterResult,
    Verdict,
    VerdictStatus,
    VerificationResult,
    VerificationStatus,
    VerifiedLocus,
)
from quorum.pipeline import _run_phase3, _write_report, _update_manifest


# ── Helpers ───────────────────────────────────────────────────────────────────


def make_finding(
    severity=Severity.MEDIUM,
    description="Test finding",
    critic="correctness",
    location="test.py:10",
    **kwargs,
):
    defaults = dict(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result="matched line 42"),
        critic=critic,
        location=location,
    )
    defaults.update(kwargs)
    return Finding(**defaults)


def make_critic_result(name="correctness", findings=None, confidence=0.85):
    return CriticResult(
        critic_name=name,
        findings=findings or [],
        confidence=confidence,
        runtime_ms=100,
    )


def make_config(depth="standard"):
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-model",
        model_tier2="test-model",
        depth_profile=depth,
    )


def make_tester_result(verification_results=None):
    """Build a TesterResult from a list of VerificationResults."""
    vrs = verification_results or []
    verified = sum(1 for vr in vrs if vr.status == VerificationStatus.VERIFIED)
    unverified = sum(1 for vr in vrs if vr.status == VerificationStatus.UNVERIFIED)
    contradicted = sum(1 for vr in vrs if vr.status == VerificationStatus.CONTRADICTED)
    return TesterResult(
        verification_results=vrs,
        total_findings=len(vrs),
        verified_count=verified,
        unverified_count=unverified,
        contradicted_count=contradicted,
        runtime_ms=42,
    )


# ── Phase 3 Depth Activation ─────────────────────────────────────────────────


class TestPhase3DepthActivation:
    """Verify _run_phase3() respects depth_profile settings."""

    def test_phase3_skipped_at_quick_depth(self, tmp_path):
        """At quick depth, Phase 3 should return None without running Tester."""
        config = make_config(depth="quick")
        result = _run_phase3(
            config=config,
            provider=MagicMock(),
            critic_results=[make_critic_result()],
            base_dir=tmp_path,
            run_dir=tmp_path,
        )
        assert result is None

    @patch("quorum.critics.tester.TesterCritic", autospec=False)
    def test_phase3_l1_only_at_standard(self, mock_tester_cls, tmp_path):
        """At standard depth, L2 should be disabled (no provider/config passed)."""
        mock_instance = MagicMock()
        mock_instance.verify.return_value = make_tester_result()
        mock_tester_cls.return_value = mock_instance

        config = make_config(depth="standard")
        _run_phase3(
            config=config,
            provider=MagicMock(),
            critic_results=[make_critic_result()],
            base_dir=tmp_path,
            run_dir=tmp_path,
        )

        # TesterCritic should be constructed with provider=None, config=None, l2_enabled=False
        mock_tester_cls.assert_called_once_with(
            provider=None,
            config=None,
            l2_enabled=False,
        )

    @patch("quorum.critics.tester.TesterCritic", autospec=False)
    def test_phase3_l1_l2_at_thorough(self, mock_tester_cls, tmp_path):
        """At thorough depth, both L1 and L2 should be active."""
        mock_instance = MagicMock()
        mock_instance.verify.return_value = make_tester_result()
        mock_tester_cls.return_value = mock_instance

        provider = MagicMock()
        config = make_config(depth="thorough")
        _run_phase3(
            config=config,
            provider=provider,
            critic_results=[make_critic_result()],
            base_dir=tmp_path,
            run_dir=tmp_path,
        )

        # TesterCritic should be constructed with provider and config passed, l2_enabled=True
        mock_tester_cls.assert_called_once_with(
            provider=provider,
            config=config,
            l2_enabled=True,
        )


# ── DEC-020: Contradiction Policy ────────────────────────────────────────────


class TestDEC020ContradictionPolicy:
    """DEC-020: L1 CONTRADICTED → exclude, L2 CONTRADICTED → annotate."""

    @pytest.fixture
    def aggregator(self):
        config = make_config(depth="standard")
        return AggregatorAgent(provider=MagicMock(), config=config)

    def test_l1_contradicted_excluded_from_verdict(self, aggregator):
        """L1 CONTRADICTED finding should be removed from the verdict entirely."""
        finding = make_finding(
            severity=Severity.HIGH,
            description="Phantom file reference",
            id="F-phantom1",
        )
        critic_result = make_critic_result("correctness", [finding])

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.CONTRADICTED,
                original_finding_id="F-phantom1",
                explanation="File not found: phantom.py",
                level=1,
            ),
        ])

        verdict = aggregator.run([critic_result], tester_result=tester_result)

        # Finding should be excluded — verdict should be PASS (no findings left)
        assert verdict.status == VerdictStatus.PASS
        assert verdict.report is not None
        assert len(verdict.report.findings) == 0
        assert "1 finding(s) excluded by Tester" in verdict.reasoning

    def test_l2_contradicted_annotated_not_excluded(self, aggregator):
        """L2 CONTRADICTED finding should stay in verdict with annotation."""
        finding = make_finding(
            severity=Severity.HIGH,
            description="Claim about code behavior",
            id="F-l2claim1",
        )
        critic_result = make_critic_result("correctness", [finding])

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.CONTRADICTED,
                original_finding_id="F-l2claim1",
                explanation="LLM says claim is inaccurate",
                level=2,
            ),
        ])

        verdict = aggregator.run([critic_result], tester_result=tester_result)

        # Finding should remain — verdict should still be REVISE (HIGH finding present)
        assert verdict.status == VerdictStatus.REVISE
        assert verdict.report is not None
        assert len(verdict.report.findings) == 1
        assert verdict.report.findings[0].description.startswith("[L2-CONTRADICTED]")

    def test_verified_findings_pass_through(self, aggregator):
        """VERIFIED findings should pass through unchanged."""
        finding = make_finding(
            severity=Severity.MEDIUM,
            description="Legit finding",
            id="F-legit1",
        )
        critic_result = make_critic_result("correctness", [finding])

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.VERIFIED,
                original_finding_id="F-legit1",
                explanation="Content matches",
                level=1,
            ),
        ])

        verdict = aggregator.run([critic_result], tester_result=tester_result)

        assert verdict.status == VerdictStatus.PASS_WITH_NOTES
        assert len(verdict.report.findings) == 1
        assert verdict.report.findings[0].description == "Legit finding"


# ── AggregatedReport ─────────────────────────────────────────────────────────


class TestTesterResultInReport:
    def test_tester_result_in_aggregated_report(self):
        """AggregatedReport.tester_result should be populated when provided."""
        config = make_config()
        aggregator = AggregatorAgent(provider=MagicMock(), config=config)

        finding = make_finding(severity=Severity.LOW, id="F-low1")
        critic_result = make_critic_result("correctness", [finding])

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.VERIFIED,
                original_finding_id="F-low1",
                explanation="OK",
                level=1,
            ),
        ])

        verdict = aggregator.run([critic_result], tester_result=tester_result)

        assert verdict.report is not None
        assert verdict.report.tester_result is not None
        assert verdict.report.tester_result.verified_count == 1

    def test_aggregator_works_without_tester(self):
        """Backward compat: aggregator.run() with no tester_result still works."""
        config = make_config()
        aggregator = AggregatorAgent(provider=MagicMock(), config=config)

        finding = make_finding(severity=Severity.HIGH)
        critic_result = make_critic_result("correctness", [finding])

        # Call without tester_result (old behavior)
        verdict = aggregator.run([critic_result])

        assert verdict.status == VerdictStatus.REVISE
        assert verdict.report is not None
        assert verdict.report.tester_result is None
        assert verdict.report.l1_excluded_count == 0


# ── Report Output ─────────────────────────────────────────────────────────────


class TestVerificationSectionInReport:
    def test_verification_section_in_report(self, tmp_path):
        """report.md should contain the Verification section when tester_result is present."""
        from quorum.models import Rubric, RubricCriterion

        rubric = Rubric(
            name="test-rubric",
            domain="test",
            criteria=[RubricCriterion(
                id="C-001",
                criterion="Test",
                severity=Severity.MEDIUM,
                evidence_required="any",
                why="test",
            )],
        )
        config = make_config(depth="standard")
        finding = make_finding(severity=Severity.MEDIUM, id="F-med1")
        report = AggregatedReport(
            findings=[finding],
            confidence=0.85,
            critic_results=[make_critic_result("correctness", [finding])],
        )
        verdict = Verdict(
            status=VerdictStatus.PASS_WITH_NOTES,
            reasoning="Test",
            confidence=0.85,
            report=report,
        )

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.VERIFIED,
                original_finding_id="F-med1",
                explanation="OK",
                level=1,
            ),
        ])

        report_path = tmp_path / "report.md"
        _write_report(
            report_path, verdict, Path("test.py"), rubric, config,
            tester_result=tester_result,
        )

        content = report_path.read_text()
        assert "## Verification (Tester)" in content
        assert "Verified | 1" in content
        assert "Verification Rate" in content

    def test_no_verification_section_without_tester(self, tmp_path):
        """report.md should NOT contain Verification section when tester_result is None."""
        from quorum.models import Rubric, RubricCriterion

        rubric = Rubric(
            name="test-rubric",
            domain="test",
            criteria=[RubricCriterion(
                id="C-001",
                criterion="Test",
                severity=Severity.MEDIUM,
                evidence_required="any",
                why="test",
            )],
        )
        config = make_config(depth="quick")
        report = AggregatedReport(findings=[], confidence=0.9, critic_results=[])
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Test",
            confidence=0.9,
            report=report,
        )

        report_path = tmp_path / "report.md"
        _write_report(report_path, verdict, Path("test.py"), rubric, config)

        content = report_path.read_text()
        assert "## Verification (Tester)" not in content


# ── Manifest ──────────────────────────────────────────────────────────────────


class TestTesterStatsInManifest:
    def test_tester_stats_in_manifest(self, tmp_path):
        """run-manifest.json should include tester stats when tester_result is present."""
        config = make_config(depth="standard")
        report = AggregatedReport(findings=[], confidence=0.9, critic_results=[])
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Test",
            confidence=0.9,
            report=report,
        )

        # Create initial manifest (as pipeline does)
        manifest_path = tmp_path / "run-manifest.json"
        manifest_path.write_text(json.dumps({"started_at": "2026-01-01T00:00:00"}))

        tester_result = make_tester_result([
            VerificationResult(
                status=VerificationStatus.VERIFIED,
                original_finding_id="F-1",
                explanation="OK",
                level=1,
            ),
            VerificationResult(
                status=VerificationStatus.CONTRADICTED,
                original_finding_id="F-2",
                explanation="File not found",
                level=1,
            ),
        ])

        _update_manifest(
            run_dir=tmp_path,
            config=config,
            prescreen_result=None,
            verdict=verdict,
            critic_results=[],
            relationships_path=None,
            tester_result=tester_result,
        )

        manifest = json.loads(manifest_path.read_text())
        assert "tester" in manifest
        assert manifest["tester"]["verified"] == 1
        assert manifest["tester"]["contradicted"] == 1
        assert manifest["tester"]["runtime_ms"] == 42
        assert 0.0 <= manifest["tester"]["verification_rate"] <= 1.0

    def test_no_tester_stats_without_tester(self, tmp_path):
        """run-manifest.json should NOT include tester key when tester_result is None."""
        config = make_config(depth="quick")
        report = AggregatedReport(findings=[], confidence=0.9, critic_results=[])
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Test",
            confidence=0.9,
            report=report,
        )

        manifest_path = tmp_path / "run-manifest.json"
        manifest_path.write_text(json.dumps({"started_at": "2026-01-01T00:00:00"}))

        _update_manifest(
            run_dir=tmp_path,
            config=config,
            prescreen_result=None,
            verdict=verdict,
            critic_results=[],
            relationships_path=None,
        )

        manifest = json.loads(manifest_path.read_text())
        assert "tester" not in manifest
