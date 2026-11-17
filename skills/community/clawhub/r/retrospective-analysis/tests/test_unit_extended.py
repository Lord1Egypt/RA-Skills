"""
Extended unit tests: edge cases, exceptions, concurrency safety (30 tests).
"""

import threading

import pytest

from src import RetrospectiveAnalyzer
from src.models import GateFriction, ProjectInfo, RetroStatus


@pytest.fixture
def project_info():
    return ProjectInfo(name="P", team="T", duration="1w", change_id="C")


@pytest.fixture
def analyzer():
    return RetrospectiveAnalyzer()


@pytest.fixture
def retro_id(analyzer, project_info):
    return analyzer.start_retrospective(project_info).id


class TestNotFound:
    def test_get_retrospective_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.get_retrospective("missing")

    def test_add_what_went_well_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.add_what_went_well("missing", "x")

    def test_add_what_was_slow_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.add_what_was_slow("missing", "x")

    def test_add_what_failed_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.add_what_failed("missing", "x")

    def test_add_gate_friction_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.add_gate_friction("missing", GateFriction("g", "i", "m", "c"))

    def test_analyze_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.analyze("missing")

    def test_generate_report_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.generate_report("missing")

    def test_get_improvement_candidates_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.get_improvement_candidates("missing")

    def test_archive_not_found(self, analyzer):
        with pytest.raises(KeyError):
            analyzer.archive("missing")


class TestItemValidation:
    def test_add_well_empty_raises(self, analyzer, retro_id):
        with pytest.raises(ValueError):
            analyzer.add_what_went_well(retro_id, "")

    def test_add_well_none_raises(self, analyzer, retro_id):
        with pytest.raises(ValueError):
            analyzer.add_what_went_well(retro_id, None)

    def test_add_well_whitespace_raises(self, analyzer, retro_id):
        with pytest.raises(ValueError):
            analyzer.add_what_went_well(retro_id, "   ")

    def test_add_gate_friction_wrong_type(self, analyzer, retro_id):
        with pytest.raises(TypeError):
            analyzer.add_gate_friction(retro_id, "not-a-friction")

    def test_add_returns_none(self, analyzer, retro_id):
        assert analyzer.add_what_went_well(retro_id, "x") is None


class TestSeverityBoundaries:
    def _add_issues(self, analyzer, retro_id, count):
        for i in range(count):
            analyzer.add_what_was_slow(retro_id, f"s-{i}")

    def test_boundary_4_is_medium(self, analyzer, retro_id):
        self._add_issues(analyzer, retro_id, 4)
        assert analyzer.analyze(retro_id).severity == "medium"

    def test_boundary_5_is_high(self, analyzer, retro_id):
        self._add_issues(analyzer, retro_id, 5)
        assert analyzer.analyze(retro_id).severity == "high"

    def test_boundary_9_is_high(self, analyzer, retro_id):
        self._add_issues(analyzer, retro_id, 9)
        assert analyzer.analyze(retro_id).severity == "high"

    def test_boundary_10_is_critical(self, analyzer, retro_id):
        self._add_issues(analyzer, retro_id, 10)
        assert analyzer.analyze(retro_id).severity == "critical"


class TestLifecycle:
    def test_archive_sets_status(self, analyzer, retro_id):
        analyzer.archive(retro_id)
        assert analyzer.get_retrospective(retro_id).status == RetroStatus.ARCHIVED

    def test_multiple_retros_independent(self, analyzer, project_info):
        r1 = analyzer.start_retrospective(project_info).id
        r2 = analyzer.start_retrospective(project_info).id
        analyzer.add_what_failed(r1, "fail-1")
        assert analyzer.get_retrospective(r1).what_failed == ["fail-1"]
        assert analyzer.get_retrospective(r2).what_failed == []

    def test_generate_report_uses_cached_analysis(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        analyzer.analyze(retro_id)
        # Adding more after analyze should not change cached report analysis
        analyzer.add_what_failed(retro_id, "fail-2")
        report = analyzer.generate_report(retro_id)
        assert report.analysis.total_issues == 1

    def test_get_report_after_generate(self, analyzer, retro_id):
        analyzer.generate_report(retro_id)
        assert analyzer.get_report(retro_id).retro_id == retro_id


class TestCandidatePriorities:
    def test_candidate_failure_high(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "boom")
        cands = analyzer.get_improvement_candidates(retro_id)
        assert cands[0].priority == "high"
        assert cands[0].target == "process"

    def test_candidate_slow_medium(self, analyzer, retro_id):
        analyzer.add_what_was_slow(retro_id, "laggy")
        cands = analyzer.get_improvement_candidates(retro_id)
        assert cands[0].priority == "medium"

    def test_candidate_low_impact(self, analyzer, retro_id):
        analyzer.add_gate_friction(
            retro_id, GateFriction("g", "i", "minor noise", "tweak")
        )
        cands = analyzer.get_improvement_candidates(retro_id)
        assert cands[0].priority == "low"

    def test_report_action_items_format(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        report = analyzer.generate_report(retro_id)
        assert report.action_items[0].startswith("[high]")

    def test_get_improvement_candidates_returns_copy(self, analyzer, retro_id):
        analyzer.add_what_failed(retro_id, "fail")
        c1 = analyzer.get_improvement_candidates(retro_id)
        c1.clear()
        c2 = analyzer.get_improvement_candidates(retro_id)
        assert len(c2) == 1


class TestConcurrency:
    def test_concurrent_adds_threadsafe(self, analyzer, retro_id):
        n = 100
        threads = [
            threading.Thread(target=analyzer.add_what_went_well, args=(retro_id, f"i-{i}"))
            for i in range(n)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(analyzer.get_retrospective(retro_id).what_went_well) == n

    def test_concurrent_start_retrospective(self, analyzer, project_info):
        ids = []
        lock = threading.Lock()

        def start():
            rid = analyzer.start_retrospective(project_info).id
            with lock:
                ids.append(rid)

        threads = [threading.Thread(target=start) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(ids) == 50
        assert len(set(ids)) == 50

    def test_created_at_is_iso(self, analyzer, project_info):
        retro = analyzer.start_retrospective(project_info)
        # ISO format contains a 'T' separator between date and time
        assert "T" in retro.created_at
