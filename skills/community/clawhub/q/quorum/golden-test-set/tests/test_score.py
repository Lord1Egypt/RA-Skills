"""Tests for the golden test set scoring framework."""

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

import pytest
import yaml

# Add scripts/ to path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from score import (
    GTFinding,
    FPTrap,
    QuorumFinding,
    Annotation,
    ArtifactScore,
    MatchResult,
    match_findings,
    compute_metrics,
    compute_sha256,
    parse_annotation,
    validate_annotations,
    _parse_line_numbers,
    _location_match,
    _fuzzy_match,
    _is_trap_match,
    _safe_div,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_golden(tmp_path):
    """Create a minimal golden test set structure."""
    (tmp_path / "artifacts" / "python").mkdir(parents=True)
    (tmp_path / "annotations").mkdir()
    return tmp_path


def _make_artifact(golden_dir: Path, rel_path: str, content: str) -> str:
    """Write an artifact file, return its SHA-256."""
    full = golden_dir / rel_path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content)
    return hashlib.sha256(content.encode()).hexdigest()


def _make_annotation(golden_dir: Path, name: str, data: dict):
    """Write an annotation YAML file."""
    ann_path = golden_dir / "annotations" / f"{name}.annotations.yaml"
    ann_path.parent.mkdir(parents=True, exist_ok=True)
    ann_path.write_text(yaml.dump(data, default_flow_style=False))


def _make_gt_finding(id: str, severity: str = "HIGH", category: str = "security",
                     critic: str = "security", location: str | None = "line 42") -> GTFinding:
    return GTFinding(
        id=id,
        description=f"Test finding {id}",
        location=location,
        severity=severity,
        category=category,
        critic=critic,
    )


def _make_q_finding(id: str = "F-test", severity: str = "HIGH", category: str = "security",
                    critic: str = "security", location: str | None = "line 42",
                    description: str = "Test finding") -> QuorumFinding:
    return QuorumFinding(
        id=id,
        severity=severity,
        category=category,
        description=description,
        location=location,
        critic=critic,
    )


# ---------------------------------------------------------------------------
# Line number parsing
# ---------------------------------------------------------------------------

class TestParseLineNumbers:
    def test_single_line(self):
        assert _parse_line_numbers("line 42") == [42]

    def test_line_range(self):
        assert _parse_line_numbers("line 42-48") == [42, 43, 44, 45, 46, 47, 48]

    def test_no_prefix(self):
        assert _parse_line_numbers("42-45") == [42, 43, 44, 45]

    def test_none(self):
        assert _parse_line_numbers(None) == []

    def test_no_numbers(self):
        assert _parse_line_numbers("section 3.2") == []

    def test_multiple_references(self):
        nums = _parse_line_numbers("line 10, line 20-22")
        assert 10 in nums
        assert 20 in nums
        assert 22 in nums


# ---------------------------------------------------------------------------
# Location matching
# ---------------------------------------------------------------------------

class TestLocationMatch:
    def test_exact_match(self):
        assert _location_match("line 42", "line 42")

    def test_within_tolerance(self):
        assert _location_match("line 42", "line 45")  # diff=3, within ±5

    def test_outside_tolerance(self):
        assert not _location_match("line 42", "line 55")  # diff=13, outside ±5

    def test_range_overlap(self):
        assert _location_match("line 40-45", "line 43")

    def test_none_inputs(self):
        assert not _location_match(None, "line 42")
        assert not _location_match("line 42", None)
        assert not _location_match(None, None)


# ---------------------------------------------------------------------------
# Fuzzy matching
# ---------------------------------------------------------------------------

class TestFuzzyMatch:
    def test_identical(self):
        assert _fuzzy_match("SQL injection", "SQL injection") == 1.0

    def test_similar(self):
        score = _fuzzy_match("SQL injection via user input", "SQL injection through user input")
        assert score >= FUZZY_THRESHOLD

    def test_dissimilar(self):
        score = _fuzzy_match("SQL injection", "Dead code removal")
        assert score < FUZZY_THRESHOLD

    def test_case_insensitive(self):
        assert _fuzzy_match("SQL Injection", "sql injection") == 1.0


FUZZY_THRESHOLD = 0.6


# ---------------------------------------------------------------------------
# Matching algorithm
# ---------------------------------------------------------------------------

class TestMatchFindings:
    def test_perfect_tp(self):
        """All GT findings matched exactly."""
        gt = [_make_gt_finding("GT-001")]
        qf = [_make_q_finding("F-001")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, qf, [])
        assert tp == 1
        assert fp == 0
        assert fn == 0
        assert results[0].matched
        assert results[0].severity_match

    def test_false_negative(self):
        """GT finding with no matching Quorum finding."""
        gt = [_make_gt_finding("GT-001")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, [], [])
        assert tp == 0
        assert fn == 1
        assert not results[0].matched

    def test_false_positive(self):
        """Quorum finding with no matching GT finding."""
        qf = [_make_q_finding("F-001", category="correctness", critic="correctness")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings([], qf, [])
        assert tp == 0
        assert fp == 1
        assert fn == 0

    def test_trapped_false_positive(self):
        """Quorum finding that matches a false-positive trap."""
        qf = [_make_q_finding("F-001", location="line 30",
                               description="Use of eval() on hardcoded constant input")]
        traps = [FPTrap(description="Use of eval() on hardcoded constant input", location="line 30")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings([], qf, traps)
        assert trapped == 1
        assert fp == 0

    def test_critic_mismatch_no_match(self):
        """Different critics should not match."""
        gt = [_make_gt_finding("GT-001", critic="security", category="security")]
        qf = [_make_q_finding("F-001", critic="correctness", category="correctness")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, qf, [])
        assert tp == 0
        assert fn == 1
        assert fp == 1

    def test_severity_mismatch_still_matches(self):
        """Detection matches even if severity differs."""
        gt = [_make_gt_finding("GT-001", severity="HIGH")]
        qf = [_make_q_finding("F-001", severity="CRITICAL")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, qf, [])
        assert tp == 1
        assert not results[0].severity_match
        assert sev_d == [1]  # |3-4| = 1

    def test_location_fuzzy_fallback(self):
        """Match by description fuzzy when no location overlap."""
        gt = [_make_gt_finding("GT-001", location=None)]
        gt[0].description = "SQL injection via unsanitized user input"
        qf = [_make_q_finding("F-001", location=None,
                               description="SQL injection through unsanitized user input")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, qf, [])
        assert tp == 1

    def test_greedy_one_to_one(self):
        """Each GT and Quorum finding matched at most once."""
        gt = [_make_gt_finding("GT-001"), _make_gt_finding("GT-002")]
        qf = [_make_q_finding("F-001")]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings(gt, qf, [])
        assert tp == 1
        assert fn == 1

    def test_empty_inputs(self):
        """No findings at all."""
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings([], [], [])
        assert tp == 0
        assert fp == 0
        assert fn == 0


# ---------------------------------------------------------------------------
# Severity distance
# ---------------------------------------------------------------------------

class TestSeverityDistance:
    def test_exact_match(self):
        gt = [_make_gt_finding("GT-001", severity="CRITICAL")]
        qf = [_make_q_finding("F-001", severity="CRITICAL")]
        _, _, _, _, _, sev_m, sev_d = match_findings(gt, qf, [])
        assert sev_m == 1
        assert sev_d == [0]

    def test_one_tier_off(self):
        gt = [_make_gt_finding("GT-001", severity="HIGH")]
        qf = [_make_q_finding("F-001", severity="CRITICAL")]
        _, _, _, _, _, sev_m, sev_d = match_findings(gt, qf, [])
        assert sev_m == 0
        assert sev_d == [1]

    def test_two_tiers_off(self):
        gt = [_make_gt_finding("GT-001", severity="LOW")]
        qf = [_make_q_finding("F-001", severity="HIGH")]
        _, _, _, _, _, sev_m, sev_d = match_findings(gt, qf, [])
        assert sev_d == [2]


# ---------------------------------------------------------------------------
# Clean (PASS) artifact handling
# ---------------------------------------------------------------------------

class TestCleanArtifacts:
    def test_clean_no_findings(self):
        """PASS artifact with no Quorum findings → perfect."""
        s = ArtifactScore(
            artifact="clean.py",
            expected_verdict="PASS",
            actual_verdict="PASS",
            verdict_correct=True,
            tp=0, fp=0, fn=0,
            metadata={"complexity": "low", "domain": "python-code", "source": "synthetic"},
        )
        metrics = compute_metrics([s])
        assert metrics["aggregate"]["fp_rate_clean"] == 0.0

    def test_clean_with_fp(self):
        """PASS artifact where Quorum incorrectly flags something."""
        s = ArtifactScore(
            artifact="clean.py",
            expected_verdict="PASS",
            actual_verdict="PASS_WITH_NOTES",
            verdict_correct=False,
            tp=0, fp=2, fn=0,
            metadata={"complexity": "low", "domain": "python-code", "source": "synthetic"},
        )
        metrics = compute_metrics([s])
        assert metrics["aggregate"]["fp_rate_clean"] == 1.0


# ---------------------------------------------------------------------------
# SHA-256 integrity
# ---------------------------------------------------------------------------

class TestSHA256:
    def test_known_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        content = "hello world\n"
        f.write_text(content)
        expected = hashlib.sha256(content.encode()).hexdigest()
        assert compute_sha256(f) == expected

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("")
        expected = hashlib.sha256(b"").hexdigest()
        assert compute_sha256(f) == expected


# ---------------------------------------------------------------------------
# Annotation parsing
# ---------------------------------------------------------------------------

class TestAnnotationParsing:
    def test_round_trip(self, tmp_golden):
        content = "print('hello')\n"
        sha = _make_artifact(tmp_golden, "artifacts/python/test.py", content)
        ann_data = {
            "schema_version": "1.0",
            "artifact": "artifacts/python/test.py",
            "artifact_sha256": sha,
            "expected_verdict": "PASS",
            "findings": [],
            "false_positive_traps": [],
            "metadata": {
                "source": "synthetic",
                "domain": "python-code",
                "complexity": "low",
                "rubric": "python-code",
                "depth": "standard",
                "author": "test",
                "created": "2026-03-12",
            },
        }
        _make_annotation(tmp_golden, "test", ann_data)
        ann = parse_annotation(tmp_golden / "annotations" / "test.annotations.yaml")
        assert ann.artifact == "artifacts/python/test.py"
        assert ann.expected_verdict == "PASS"
        assert len(ann.findings) == 0

    def test_with_findings(self, tmp_golden):
        sha = _make_artifact(tmp_golden, "artifacts/python/vuln.py", "x = 1\n")
        ann_data = {
            "schema_version": "1.0",
            "artifact": "artifacts/python/vuln.py",
            "artifact_sha256": sha,
            "expected_verdict": "REVISE",
            "findings": [
                {
                    "id": "GT-001",
                    "description": "SQL injection",
                    "location": "line 42",
                    "severity": "CRITICAL",
                    "category": "security",
                    "critic": "security",
                }
            ],
            "metadata": {
                "source": "synthetic", "domain": "python-code", "complexity": "medium",
                "rubric": "python-code", "depth": "standard", "author": "test", "created": "2026-03-12",
            },
        }
        _make_annotation(tmp_golden, "vuln", ann_data)
        ann = parse_annotation(tmp_golden / "annotations" / "vuln.annotations.yaml")
        assert len(ann.findings) == 1
        assert ann.findings[0].id == "GT-001"
        assert ann.findings[0].severity == "CRITICAL"


# ---------------------------------------------------------------------------
# Validation mode
# ---------------------------------------------------------------------------

class TestValidation:
    def test_valid_annotation(self, tmp_golden):
        content = "x = 1\n"
        sha = _make_artifact(tmp_golden, "artifacts/python/test.py", content)
        _make_annotation(tmp_golden, "test", {
            "schema_version": "1.0",
            "artifact": "artifacts/python/test.py",
            "artifact_sha256": sha,
            "expected_verdict": "PASS",
            "findings": [],
            "metadata": {
                "source": "synthetic", "domain": "python-code", "complexity": "low",
                "rubric": "python-code", "depth": "standard", "author": "test", "created": "2026-03-12",
            },
        })
        errors = validate_annotations(tmp_golden / "annotations", tmp_golden)
        assert errors == []

    def test_sha_mismatch(self, tmp_golden):
        _make_artifact(tmp_golden, "artifacts/python/test.py", "x = 1\n")
        _make_annotation(tmp_golden, "test", {
            "schema_version": "1.0",
            "artifact": "artifacts/python/test.py",
            "artifact_sha256": "deadbeef" * 8,
            "expected_verdict": "PASS",
            "findings": [],
            "metadata": {
                "source": "synthetic", "domain": "python-code", "complexity": "low",
                "rubric": "python-code", "depth": "standard", "author": "test", "created": "2026-03-12",
            },
        })
        errors = validate_annotations(tmp_golden / "annotations", tmp_golden)
        assert any("SHA-256 mismatch" in e for e in errors)

    def test_missing_artifact(self, tmp_golden):
        _make_annotation(tmp_golden, "test", {
            "schema_version": "1.0",
            "artifact": "artifacts/python/nonexistent.py",
            "artifact_sha256": "abc123",
            "expected_verdict": "PASS",
            "findings": [],
            "metadata": {
                "source": "synthetic", "domain": "python-code", "complexity": "low",
                "rubric": "python-code", "depth": "standard", "author": "test", "created": "2026-03-12",
            },
        })
        errors = validate_annotations(tmp_golden / "annotations", tmp_golden)
        assert any("not found" in e for e in errors)

    def test_pass_with_findings_error(self, tmp_golden):
        sha = _make_artifact(tmp_golden, "artifacts/python/test.py", "x = 1\n")
        _make_annotation(tmp_golden, "test", {
            "schema_version": "1.0",
            "artifact": "artifacts/python/test.py",
            "artifact_sha256": sha,
            "expected_verdict": "PASS",
            "findings": [{"id": "GT-001", "description": "bug", "severity": "HIGH",
                          "category": "security", "critic": "security"}],
            "metadata": {
                "source": "synthetic", "domain": "python-code", "complexity": "low",
                "rubric": "python-code", "depth": "standard", "author": "test", "created": "2026-03-12",
            },
        })
        errors = validate_annotations(tmp_golden / "annotations", tmp_golden)
        assert any("PASS verdict but has" in e for e in errors)

    def test_no_annotations(self, tmp_golden):
        errors = validate_annotations(tmp_golden / "annotations", tmp_golden)
        assert any("No annotation" in e for e in errors)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_all_false_positives(self):
        """Quorum only produces findings that don't match anything."""
        qf = [
            _make_q_finding("F-001", critic="correctness", category="correctness"),
            _make_q_finding("F-002", critic="completeness", category="completeness"),
        ]
        results, tp, fp, fn, trapped, sev_m, sev_d = match_findings([], qf, [])
        assert tp == 0
        assert fp == 2
        assert fn == 0

    def test_metrics_with_zero_scores(self):
        """Empty scores list should not crash."""
        metrics = compute_metrics([])
        assert metrics["aggregate"]["precision"] == 0.0
        assert metrics["aggregate"]["recall"] == 0.0

    def test_safe_div_zero(self):
        assert _safe_div(1, 0) == 0.0
        assert _safe_div(0, 0) == 0.0
        assert _safe_div(3, 4) == 0.75
