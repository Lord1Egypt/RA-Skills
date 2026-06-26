# SPDX-License-Identifier: MIT
# Copyright 2026 SharedIntellect — https://github.com/SharedIntellect/quorum

"""
Comprehensive tests for the Tester critic (Phase 1).

Covers:
- Locus parsing from various text formats
- Level 1 deterministic verification (good, bad, edge cases)
- Level 2 LLM-assisted verification (mocked)
- TesterCritic orchestration
- Edge cases: empty findings, binary files, large files, no loci
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.critics.tester import (
    FUZZY_MATCH_CONTRADICTED,
    FUZZY_MATCH_VERIFIED,
    ParsedLocus,
    TesterCritic,
    parse_loci_from_finding,
    parse_locus_from_text,
    verify_finding_l1,
    verify_finding_l2,
    _is_binary_content,
    _read_file_lines,
    _fuzzy_match_in_lines,
    _best_subsequence_match,
    _resolve_file_path,
)
from quorum.models import (
    CriticResult,
    Evidence,
    Finding,
    Locus,
    Severity,
    TesterResult,
    VerificationResult,
    VerificationStatus,
    VerifiedLocus,
)


# ── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_py_file(tmp_path: Path) -> Path:
    """Create a sample Python file with known content."""
    content = textwrap.dedent("""\
        import os
        import sys

        def calculate_total(items):
            total = 0
            for item in items:
                total += item.price
            return total

        def process_data(data):
            if not data:
                return None
            result = []
            for entry in data:
                result.append(entry.strip())
            return result

        class UserManager:
            def __init__(self):
                self.users = {}

            def add_user(self, name, email):
                self.users[name] = email

            def get_user(self, name):
                return self.users.get(name)
    """)
    f = tmp_path / "sample.py"
    f.write_text(content)
    return f


@pytest.fixture
def sample_py_content() -> str:
    return textwrap.dedent("""\
        import os
        import sys

        def calculate_total(items):
            total = 0
            for item in items:
                total += item.price
            return total

        def process_data(data):
            if not data:
                return None
            result = []
            for entry in data:
                result.append(entry.strip())
            return result

        class UserManager:
            def __init__(self):
                self.users = {}

            def add_user(self, name, email):
                self.users[name] = email

            def get_user(self, name):
                return self.users.get(name)
    """)


@pytest.fixture
def tester_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["tester"],
        model_tier1="anthropic/claude-opus-4-6",
        model_tier2="anthropic/claude-sonnet-4-6",
        depth_profile="quick",
    )


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.complete_json.return_value = {
        "verdict": "VERIFIED",
        "explanation": "The claim accurately describes the code.",
    }
    return provider


def _make_finding(
    location: str | None = None,
    evidence_result: str = "some evidence",
    severity: Severity = Severity.HIGH,
    description: str = "Test finding",
    loci: list[Locus] | None = None,
    **kwargs: Any,
) -> Finding:
    return Finding(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result=evidence_result),
        location=location,
        critic="correctness",
        loci=loci or [],
        **kwargs,
    )


# ── Locus parsing tests ────────────────────────────────────────────────────


class TestLocusParsing:
    """Tests for parse_locus_from_text and parse_loci_from_finding."""

    def test_file_colon_line(self):
        pl = parse_locus_from_text("sample.py:42")
        assert pl is not None
        assert pl.file_path == "sample.py"
        assert pl.start_line == 42
        assert pl.end_line == 42

    def test_file_colon_line_range(self):
        pl = parse_locus_from_text("src/main.py:10-20")
        assert pl is not None
        assert pl.file_path == "src/main.py"
        assert pl.start_line == 10
        assert pl.end_line == 20

    def test_line_of_file(self):
        pl = parse_locus_from_text("line 42 of sample.py")
        assert pl is not None
        assert pl.file_path == "sample.py"
        assert pl.start_line == 42

    def test_lines_of_file(self):
        pl = parse_locus_from_text("lines 10-20 of src/main.py")
        assert pl is not None
        assert pl.file_path == "src/main.py"
        assert pl.start_line == 10
        assert pl.end_line == 20

    def test_file_comma_line(self):
        pl = parse_locus_from_text("sample.py, line 42")
        assert pl is not None
        assert pl.file_path == "sample.py"
        assert pl.start_line == 42

    def test_in_file_paren_line(self):
        pl = parse_locus_from_text("in sample.py (line 42)")
        assert pl is not None
        assert pl.file_path == "sample.py"
        assert pl.start_line == 42

    def test_file_only(self):
        pl = parse_locus_from_text("Found issue in config.yaml")
        assert pl is not None
        assert pl.file_path == "config.yaml"
        assert pl.start_line is None

    def test_no_locus(self):
        pl = parse_locus_from_text("General code quality concern")
        assert pl is None

    def test_empty_string(self):
        assert parse_locus_from_text("") is None

    def test_none_input(self):
        assert parse_locus_from_text(None) is None

    def test_complex_path(self):
        pl = parse_locus_from_text("src/utils/helpers.py:100")
        assert pl is not None
        assert pl.file_path == "src/utils/helpers.py"
        assert pl.start_line == 100

    def test_line_in_file(self):
        pl = parse_locus_from_text("line 5 in models.py")
        assert pl is not None
        assert pl.file_path == "models.py"
        assert pl.start_line == 5


class TestParseLocifromFinding:
    """Tests for parse_loci_from_finding — extraction from Finding objects."""

    def test_from_structured_locus(self):
        locus = Locus(
            file="sample.py",
            start_line=10,
            end_line=15,
            role="implementation",
            source_hash="abc123",
        )
        finding = _make_finding(loci=[locus])
        parsed = parse_loci_from_finding(finding)
        assert len(parsed) >= 1
        assert parsed[0].file_path == "sample.py"
        assert parsed[0].start_line == 10
        assert parsed[0].end_line == 15

    def test_from_location_text(self):
        finding = _make_finding(location="sample.py:42")
        parsed = parse_loci_from_finding(finding)
        assert len(parsed) >= 1
        assert parsed[0].file_path == "sample.py"
        assert parsed[0].start_line == 42

    def test_from_evidence_text(self):
        finding = _make_finding(
            location=None,
            evidence_result="Found at config.yaml:10",
        )
        parsed = parse_loci_from_finding(finding)
        assert len(parsed) >= 1
        assert parsed[0].file_path == "config.yaml"

    def test_no_loci_at_all(self):
        finding = _make_finding(
            location=None,
            evidence_result="General quality concern",
        )
        parsed = parse_loci_from_finding(finding)
        assert parsed == []

    def test_deduplicates_same_file_line(self):
        """Same file:line from location and evidence should only appear once."""
        locus = Locus(
            file="sample.py",
            start_line=42,
            end_line=42,
            role="impl",
            source_hash="x",
        )
        finding = _make_finding(
            location="sample.py:42",
            evidence_result="at sample.py:42",
            loci=[locus],
        )
        parsed = parse_loci_from_finding(finding)
        # All three sources point to the same file:line
        assert len(parsed) == 1

    def test_multiple_distinct_loci(self):
        """Different file:line from structured locus and location text."""
        locus = Locus(
            file="a.py",
            start_line=1,
            end_line=1,
            role="impl",
            source_hash="x",
        )
        finding = _make_finding(
            location="b.py:10",
            loci=[locus],
        )
        parsed = parse_loci_from_finding(finding)
        assert len(parsed) == 2


# ── Level 1 verification tests ─────────────────────────────────────────────


class TestLevel1Verification:
    """Tests for verify_finding_l1 — deterministic file/content verification."""

    def test_verified_exact_match(self, sample_py_file: Path, tmp_path: Path):
        """Finding with correct locus and exact evidence should VERIFY."""
        finding = _make_finding(
            location="sample.py:4",
            evidence_result="def calculate_total(items):",
            description="Function calculate_total at line 4",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.VERIFIED
        assert result.original_finding_id == finding.id
        assert result.level == 1
        assert result.verified_locus is not None
        assert result.verified_locus.similarity_score >= FUZZY_MATCH_VERIFIED

    def test_verified_fuzzy_match(self, sample_py_file: Path, tmp_path: Path):
        """Finding with slightly different evidence text should still VERIFY."""
        finding = _make_finding(
            location="sample.py:4",
            evidence_result="def  calculate_total(items) :",  # extra spaces
            description="Function with extra whitespace",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.VERIFIED

    def test_wrong_line_but_content_found_in_file(self, sample_py_file: Path, tmp_path: Path):
        """Finding citing wrong line but real content should VERIFY via full-file scan."""
        finding = _make_finding(
            location="sample.py:1",
            evidence_result="def calculate_total(items):",
            description="Claims calculate_total is at line 1 (it's actually at line 4)",
        )
        result = verify_finding_l1(finding, tmp_path)
        # The full-file fallback scan finds the exact content → VERIFIED
        assert result.status == VerificationStatus.VERIFIED

    def test_contradicted_hallucinated_line(self, sample_py_file: Path, tmp_path: Path):
        """Finding citing a line beyond file length should CONTRADICT."""
        finding = _make_finding(
            location="sample.py:9999",
            evidence_result="this line does not exist",
            description="Hallucinated line number",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.CONTRADICTED
        assert "beyond file length" in result.explanation

    def test_contradicted_file_not_found(self, tmp_path: Path):
        """Finding citing a nonexistent file should CONTRADICT."""
        finding = _make_finding(
            location="nonexistent.py:10",
            evidence_result="some code",
            description="File does not exist",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.CONTRADICTED
        assert "not found" in result.explanation.lower() or "Cannot read" in result.explanation

    def test_unverified_no_locus(self):
        """Finding with no parseable locus should be UNVERIFIED (not crash)."""
        finding = _make_finding(
            location=None,
            evidence_result="General quality concern without file reference",
            description="Vague finding",
        )
        result = verify_finding_l1(finding, Path("/tmp"))
        assert result.status == VerificationStatus.UNVERIFIED
        assert "No parseable" in result.explanation

    def test_verified_multiline_locus(self, sample_py_file: Path, tmp_path: Path):
        """Finding citing a range of lines should verify against that range."""
        finding = _make_finding(
            location="sample.py:4-8",
            evidence_result="def calculate_total(items):\n    total = 0\n    for item in items:\n        total += item.price\n    return total",
            description="Multi-line function body",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.VERIFIED

    def test_verified_without_line_number(self, sample_py_file: Path, tmp_path: Path):
        """Finding with file but no line — should still search the whole file."""
        finding = _make_finding(
            location="sample.py",
            evidence_result="def calculate_total(items):",
            description="Function exists somewhere in file",
        )
        result = verify_finding_l1(finding, tmp_path)
        # Full-file scan should find the match
        assert result.status == VerificationStatus.VERIFIED

    def test_contradicted_completely_wrong_content(self, sample_py_file: Path, tmp_path: Path):
        """Cited evidence that doesn't exist anywhere in the file → CONTRADICTED or UNVERIFIED."""
        finding = _make_finding(
            location="sample.py:4",
            evidence_result="QQWWZZ JJKKXX = 99999; /* QQWWZZ JJKKXX */ #QQWWZZ",
            description="Completely fabricated code citation",
        )
        result = verify_finding_l1(finding, tmp_path)
        # Fabricated content should never be VERIFIED
        assert result.status in (
            VerificationStatus.CONTRADICTED,
            VerificationStatus.UNVERIFIED,
        )
        assert result.verified_locus is not None
        assert result.verified_locus.similarity_score < FUZZY_MATCH_VERIFIED

    def test_binary_file(self, tmp_path: Path):
        """Binary files should result in CONTRADICTED (can't verify text loci)."""
        binary_file = tmp_path / "image.png"
        binary_file.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
        finding = _make_finding(
            location="image.png:1",
            evidence_result="some text",
            description="Claims text in binary file",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.CONTRADICTED
        assert "Binary" in result.explanation or "Cannot read" in result.explanation

    def test_large_file_within_limit(self, tmp_path: Path):
        """Files within size limit should be read and verified normally."""
        large = tmp_path / "big.py"
        lines = [f"# line {i}\n" for i in range(10000)]
        large.write_text("".join(lines))
        finding = _make_finding(
            location="big.py:5000",
            evidence_result="# line 4999",
            description="Line in the middle of a large file",
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.VERIFIED

    def test_structured_locus_used(self, sample_py_file: Path, tmp_path: Path):
        """Findings with structured Locus objects should use them for verification."""
        locus = Locus(
            file="sample.py",
            start_line=4,
            end_line=4,
            role="implementation",
            source_hash="ignored_for_tester",
        )
        finding = _make_finding(
            evidence_result="def calculate_total(items):",
            loci=[locus],
        )
        result = verify_finding_l1(finding, tmp_path)
        assert result.status == VerificationStatus.VERIFIED


# ── Level 2 verification tests (mocked LLM) ────────────────────────────────


class TestLevel2Verification:
    """Tests for verify_finding_l2 — LLM-assisted claim verification."""

    def test_l2_verified(self, mock_provider: MagicMock, tester_config: QuorumConfig):
        """LLM returns VERIFIED → result should be VERIFIED."""
        mock_provider.complete_json.return_value = {
            "verdict": "VERIFIED",
            "explanation": "The function indeed has no return type annotation.",
        }
        finding = _make_finding(
            description="Function calculate_total has no return type annotation",
        )
        result = verify_finding_l2(
            finding, "def calculate_total(items):\n    total = 0", mock_provider, tester_config
        )
        assert result.status == VerificationStatus.VERIFIED
        assert result.level == 2
        mock_provider.complete_json.assert_called_once()

    def test_l2_contradicted(self, mock_provider: MagicMock, tester_config: QuorumConfig):
        """LLM returns CONTRADICTED → result should be CONTRADICTED."""
        mock_provider.complete_json.return_value = {
            "verdict": "CONTRADICTED",
            "explanation": "The function actually does have a return statement.",
        }
        finding = _make_finding(
            description="Function never returns a value",
        )
        result = verify_finding_l2(
            finding, "def foo():\n    return 42", mock_provider, tester_config
        )
        assert result.status == VerificationStatus.CONTRADICTED

    def test_l2_unverified(self, mock_provider: MagicMock, tester_config: QuorumConfig):
        """LLM returns UNVERIFIED → result should be UNVERIFIED."""
        mock_provider.complete_json.return_value = {
            "verdict": "UNVERIFIED",
            "explanation": "Cannot determine from this excerpt alone.",
        }
        finding = _make_finding(description="Ambiguous claim")
        result = verify_finding_l2(
            finding, "some code", mock_provider, tester_config
        )
        assert result.status == VerificationStatus.UNVERIFIED

    def test_l2_invalid_verdict_defaults_unverified(
        self, mock_provider: MagicMock, tester_config: QuorumConfig
    ):
        """LLM returns unknown verdict → should default to UNVERIFIED."""
        mock_provider.complete_json.return_value = {
            "verdict": "MAYBE",
            "explanation": "Not sure.",
        }
        finding = _make_finding(description="Ambiguous")
        result = verify_finding_l2(
            finding, "code", mock_provider, tester_config
        )
        assert result.status == VerificationStatus.UNVERIFIED
        assert "unknown verdict" in result.explanation.lower()

    def test_l2_provider_exception(self, mock_provider: MagicMock, tester_config: QuorumConfig):
        """Provider exception → should return UNVERIFIED gracefully."""
        mock_provider.complete_json.side_effect = RuntimeError("API timeout")
        finding = _make_finding(description="Some claim")
        result = verify_finding_l2(
            finding, "code", mock_provider, tester_config
        )
        assert result.status == VerificationStatus.UNVERIFIED
        assert "failed" in result.explanation.lower()


# ── TesterCritic orchestration tests ────────────────────────────────────────


class TestTesterCritic:
    """Tests for the TesterCritic orchestrator."""

    def test_empty_findings_list(self, tmp_path: Path):
        """Empty critic results → empty TesterResult, no crash."""
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([], tmp_path)
        assert isinstance(result, TesterResult)
        assert result.total_findings == 0
        assert result.verified_count == 0
        assert result.verification_rate == 1.0  # no findings = all good

    def test_skipped_critics_ignored(self, tmp_path: Path):
        """Findings from skipped critics should not be verified."""
        skipped_result = CriticResult(
            critic_name="security",
            findings=[_make_finding(location="foo.py:1")],
            confidence=0.0,
            skipped=True,
            skip_reason="Not applicable",
        )
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([skipped_result], tmp_path)
        assert result.total_findings == 0

    def test_verify_good_findings(self, sample_py_file: Path, tmp_path: Path):
        """Findings with correct loci should be VERIFIED."""
        findings = [
            _make_finding(
                location="sample.py:4",
                evidence_result="def calculate_total(items):",
                description="Function at line 4",
            ),
            _make_finding(
                location="sample.py:10",
                evidence_result="def process_data(data):",
                description="Function at line 10",
            ),
        ]
        critic_result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.9,
        )
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([critic_result], tmp_path)
        assert result.total_findings == 2
        assert result.verified_count == 2
        assert result.contradicted_count == 0

    def test_verify_bad_findings(self, sample_py_file: Path, tmp_path: Path):
        """Findings with fabricated evidence should be CONTRADICTED."""
        findings = [
            _make_finding(
                location="sample.py:9999",
                evidence_result="this does not exist",
                description="Hallucinated line",
            ),
        ]
        critic_result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.9,
        )
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([critic_result], tmp_path)
        assert result.total_findings == 1
        assert result.contradicted_count == 1

    def test_verify_mixed_findings(self, sample_py_file: Path, tmp_path: Path):
        """Mix of good and bad findings should produce mixed results."""
        findings = [
            _make_finding(
                location="sample.py:4",
                evidence_result="def calculate_total(items):",
                description="Good locus",
            ),
            _make_finding(
                location="sample.py:9999",
                evidence_result="nonexistent",
                description="Bad locus",
            ),
            _make_finding(
                location=None,
                evidence_result="general concern",
                description="No locus",
            ),
        ]
        critic_result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.9,
        )
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([critic_result], tmp_path)
        assert result.total_findings == 3
        assert result.verified_count >= 1
        assert result.contradicted_count >= 1
        assert result.unverified_count >= 1

    def test_l2_only_for_critical_high(
        self,
        sample_py_file: Path,
        tmp_path: Path,
        mock_provider: MagicMock,
        tester_config: QuorumConfig,
    ):
        """Level 2 should only fire for CRITICAL/HIGH by default."""
        findings = [
            _make_finding(
                location="sample.py:4",
                evidence_result="def calculate_total(items):",
                severity=Severity.CRITICAL,
                description="Critical finding",
            ),
            _make_finding(
                location="sample.py:10",
                evidence_result="def process_data(data):",
                severity=Severity.LOW,
                description="Low severity finding",
            ),
        ]
        critic_result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.9,
        )
        tester = TesterCritic(
            provider=mock_provider,
            config=tester_config,
            l2_enabled=True,
        )
        result = tester.verify([critic_result], tmp_path)
        assert result.total_findings == 2
        # L2 should have been called once (for the CRITICAL finding only)
        assert mock_provider.complete_json.call_count == 1

    def test_l2_disabled(
        self,
        sample_py_file: Path,
        tmp_path: Path,
        mock_provider: MagicMock,
        tester_config: QuorumConfig,
    ):
        """When l2_enabled=False, provider should never be called."""
        findings = [
            _make_finding(
                location="sample.py:4",
                evidence_result="def calculate_total(items):",
                severity=Severity.CRITICAL,
            ),
        ]
        critic_result = CriticResult(
            critic_name="correctness",
            findings=findings,
            confidence=0.9,
        )
        tester = TesterCritic(
            provider=mock_provider,
            config=tester_config,
            l2_enabled=False,
        )
        result = tester.verify([critic_result], tmp_path)
        mock_provider.complete_json.assert_not_called()

    def test_verify_findings_convenience(self, sample_py_file: Path, tmp_path: Path):
        """verify_findings() should work as a flat-list convenience method."""
        findings = [
            _make_finding(
                location="sample.py:4",
                evidence_result="def calculate_total(items):",
            ),
        ]
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify_findings(findings, tmp_path)
        assert result.total_findings == 1
        assert result.verified_count == 1

    def test_multiple_critic_results(self, sample_py_file: Path, tmp_path: Path):
        """Findings from multiple critics should all be verified."""
        cr1 = CriticResult(
            critic_name="correctness",
            findings=[
                _make_finding(
                    location="sample.py:4",
                    evidence_result="def calculate_total(items):",
                ),
            ],
            confidence=0.9,
        )
        cr2 = CriticResult(
            critic_name="security",
            findings=[
                Finding(
                    severity=Severity.HIGH,
                    description="Security finding at line 10",
                    evidence=Evidence(tool="grep", result="def process_data(data):"),
                    location="sample.py:10",
                    critic="security",
                ),
            ],
            confidence=0.85,
        )
        tester = TesterCritic(l2_enabled=False)
        result = tester.verify([cr1, cr2], tmp_path)
        assert result.total_findings == 2
        assert result.verified_count == 2


# ── L1/L2 merge logic tests ────────────────────────────────────────────────


class TestL1L2Merge:
    """Tests for the _merge_l1_l2 logic."""

    def _make_vr(
        self, status: VerificationStatus, level: int = 1
    ) -> VerificationResult:
        return VerificationResult(
            status=status,
            original_finding_id="F-test",
            explanation=f"Test {status.value} at L{level}",
            level=level,
            verified_locus=VerifiedLocus(
                file_path="test.py",
                actual_content="code",
                similarity_score=0.8,
            ),
        )

    def test_both_verified(self):
        tester = TesterCritic(l2_enabled=False)
        l1 = self._make_vr(VerificationStatus.VERIFIED, 1)
        l2 = self._make_vr(VerificationStatus.VERIFIED, 2)
        result = tester._merge_l1_l2(l1, l2)
        assert result.status == VerificationStatus.VERIFIED

    def test_l2_contradicts_overrides(self):
        tester = TesterCritic(l2_enabled=False)
        l1 = self._make_vr(VerificationStatus.VERIFIED, 1)
        l2 = self._make_vr(VerificationStatus.CONTRADICTED, 2)
        result = tester._merge_l1_l2(l1, l2)
        assert result.status == VerificationStatus.CONTRADICTED

    def test_l1_verified_l2_unverified_downgrades(self):
        tester = TesterCritic(l2_enabled=False)
        l1 = self._make_vr(VerificationStatus.VERIFIED, 1)
        l2 = self._make_vr(VerificationStatus.UNVERIFIED, 2)
        result = tester._merge_l1_l2(l1, l2)
        assert result.status == VerificationStatus.UNVERIFIED

    def test_l1_unverified_l2_verified_upgrades(self):
        tester = TesterCritic(l2_enabled=False)
        l1 = self._make_vr(VerificationStatus.UNVERIFIED, 1)
        l2 = self._make_vr(VerificationStatus.VERIFIED, 2)
        result = tester._merge_l1_l2(l1, l2)
        assert result.status == VerificationStatus.VERIFIED


# ── Utility function tests ──────────────────────────────────────────────────


class TestUtilities:
    """Tests for internal utility functions."""

    def test_is_binary_content_true(self):
        assert _is_binary_content(b"\x89PNG\r\n\x1a\n\x00\x00")

    def test_is_binary_content_false(self):
        assert not _is_binary_content(b"def foo(): pass\n")

    def test_read_file_lines_success(self, sample_py_file: Path):
        lines, err = _read_file_lines(sample_py_file)
        assert err is None
        assert lines is not None
        assert len(lines) > 0
        assert "import os\n" in lines

    def test_read_file_lines_not_found(self, tmp_path: Path):
        lines, err = _read_file_lines(tmp_path / "nope.py")
        assert lines is None
        assert "not found" in err.lower()

    def test_read_file_lines_binary(self, tmp_path: Path):
        f = tmp_path / "bin.dat"
        f.write_bytes(b"\x00\x01\x02\x03")
        lines, err = _read_file_lines(f)
        assert lines is None
        assert "binary" in err.lower()

    def test_read_file_lines_directory(self, tmp_path: Path):
        lines, err = _read_file_lines(tmp_path)
        assert lines is None
        assert err is not None

    def test_fuzzy_match_exact(self):
        lines = ["def foo():\n", "    pass\n"]
        score, _ = _fuzzy_match_in_lines("def foo():", lines, start_line=1)
        assert score >= 0.9

    def test_fuzzy_match_zero(self):
        lines = ["def foo():\n", "    pass\n"]
        score, _ = _fuzzy_match_in_lines(
            "class BarBazQuux(metaclass=Meta):", lines, start_line=1
        )
        assert score < FUZZY_MATCH_VERIFIED

    def test_fuzzy_match_empty_cited(self):
        lines = ["def foo():\n"]
        score, content = _fuzzy_match_in_lines("", lines, start_line=1)
        assert score == 0.0

    def test_fuzzy_match_empty_lines(self):
        score, content = _fuzzy_match_in_lines("something", [], start_line=1)
        assert score == 0.0

    def test_best_subsequence_match_identical(self):
        assert _best_subsequence_match("hello world", "hello world") > 0.99

    def test_best_subsequence_match_substring(self):
        score = _best_subsequence_match(
            "def calculate_total(items):",
            "import os\nimport sys\n\ndef calculate_total(items):\n    total = 0\n",
        )
        assert score >= 0.8

    def test_best_subsequence_match_empty(self):
        assert _best_subsequence_match("", "something") == 0.0
        assert _best_subsequence_match("something", "") == 0.0

    def test_resolve_file_path_relative(self, sample_py_file: Path, tmp_path: Path):
        resolved = _resolve_file_path("sample.py", tmp_path)
        assert resolved == sample_py_file

    def test_resolve_file_path_not_found(self, tmp_path: Path):
        """Non-existent file should still return a path (resolution doesn't fail)."""
        resolved = _resolve_file_path("nope.py", tmp_path)
        assert resolved == tmp_path / "nope.py"

    def test_resolve_file_path_absolute(self, sample_py_file: Path, tmp_path: Path):
        resolved = _resolve_file_path(str(sample_py_file), tmp_path)
        assert resolved == sample_py_file


# ── Model tests ─────────────────────────────────────────────────────────────


class TestVerificationModels:
    """Tests for the new Pydantic models."""

    def test_verification_status_enum(self):
        assert VerificationStatus.VERIFIED.value == "VERIFIED"
        assert VerificationStatus.UNVERIFIED.value == "UNVERIFIED"
        assert VerificationStatus.CONTRADICTED.value == "CONTRADICTED"

    def test_verification_result_serialization(self):
        vr = VerificationResult(
            status=VerificationStatus.VERIFIED,
            original_finding_id="F-abc12345",
            explanation="Content matches",
            level=1,
        )
        d = vr.model_dump()
        assert d["status"] == "VERIFIED"
        assert d["original_finding_id"] == "F-abc12345"

    def test_verified_locus_model(self):
        vl = VerifiedLocus(
            file_path="test.py",
            line_start=10,
            line_end=15,
            actual_content="def foo(): pass",
            similarity_score=0.92,
        )
        assert vl.file_path == "test.py"
        assert vl.similarity_score == 0.92

    def test_tester_result_rates(self):
        tr = TesterResult(
            total_findings=10,
            verified_count=7,
            unverified_count=2,
            contradicted_count=1,
        )
        assert tr.verification_rate == 0.7
        assert tr.contradiction_rate == 0.1

    def test_tester_result_empty(self):
        tr = TesterResult()
        assert tr.verification_rate == 1.0
        assert tr.contradiction_rate == 0.0

    def test_verification_result_with_locus(self):
        vl = VerifiedLocus(
            file_path="x.py",
            actual_content="code",
            similarity_score=0.5,
        )
        vr = VerificationResult(
            status=VerificationStatus.UNVERIFIED,
            original_finding_id="F-test",
            explanation="Partial match",
            verified_locus=vl,
            level=1,
        )
        assert vr.verified_locus is not None
        assert vr.verified_locus.file_path == "x.py"


# ── ParsedLocus repr test ──────────────────────────────────────────────────


class TestParsedLocus:
    def test_repr_with_line(self):
        pl = ParsedLocus("foo.py", 10, 10)
        assert "foo.py:10" in repr(pl)

    def test_repr_with_range(self):
        pl = ParsedLocus("foo.py", 10, 20)
        assert "foo.py:10-20" in repr(pl)

    def test_repr_without_line(self):
        pl = ParsedLocus("foo.py")
        assert "foo.py" in repr(pl)
        assert ":" not in repr(pl)


# ── Import test ─────────────────────────────────────────────────────────────


class TestImports:
    """Verify the module is importable from the expected paths."""

    def test_import_from_critics_package(self):
        from quorum.critics import TesterCritic
        assert TesterCritic.name == "tester"

    def test_import_from_critics_tester(self):
        from quorum.critics.tester import TesterCritic
        assert TesterCritic.name == "tester"

    def test_import_models(self):
        from quorum.models import (
            VerificationStatus,
            VerificationResult,
            VerifiedLocus,
            TesterResult,
        )
        assert VerificationStatus.VERIFIED.value == "VERIFIED"
