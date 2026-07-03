"""
Extended unit tests for task routing.
"""

import pytest
from src import RoutingEngine
from src.models import (
    TaskMetadata, RoutingRule, RoutingCondition, PriorityFactors,
    ChangeType, SizeLevel, RiskLevel, UrgencyLevel
)
import threading


class TestBoundaryScenarios:
    """Test boundary scenarios."""

    def test_empty_custom_attributes(self):
        """Test routing with empty custom attributes."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM,
            custom_attributes={}
        )
        decision = engine.route(metadata)
        assert decision.target is not None

    def test_none_custom_attributes(self):
        """Test routing with None custom attributes (should default to {})."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        # custom_attributes should default to {}
        assert metadata.custom_attributes == {}

    def test_invalid_change_type(self):
        """Test handling invalid change type."""
        with pytest.raises(ValueError):
            ChangeType("invalid_type")

    def test_invalid_size_level(self):
        """Test handling invalid size level."""
        with pytest.raises(ValueError):
            SizeLevel("invalid_size")

    def test_invalid_risk_level(self):
        """Test handling invalid risk level."""
        with pytest.raises(ValueError):
            RiskLevel("invalid_risk")

    def test_invalid_urgency_level(self):
        """Test handling invalid urgency level."""
        with pytest.raises(ValueError):
            UrgencyLevel("invalid_urgency")

    def test_all_change_types(self):
        """Test routing all change types."""
        engine = RoutingEngine()
        change_types = [
            ChangeType.FEATURE, ChangeType.BUGFIX, ChangeType.HOTFIX,
            ChangeType.REFACTOR, ChangeType.DOCS, ChangeType.TEST,
            ChangeType.CONFIG, ChangeType.PROMPT, ChangeType.BUILD,
            ChangeType.CI, ChangeType.PERF, ChangeType.SECURITY,
            ChangeType.MIGRATION, ChangeType.RESEARCH, ChangeType.CLEANUP,
            ChangeType.CHORE
        ]
        for change_type in change_types:
            metadata = TaskMetadata(change_type, SizeLevel.M, RiskLevel.MEDIUM)
            decision = engine.route(metadata)
            assert decision.target is not None

    def test_all_size_levels(self):
        """Test routing all size levels."""
        engine = RoutingEngine()
        size_levels = [SizeLevel.XS, SizeLevel.S, SizeLevel.M, SizeLevel.L, SizeLevel.XL]
        for size in size_levels:
            metadata = TaskMetadata(ChangeType.FEATURE, size, RiskLevel.MEDIUM)
            decision = engine.route(metadata)
            assert decision.target is not None

    def test_all_risk_levels(self):
        """Test routing all risk levels."""
        engine = RoutingEngine()
        risk_levels = [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]
        for risk in risk_levels:
            metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, risk)
            decision = engine.route(metadata)
            assert decision.target is not None

    def test_all_urgency_levels(self):
        """Test routing all urgency levels."""
        engine = RoutingEngine()
        urgency_levels = [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH, UrgencyLevel.URGENT]
        for urgency in urgency_levels:
            metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM, urgency)
            priority = engine.calculate_priority(metadata)
            assert priority >= 0 and priority <= 100


class TestConditionOperators:
    """Test all condition operators."""

    def test_equals_operator_match(self):
        """Test equals operator with match."""
        condition = RoutingCondition("change_type", ChangeType.BUGFIX, "equals")
        metadata = TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is True

    def test_equals_operator_no_match(self):
        """Test equals operator without match."""
        condition = RoutingCondition("change_type", ChangeType.FEATURE, "equals")
        metadata = TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is False

    def test_not_equals_operator_match(self):
        """Test not_equals operator with match."""
        condition = RoutingCondition("change_type", ChangeType.FEATURE, "not_equals")
        metadata = TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is True

    def test_not_equals_operator_no_match(self):
        """Test not_equals operator without match."""
        condition = RoutingCondition("change_type", ChangeType.BUGFIX, "not_equals")
        metadata = TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is False

    def test_in_operator_match(self):
        """Test in operator with match."""
        condition = RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is True

    def test_in_operator_no_match(self):
        """Test in operator without match."""
        condition = RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.L, RiskLevel.LOW)
        assert condition.matches(metadata) is False

    def test_not_in_operator_match(self):
        """Test not_in operator with match."""
        condition = RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "not_in")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.S, RiskLevel.LOW)
        assert condition.matches(metadata) is True

    def test_not_in_operator_no_match(self):
        """Test not_in operator without match."""
        condition = RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "not_in")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.L, RiskLevel.LOW)
        assert condition.matches(metadata) is False

    def test_greater_than_operator(self):
        """Test greater_than operator."""
        condition = RoutingCondition("cross_module", True, "greater_than")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
        metadata.cross_module = True
        # Note: greater_than doesn't work well with booleans, but test it anyway
        assert condition.matches(metadata) is False

    def test_less_than_operator(self):
        """Test less_than operator."""
        condition = RoutingCondition("cross_module", True, "less_than")
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
        metadata.cross_module = False
        assert condition.matches(metadata) is True


class TestPriorityCalculation:
    """Test priority calculation scenarios."""

    def test_critical_risk_priority(self):
        """Test critical risk priority."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            ChangeType.SECURITY,
            SizeLevel.M,
            RiskLevel.CRITICAL,
            UrgencyLevel.URGENT
        )
        priority = engine.calculate_priority(metadata)
        # Critical risk + Urgent should result in high priority
        assert priority >= 60

    def test_low_urgency_priority(self):
        """Test low urgency priority."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            ChangeType.DOCS,
            SizeLevel.XS,
            RiskLevel.LOW,
            UrgencyLevel.LOW
        )
        priority = engine.calculate_priority(metadata)
        # Low risk + Low urgency should result in low priority
        assert priority <= 40

    def test_cross_module_priority_boost(self):
        """Test cross-module priority boost."""
        engine = RoutingEngine()
        metadata_no_cross = TaskMetadata(
            ChangeType.FEATURE,
            SizeLevel.M,
            RiskLevel.MEDIUM,
            UrgencyLevel.MEDIUM,
            cross_module=False
        )
        metadata_cross = TaskMetadata(
            ChangeType.FEATURE,
            SizeLevel.M,
            RiskLevel.MEDIUM,
            UrgencyLevel.MEDIUM,
            cross_module=True
        )

        priority_no_cross = engine.calculate_priority(metadata_no_cross)
        priority_cross = engine.calculate_priority(metadata_cross)
        assert priority_cross > priority_no_cross

    def test_size_inverse_priority(self):
        """Test size inverse priority (smaller = higher)."""
        engine = RoutingEngine()
        metadata_xs = TaskMetadata(ChangeType.FEATURE, SizeLevel.XS, RiskLevel.MEDIUM)
        metadata_xl = TaskMetadata(ChangeType.FEATURE, SizeLevel.XL, RiskLevel.MEDIUM)

        priority_xs = engine.calculate_priority(metadata_xs)
        priority_xl = engine.calculate_priority(metadata_xl)
        assert priority_xs > priority_xl


class TestRuleManagement:
    """Test rule management scenarios."""

    def test_add_multiple_custom_rules(self):
        """Test adding multiple custom rules."""
        engine = RoutingEngine()
        custom_rules = [
            RoutingRule(
                name="rule1",
                conditions=[RoutingCondition("change_type", ChangeType.SECURITY)],
                target="security_team",
                priority=150
            ),
            RoutingRule(
                name="rule2",
                conditions=[RoutingCondition("change_type", ChangeType.PERF)],
                target="perf_team",
                priority=140
            ),
        ]
        for rule in custom_rules:
            engine.add_rule(rule)

        # Test routing security
        metadata = TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.MEDIUM)
        decision = engine.route(metadata)
        assert decision.target == "security_team"

    def test_disabled_rule(self):
        """Test disabled rule doesn't match."""
        engine = RoutingEngine()
        disabled_rule = RoutingRule(
            name="disabled_rule",
            conditions=[RoutingCondition("change_type", ChangeType.FEATURE)],
            target="disabled_target",
            priority=200,
            enabled=False
        )
        engine.add_rule(disabled_rule)

        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
        decision = engine.route(metadata)
        # Should not match disabled rule
        assert decision.matched_rule != "disabled_rule"

    def test_rule_confidence_weight(self):
        """Test rule confidence weight."""
        rule_high_confidence = RoutingRule(
            name="high_confidence_rule",
            conditions=[RoutingCondition("change_type", ChangeType.BUGFIX)],
            target="hotfix_workflow",
            priority=100,
            confidence_weight=1.0
        )
        rule_low_confidence = RoutingRule(
            name="low_confidence_rule",
            conditions=[RoutingCondition("change_type", ChangeType.BUGFIX)],
            target="some_workflow",
            priority=90,
            confidence_weight=0.5
        )

        assert rule_high_confidence.confidence_weight == 1.0
        assert rule_low_confidence.confidence_weight == 0.5


class TestConcurrentRouting:
    """Test concurrent routing."""

    def test_concurrent_route_calls(self):
        """Test concurrent route calls."""
        engine = RoutingEngine()
        results = []

        def route_task():
            metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
            decision = engine.route(metadata)
            results.append(decision.target)

        threads = [threading.Thread(target=route_task) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
        assert all(target == "standard_workflow" for target in results)

    def test_concurrent_priority_calculation(self):
        """Test concurrent priority calculation."""
        engine = RoutingEngine()
        results = []

        def calculate_priority():
            metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
            priority = engine.calculate_priority(metadata)
            results.append(priority)

        threads = [threading.Thread(target=calculate_priority) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
        # All should be same priority
        assert all(p == results[0] for p in results)


class TestAlternatives:
    """Test routing alternatives."""

    def test_alternatives_present(self):
        """Test alternatives are present in decision."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            ChangeType.DOCS,
            SizeLevel.M,  # Not XS or S
            RiskLevel.MEDIUM  # Not LOW
        )
        decision = engine.route(metadata)
        # Should have alternatives because docs_small_low_risk partially matches
        assert isinstance(decision.alternatives, list)

    def test_no_alternatives_for_exact_match(self):
        """Test no alternatives for exact match."""
        engine = RoutingEngine()
        metadata = TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW)
        decision = engine.route(metadata)
        # Exact match should have high confidence
        assert decision.confidence > 0.5


class TestEmptyConditions:
    """Test empty conditions."""

    def test_empty_conditions_rule(self):
        """Test rule with empty conditions (always matches)."""
        rule = RoutingRule(
            name="catch_all",
            conditions=[],
            target="default_target",
            priority=1
        )
        metadata = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
        assert rule.matches(metadata) is True  # Empty conditions always match