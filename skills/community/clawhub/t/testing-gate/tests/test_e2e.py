"""
End-to-end tests for testing gate - complete workflows.
"""

import json
import pytest
from src import TestingGate, CoverageMetrics, TestStrategy, GateResult


class TestCompletePipelines:
    """Test complete end-to-end pipelines."""

    def test_full_passing_pipeline(self):
        """Complete CI pipeline where everything passes."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(95, 85, 90),
            "test_strategy": TestStrategy(
                unit_tests=["test_unit_a", "test_unit_b"],
                integration_tests=["test_int"],
                e2e_tests=["test_e2e"],
                min_test_count=3,
            ),
            "regression_artifacts": {
                "previous_passing": 50,
                "current_passing": 55,
                "current_total": 55,
                "new_tests": 5,
            },
        }
        results = gate.run_all_checks(context)
        assert len(results) == 3
        assert gate.overall_passed() is True
        assert all(r.score > 0 for r in results)

    def test_pipeline_with_coverage_failure(self):
        """Pipeline fails due to insufficient coverage."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(50, 40, 50),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        results = gate.run_all_checks(context)
        assert results[0].passed is False
        assert gate.overall_passed() is False

    def test_pipeline_with_strategy_failure(self):
        """Pipeline fails due to missing unit tests."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
            "test_strategy": TestStrategy(unit_tests=[], min_test_count=5),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        results = gate.run_all_checks(context)
        assert results[1].passed is False
        assert gate.overall_passed() is False

    def test_pipeline_with_regression_detected(self):
        """Pipeline fails due to regressions."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 50,
                "current_passing": 45,
                "current_total": 50,
            },
        }
        results = gate.run_all_checks(context)
        assert results[2].passed is False
        assert results[2].details["regressions"] == 5

    def test_pipeline_with_mixed_results(self):
        """Pipeline with some checks passing and others failing."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 60, 85),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        results = gate.run_all_checks(context)
        assert results[0].passed is False
        assert results[1].passed is True
        assert results[2].passed is True
        assert gate.overall_passed() is False

    def test_development_workflow_scenario(self):
        """Simulate a development workflow with all checks."""
        gate = TestingGate()
        # Developer commits new feature with good coverage
        gate.check_coverage(CoverageMetrics(88, 75, 82))
        gate.check_test_strategy(TestStrategy(
            unit_tests=["test_feature", "test_edge"],
            integration_tests=["test_integration"],
            min_test_count=2,
        ))
        gate.check_regression({
            "previous_passing": 30,
            "current_passing": 32,
            "current_total": 32,
            "new_tests": 2,
        })
        assert gate.overall_passed() is True
        assert len(gate.results) == 3

    def test_hotfix_scenario_verification(self):
        """Simulate hotfix verification with regression check."""
        gate = TestingGate()
        # Hotfix should not introduce regressions
        result = gate.check_regression({
            "previous_passing": 100,
            "current_passing": 100,
            "current_total": 100,
        })
        assert result.passed is True
        # Now a bad hotfix
        gate.clear()
        result = gate.check_regression({
            "previous_passing": 100,
            "current_passing": 98,
            "current_total": 100,
        })
        assert result.passed is False

    def test_pipeline_with_custom_targets(self):
        """Pipeline with custom coverage targets."""
        gate = TestingGate()
        metrics = CoverageMetrics(60, 50, 60, target_line=60, target_branch=50, target_function=60)
        context = {
            "coverage_metrics": metrics,
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        results = gate.run_all_checks(context)
        assert results[0].passed is True
        assert gate.overall_passed() is True

    def test_pipeline_decision_and_aggregation(self):
        """Aggregate results and make a release decision."""
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(92, 82, 88),
            "test_strategy": TestStrategy(
                unit_tests=["u1", "u2", "u3"],
                integration_tests=["i1"],
                e2e_tests=["e1"],
                min_test_count=3,
            ),
            "regression_artifacts": {
                "previous_passing": 40,
                "current_passing": 45,
                "current_total": 45,
                "new_tests": 5,
            },
        }
        results = gate.run_all_checks(context)
        avg_score = sum(r.score for r in results) / len(results)
        assert gate.overall_passed() is True
        assert avg_score > 0.5
        # Release decision: all pass and avg score high
        can_release = gate.overall_passed() and avg_score > 0.5
        assert can_release is True

    def test_full_pipeline_serialization_reload(self, tmp_path):
        """Run full pipeline, serialize, reload, and verify."""
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
        results = gate.run_all_checks(context)
        # Serialize to file
        path = tmp_path / "e2e_results.json"
        path.write_text(json.dumps([r.to_dict() for r in results]))
        # Reload and verify
        loaded = [GateResult.from_dict(d) for d in json.loads(path.read_text())]
        assert len(loaded) == 3
        assert all(r.passed for r in loaded)
        assert loaded[0].check_name == "coverage"
        assert loaded[1].check_name == "test_strategy"
        assert loaded[2].check_name == "regression"
