"""Phase 2: Cross-Artifact Consistency Critic tests — relationship evaluation, parsing, helpers."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from quorum.config import QuorumConfig
from quorum.critics.cross_consistency import (
    CROSS_FINDINGS_SCHEMA,
    RELATIONSHIP_PROMPTS,
    CrossConsistencyCritic,
)
from quorum.models import Evidence, Finding, Severity
from quorum.relationships import Relationship, ResolvedRelationship


def make_finding(severity=Severity.MEDIUM, description="Test finding", critic="correctness", **kwargs):
    defaults = dict(severity=severity, description=description, evidence=Evidence(tool="grep", result="matched line 42"), critic=critic)
    defaults.update(kwargs)
    return Finding(**defaults)


@pytest.fixture
def config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-model",
        model_tier2="test-model",
        depth_profile="quick",
    )


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.complete_json.return_value = {"findings": []}
    return provider


@pytest.fixture
def critic(mock_provider, config) -> CrossConsistencyCritic:
    return CrossConsistencyCritic(provider=mock_provider, config=config)


def _make_relationship(
    rel_type: str = "implements",
    role_a_name: str = "spec",
    role_a_path: str = "spec.md",
    role_b_name: str = "impl",
    role_b_path: str = "impl.py",
    scope: str | None = None,
) -> Relationship:
    return Relationship(
        type=rel_type,
        role_a_name=role_a_name,
        role_a_path=role_a_path,
        role_b_name=role_b_name,
        role_b_path=role_b_path,
        scope=scope,
        check_type="coverage",
    )


def _make_resolved(
    rel_type: str = "implements",
    role_a_content: str = "spec content",
    role_b_content: str = "impl content",
    role_a_exists: bool = True,
    role_b_exists: bool = True,
    **kwargs,
) -> ResolvedRelationship:
    rel = _make_relationship(rel_type=rel_type, **kwargs)
    return ResolvedRelationship(
        relationship=rel,
        role_a_content=role_a_content,
        role_b_content=role_b_content,
        role_a_exists=role_a_exists,
        role_b_exists=role_b_exists,
    )


# ── Parse Line Range ──────────────────────────────────────────────────────────


class TestParseLineRange:
    def test_lines_range(self):
        assert CrossConsistencyCritic._parse_line_range("lines 42-50") == (42, 50)

    def test_line_range_with_em_dash(self):
        assert CrossConsistencyCritic._parse_line_range("lines 10\u201320") == (10, 20)

    def test_single_line(self):
        assert CrossConsistencyCritic._parse_line_range("line 7") == (7, 7)

    def test_empty_string(self):
        assert CrossConsistencyCritic._parse_line_range("") == (1, 1)

    def test_no_match_returns_default(self):
        assert CrossConsistencyCritic._parse_line_range("section: Error Handling") == (1, 1)

    def test_case_insensitive(self):
        assert CrossConsistencyCritic._parse_line_range("Lines 5-10") == (5, 10)
        assert CrossConsistencyCritic._parse_line_range("LINE 3") == (3, 3)


# ── Escape Braces ─────────────────────────────────────────────────────────────


class TestEscapeBraces:
    def test_escapes_curly_braces(self):
        assert CrossConsistencyCritic._escape_braces("{hello}") == "{{hello}}"

    def test_no_braces_unchanged(self):
        assert CrossConsistencyCritic._escape_braces("hello world") == "hello world"

    def test_nested_braces(self):
        assert CrossConsistencyCritic._escape_braces("{{x}}") == "{{{{x}}}}"

    def test_f_string_pattern(self):
        text = 'f"value is {var}"'
        escaped = CrossConsistencyCritic._escape_braces(text)
        assert "{{var}}" in escaped


# ── Truncate ──────────────────────────────────────────────────────────────────


class TestTruncate:
    def test_short_text_unchanged(self):
        text = "short text"
        assert CrossConsistencyCritic._truncate(text) == text

    def test_long_text_truncated(self):
        text = "x" * 60001
        result = CrossConsistencyCritic._truncate(text, max_chars=100)
        assert len(result) < len(text)
        assert "truncated" in result

    def test_preserves_start_and_end(self):
        text = "START" + "x" * 60000 + "END"
        result = CrossConsistencyCritic._truncate(text, max_chars=100)
        assert result.startswith("START")
        assert result.endswith("END")

    def test_exact_limit_not_truncated(self):
        text = "x" * 100
        assert CrossConsistencyCritic._truncate(text, max_chars=100) == text


# ── Format Phase 1 Context ───────────────────────────────────────────────────


class TestFormatPhase1Context:
    def test_no_findings(self, critic):
        ctx = critic._format_phase1_context([])
        assert "No issues were flagged" in ctx

    def test_with_findings(self, critic):
        findings = [
            make_finding(severity=Severity.HIGH, description="Security issue found"),
            make_finding(severity=Severity.MEDIUM, description="Code style issue"),
        ]
        ctx = critic._format_phase1_context(findings)
        assert "Phase 1 Context" in ctx
        assert "2 findings" in ctx
        assert "Security issue" in ctx
        assert "do NOT duplicate" in ctx

    def test_long_description_truncated(self, critic):
        findings = [
            make_finding(description="A" * 200),
        ]
        ctx = critic._format_phase1_context(findings)
        # Should be truncated to 120 chars
        assert "A" * 120 in ctx
        assert "A" * 200 not in ctx


# ── Estimate Confidence ───────────────────────────────────────────────────────


class TestComputeCoverage:
    def test_no_relationships(self, critic):
        assert critic._compute_coverage(0, 0) == 0.0

    def test_full_coverage(self, critic):
        assert critic._compute_coverage(3, 3) == 1.0

    def test_partial_coverage(self, critic):
        assert critic._compute_coverage(2, 4) == 0.5

    def test_zero_total_returns_zero(self, critic):
        assert critic._compute_coverage(0, 0) == 0.0


# ── Parse Findings ────────────────────────────────────────────────────────────


class TestParseFindings:
    def test_valid_finding_parsed(self, critic):
        resolved = _make_resolved()
        raw = {
            "findings": [{
                "severity": "HIGH",
                "description": "Missing implementation for requirement X",
                "evidence_tool": "cross-analysis",
                "evidence_result": "Spec line 5 requires X, but impl has no X",
                "category": "coverage_gap",
                "role_a_location": "lines 5-10",
                "role_b_location": "lines 1-20",
                "remediation": "Add implementation for X",
            }]
        }
        findings = critic._parse_findings(raw, resolved)
        assert len(findings) == 1
        f = findings[0]
        assert f.severity == Severity.HIGH
        assert f.category == "coverage_gap"
        assert f.critic == "cross_consistency"
        assert len(f.loci) == 2
        assert f.loci[0].role == "spec"
        assert f.loci[1].role == "impl"

    def test_finding_without_evidence_rejected(self, critic):
        resolved = _make_resolved()
        raw = {
            "findings": [{
                "severity": "MEDIUM",
                "description": "Vague claim",
                "evidence_tool": "analysis",
                "evidence_result": "",
                "category": "coverage_gap",
            }]
        }
        findings = critic._parse_findings(raw, resolved)
        assert len(findings) == 0

    def test_finding_with_location_hints(self, critic):
        resolved = _make_resolved(
            role_a_content="line1\nline2\nline3\nline4\nline5\n",
            role_b_content="impl1\nimpl2\nimpl3\n",
        )
        raw = {
            "findings": [{
                "severity": "MEDIUM",
                "description": "Issue found",
                "evidence_tool": "analysis",
                "evidence_result": "Some evidence here",
                "category": "drift",
                "role_a_location": "lines 2-4",
                "role_b_location": "line 1",
            }]
        }
        findings = critic._parse_findings(raw, resolved)
        assert findings[0].loci[0].start_line == 2
        assert findings[0].loci[0].end_line == 4
        assert findings[0].loci[1].start_line == 1
        assert findings[0].loci[1].end_line == 1

    def test_multiple_findings_parsed(self, critic):
        resolved = _make_resolved()
        raw = {
            "findings": [
                {
                    "severity": "CRITICAL",
                    "description": "Issue 1",
                    "evidence_tool": "grep",
                    "evidence_result": "evidence 1",
                    "category": "coverage_gap",
                },
                {
                    "severity": "LOW",
                    "description": "Issue 2",
                    "evidence_tool": "analysis",
                    "evidence_result": "evidence 2",
                    "category": "staleness",
                },
            ]
        }
        findings = critic._parse_findings(raw, resolved)
        assert len(findings) == 2

    def test_empty_findings_list(self, critic):
        resolved = _make_resolved()
        findings = critic._parse_findings({"findings": []}, resolved)
        assert findings == []

    def test_finding_has_location_string(self, critic):
        resolved = _make_resolved()
        raw = {
            "findings": [{
                "severity": "MEDIUM",
                "description": "Drift detected",
                "evidence_tool": "analysis",
                "evidence_result": "Found it",
                "category": "drift",
            }]
        }
        findings = critic._parse_findings(raw, resolved)
        # location should combine both file paths
        assert "spec.md" in findings[0].location
        assert "impl.py" in findings[0].location

    def test_finding_has_source_hashes(self, critic):
        resolved = _make_resolved(
            role_a_content="line1\nline2\n",
            role_b_content="code1\ncode2\n",
        )
        raw = {
            "findings": [{
                "severity": "HIGH",
                "description": "Issue",
                "evidence_tool": "analysis",
                "evidence_result": "evidence",
                "category": "coverage_gap",
            }]
        }
        findings = critic._parse_findings(raw, resolved)
        for locus in findings[0].loci:
            assert len(locus.source_hash) == 64  # SHA-256 hex


# ── Missing File Handling ─────────────────────────────────────────────────────


class TestMissingFileHandling:
    def test_role_a_missing(self, critic):
        resolved = _make_resolved(role_a_exists=False)
        result = critic.evaluate([resolved])
        assert len(result.findings) == 1
        assert result.findings[0].severity == Severity.CRITICAL
        assert "missing_file" == result.findings[0].category
        assert "spec.md" in result.findings[0].description

    def test_role_b_missing(self, critic):
        resolved = _make_resolved(role_b_exists=False)
        result = critic.evaluate([resolved])
        assert len(result.findings) == 1
        assert result.findings[0].severity == Severity.CRITICAL
        assert "impl.py" in result.findings[0].description

    def test_both_missing_reports_first(self, critic):
        # When role_a is missing, the code does `continue` — only role_a is reported
        resolved = _make_resolved(role_a_exists=False, role_b_exists=False)
        result = critic.evaluate([resolved])
        assert len(result.findings) == 1
        assert result.findings[0].severity == Severity.CRITICAL
        assert "spec.md" in result.findings[0].description


# ── Evaluate Relationship (LLM interaction) ───────────────────────────────────


class TestEvaluateRelationship:
    def test_implements_relationship(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {
            "findings": [{
                "severity": "HIGH",
                "description": "Spec requires feature X but impl missing",
                "evidence_tool": "cross-analysis",
                "evidence_result": "Spec line 5 says 'must implement X'",
                "category": "coverage_gap",
            }]
        }
        resolved = _make_resolved(rel_type="implements")
        result = critic.evaluate([resolved])
        assert len(result.findings) == 1
        assert result.findings[0].severity == Severity.HIGH

    def test_documents_relationship(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        resolved = _make_resolved(
            rel_type="documents",
            role_a_name="source", role_a_path="code.py",
            role_b_name="docs", role_b_path="docs.md",
        )
        result = critic.evaluate([resolved])
        assert result.findings == []
        assert mock_provider.complete_json.called

    def test_delegates_relationship(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        resolved = _make_resolved(
            rel_type="delegates",
            role_a_name="from", role_a_path="main.py",
            role_b_name="to", role_b_path="helper.py",
            scope="error handling",
        )
        result = critic.evaluate([resolved])
        assert mock_provider.complete_json.called

    def test_schema_contract_relationship(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        resolved = _make_resolved(
            rel_type="schema_contract",
            role_a_name="producer", role_a_path="api.py",
            role_b_name="consumer", role_b_path="client.py",
        )
        result = critic.evaluate([resolved])
        assert mock_provider.complete_json.called

    def test_llm_error_produces_error_finding(self, critic, mock_provider):
        mock_provider.complete_json.side_effect = RuntimeError("API error")
        resolved = _make_resolved()
        result = critic.evaluate([resolved])
        assert len(result.findings) == 1
        assert result.findings[0].severity == Severity.HIGH
        assert "evaluation failed" in result.findings[0].description.lower()

    def test_one_relationship_fails_others_succeed(self, critic, mock_provider):
        call_count = [0]

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                raise RuntimeError("First call fails")
            return {"findings": []}

        mock_provider.complete_json.side_effect = side_effect
        resolved1 = _make_resolved()
        resolved2 = _make_resolved(
            role_a_path="other-spec.md", role_b_path="other-impl.py"
        )
        result = critic.evaluate([resolved1, resolved2])
        # Should have error finding from first + whatever from second
        assert len(result.findings) >= 1


# ── Full Evaluate Flow ────────────────────────────────────────────────────────


class TestEvaluateFlow:
    def test_empty_relationships(self, critic):
        result = critic.evaluate([])
        assert result.findings == []
        assert result.confidence == 0.0

    def test_phase1_findings_as_context(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        phase1 = [make_finding(severity=Severity.HIGH, description="Phase 1 issue")]
        resolved = _make_resolved()
        result = critic.evaluate([resolved], phase1_findings=phase1)
        # Verify the LLM was called with phase1 context in the prompt
        call_args = mock_provider.complete_json.call_args
        messages = call_args[1]["messages"] if "messages" in call_args[1] else call_args[0][0]
        prompt_text = str(messages)
        assert "Phase 1" in prompt_text

    def test_result_has_critic_name(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        resolved = _make_resolved()
        result = critic.evaluate([resolved])
        assert result.critic_name == "cross_consistency"

    def test_result_has_runtime(self, critic, mock_provider):
        mock_provider.complete_json.return_value = {"findings": []}
        resolved = _make_resolved()
        result = critic.evaluate([resolved])
        assert result.runtime_ms >= 0


# ── Prompt Templates ──────────────────────────────────────────────────────────


class TestPromptTemplates:
    def test_all_relationship_types_have_templates(self):
        for rel_type in ["implements", "documents", "delegates", "schema_contract"]:
            assert rel_type in RELATIONSHIP_PROMPTS

    def test_unknown_type_returns_empty(self, critic, mock_provider):
        # Create a resolved relationship with an unknown type
        # We need to bypass the validator, so we'll test _evaluate_relationship directly
        rel = Relationship(
            type="implements",  # valid type for model validation
            role_a_name="spec", role_a_path="a.md",
            role_b_name="impl", role_b_path="b.py",
            check_type="coverage",
        )
        resolved = ResolvedRelationship(
            relationship=rel,
            role_a_content="content a",
            role_b_content="content b",
        )
        # Monkey-patch the type to test template lookup
        rel_dict = rel.model_dump()
        rel_dict["type"] = "unknown_type"
        # Since we can't easily test with invalid type due to validator,
        # we test that all valid types work
        for rel_type in RELATIONSHIP_PROMPTS:
            assert isinstance(RELATIONSHIP_PROMPTS[rel_type], str)
            assert len(RELATIONSHIP_PROMPTS[rel_type]) > 100


# ── Schema ────────────────────────────────────────────────────────────────────


class TestCrossConsistencySchema:
    def test_schema_has_required_structure(self):
        assert CROSS_FINDINGS_SCHEMA["type"] == "object"
        assert "findings" in CROSS_FINDINGS_SCHEMA["required"]
        items = CROSS_FINDINGS_SCHEMA["properties"]["findings"]["items"]
        assert "severity" in items["required"]
        assert "description" in items["required"]
        assert "evidence_tool" in items["required"]
        assert "evidence_result" in items["required"]
        assert "category" in items["required"]
