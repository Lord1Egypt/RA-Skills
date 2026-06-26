"""Phase 2: Aggregator Agent tests — deduplication, confidence, verdict assignment."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from quorum.agents.aggregator import DEDUP_THRESHOLD, AggregatorAgent
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


def make_finding(severity=Severity.MEDIUM, description="Test finding", critic="correctness", **kwargs):
    defaults = dict(severity=severity, description=description, evidence=Evidence(tool="grep", result="matched line 42"), critic=critic)
    defaults.update(kwargs)
    return Finding(**defaults)


def make_critic_result(
    name="correctness", findings=None, confidence=0.85,
    criteria_total=10, criteria_evaluated=10,
):
    return CriticResult(
        critic_name=name, findings=findings or [], confidence=confidence,
        criteria_total=criteria_total, criteria_evaluated=criteria_evaluated,
        runtime_ms=100,
    )


@pytest.fixture
def config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-model",
        model_tier2="test-model",
        depth_profile="quick",
    )


@pytest.fixture
def aggregator(config) -> AggregatorAgent:
    provider = MagicMock()
    return AggregatorAgent(provider=provider, config=config)


# ── Collect Findings ──────────────────────────────────────────────────────────


class TestCollectFindings:
    def test_collects_from_multiple_critics(self, aggregator):
        f1 = make_finding(description="Issue A", critic="correctness")
        f2 = make_finding(description="Issue B", critic="completeness")
        results = [
            make_critic_result("correctness", [f1]),
            make_critic_result("completeness", [f2]),
        ]
        collected = aggregator._collect_findings(results)
        assert len(collected) == 2

    def test_skips_skipped_results(self, aggregator):
        f1 = make_finding(description="Issue A")
        active = make_critic_result("correctness", [f1])
        skipped = CriticResult(
            critic_name="security",
            findings=[make_finding(description="Should be skipped")],
            confidence=0.0,
            runtime_ms=0,
            skipped=True,
            skip_reason="test skip",
        )
        collected = aggregator._collect_findings([active, skipped])
        assert len(collected) == 1
        assert collected[0].description == "Issue A"

    def test_empty_results(self, aggregator):
        collected = aggregator._collect_findings([])
        assert collected == []

    def test_all_skipped(self, aggregator):
        skipped = CriticResult(
            critic_name="correctness",
            findings=[make_finding()],
            confidence=0.0,
            runtime_ms=0,
            skipped=True,
        )
        collected = aggregator._collect_findings([skipped])
        assert collected == []


# ── Similarity ────────────────────────────────────────────────────────────────


class TestSimilarity:
    def test_identical_strings(self, aggregator):
        assert aggregator._similarity("hello world", "hello world") == 1.0

    def test_completely_different(self, aggregator):
        sim = aggregator._similarity("aaa", "zzz")
        assert sim < 0.5

    def test_case_insensitive(self, aggregator):
        sim = aggregator._similarity("Hello World", "hello world")
        assert sim == 1.0

    def test_similar_above_threshold(self, aggregator):
        sim = aggregator._similarity(
            "Missing error handling in validate function",
            "Missing error handling in validation function",
        )
        assert sim >= DEDUP_THRESHOLD


# ── Deduplication ─────────────────────────────────────────────────────────────


class TestDeduplicate:
    def test_no_duplicates(self, aggregator):
        findings = [
            make_finding(description="Completely different issue about security"),
            make_finding(description="Unrelated problem with formatting"),
        ]
        deduped, conflicts = aggregator._deduplicate(findings)
        assert len(deduped) == 2
        assert conflicts == 0

    def test_identical_descriptions_merged(self, aggregator):
        findings = [
            make_finding(description="Missing error handling in function", critic="correctness"),
            make_finding(description="Missing error handling in function", critic="completeness"),
        ]
        deduped, conflicts = aggregator._deduplicate(findings)
        assert len(deduped) == 1
        assert conflicts == 1
        assert "correctness" in deduped[0].critic
        assert "completeness" in deduped[0].critic

    def test_higher_severity_wins(self, aggregator):
        findings = [
            make_finding(
                description="Missing error handling in function",
                severity=Severity.MEDIUM,
                critic="correctness",
            ),
            make_finding(
                description="Missing error handling in function",
                severity=Severity.HIGH,
                critic="completeness",
            ),
        ]
        deduped, conflicts = aggregator._deduplicate(findings)
        assert len(deduped) == 1
        assert deduped[0].severity == Severity.HIGH

    def test_equal_severity_keeps_first(self, aggregator):
        findings = [
            make_finding(
                description="Missing error handling in function",
                severity=Severity.MEDIUM,
                critic="first_critic",
            ),
            make_finding(
                description="Missing error handling in function",
                severity=Severity.MEDIUM,
                critic="second_critic",
            ),
        ]
        deduped, _ = aggregator._deduplicate(findings)
        assert len(deduped) == 1
        # First finding kept, with merged critic
        assert "first_critic" in deduped[0].critic

    def test_empty_findings(self, aggregator):
        deduped, conflicts = aggregator._deduplicate([])
        assert deduped == []
        assert conflicts == 0

    def test_three_similar_findings(self, aggregator):
        findings = [
            make_finding(description="Missing error handling in function", critic="a"),
            make_finding(description="Missing error handling in function", critic="b"),
            make_finding(description="Missing error handling in function", critic="c"),
        ]
        deduped, conflicts = aggregator._deduplicate(findings)
        assert len(deduped) == 1
        assert conflicts == 2


# ── Confidence Calculation ────────────────────────────────────────────────────


class TestCalculateConfidence:
    def test_single_active_result(self, aggregator):
        results = [make_critic_result("correctness", criteria_total=10, criteria_evaluated=10)]
        conf = aggregator._calculate_confidence(results, [])
        assert conf == 1.0  # 10/10 = full coverage

    def test_partial_coverage(self, aggregator):
        results = [
            make_critic_result("correctness", criteria_total=10, criteria_evaluated=10),
            make_critic_result("completeness", criteria_total=10, criteria_evaluated=10),
        ]
        conf = aggregator._calculate_confidence(results, [])
        assert conf == 1.0  # 20/20 = full coverage

    def test_skipped_reduces_coverage(self, aggregator):
        active = make_critic_result("correctness", criteria_total=10, criteria_evaluated=10)
        skipped = CriticResult(
            critic_name="security",
            findings=[],
            confidence=0.0,
            criteria_total=10,
            criteria_evaluated=0,
            runtime_ms=0,
            skipped=True,
        )
        conf = aggregator._calculate_confidence([active, skipped], [])
        assert conf == 0.5  # 10/20 = half coverage

    def test_all_skipped_returns_zero(self, aggregator):
        skipped = CriticResult(
            critic_name="correctness",
            findings=[],
            confidence=0.0,
            criteria_total=10,
            criteria_evaluated=0,
            runtime_ms=0,
            skipped=True,
        )
        conf = aggregator._calculate_confidence([skipped], [])
        assert conf == 0.0

    def test_coverage_clamped_to_one(self, aggregator):
        results = [
            make_critic_result("correctness", criteria_total=10, criteria_evaluated=10),
            make_critic_result("completeness", criteria_total=10, criteria_evaluated=10),
        ]
        findings = [make_finding(critic="a,b") for _ in range(20)]
        conf = aggregator._calculate_confidence(results, findings)
        assert conf <= 1.0

    def test_zero_criteria_returns_zero(self, aggregator):
        results = [
            make_critic_result("correctness", criteria_total=0, criteria_evaluated=0),
        ]
        conf = aggregator._calculate_confidence(results, [])
        assert conf >= 0.0


# ── Verdict Assignment ────────────────────────────────────────────────────────


class TestAssignVerdict:
    def test_no_findings_pass(self, aggregator):
        report = AggregatedReport(findings=[], confidence=0.9, critic_results=[])
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.PASS
        assert "No issues found" in verdict.reasoning

    def test_critical_finding_reject(self, aggregator):
        report = AggregatedReport(
            findings=[make_finding(severity=Severity.CRITICAL)],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.REJECT
        assert "CRITICAL" in verdict.reasoning

    def test_high_finding_revise(self, aggregator):
        report = AggregatedReport(
            findings=[make_finding(severity=Severity.HIGH)],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.REVISE
        assert "HIGH" in verdict.reasoning

    def test_medium_finding_pass_with_notes(self, aggregator):
        report = AggregatedReport(
            findings=[make_finding(severity=Severity.MEDIUM)],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.PASS_WITH_NOTES

    def test_low_finding_pass_with_notes(self, aggregator):
        report = AggregatedReport(
            findings=[make_finding(severity=Severity.LOW)],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.PASS_WITH_NOTES

    def test_info_only_findings_produce_pass(self, aggregator):
        """INFO-only findings produce PASS per documented contract (not PASS_WITH_NOTES)."""
        report = AggregatedReport(
            findings=[make_finding(severity=Severity.INFO)],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.PASS
        assert "informational" in verdict.reasoning.lower()

    def test_critical_trumps_high(self, aggregator):
        report = AggregatedReport(
            findings=[
                make_finding(severity=Severity.CRITICAL),
                make_finding(severity=Severity.HIGH),
            ],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert verdict.status == VerdictStatus.REJECT

    def test_verdict_has_summary_counts(self, aggregator):
        report = AggregatedReport(
            findings=[
                make_finding(severity=Severity.HIGH),
                make_finding(severity=Severity.MEDIUM),
            ],
            confidence=0.9,
            critic_results=[],
        )
        verdict = aggregator._assign_verdict(report)
        assert "1 HIGH" in verdict.reasoning
        assert "1 MEDIUM" in verdict.reasoning

    def test_verdict_confidence_from_report(self, aggregator):
        report = AggregatedReport(findings=[], confidence=0.77, critic_results=[])
        verdict = aggregator._assign_verdict(report)
        assert verdict.confidence == 0.77


# ── Full Run ──────────────────────────────────────────────────────────────────


class TestAggregatorRun:
    def test_full_run_pass(self, aggregator):
        results = [make_critic_result("correctness", [], confidence=0.9)]
        verdict = aggregator.run(results)
        assert verdict.status == VerdictStatus.PASS
        assert verdict.report is not None
        assert verdict.report.findings == []

    def test_full_run_reject(self, aggregator):
        findings = [make_finding(severity=Severity.CRITICAL)]
        results = [make_critic_result("correctness", findings, confidence=0.9)]
        verdict = aggregator.run(results)
        assert verdict.status == VerdictStatus.REJECT

    def test_full_run_deduplicates(self, aggregator):
        f1 = make_finding(description="Same issue found here", critic="correctness")
        f2 = make_finding(description="Same issue found here", critic="completeness")
        results = [
            make_critic_result("correctness", [f1]),
            make_critic_result("completeness", [f2]),
        ]
        verdict = aggregator.run(results)
        assert len(verdict.report.findings) == 1
        assert verdict.report.conflicts_resolved == 1

    def test_full_run_with_mixed_severity(self, aggregator):
        results = [
            make_critic_result("correctness", [
                make_finding(severity=Severity.HIGH),
                make_finding(severity=Severity.LOW),
            ]),
        ]
        verdict = aggregator.run(results)
        assert verdict.status == VerdictStatus.REVISE

    def test_full_run_empty_results(self, aggregator):
        verdict = aggregator.run([])
        assert verdict.status == VerdictStatus.PASS
        assert verdict.confidence == 0.0

    def test_verdict_json_serialization_never_none(self, aggregator):
        """Regression test: verdict.json must always have a valid status string,
        never None. See: fix/verdict-json-none."""
        import json

        # Test all verdict paths
        test_cases = [
            ([], VerdictStatus.PASS),  # empty → PASS
            ([make_critic_result("c", [make_finding(severity=Severity.INFO)])],
             VerdictStatus.PASS),  # INFO-only → PASS per documented contract
            ([make_critic_result("c", [make_finding(severity=Severity.HIGH)])],
             VerdictStatus.REVISE),
            ([make_critic_result("c", [make_finding(severity=Severity.CRITICAL)])],
             VerdictStatus.REJECT),
        ]

        valid_statuses = {s.value for s in VerdictStatus}

        for critic_results, expected_status in test_cases:
            verdict = aggregator.run(critic_results)

            # Verify the object
            assert verdict.status == expected_status
            assert verdict.status is not None

            # Verify serialization (what gets written to verdict.json)
            dumped = verdict.model_dump()
            assert dumped["status"] is not None, f"verdict.json status is None for {expected_status}"
            assert dumped["status"] in valid_statuses, f"verdict.json status '{dumped['status']}' not in {valid_statuses}"

            # Verify round-trip through JSON (what gets read back)
            json_str = json.dumps(dumped)
            loaded = json.loads(json_str)
            assert loaded["status"] is not None
            assert loaded["status"] in valid_statuses

    def test_verdict_fallback_serialization(self, aggregator):
        """Regression test: even the aggregator-crash fallback path must serialize
        a valid status, never None."""
        import json

        fallback = Verdict(
            status=VerdictStatus.REJECT,
            reasoning="Aggregator failed: test",
            confidence=0.0,
            report=None,
        )
        dumped = fallback.model_dump()
        assert dumped["status"] == "REJECT"
        assert dumped["status"] is not None

        json_str = json.dumps(dumped)
        loaded = json.loads(json_str)
        assert loaded["status"] == "REJECT"
