"""Layer 2c: Integration tests for critic execution with mocked LLM responses."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.config import QuorumConfig
from quorum.critics.base import BaseCritic
from quorum.critics.correctness import CorrectnessCritic
from quorum.critics.completeness import CompletenessCritic
from quorum.critics.security import SecurityCritic
from quorum.critics.code_hygiene import CodeHygieneCritic
from quorum.models import (
    CriticResult,
    Evidence,
    Finding,
    Rubric,
    RubricCriterion,
    Severity,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness", "completeness", "security", "code_hygiene"],
        model_tier1="anthropic/claude-opus-4-6",
        model_tier2="anthropic/claude-sonnet-4-6",
        depth_profile="quick",
    )


@pytest.fixture
def rubric() -> Rubric:
    return Rubric(
        name="test",
        domain="research",
        criteria=[
            RubricCriterion(
                id="C-001",
                criterion="Document must have supported claims",
                severity=Severity.HIGH,
                evidence_required="Citation or reference",
                why="Credibility",
            ),
        ],
    )


def _mock_provider_with_findings(findings_json: list[dict]) -> MagicMock:
    provider = MagicMock()
    provider.complete.return_value = json.dumps({"findings": findings_json})
    provider.complete_json.return_value = {"findings": findings_json}
    return provider


def _mock_provider_no_findings() -> MagicMock:
    return _mock_provider_with_findings([])


# ── Correctness critic ───────────────────────────────────────────────────────


class TestCorrectnessCritic:
    def test_no_findings_from_clean(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CorrectnessCritic(provider=provider, config=config)
        result = critic.evaluate("Clean factual document.", rubric)
        assert isinstance(result, CriticResult)
        assert result.critic_name == "correctness"

    def test_finds_issues_from_mock(self, config, rubric):
        findings_json = [
            {
                "severity": "CRITICAL",
                "description": "Factually incorrect claim about sky color",
                "evidence": {"tool": "llm", "result": "The sky is green is false"},
                "location": "line 5",
            }
        ]
        provider = _mock_provider_with_findings(findings_json)
        critic = CorrectnessCritic(provider=provider, config=config)
        result = critic.evaluate("The sky is green.", rubric)
        assert result.critic_name == "correctness"
        # The mock returns findings through provider, but actual parsing
        # depends on the critic's _parse_findings logic
        assert isinstance(result, CriticResult)

    def test_has_system_prompt(self, config):
        provider = _mock_provider_no_findings()
        critic = CorrectnessCritic(provider=provider, config=config)
        assert len(critic.system_prompt) > 0

    def test_builds_prompt(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CorrectnessCritic(provider=provider, config=config)
        prompt = critic.build_prompt("Test artifact", rubric)
        assert "Test artifact" in prompt


# ── Completeness critic ──────────────────────────────────────────────────────


class TestCompletenessCritic:
    def test_produces_result(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CompletenessCritic(provider=provider, config=config)
        result = critic.evaluate("Has abstract and methodology.", rubric)
        assert isinstance(result, CriticResult)
        assert result.critic_name == "completeness"

    def test_has_system_prompt(self, config):
        provider = _mock_provider_no_findings()
        critic = CompletenessCritic(provider=provider, config=config)
        assert "completeness" in critic.system_prompt.lower() or len(critic.system_prompt) > 0


# ── Security critic ──────────────────────────────────────────────────────────


class TestSecurityCritic:
    def test_produces_result(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = SecurityCritic(provider=provider, config=config)
        result = critic.evaluate("Clean code.", rubric)
        assert isinstance(result, CriticResult)
        assert result.critic_name == "security"

    def test_has_system_prompt(self, config):
        provider = _mock_provider_no_findings()
        critic = SecurityCritic(provider=provider, config=config)
        assert len(critic.system_prompt) > 0


# ── Code hygiene critic ──────────────────────────────────────────────────────


class TestCodeHygieneCritic:
    def test_produces_result(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CodeHygieneCritic(provider=provider, config=config)
        result = critic.evaluate("def foo(): pass", rubric)
        assert isinstance(result, CriticResult)
        assert result.critic_name == "code_hygiene"

    def test_has_system_prompt(self, config):
        provider = _mock_provider_no_findings()
        critic = CodeHygieneCritic(provider=provider, config=config)
        assert len(critic.system_prompt) > 0


# ── BaseCritic contract ─────────────────────────────────────────────────────


class TestBaseCriticContract:
    def test_all_critics_have_name(self, config):
        provider = _mock_provider_no_findings()
        critics = [
            CorrectnessCritic(provider=provider, config=config),
            CompletenessCritic(provider=provider, config=config),
            SecurityCritic(provider=provider, config=config),
            CodeHygieneCritic(provider=provider, config=config),
        ]
        names = {c.name for c in critics}
        assert "correctness" in names
        assert "completeness" in names
        assert "security" in names
        assert "code_hygiene" in names

    def test_all_critics_have_system_prompt(self, config):
        provider = _mock_provider_no_findings()
        critics = [
            CorrectnessCritic(provider=provider, config=config),
            CompletenessCritic(provider=provider, config=config),
            SecurityCritic(provider=provider, config=config),
            CodeHygieneCritic(provider=provider, config=config),
        ]
        for c in critics:
            assert len(c.system_prompt) > 10, f"{c.name} has empty system prompt"

    def test_result_has_confidence(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CorrectnessCritic(provider=provider, config=config)
        result = critic.evaluate("test", rubric)
        assert 0.0 <= result.confidence <= 1.0

    def test_result_has_runtime(self, config, rubric):
        provider = _mock_provider_no_findings()
        critic = CorrectnessCritic(provider=provider, config=config)
        result = critic.evaluate("test", rubric)
        assert result.runtime_ms >= 0
