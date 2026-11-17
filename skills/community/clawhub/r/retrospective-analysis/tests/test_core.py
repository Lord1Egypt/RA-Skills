"""
Core functionality tests for RetrospectiveAnalyzer (25 tests).
"""

import pytest

from src import RetrospectiveAnalyzer
from src.models import (
    AnalysisResult,
    GateFriction,
    ImprovementCandidate,
    ProjectInfo,
    Retrospective,
    RetrospectiveReport,
    RetroStatus,
)


@pytest.fixture
def project_info():
    return ProjectInfo(name="Demo", team="Alpha", duration="2 weeks", change_id="CH-1")


@pytest.fixture
def analyzer():
    return RetrospectiveAnalyzer()


@pytest.fixture
def retro_id(analyzer, project_info):
    return analyzer.start_retrospective(project_info).id


class TestStartRetrospective:
    def test_start_returns_retrospective(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        assert isinstance(retro, Retrospective)

    def test_start_assigns_unique_id(self, analyzer, project_info):
        r1 = analyzer.start_retrospective(project_info)
        r2 = analyzer.start_retrospective(project_info)
        assert r1.id != r2.id

    def test_start_default_status_active(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        assert retro.status == RetroStatus.ACTIVE

    def test_start_sets_project_info(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        assert retro.project_info is project_info

    def test_start_sets_created_at(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        assert retro.created_at
        assert isinstance(retro.created_at, str)


class TestAddingEntries:
    def test_add_what_went_well(self, analyzer, retro_id):
        analyzer.add_what_went_well(retro_id, "fast review")
        retro = analyzer.get_retrospective(retro_id)
        assert retro.what_went_well == ["fast review"]

    def test_add_what_was_slow(self, analyzer, retro_id):
        analyzer.add_what_was_slow(retro_id, "slow gate")
        retro = analyzer.get_retrospective(retro_id)
        assert retro.what_was_slow == ["slow gate"]

    def test_add_what_failed(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "build broken")
        retro = analyzer.get_retrospective(retro_id)
        assert retro.what_failed == ["build broken"]

    def test_add_gate_friction(self, analyzer, retro_id):
        friction = GateFriction("design-gate", "unclear", "delay", "clarify")
        analyzer.add_gate_friction(retro_id, friction)
        retro = analyzer.get_retrospective(retro_id)
        assert retro.gate_frictions == [friction]

    def test_add_multiple_entries_accumulate(self, analyzer, retro_id):
        analyzer.add_what_went_well(retro_id, "a")
        analyzer.add_what_went_well(retro_id, "b")
        retro = analyzer.get_retrospective(retro_id)
        assert retro.what_went_well == ["a", "b"]


class TestAnalyze:
    def test_analyze_returns_result(self, analyzer, retro_id):
        result = analyzer.analyze(retro_id)
        assert isinstance(result, AnalysisResult)

    def test_analyze_total_issues_zero(self, analyzer, retro_id):
        result = analyzer.analyze(retro_id)
        assert result.total_issues == 0

    def test_analyze_total_issues_counts_all(self, analyzer, retro_id):
        analyzer.add_what_was_slow(retro_id, "slow")
        analyzer.add_what_failed(retro_id, "fail")
        analyzer.add_gate_friction(retro_id, GateFriction("g", "i", "impact", "c"))
        result = analyzer.analyze(retro_id)
        assert result.total_issues == 3

    def test_analyze_friction_points(self, analyzer, retro_id):
        analyzer.add_gate_friction(retro_id, GateFriction("g1", "i", "impact", "c"))
        analyzer.add_gate_friction(retro_id, GateFriction("g2", "i", "impact", "c"))
        result = analyzer.analyze(retro_id)
        assert result.friction_points == 2

    def test_analyze_severity_low(self, analyzer, retro_id):
        assert analyzer.analyze(retro_id).severity == "low"

    def test_analyze_severity_medium(self, analyzer, retro_id):
        for i in range(4):
            analyzer.add_what_was_slow(retro_id, f"slow-{i}")
        assert analyzer.analyze(retro_id).severity == "medium"

    def test_analyze_severity_high(self, analyzer, retro_id):
        for i in range(5):
            analyzer.add_what_was_slow(retro_id, f"slow-{i}")
        assert analyzer.analyze(retro_id).severity == "high"

    def test_analyze_severity_critical(self, analyzer, retro_id):
        for i in range(10):
            analyzer.add_what_was_slow(retro_id, f"slow-{i}")
        assert analyzer.analyze(retro_id).severity == "critical"

    def test_analyze_sets_status_analyzed(self, analyzer, retro_id):
        analyzer.analyze(retro_id)
        retro = analyzer.get_retrospective(retro_id)
        assert retro.status == RetroStatus.ANALYZED

    def test_analyze_summary_contains_counts(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        analyzer.add_gate_friction(retro_id, GateFriction("g", "i", "impact", "c"))
        result = analyzer.analyze(retro_id)
        assert "2" in result.summary
        assert "1" in result.summary


class TestImprovementCandidates:
    def test_get_improvement_candidates_after_analyze(self, analyzer, retro_id):
        analyzer.add_gate_friction(retro_id, GateFriction("g", "i", "impact", "do X"))
        analyzer.analyze(retro_id)
        candidates = analyzer.get_improvement_candidates(retro_id)
        assert len(candidates) == 1
        assert isinstance(candidates[0], ImprovementCandidate)

    def test_get_improvement_candidates_triggers_analyze(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        candidates = analyzer.get_improvement_candidates(retro_id)
        assert len(candidates) == 1
        assert candidates[0].priority == "high"

    def test_candidate_priority_high_for_block(self, analyzer, retro_id):
        analyzer.add_gate_friction(
            retro_id, GateFriction("g", "i", "blocked release", "fix")
        )
        candidates = analyzer.get_improvement_candidates(retro_id)
        assert candidates[0].priority == "high"

    def test_candidate_priority_medium_default(self, analyzer, retro_id):
        analyzer.add_gate_friction(
            retro_id, GateFriction("g", "i", "moderate delay", "adjust")
        )
        candidates = analyzer.get_improvement_candidates(retro_id)
        assert candidates[0].priority == "medium"


class TestReport:
    def test_generate_report(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        report = analyzer.generate_report(retro_id)
        assert isinstance(report, RetrospectiveReport)
        assert report.retro_id == retro_id

    def test_generate_report_sets_status_reported(self, analyzer, retro_id):
        analyzer.generate_report(retro_id)
        retro = analyzer.get_retrospective(retro_id)
        assert retro.status == RetroStatus.REPORTED
