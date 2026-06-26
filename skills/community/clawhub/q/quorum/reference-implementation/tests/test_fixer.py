"""Phase 2: Fixer Agent tests — proposal generation, filtering, error handling."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from quorum.agents.fixer import FixerAgent, _format_findings
from quorum.config import QuorumConfig
from quorum.models import Evidence, Finding, FixProposal, FixReport, Severity


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
    provider.complete_json.return_value = {"fixes": []}
    return provider


@pytest.fixture
def fixer(mock_provider, config) -> FixerAgent:
    return FixerAgent(provider=mock_provider, config=config)


SAMPLE_ARTIFACT = "line one\nline two has a bug\nline three\n"


# ── Format Findings Helper ───────────────────────────────────────────────────


class TestFormatFindings:
    def test_formats_numbered_list(self):
        findings = [
            make_finding(severity=Severity.CRITICAL, description="Bad thing"),
            make_finding(severity=Severity.HIGH, description="Another issue"),
        ]
        text = _format_findings(findings)
        assert "1." in text
        assert "2." in text
        assert "CRITICAL" in text
        assert "HIGH" in text
        assert "Bad thing" in text

    def test_includes_location(self):
        f = make_finding(description="Issue here", location="line 42")
        text = _format_findings([f])
        assert "line 42" in text

    def test_includes_remediation(self):
        f = make_finding(description="Issue", remediation="Fix it this way")
        text = _format_findings([f])
        assert "Fix it this way" in text

    def test_empty_findings(self):
        text = _format_findings([])
        assert text == ""


# ── Severity Filtering ────────────────────────────────────────────────────────


class TestFixerFiltering:
    def test_only_critical_high_processed(self, fixer, mock_provider):
        findings = [
            make_finding(severity=Severity.CRITICAL, description="critical issue"),
            make_finding(severity=Severity.HIGH, description="high issue"),
            make_finding(severity=Severity.MEDIUM, description="medium issue"),
            make_finding(severity=Severity.LOW, description="low issue"),
        ]
        report = fixer.run(findings, SAMPLE_ARTIFACT, "test.py")
        # The provider should have been called — CRITICAL and HIGH exist
        assert mock_provider.complete_json.called

    def test_no_actionable_findings(self, fixer, mock_provider):
        findings = [
            make_finding(severity=Severity.MEDIUM, description="only medium"),
            make_finding(severity=Severity.LOW, description="only low"),
        ]
        report = fixer.run(findings, SAMPLE_ARTIFACT, "test.py")
        assert report.proposals == []
        assert report.findings_skipped == 2
        assert "below CRITICAL/HIGH threshold" in report.skip_reasons[0]
        assert not mock_provider.complete_json.called

    def test_empty_findings_returns_empty_report(self, fixer, mock_provider):
        report = fixer.run([], SAMPLE_ARTIFACT, "test.py")
        assert report.proposals == []
        assert report.findings_addressed == 0
        assert not mock_provider.complete_json.called


# ── Proposal Generation ──────────────────────────────────────────────────────


class TestFixerProposalGeneration:
    def test_valid_proposal_accepted(self, fixer, mock_provider):
        finding = make_finding(
            severity=Severity.CRITICAL,
            description="Bug in line two",
        )
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id,
                "original_text": "line two has a bug",
                "replacement_text": "line two is fixed",
                "explanation": "Fixed the bug",
                "confidence": 0.95,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 1
        assert report.proposals[0].original_text == "line two has a bug"
        assert report.proposals[0].replacement_text == "line two is fixed"
        assert report.proposals[0].confidence == 0.95
        assert report.findings_addressed == 1

    def test_original_text_not_in_artifact_skipped(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id,
                "original_text": "text not in artifact at all",
                "replacement_text": "replacement",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 0
        assert any("not found verbatim" in r for r in report.skip_reasons)

    def test_empty_original_text_skipped(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id,
                "original_text": "",
                "replacement_text": "replacement",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 0

    def test_unknown_finding_id_skipped(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": "F-nonexistent",
                "original_text": "line one",
                "replacement_text": "replaced",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 0
        assert any("unknown finding_id" in r for r in report.skip_reasons)

    def test_partial_finding_id_match(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        # LLM returns partial ID that is a substring of the real ID
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id[2:],  # drop "F-" prefix
                "original_text": "line one",
                "replacement_text": "replaced line one",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 1

    def test_multiple_proposals(self, fixer, mock_provider):
        f1 = make_finding(severity=Severity.CRITICAL, description="Issue 1")
        f2 = make_finding(severity=Severity.HIGH, description="Issue 2")
        mock_provider.complete_json.return_value = {
            "fixes": [
                {
                    "finding_id": f1.id,
                    "original_text": "line one",
                    "replacement_text": "fixed line one",
                    "explanation": "Fix 1",
                    "confidence": 0.9,
                },
                {
                    "finding_id": f2.id,
                    "original_text": "line three",
                    "replacement_text": "fixed line three",
                    "explanation": "Fix 2",
                    "confidence": 0.85,
                },
            ]
        }
        report = fixer.run([f1, f2], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 2
        assert report.findings_addressed == 2

    def test_unaddressed_finding_noted(self, fixer, mock_provider):
        f1 = make_finding(severity=Severity.CRITICAL, description="Issue 1")
        f2 = make_finding(severity=Severity.CRITICAL, description="Issue 2")
        # LLM only addresses f1
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": f1.id,
                "original_text": "line one",
                "replacement_text": "fixed",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([f1, f2], SAMPLE_ARTIFACT, "test.py")
        assert len(report.proposals) == 1
        assert any(f2.id in r for r in report.skip_reasons)


# ── Proposal Structure ────────────────────────────────────────────────────────


class TestFixerProposalStructure:
    def test_proposal_has_all_fields(self, fixer, mock_provider):
        finding = make_finding(
            severity=Severity.HIGH,
            description="A long description that exceeds two hundred characters " * 3,
        )
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id,
                "original_text": "line one",
                "replacement_text": "fixed line one",
                "explanation": "Explains the fix",
                "confidence": 0.88,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        proposal = report.proposals[0]
        assert proposal.finding_id == finding.id
        assert proposal.file_path == "test.py"
        assert proposal.original_text == "line one"
        assert proposal.replacement_text == "fixed line one"
        assert proposal.explanation == "Explains the fix"
        assert proposal.confidence == 0.88
        # Description truncated to 200 chars
        assert len(proposal.finding_description) <= 200

    def test_fix_report_serializes(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        mock_provider.complete_json.return_value = {
            "fixes": [{
                "finding_id": finding.id,
                "original_text": "line one",
                "replacement_text": "fixed",
                "explanation": "Fix",
                "confidence": 0.9,
            }]
        }
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        data = report.model_dump()
        assert "proposals" in data
        assert data["findings_addressed"] == 1
        assert data["loop_number"] == 1


# ── Error Handling ────────────────────────────────────────────────────────────


class TestFixerErrorHandling:
    def test_llm_error_returns_report_not_crash(self, fixer, mock_provider):
        mock_provider.complete_json.side_effect = RuntimeError("API timeout")
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert report.proposals == []
        assert report.findings_skipped == 1
        assert any("LLM call failed" in r for r in report.skip_reasons)

    def test_llm_returns_empty_fixes(self, fixer, mock_provider):
        mock_provider.complete_json.return_value = {"fixes": []}
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert report.proposals == []
        # Finding should be in skip_reasons as unaddressed
        assert any(finding.id in r for r in report.skip_reasons)

    def test_llm_returns_no_fixes_key(self, fixer, mock_provider):
        mock_provider.complete_json.return_value = {}
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert report.proposals == []

    def test_fix_report_loop_number(self, fixer, mock_provider):
        finding = make_finding(severity=Severity.CRITICAL, description="Issue")
        report = fixer.run([finding], SAMPLE_ARTIFACT, "test.py")
        assert report.loop_number == 1
        assert report.revalidation_verdict is None
        assert report.revalidation_delta is None
