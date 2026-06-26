"""Phase 2: Supervisor Agent tests — domain classification, critic dispatch, model routing."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from quorum.agents.supervisor import CRITIC_REGISTRY, SupervisorAgent
from quorum.config import QuorumConfig
from quorum.critics.base import BaseCritic
from quorum.models import (
    CriticResult,
    Evidence,
    Finding,
    PreScreenCheck,
    PreScreenResult,
    Rubric,
    RubricCriterion,
    Severity,
)


def make_finding(severity=Severity.MEDIUM, description="Test finding", critic="correctness", **kwargs):
    defaults = dict(severity=severity, description=description, evidence=Evidence(tool="grep", result="matched line 42"), critic=critic)
    defaults.update(kwargs)
    return Finding(**defaults)


@pytest.fixture
def mock_provider() -> MagicMock:
    provider = MagicMock()
    provider.complete_json.return_value = {"findings": []}
    return provider


@pytest.fixture
def quick_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness"],
        model_tier1="test-tier1",
        model_tier2="test-tier2",
        depth_profile="quick",
    )


@pytest.fixture
def full_config() -> QuorumConfig:
    return QuorumConfig(
        critics=["correctness", "completeness", "security", "code_hygiene"],
        model_tier1="test-tier1",
        model_tier2="test-tier2",
        depth_profile="thorough",
    )


@pytest.fixture
def rubric() -> Rubric:
    return Rubric(
        name="test-rubric",
        domain="test",
        version="1.0",
        criteria=[
            RubricCriterion(
                id="T-001",
                criterion="Test criterion",
                severity=Severity.MEDIUM,
                evidence_required="any",
                why="testing",
            ),
        ],
    )


# ── Domain Classification ─────────────────────────────────────────────────────


class TestClassifyDomain:
    def test_python_code(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain("def foo(): pass", "main.py") == "code"

    def test_javascript_code(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain("const x = 1;", "app.js") == "code"

    def test_yaml_config(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain("key: value", "config.yaml") == "config"

    def test_json_config(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain('{"key": "value"}', "settings.json") == "config"

    def test_research_markdown(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        text = "# Abstract\n\nThis study explores the hypothesis that methodology and results matter."
        assert sup.classify_domain(text, "paper.md") == "research"

    def test_generic_docs(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain("# README\n\nInstallation instructions", "README.md") == "docs"

    def test_unknown_extension(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        assert sup.classify_domain("binary stuff", "file.xyz") == "unknown"

    def test_research_requires_three_signals(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        # Only two signals — should be docs, not research
        text = "# Abstract\n\nThis study is interesting."
        assert sup.classify_domain(text, "doc.md") == "docs"


# ── Build Critics ─────────────────────────────────────────────────────────────


class TestBuildCritics:
    def test_single_critic(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        critics = sup.build_critics()
        assert len(critics) == 1
        assert critics[0].name == "correctness"

    def test_all_critics(self, mock_provider, full_config):
        sup = SupervisorAgent(mock_provider, full_config)
        critics = sup.build_critics()
        assert len(critics) == 4
        names = {c.name for c in critics}
        assert names == {"correctness", "completeness", "security", "code_hygiene"}

    def test_unknown_critic_skipped(self, mock_provider, quick_config):
        # Temporarily modify the config's critic list to include an unknown name
        # We bypass QuorumConfig validator by patching the instance
        sup = SupervisorAgent(mock_provider, quick_config)
        quick_config.critics = ["correctness", "nonexistent_critic"]
        critics = sup.build_critics()
        assert len(critics) == 1
        assert critics[0].name == "correctness"

    def test_all_unknown_raises(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        quick_config.critics = ["fake_critic"]
        with pytest.raises(RuntimeError, match="No valid critics"):
            sup.build_critics()

    def test_critics_get_provider_and_config(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        critics = sup.build_critics()
        assert critics[0].provider is mock_provider
        assert critics[0].config is quick_config


# ── Run One Critic ────────────────────────────────────────────────────────────


class TestRunOneCritic:
    def test_success_returns_result(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        critic = MagicMock(spec=BaseCritic)
        critic.name = "correctness"
        critic.evaluate.return_value = CriticResult(
            critic_name="correctness",
            findings=[make_finding()],
            confidence=0.9,
            runtime_ms=50,
        )
        result = sup._run_one_critic(critic, "text", rubric, None)
        assert not result.skipped
        assert len(result.findings) == 1

    def test_crash_returns_skipped(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        critic = MagicMock(spec=BaseCritic)
        critic.name = "correctness"
        critic.evaluate.side_effect = RuntimeError("LLM broke")
        result = sup._run_one_critic(critic, "text", rubric, None)
        assert result.skipped is True
        assert "LLM broke" in result.skip_reason
        assert result.findings == []

    def test_extra_context_passed(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        critic = MagicMock(spec=BaseCritic)
        critic.name = "correctness"
        critic.evaluate.return_value = CriticResult(
            critic_name="correctness", findings=[], confidence=0.8, runtime_ms=10,
        )
        context = {"pre_verified_evidence": "some evidence"}
        sup._run_one_critic(critic, "text", rubric, context)
        _, kwargs = critic.evaluate.call_args
        assert kwargs["extra_context"] == context


# ── Full Run (Parallel Dispatch) ──────────────────────────────────────────────


class TestSupervisorRun:
    def test_run_returns_sorted_results(self, mock_provider, full_config, rubric):
        sup = SupervisorAgent(mock_provider, full_config)
        results = sup.run("def foo(): pass", "code.py", rubric)
        assert len(results) == 4
        # Sorted by critic_name
        names = [r.critic_name for r in results]
        assert names == sorted(names)

    def test_run_rejects_empty_text(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        with pytest.raises(ValueError, match="artifact_text"):
            sup.run("", "file.py", rubric)

    def test_run_rejects_none_rubric(self, mock_provider, quick_config):
        sup = SupervisorAgent(mock_provider, quick_config)
        with pytest.raises(ValueError, match="rubric"):
            sup.run("some text", "file.py", None)

    def test_prescreen_injected_into_context(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        prescreen = PreScreenResult(
            checks=[
                PreScreenCheck(
                    id="PS-001", name="hardcoded_paths", category="security",
                    severity=Severity.HIGH, description="Found paths",
                    result="FAIL", evidence="L5: /Users/test",
                    locations=["L5"],
                ),
            ],
            total_checks=1, passed=0, failed=1, skipped=0, runtime_ms=5,
        )
        results = sup.run("def foo(): pass", "code.py", rubric, prescreen_result=prescreen)
        assert len(results) == 1

    def test_run_without_prescreen(self, mock_provider, quick_config, rubric):
        sup = SupervisorAgent(mock_provider, quick_config)
        results = sup.run("def foo(): pass", "code.py", rubric)
        assert len(results) == 1
        assert not results[0].skipped

    def test_one_critic_fails_others_succeed(self, mock_provider, rubric):
        config = QuorumConfig(
            critics=["correctness", "completeness"],
            model_tier1="test", model_tier2="test",
            depth_profile="quick",
        )
        # Make correctness succeed and completeness fail
        call_count = [0]
        original_return = {"findings": []}

        def side_effect(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] % 2 == 0:
                raise RuntimeError("Critic failed")
            return original_return

        mock_provider.complete_json.side_effect = side_effect
        sup = SupervisorAgent(mock_provider, config)
        results = sup.run("def foo(): pass", "code.py", rubric)
        assert len(results) == 2
        # At least one should have succeeded
        statuses = [r.skipped for r in results]
        assert not all(statuses)  # Not all skipped


# ── Critic Registry ───────────────────────────────────────────────────────────


class TestCriticRegistry:
    def test_all_registered_critics_exist(self):
        expected = {"correctness", "completeness", "security", "code_hygiene"}
        assert set(CRITIC_REGISTRY.keys()) == expected

    def test_all_registered_are_base_critic_subclasses(self):
        for name, cls in CRITIC_REGISTRY.items():
            assert issubclass(cls, BaseCritic), f"{name} is not a BaseCritic subclass"

    def test_cross_consistency_not_in_registry(self):
        assert "cross_consistency" not in CRITIC_REGISTRY
