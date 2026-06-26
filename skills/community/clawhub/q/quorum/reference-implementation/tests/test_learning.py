"""Tests for learning memory — quorum/learning.py (Milestone #7)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from quorum.learning import LearningMemory, _make_pattern_id
from quorum.models import (
    AggregatedReport,
    CriticResult,
    Evidence,
    Finding,
    Issue,
    Severity,
    UpdateResult,
    Verdict,
    VerdictStatus,
)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _make_finding(description: str = "Test issue", critic: str = "correctness", severity: Severity = Severity.MEDIUM) -> Finding:
    return Finding(
        severity=severity,
        description=description,
        evidence=Evidence(tool="grep", result="matched line 10"),
        critic=critic,
    )


def _make_issue(
    pattern_id: str = "P-abc123",
    description: str = "Test issue",
    frequency: int = 1,
    mandatory: bool = False,
) -> Issue:
    return Issue(
        pattern_id=pattern_id,
        description=description,
        domain="code",
        severity=Severity.MEDIUM,
        frequency=frequency,
        first_seen="2026-01-01",
        last_seen="2026-01-01",
        mandatory=mandatory,
    )


# ── UpdateResult model ────────────────────────────────────────────────────────


class TestUpdateResult:
    def test_defaults(self):
        r = UpdateResult()
        assert r.new_patterns == 0
        assert r.updated_patterns == 0
        assert r.promoted_patterns == 0
        assert r.total_known == 0

    def test_with_values(self):
        r = UpdateResult(new_patterns=2, updated_patterns=1, promoted_patterns=1, total_known=5)
        assert r.new_patterns == 2
        assert r.total_known == 5


# ── _make_pattern_id ─────────────────────────────────────────────────────────


class TestMakePatternId:
    def test_returns_string_with_prefix(self):
        pid = _make_pattern_id("missing null check", "security")
        assert pid.startswith("P-")

    def test_stable_across_calls(self):
        pid1 = _make_pattern_id("missing null check", "security")
        pid2 = _make_pattern_id("missing null check", "security")
        assert pid1 == pid2

    def test_case_insensitive(self):
        pid1 = _make_pattern_id("Missing Null Check", "Security")
        pid2 = _make_pattern_id("missing null check", "security")
        assert pid1 == pid2

    def test_different_descriptions_differ(self):
        pid1 = _make_pattern_id("issue A", "correctness")
        pid2 = _make_pattern_id("issue B", "correctness")
        assert pid1 != pid2

    def test_different_critics_differ(self):
        pid1 = _make_pattern_id("same issue", "correctness")
        pid2 = _make_pattern_id("same issue", "security")
        assert pid1 != pid2

    def test_length_is_12_chars(self):
        pid = _make_pattern_id("anything", "critic")
        # "P-" + 10 hex chars = 12
        assert len(pid) == 12


# ── LearningMemory.load / save ────────────────────────────────────────────────


class TestLoadSave:
    def test_load_empty_if_not_exists(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "known_issues.json")
        assert lm.load() == []

    def test_save_creates_file(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "known_issues.json")
        issues = [_make_issue("P-001")]
        lm.save(issues)
        assert lm.path.exists()

    def test_save_load_roundtrip(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "known_issues.json")
        issues = [
            _make_issue("P-001", description="Issue A", frequency=2),
            _make_issue("P-002", description="Issue B", frequency=5, mandatory=True),
        ]
        lm.save(issues)
        loaded = lm.load()
        assert len(loaded) == 2
        assert loaded[0].pattern_id in {"P-001", "P-002"}
        mandatory = [i for i in loaded if i.mandatory]
        assert len(mandatory) == 1

    def test_save_creates_parent_dirs(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "nested" / "deep" / "known_issues.json")
        lm.save([_make_issue()])
        assert lm.path.exists()

    def test_load_returns_empty_on_bad_json(self, tmp_path: Path):
        bad = tmp_path / "known_issues.json"
        bad.write_text("not json at all", encoding="utf-8")
        lm = LearningMemory(path=bad)
        assert lm.load() == []

    def test_save_human_readable_json(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "known_issues.json")
        lm.save([_make_issue("P-001")])
        raw = lm.path.read_text()
        assert "\n" in raw  # indented

    def test_save_atomic_no_tmp_left(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "known_issues.json")
        lm.save([_make_issue()])
        tmp_file = lm.path.with_suffix(".tmp")
        assert not tmp_file.exists()


# ── LearningMemory.update_from_findings ──────────────────────────────────────


class TestUpdateFromFindings:
    def test_new_pattern_created(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("SQL injection risk", "security")
        result = lm.update_from_findings([finding], domain="code")
        assert result.new_patterns == 1
        assert result.updated_patterns == 0
        issues = lm.load()
        assert len(issues) == 1
        assert issues[0].description == "SQL injection risk"
        assert issues[0].frequency == 1

    def test_frequency_incremented_on_second_run(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("SQL injection risk", "security")
        lm.update_from_findings([finding], domain="code")
        result = lm.update_from_findings([finding], domain="code")
        assert result.new_patterns == 0
        assert result.updated_patterns == 1
        issues = lm.load()
        assert len(issues) == 1
        assert issues[0].frequency == 2

    def test_pattern_id_is_stable_across_runs(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("Missing type hints", "code_hygiene")
        lm.update_from_findings([finding], domain="code")
        lm.update_from_findings([finding], domain="code")
        issues = lm.load()
        assert len(issues) == 1  # same pattern, not duplicated

    def test_multiple_findings_different_patterns(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        findings = [
            _make_finding("Issue A", "correctness"),
            _make_finding("Issue B", "completeness"),
        ]
        result = lm.update_from_findings(findings, domain="docs")
        assert result.new_patterns == 2
        assert result.total_known == 2

    def test_domain_stored_on_new_pattern(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("Test", "correctness")
        lm.update_from_findings([finding], domain="research")
        issues = lm.load()
        assert issues[0].domain == "research"

    def test_severity_stored(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("Critical bug", "security", severity=Severity.CRITICAL)
        lm.update_from_findings([finding], domain="code")
        issues = lm.load()
        assert issues[0].severity == Severity.CRITICAL

    def test_empty_findings_returns_zero_counts(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        result = lm.update_from_findings([], domain="code")
        assert result.new_patterns == 0
        assert result.updated_patterns == 0
        assert result.total_known == 0

    def test_returns_update_result_instance(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        result = lm.update_from_findings([_make_finding()], domain="code")
        assert isinstance(result, UpdateResult)


# ── LearningMemory.promote ────────────────────────────────────────────────────


class TestPromotion:
    def test_below_threshold_not_promoted(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", frequency=2)
        lm.save([issue])
        lm.promote(threshold=3)
        assert not lm.load()[0].mandatory

    def test_at_threshold_promoted(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", frequency=3)
        lm.save([issue])
        lm.promote(threshold=3)
        assert lm.load()[0].mandatory

    def test_above_threshold_promoted(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", frequency=10)
        lm.save([issue])
        lm.promote(threshold=3)
        assert lm.load()[0].mandatory

    def test_already_mandatory_not_double_counted(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", frequency=5, mandatory=True)
        lm.save([issue])
        n = lm.promote(threshold=3)
        assert n == 0  # was already mandatory

    def test_returns_count_of_newly_promoted(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issues = [
            _make_issue("P-001", frequency=1),
            _make_issue("P-002", frequency=4),
            _make_issue("P-003", frequency=5),
        ]
        lm.save(issues)
        n = lm.promote(threshold=3)
        assert n == 2

    def test_auto_promote_in_update_from_findings(self, tmp_path: Path):
        """Patterns reaching threshold during update_from_findings are promoted."""
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("Repeated bug", "correctness")
        # Run 3 times to hit default threshold
        lm.update_from_findings([finding], domain="code")
        lm.update_from_findings([finding], domain="code")
        result = lm.update_from_findings([finding], domain="code")
        assert result.promoted_patterns == 1
        assert lm.load()[0].mandatory

    def test_custom_threshold_in_update_from_findings(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        finding = _make_finding("Bug", "correctness")
        lm.update_from_findings([finding], domain="code")
        result = lm.update_from_findings([finding], domain="code", threshold=2)
        assert result.promoted_patterns == 1


# ── LearningMemory.get_mandatory ──────────────────────────────────────────────


class TestGetMandatory:
    def test_empty_when_none_mandatory(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([_make_issue("P-001", mandatory=False)])
        assert lm.get_mandatory() == []

    def test_returns_only_mandatory(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([
            _make_issue("P-001", mandatory=False),
            _make_issue("P-002", mandatory=True),
        ])
        mandatory = lm.get_mandatory()
        assert len(mandatory) == 1
        assert mandatory[0].pattern_id == "P-002"


# ── LearningMemory.to_critic_context ─────────────────────────────────────────


class TestToCriticContext:
    def test_empty_string_when_no_mandatory(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([_make_issue("P-001", mandatory=False)])
        assert lm.to_critic_context() == ""

    def test_empty_string_when_no_issues(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        assert lm.to_critic_context() == ""

    def test_includes_mandatory_description(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", description="SQL injection risk", mandatory=True)
        lm.save([issue])
        ctx = lm.to_critic_context()
        assert "SQL injection risk" in ctx

    def test_includes_known_recurring_preamble(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        issue = _make_issue("P-001", description="Missing docstrings", mandatory=True)
        lm.save([issue])
        ctx = lm.to_critic_context()
        assert "Known recurring issue" in ctx
        assert "Always check for this pattern" in ctx

    def test_multiple_mandatory_all_included(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([
            _make_issue("P-001", description="Issue A", mandatory=True),
            _make_issue("P-002", description="Issue B", mandatory=True),
            _make_issue("P-003", description="Issue C", mandatory=False),
        ])
        ctx = lm.to_critic_context()
        assert "Issue A" in ctx
        assert "Issue B" in ctx
        assert "Issue C" not in ctx

    def test_has_section_header(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([_make_issue("P-001", mandatory=True)])
        ctx = lm.to_critic_context()
        assert "Known Recurring Issues" in ctx


# ── Atomic write (tmp+rename) ─────────────────────────────────────────────────


class TestAtomicWrite:
    def test_no_tmp_file_after_save(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([_make_issue()])
        assert not (tmp_path / "ki.tmp").exists()

    def test_existing_file_replaced_atomically(self, tmp_path: Path):
        lm = LearningMemory(path=tmp_path / "ki.json")
        lm.save([_make_issue("P-001", description="Old")])
        lm.save([_make_issue("P-002", description="New")])
        issues = lm.load()
        assert len(issues) == 1
        assert issues[0].description == "New"


# ── Pipeline integration ──────────────────────────────────────────────────────


class TestPipelineIntegration:
    """Integration tests for learning memory in the pipeline (mocked LLM)."""

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_learning_memory_updated_after_run(
        self,
        mock_supervisor_cls,
        mock_aggregator_cls,
        mock_provider_cls,
        tmp_path: Path,
    ):
        from quorum.config import QuorumConfig
        from quorum.pipeline import run_validation

        # Set up mocks
        mock_provider_cls.return_value = MagicMock()
        mock_supervisor = MagicMock()
        mock_supervisor.classify_domain.return_value = "code"
        finding = _make_finding("Unchecked return value", "correctness", Severity.HIGH)
        mock_supervisor.run.return_value = [
            CriticResult(
                critic_name="correctness",
                findings=[finding],
                confidence=0.8,
                runtime_ms=100,
            )
        ]
        mock_supervisor_cls.return_value = mock_supervisor

        report = AggregatedReport(findings=[finding], confidence=0.8)
        verdict = Verdict(
            status=VerdictStatus.REVISE,
            reasoning="Findings found",
            confidence=0.8,
            report=report,
        )
        mock_aggregator = MagicMock()
        mock_aggregator.run.return_value = verdict
        mock_aggregator_cls.return_value = mock_aggregator

        # Create a test artifact
        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n")

        # Use a project-local known_issues.json path
        ki_path = tmp_path / "known_issues.json"

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        with patch("quorum.pipeline.LearningMemory") as mock_lm_cls:
            mock_lm = MagicMock()
            mock_lm.to_critic_context.return_value = ""
            mock_lm.classify_domain = mock_supervisor.classify_domain
            mock_lm_cls.return_value = mock_lm

            run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=True,
            )

            # Learning memory should have been called
            assert mock_lm.to_critic_context.called
            assert mock_lm.update_from_findings.called

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_no_learning_skips_learning_memory(
        self,
        mock_supervisor_cls,
        mock_aggregator_cls,
        mock_provider_cls,
        tmp_path: Path,
    ):
        from quorum.config import QuorumConfig
        from quorum.pipeline import run_validation

        mock_provider_cls.return_value = MagicMock()
        mock_supervisor = MagicMock()
        mock_supervisor.classify_domain.return_value = "code"
        mock_supervisor.run.return_value = [
            CriticResult(
                critic_name="correctness",
                findings=[],
                confidence=0.8,
                runtime_ms=50,
            )
        ]
        mock_supervisor_cls.return_value = mock_supervisor

        report = AggregatedReport(findings=[], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Clean",
            confidence=0.9,
            report=report,
        )
        mock_aggregator = MagicMock()
        mock_aggregator.run.return_value = verdict
        mock_aggregator_cls.return_value = mock_aggregator

        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        with patch("quorum.pipeline.LearningMemory") as mock_lm_cls:
            run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=False,
            )
            # LearningMemory should NOT be instantiated when disabled
            assert not mock_lm_cls.called

    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_mandatory_context_passed_to_supervisor(
        self,
        mock_supervisor_cls,
        mock_aggregator_cls,
        mock_provider_cls,
        tmp_path: Path,
    ):
        from quorum.config import QuorumConfig
        from quorum.pipeline import run_validation

        mock_provider_cls.return_value = MagicMock()
        mock_supervisor = MagicMock()
        mock_supervisor.classify_domain.return_value = "code"
        mock_supervisor.run.return_value = [
            CriticResult(
                critic_name="correctness",
                findings=[],
                confidence=0.8,
                runtime_ms=50,
            )
        ]
        mock_supervisor_cls.return_value = mock_supervisor

        report = AggregatedReport(findings=[], confidence=0.9)
        verdict = Verdict(
            status=VerdictStatus.PASS,
            reasoning="Clean",
            confidence=0.9,
            report=report,
        )
        mock_aggregator = MagicMock()
        mock_aggregator.run.return_value = verdict
        mock_aggregator_cls.return_value = mock_aggregator

        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        mandatory_ctx = "## Known Recurring Issues\n- Known recurring issue: SQL injection."

        with patch("quorum.pipeline.LearningMemory") as mock_lm_cls:
            mock_lm = MagicMock()
            mock_lm.to_critic_context.return_value = mandatory_ctx
            mock_lm_cls.return_value = mock_lm

            run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=True,
            )

            # supervisor.run should have been called with mandatory_context
            call_kwargs = mock_supervisor.run.call_args
            assert call_kwargs.kwargs.get("mandatory_context") == mandatory_ctx


# ── BaseCritic mandatory_context integration ──────────────────────────────────


class TestCriticMandatoryContext:
    def test_mandatory_context_prepended_to_system_prompt(self):
        from quorum.critics.correctness import CorrectnessCritic
        from quorum.models import Rubric, RubricCriterion

        rubric = Rubric(
            name="test",
            domain="code",
            criteria=[RubricCriterion(
                id="T-001",
                criterion="No bugs",
                severity=Severity.HIGH,
                evidence_required="Direct quote",
                why="Bugs are bad",
            )],
        )

        mock_provider = MagicMock()
        mock_provider.complete_json.return_value = {"findings": []}

        from quorum.config import QuorumConfig
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        critic = CorrectnessCritic(provider=mock_provider, config=config)
        mandatory_ctx = "## Known Issues\n- Check for null pointer exceptions."
        critic.evaluate("def foo(): pass", rubric, mandatory_context=mandatory_ctx)

        # The system prompt passed to the LLM should start with mandatory_context
        assert mock_provider.complete_json.called
        call_args = mock_provider.complete_json.call_args
        messages = call_args.kwargs.get("messages") or call_args.args[0]
        system_msg = next(m for m in messages if m["role"] == "system")
        assert system_msg["content"].startswith(mandatory_ctx)

    def test_no_mandatory_context_uses_base_prompt(self):
        from quorum.critics.correctness import CorrectnessCritic
        from quorum.models import Rubric, RubricCriterion

        rubric = Rubric(
            name="test",
            domain="code",
            criteria=[RubricCriterion(
                id="T-001",
                criterion="No bugs",
                severity=Severity.HIGH,
                evidence_required="Direct quote",
                why="Bugs are bad",
            )],
        )

        mock_provider = MagicMock()
        mock_provider.complete_json.return_value = {"findings": []}

        from quorum.config import QuorumConfig
        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        critic = CorrectnessCritic(provider=mock_provider, config=config)
        critic.evaluate("def foo(): pass", rubric)

        call_args = mock_provider.complete_json.call_args
        messages = call_args.kwargs.get("messages") or call_args.args[0]
        system_msg = next(m for m in messages if m["role"] == "system")
        # Should be the plain system prompt (no prepended context)
        assert system_msg["content"] == critic.system_prompt


# ── Run-manifest learning stats ───────────────────────────────────────────────


class TestManifestLearningStats:
    @patch("quorum.pipeline.LiteLLMProvider")
    @patch("quorum.pipeline.AggregatorAgent")
    @patch("quorum.pipeline.SupervisorAgent")
    def test_learning_stats_in_manifest(
        self,
        mock_supervisor_cls,
        mock_aggregator_cls,
        mock_provider_cls,
        tmp_path: Path,
    ):
        import json as _json
        from quorum.config import QuorumConfig
        from quorum.pipeline import run_validation

        mock_provider_cls.return_value = MagicMock()
        mock_supervisor = MagicMock()
        mock_supervisor.classify_domain.return_value = "code"
        finding = _make_finding("Test finding", "correctness")
        mock_supervisor.run.return_value = [
            CriticResult(
                critic_name="correctness",
                findings=[finding],
                confidence=0.8,
                runtime_ms=50,
            )
        ]
        mock_supervisor_cls.return_value = mock_supervisor

        report = AggregatedReport(findings=[finding], confidence=0.8)
        verdict = Verdict(
            status=VerdictStatus.REVISE,
            reasoning="Has findings",
            confidence=0.8,
            report=report,
        )
        mock_aggregator = MagicMock()
        mock_aggregator.run.return_value = verdict
        mock_aggregator_cls.return_value = mock_aggregator

        artifact = tmp_path / "test.py"
        artifact.write_text("def foo(): pass\n")

        config = QuorumConfig(
            critics=["correctness"],
            model_tier1="test/model",
            model_tier2="test/model",
            depth_profile="quick",
        )

        update_result = UpdateResult(new_patterns=1, updated_patterns=0, promoted_patterns=0, total_known=1)
        with patch("quorum.pipeline.LearningMemory") as mock_lm_cls:
            mock_lm = MagicMock()
            mock_lm.to_critic_context.return_value = ""
            mock_lm.update_from_findings.return_value = update_result
            mock_lm_cls.return_value = mock_lm

            _, run_dir = run_validation(
                target_path=artifact,
                config=config,
                runs_dir=tmp_path / "runs",
                enable_learning=True,
            )

        manifest = _json.loads((run_dir / "run-manifest.json").read_text())
        assert "learning" in manifest
        assert manifest["learning"]["new_patterns"] == 1
        assert manifest["learning"]["total_known"] == 1
