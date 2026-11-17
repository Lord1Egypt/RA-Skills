"""
End-to-end tests: complete retrospective workflows (10 tests).
"""

import json

import pytest

from src import RetrospectiveAnalyzer
from src.models import (
    GateFriction,
    ProjectInfo,
    RetrospectiveReport,
    RetroStatus,
)


@pytest.fixture
def project_info():
    return ProjectInfo(name="E2E Project", team="Gamma", duration="4w", change_id="CH-E2E")


@pytest.fixture
def analyzer():
    return RetrospectiveAnalyzer()


def _run_full_flow(analyzer, project_info):
    retro = analyzer.start_retrospective(project_info)
    rid = retro.id
    analyzer.add_what_went_well(rid, "smooth design")
    analyzer.add_what_was_slow(rid, "slow test gate")
    analyzer.add_what_failed(rid, "deploy rollback")
    analyzer.add_gate_friction(
        rid, GateFriction("testing-gate", "flaky tests", "blocked merge", "stabilize suite")
    )
    analysis = analyzer.analyze(rid)
    report = analyzer.generate_report(rid)
    return rid, analysis, report


class TestFullWorkflow:
    def test_start_to_report(self, analyzer, project_info):
        rid, analysis, report = _run_full_flow(analyzer, project_info)
        assert report.retro_id == rid
        assert report.analysis is analysis
        assert len(report.recommendations) > 0

    def test_status_transitions(self, analyzer, project_info):
        rid, _, _ = _run_full_flow(analyzer, project_info)
        retro = analyzer.get_retrospective(rid)
        assert retro.status == RetroStatus.REPORTED

    def test_full_workflow_with_gate_friction(self, analyzer, project_info):
        rid, analysis, _ = _run_full_flow(analyzer, project_info)
        assert analysis.friction_points == 1
        cands = analyzer.get_improvement_candidates(rid)
        gate_cand = [c for c in cands if c.target == "testing-gate"]
        assert gate_cand and gate_cand[0].priority == "high"

    def test_full_workflow_archive(self, analyzer, project_info):
        rid, _, _ = _run_full_flow(analyzer, project_info)
        analyzer.archive(rid)
        assert analyzer.get_retrospective(rid).status == RetroStatus.ARCHIVED

    def test_full_workflow_no_issues(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        analysis = analyzer.analyze(retro.id)
        report = analyzer.generate_report(retro.id)
        assert analysis.total_issues == 0
        assert analysis.severity == "low"
        assert report.recommendations == []
        assert report.action_items == []

    def test_full_workflow_many_issues(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        for i in range(12):
            analyzer.add_what_was_slow(retro.id, f"slow-{i}")
        analysis = analyzer.analyze(retro.id)
        assert analysis.severity == "critical"
        assert analysis.total_issues == 12

    def test_full_workflow_save_and_reload(self, analyzer, project_info, tmp_path):
        rid, _, _ = _run_full_flow(analyzer, project_info)
        path = tmp_path / "e2e.json"
        analyzer.save_to_file(rid, str(path))
        fresh = RetrospectiveAnalyzer()
        loaded = fresh.load_from_file(str(path))
        assert loaded.id == rid
        assert "deploy rollback" in loaded.what_failed

    def test_full_workflow_report_recommendations(self, analyzer, project_info):
        rid, _, report = _run_full_flow(analyzer, project_info)
        # Expect recommendations for friction, failure, and slow step
        assert len(report.recommendations) == 3
        assert any("stabilize suite" in r for r in report.recommendations)

    def test_full_workflow_improvement_candidates_count(self, analyzer, project_info):
        rid, _, _ = _run_full_flow(analyzer, project_info)
        cands = analyzer.get_improvement_candidates(rid)
        # 1 friction + 1 failure + 1 slow = 3 candidates
        assert len(cands) == 3
        priorities = {c.priority for c in cands}
        assert priorities == {"high", "medium"}

    def test_full_workflow_export_report_json(self, analyzer, project_info, tmp_path):
        rid, _, _ = _run_full_flow(analyzer, project_info)
        path = tmp_path / "report.json"
        analyzer.export_report(rid, str(path))
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["retro_id"] == rid
        assert isinstance(data["report" if "report" in data else "recommendations"], list)
        assert len(data["recommendations"]) == 3
