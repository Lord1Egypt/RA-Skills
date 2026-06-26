"""Shared fixtures for the Quorum test suite."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from quorum.config import QuorumConfig
from quorum.models import (
    AggregatedReport,
    CriticResult,
    Evidence,
    Finding,
    Rubric,
    RubricCriterion,
    Severity,
    Verdict,
    VerdictStatus,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ── Paths ────────────────────────────────────────────────────────────────────


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def good_dir() -> Path:
    return FIXTURES_DIR / "good"


@pytest.fixture
def bad_dir() -> Path:
    return FIXTURES_DIR / "bad"


@pytest.fixture
def edge_dir() -> Path:
    return FIXTURES_DIR / "edge"


# ── Minimal valid config ─────────────────────────────────────────────────────


@pytest.fixture
def minimal_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="anthropic/claude-opus-4-6",
        model_tier2="anthropic/claude-sonnet-4-6",
        depth_profile="quick",
    )


@pytest.fixture
def full_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness", "completeness", "security", "code_hygiene"],
        model_tier1="anthropic/claude-opus-4-6",
        model_tier2="anthropic/claude-sonnet-4-6",
        depth_profile="thorough",
        temperature=0.05,
        max_tokens=8192,
        enable_prescreen=True,
    )


# ── Rubric fixtures ──────────────────────────────────────────────────────────


@pytest.fixture
def sample_rubric() -> Rubric:
    return Rubric(
        name="test-rubric",
        domain="test",
        version="1.0",
        description="A rubric for testing",
        criteria=[
            RubricCriterion(
                id="TEST-001",
                criterion="Document must have an introduction",
                severity=Severity.HIGH,
                evidence_required="Quote from the introduction section",
                why="Introductions provide context",
            ),
            RubricCriterion(
                id="TEST-002",
                criterion="All claims must be supported by evidence",
                severity=Severity.CRITICAL,
                evidence_required="Citation or data reference",
                why="Unsupported claims reduce credibility",
            ),
        ],
    )


@pytest.fixture
def sample_rubric_json(tmp_path: Path, sample_rubric: Rubric) -> Path:
    path = tmp_path / "test-rubric.json"
    path.write_text(json.dumps(sample_rubric.model_dump(), indent=2, default=str))
    return path


# ── Finding / Verdict factories ──────────────────────────────────────────────


def make_finding(
    severity: Severity = Severity.MEDIUM,
    description: str = "Test finding",
    critic: str = "correctness",
    **kwargs: Any,
) -> Finding:
    defaults = dict(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result="matched line 42"),
        critic=critic,
    )
    defaults.update(kwargs)
    return Finding(**defaults)


def make_critic_result(
    name: str = "correctness",
    findings: list[Finding] | None = None,
    confidence: float = 0.85,
) -> CriticResult:
    return CriticResult(
        critic_name=name,
        findings=findings or [],
        confidence=confidence,
        runtime_ms=100,
    )


def make_verdict(
    status: VerdictStatus = VerdictStatus.PASS,
    findings: list[Finding] | None = None,
    confidence: float = 0.9,
) -> Verdict:
    report = AggregatedReport(
        findings=findings or [],
        confidence=confidence,
        critic_results=[],
    )
    return Verdict(
        status=status,
        reasoning="Test verdict",
        confidence=confidence,
        report=report,
    )


# ── Mock provider ────────────────────────────────────────────────────────────


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.complete.return_value = "No issues found."
    provider.complete_json.return_value = {"findings": []}
    return provider
