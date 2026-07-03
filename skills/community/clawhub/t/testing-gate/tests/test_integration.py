"""
Integration tests for testing gate - serialization and persistence.
"""

import json
import os
import tempfile
import pytest
from src import TestingGate, CoverageMetrics, TestStrategy, GateResult


class TestSerializationRoundTrip:
    """Test serialization round trips."""

    def test_coverage_metrics_round_trip(self):
        metrics = CoverageMetrics(90, 80, 85)
        loaded = CoverageMetrics.from_dict(metrics.to_dict())
        assert loaded.line_coverage == 90
        assert loaded.branch_coverage == 80
        assert loaded.function_coverage == 85

    def test_coverage_metrics_custom_targets_round_trip(self):
        metrics = CoverageMetrics(50, 40, 50, target_line=50, target_branch=40, target_function=50)
        loaded = CoverageMetrics.from_dict(metrics.to_dict())
        assert loaded.target_line == 50
        assert loaded.target_branch == 40
        assert loaded.target_function == 50

    def test_test_strategy_round_trip(self):
        strategy = TestStrategy(
            unit_tests=["a", "b"],
            integration_tests=["c"],
            e2e_tests=["d"],
            min_test_count=2,
        )
        loaded = TestStrategy.from_dict(strategy.to_dict())
        assert loaded.unit_tests == ["a", "b"]
        assert loaded.integration_tests == ["c"]
        assert loaded.e2e_tests == ["d"]
        assert loaded.min_test_count == 2

    def test_gate_result_round_trip(self):
        result = GateResult(
            check_name="coverage",
            passed=True,
            score=0.95,
            message="All good",
            details={"line": 90},
        )
        loaded = GateResult.from_dict(result.to_dict())
        assert loaded.check_name == "coverage"
        assert loaded.passed is True
        assert loaded.score == 0.95
        assert loaded.message == "All good"
        assert loaded.details == {"line": 90}

    def test_gate_result_with_empty_details_round_trip(self):
        result = GateResult(check_name="x", passed=False, score=0.0, message="bad")
        loaded = GateResult.from_dict(result.to_dict())
        assert loaded.details == {}


class TestJsonSerialization:
    """Test JSON serialization."""

    def test_coverage_metrics_json(self):
        metrics = CoverageMetrics(90, 80, 85)
        json_str = json.dumps(metrics.to_dict())
        loaded = CoverageMetrics.from_dict(json.loads(json_str))
        assert loaded.line_coverage == 90

    def test_test_strategy_json(self):
        strategy = TestStrategy(unit_tests=["a"], min_test_count=1)
        json_str = json.dumps(strategy.to_dict())
        loaded = TestStrategy.from_dict(json.loads(json_str))
        assert loaded.unit_tests == ["a"]
        assert loaded.min_test_count == 1

    def test_gate_result_json(self):
        result = GateResult("regression", True, 1.0, "ok", {"regressions": 0})
        json_str = json.dumps(result.to_dict())
        loaded = GateResult.from_dict(json.loads(json_str))
        assert loaded.passed is True
        assert loaded.details["regressions"] == 0

    def test_results_list_json_serialization(self):
        gate = TestingGate()
        gate.check_coverage(CoverageMetrics(90, 80, 85))
        gate.check_test_strategy(TestStrategy(unit_tests=["a"], min_test_count=1))
        results_json = json.dumps([r.to_dict() for r in gate.results])
        loaded = [GateResult.from_dict(d) for d in json.loads(results_json)]
        assert len(loaded) == 2
        assert loaded[0].check_name == "coverage"
        assert loaded[1].check_name == "test_strategy"


class TestFilePersistence:
    """Test file-based persistence."""

    def test_save_load_coverage_metrics_to_file(self, tmp_path):
        metrics = CoverageMetrics(90, 80, 85)
        path = tmp_path / "coverage.json"
        path.write_text(json.dumps(metrics.to_dict()))
        loaded = CoverageMetrics.from_dict(json.loads(path.read_text()))
        assert loaded.line_coverage == 90

    def test_save_load_test_strategy_to_file(self, tmp_path):
        strategy = TestStrategy(unit_tests=["a"], min_test_count=1)
        path = tmp_path / "strategy.json"
        path.write_text(json.dumps(strategy.to_dict()))
        loaded = TestStrategy.from_dict(json.loads(path.read_text()))
        assert loaded.unit_tests == ["a"]

    def test_save_load_gate_results_to_file(self, tmp_path):
        gate = TestingGate()
        result = gate.check_coverage(CoverageMetrics(90, 80, 85))
        path = tmp_path / "results.json"
        path.write_text(json.dumps([result.to_dict()]))
        loaded = [GateResult.from_dict(d) for d in json.loads(path.read_text())]
        assert loaded[0].passed is True

    def test_persist_full_pipeline(self, tmp_path):
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        gate.run_all_checks(context)
        path = tmp_path / "pipeline.json"
        path.write_text(json.dumps([r.to_dict() for r in gate.results]))
        loaded = [GateResult.from_dict(d) for d in json.loads(path.read_text())]
        assert len(loaded) == 3
        assert all(r.passed for r in loaded)

    def test_reload_results_and_verify_overall(self, tmp_path):
        gate = TestingGate()
        gate.check_coverage(CoverageMetrics(90, 80, 85))
        gate.check_regression({
            "previous_passing": 10,
            "current_passing": 10,
            "current_total": 10,
        })
        path = tmp_path / "verify.json"
        path.write_text(json.dumps([r.to_dict() for r in gate.results]))
        loaded = [GateResult.from_dict(d) for d in json.loads(path.read_text())]
        assert all(r.passed for r in loaded)

    def test_persist_mixed_pass_fail_results(self, tmp_path):
        gate = TestingGate()
        gate.check_coverage(CoverageMetrics(90, 80, 85))
        gate.check_test_strategy(TestStrategy(unit_tests=[], min_test_count=1))
        path = tmp_path / "mixed.json"
        path.write_text(json.dumps([r.to_dict() for r in gate.results]))
        loaded = [GateResult.from_dict(d) for d in json.loads(path.read_text())]
        assert len(loaded) == 2
        assert loaded[0].passed is True
        assert loaded[1].passed is False
