"""
Integration tests: serialization and persistence (15 tests).
"""

import json
import os

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
    return ProjectInfo(name="Integration", team="Beta", duration="3w", change_id="CH-9")


@pytest.fixture
def analyzer():
    return RetrospectiveAnalyzer()


def _build_retro(analyzer, project_info):
    retro = analyzer.start_retrospective(project_info)
    rid = retro.id
    analyzer.add_what_went_well(rid, "fast feedback")
    analyzer.add_what_was_slow(rid, "slow review")
    analyzer.add_what_failed(rid, "broken build")
    analyzer.add_gate_friction(rid, GateFriction("design", "unclear", "delay", "clarify"))
    return rid


class TestModelSerialization:
    def test_project_info_to_dict(self, project_info):
        d = project_info.to_dict()
        assert d["name"] == "Integration"
        assert d["change_id"] == "CH-9"

    def test_project_info_roundtrip(self, project_info):
        assert ProjectInfo.from_dict(project_info.to_dict()) == project_info

    def test_gate_friction_roundtrip(self):
        f = GateFriction("g", "i", "impact", "c")
        assert GateFriction.from_dict(f.to_dict()) == f

    def test_improvement_candidate_roundtrip(self):
        c = ImprovementCandidate("t", "r", "reason", "high")
        assert ImprovementCandidate.from_dict(c.to_dict()) == c

    def test_retrospective_to_dict_includes_status(self, analyzer, project_info):
        rid = analyzer.start_retrospective(project_info).id
        d = analyzer.get_retrospective(rid).to_dict()
        assert d["status"] == "active"

    def test_retrospective_roundtrip(self, analyzer, project_info):
        rid = _build_retro(analyzer, project_info)
        retro = analyzer.get_retrospective(rid)
        restored = Retrospective.from_dict(retro.to_dict())
        assert restored.id == retro.id
        assert restored.status == retro.status
        assert restored.what_failed == retro.what_failed
        assert len(restored.gate_frictions) == len(retro.gate_frictions)

    def test_analysis_to_dict(self, analyzer, project_info):
        rid = _build_retro(analyzer, project_info)
        result = analyzer.analyze(rid)
        d = result.to_dict()
        restored = AnalysisResult.from_dict(d)
        assert restored.total_issues == result.total_issues
        assert restored.severity == result.severity

    def test_report_roundtrip(self, analyzer, project_info):
        rid = _build_retro(analyzer, project_info)
        report = analyzer.generate_report(rid)
        restored = RetrospectiveReport.from_dict(report.to_dict())
        assert restored.retro_id == report.retro_id
        assert restored.recommendations == report.recommendations


class TestFilePersistence:
    def test_save_to_file_writes_json(self, analyzer, project_info, tmp_path):
        rid = _build_retro(analyzer, project_info)
        path = tmp_path / "retro.json"
        analyzer.save_to_file(rid, str(path))
        assert path.exists()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["id"] == rid

    def test_load_from_file_restores(self, analyzer, project_info, tmp_path):
        rid = _build_retro(analyzer, project_info)
        path = tmp_path / "retro.json"
        analyzer.save_to_file(rid, str(path))

        fresh = RetrospectiveAnalyzer()
        retro = fresh.load_from_file(str(path))
        assert retro.id == rid
        assert retro.what_failed == ["broken build"]
        assert retro.status == RetroStatus.ACTIVE

    def test_save_load_roundtrip(self, analyzer, project_info, tmp_path):
        rid = _build_retro(analyzer, project_info)
        path = tmp_path / "retro.json"
        analyzer.save_to_file(rid, str(path))
        fresh = RetrospectiveAnalyzer()
        loaded = fresh.load_from_file(str(path))
        original = analyzer.get_retrospective(rid)
        assert loaded.to_dict() == original.to_dict()

    def test_load_nonexistent_file_raises(self, tmp_path):
        analyzer = RetrospectiveAnalyzer()
        with pytest.raises(FileNotFoundError):
            analyzer.load_from_file(str(tmp_path / "nope.json"))

    def test_save_creates_nested_directory(self, analyzer, project_info, tmp_path):
        rid = analyzer.start_retrospective(project_info).id
        path = tmp_path / "nested" / "dir" / "retro.json"
        analyzer.save_to_file(rid, str(path))
        assert path.exists()

    def test_load_registers_retro_in_analyzer(self, analyzer, project_info, tmp_path):
        rid = _build_retro(analyzer, project_info)
        path = tmp_path / "retro.json"
        analyzer.save_to_file(rid, str(path))
        fresh = RetrospectiveAnalyzer()
        loaded = fresh.load_from_file(str(path))
        assert fresh.get_retrospective(loaded.id).id == loaded.id

    def test_export_report_to_file(self, analyzer, project_info, tmp_path):
        rid = _build_retro(analyzer, project_info)
        analyzer.generate_report(rid)
        path = tmp_path / "report.json"
        analyzer.export_report(rid, str(path))
        assert path.exists()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        assert data["retro_id"] == rid
