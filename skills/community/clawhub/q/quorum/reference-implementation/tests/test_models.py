"""Layer 1c: Unit tests for data models — Finding, Verdict, Rubric, etc."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from quorum.models import (
    AggregatedReport,
    BatchVerdict,
    CriticResult,
    Evidence,
    FileResult,
    Finding,
    FixProposal,
    FixReport,
    Issue,
    Locus,
    PreScreenCheck,
    PreScreenResult,
    Rubric,
    RubricCriterion,
    Severity,
    Verdict,
    VerdictStatus,
)


# ── Severity enum ────────────────────────────────────────────────────────────


class TestSeverity:
    def test_all_values_exist(self):
        assert set(Severity) == {
            Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO,
        }

    def test_string_value(self):
        assert Severity.CRITICAL.value == "CRITICAL"

    def test_ordering_by_value(self):
        ordered = sorted(Severity, key=lambda s: ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"].index(s.value))
        assert ordered[0] == Severity.CRITICAL
        assert ordered[-1] == Severity.INFO


class TestVerdictStatus:
    def test_all_values_exist(self):
        assert set(VerdictStatus) == {
            VerdictStatus.PASS, VerdictStatus.PASS_WITH_NOTES,
            VerdictStatus.REVISE, VerdictStatus.REJECT,
        }


# ── Evidence ─────────────────────────────────────────────────────────────────


class TestEvidence:
    def test_create_minimal(self):
        e = Evidence(tool="grep", result="found match")
        assert e.tool == "grep"
        assert e.citation is None

    def test_create_with_citation(self):
        e = Evidence(tool="llm", result="analyzed", citation="CRIT-001")
        assert e.citation == "CRIT-001"

    def test_serialization_roundtrip(self):
        e = Evidence(tool="schema", result="valid", citation="SC-001")
        data = json.loads(e.model_dump_json())
        e2 = Evidence(**data)
        assert e == e2


# ── Locus ────────────────────────────────────────────────────────────────────


class TestLocus:
    def test_create_valid(self):
        loc = Locus(file="src/main.py", start_line=10, end_line=20, role="impl", source_hash="abc123")
        assert loc.start_line == 10

    def test_start_line_minimum(self):
        with pytest.raises(ValidationError):
            Locus(file="f.py", start_line=0, end_line=1, role="x", source_hash="h")

    def test_compute_hash_from_content(self):
        content = "line1\nline2\nline3\nline4\n"
        h1 = Locus.compute_hash_from_content(content, 2, 3)
        h2 = Locus.compute_hash_from_content(content, 2, 3)
        assert h1 == h2  # deterministic

    def test_hash_changes_with_content(self):
        h1 = Locus.compute_hash_from_content("aaa\nbbb\n", 1, 2)
        h2 = Locus.compute_hash_from_content("aaa\nccc\n", 1, 2)
        assert h1 != h2


# ── Finding ──────────────────────────────────────────────────────────────────


class TestFinding:
    def test_create_minimal(self):
        f = Finding(
            severity=Severity.HIGH,
            description="Test issue",
            evidence=Evidence(tool="grep", result="match"),
            critic="correctness",
        )
        assert f.id.startswith("F-")
        assert f.severity == Severity.HIGH

    def test_auto_generated_id(self):
        f1 = Finding(
            severity=Severity.LOW,
            description="a",
            evidence=Evidence(tool="t", result="r"),
        )
        f2 = Finding(
            severity=Severity.LOW,
            description="b",
            evidence=Evidence(tool="t", result="r"),
        )
        assert f1.id != f2.id

    def test_serialization_roundtrip(self):
        f = Finding(
            severity=Severity.CRITICAL,
            description="Critical issue",
            evidence=Evidence(tool="llm", result="found"),
            critic="security",
            location="line 42",
            framework_refs=["CWE-78"],
            remediation="Fix it",
        )
        data = json.loads(f.model_dump_json())
        f2 = Finding(**data)
        assert f2.severity == Severity.CRITICAL
        assert f2.framework_refs == ["CWE-78"]

    def test_with_loci(self):
        f = Finding(
            severity=Severity.MEDIUM,
            description="Cross-artifact issue",
            evidence=Evidence(tool="llm", result="drift"),
            loci=[
                Locus(file="a.py", start_line=1, end_line=5, role="impl", source_hash="h1"),
                Locus(file="b.md", start_line=10, end_line=15, role="docs", source_hash="h2"),
            ],
        )
        assert len(f.loci) == 2

    def test_defaults(self):
        f = Finding(
            severity=Severity.INFO,
            description="Info",
            evidence=Evidence(tool="t", result="r"),
        )
        assert f.category is None
        assert f.location is None
        assert f.loci == []
        assert f.critic == ""
        assert f.rubric_criterion is None
        assert f.framework_refs == []
        assert f.remediation is None


# ── CriticResult ─────────────────────────────────────────────────────────────


class TestCriticResult:
    def test_create_empty(self):
        cr = CriticResult(critic_name="test", confidence=0.8)
        assert cr.findings == []
        assert cr.skipped is False

    def test_create_with_findings(self):
        f = Finding(
            severity=Severity.LOW,
            description="minor",
            evidence=Evidence(tool="t", result="r"),
        )
        cr = CriticResult(critic_name="test", findings=[f], confidence=0.9, runtime_ms=50)
        assert len(cr.findings) == 1
        assert cr.runtime_ms == 50

    def test_skipped(self):
        cr = CriticResult(
            critic_name="test",
            confidence=0.0,
            skipped=True,
            skip_reason="Not applicable",
        )
        assert cr.skipped
        assert cr.skip_reason == "Not applicable"

    def test_confidence_bounds(self):
        with pytest.raises(ValidationError):
            CriticResult(critic_name="t", confidence=1.5)
        with pytest.raises(ValidationError):
            CriticResult(critic_name="t", confidence=-0.1)


# ── AggregatedReport ─────────────────────────────────────────────────────────


class TestAggregatedReport:
    def _make_report(self, severities: list[Severity]) -> AggregatedReport:
        findings = [
            Finding(
                severity=s,
                description=f"Finding {i}",
                evidence=Evidence(tool="t", result="r"),
            )
            for i, s in enumerate(severities)
        ]
        return AggregatedReport(findings=findings, confidence=0.8)

    def test_critical_count(self):
        r = self._make_report([Severity.CRITICAL, Severity.CRITICAL, Severity.HIGH])
        assert r.critical_count == 2

    def test_high_count(self):
        r = self._make_report([Severity.HIGH, Severity.HIGH, Severity.LOW])
        assert r.high_count == 2

    def test_medium_count(self):
        r = self._make_report([Severity.MEDIUM])
        assert r.medium_count == 1

    def test_low_count(self):
        r = self._make_report([Severity.LOW, Severity.LOW])
        assert r.low_count == 2

    def test_info_count(self):
        r = self._make_report([Severity.INFO, Severity.INFO, Severity.INFO])
        assert r.info_count == 3

    def test_low_info_count(self):
        r = self._make_report([Severity.LOW, Severity.INFO])
        assert r.low_info_count == 2

    def test_empty_counts(self):
        r = AggregatedReport(findings=[], confidence=0.5)
        assert r.critical_count == 0
        assert r.high_count == 0


# ── Verdict ──────────────────────────────────────────────────────────────────


class TestVerdict:
    def test_pass_not_actionable(self):
        v = Verdict(status=VerdictStatus.PASS, reasoning="All good", confidence=0.95)
        assert v.is_actionable is False

    def test_pass_with_notes_not_actionable(self):
        v = Verdict(status=VerdictStatus.PASS_WITH_NOTES, reasoning="Minor", confidence=0.85)
        assert v.is_actionable is False

    def test_revise_is_actionable(self):
        v = Verdict(status=VerdictStatus.REVISE, reasoning="Needs work", confidence=0.7)
        assert v.is_actionable is True

    def test_reject_is_actionable(self):
        v = Verdict(status=VerdictStatus.REJECT, reasoning="Failed", confidence=0.6)
        assert v.is_actionable is True

    def test_serialization_roundtrip(self):
        v = Verdict(status=VerdictStatus.PASS, reasoning="ok", confidence=0.9)
        data = json.loads(v.model_dump_json())
        v2 = Verdict(**data)
        assert v2.status == VerdictStatus.PASS


# ── BatchVerdict ─────────────────────────────────────────────────────────────


class TestBatchVerdict:
    def test_actionable_when_reject(self):
        bv = BatchVerdict(status=VerdictStatus.REJECT, reasoning="fail")
        assert bv.is_actionable is True

    def test_not_actionable_when_pass(self):
        bv = BatchVerdict(status=VerdictStatus.PASS, reasoning="ok")
        assert bv.is_actionable is False


# ── Rubric ───────────────────────────────────────────────────────────────────


class TestRubric:
    def test_create_valid(self):
        r = Rubric(
            name="test",
            domain="research",
            criteria=[
                RubricCriterion(
                    id="C-001",
                    criterion="Has abstract",
                    severity=Severity.HIGH,
                    evidence_required="Quote",
                    why="Context",
                ),
            ],
        )
        assert len(r.criteria) == 1

    def test_empty_criteria_rejected(self):
        with pytest.raises(ValidationError, match="at least one criterion"):
            Rubric(name="t", domain="d", criteria=[])

    def test_serialization_roundtrip(self):
        r = Rubric(
            name="test",
            domain="code",
            version="2.0",
            description="Test rubric",
            criteria=[
                RubricCriterion(
                    id="C-001",
                    criterion="Does X",
                    severity=Severity.MEDIUM,
                    evidence_required="Show X",
                    why="Because",
                ),
            ],
        )
        data = json.loads(r.model_dump_json())
        r2 = Rubric(**data)
        assert r2.name == "test"
        assert r2.version == "2.0"


# ── PreScreenCheck / PreScreenResult ─────────────────────────────────────────


class TestPreScreenModels:
    def test_check_creation(self):
        c = PreScreenCheck(
            id="PS-001",
            name="hardcoded_paths",
            category="security",
            severity=Severity.HIGH,
            description="Found paths",
            result="FAIL",
            evidence="L1: /Users/x",
            locations=["line 1"],
        )
        assert c.result == "FAIL"

    def test_result_has_failures(self):
        r = PreScreenResult(
            checks=[
                PreScreenCheck(
                    id="PS-001", name="t", category="c",
                    severity=Severity.HIGH, description="d", result="FAIL",
                ),
            ],
            total_checks=1, passed=0, failed=1, skipped=0,
        )
        assert r.has_failures is True

    def test_result_no_failures(self):
        r = PreScreenResult(
            checks=[
                PreScreenCheck(
                    id="PS-001", name="t", category="c",
                    severity=Severity.HIGH, description="d", result="PASS",
                ),
            ],
            total_checks=1, passed=1, failed=0, skipped=0,
        )
        assert r.has_failures is False


# ── FixProposal / FixReport ──────────────────────────────────────────────────


class TestFixModels:
    def test_fix_proposal(self):
        fp = FixProposal(
            finding_id="F-001",
            finding_description="Bad code",
            file_path="src/main.py",
            original_text="eval(x)",
            replacement_text="safe_eval(x)",
            explanation="Prevents injection",
            confidence=0.9,
        )
        assert fp.confidence == 0.9

    def test_fix_report(self):
        fr = FixReport(
            proposals=[],
            findings_addressed=0,
            findings_skipped=2,
            skip_reasons=["Too complex", "Ambiguous"],
        )
        assert fr.findings_skipped == 2


# ── Issue ────────────────────────────────────────────────────────────────────


class TestIssue:
    def test_create_and_to_dict(self):
        iss = Issue(
            pattern_id="PAT-001",
            description="Missing error handling",
            domain="code",
            severity=Severity.HIGH,
            frequency=3,
            first_seen="2026-01-01",
            last_seen="2026-03-01",
            mandatory=True,
        )
        d = iss.to_dict()
        assert d["pattern_id"] == "PAT-001"
        assert d["mandatory"] is True
