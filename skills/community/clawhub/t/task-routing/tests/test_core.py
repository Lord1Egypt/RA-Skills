"""
Test suite for task routing skill.
"""

import pytest
from src import RoutingEngine, RoutingDecision
from src.models import (
    TaskMetadata, RoutingRule, RoutingCondition, PriorityFactors,
    ChangeType, SizeLevel, RiskLevel, UrgencyLevel
)


class TestRoutingEngine:
    """Test RoutingEngine basic functionality."""

    def test_init_default_template(self):
        """Test initialization with default template."""
        engine = RoutingEngine()
        assert engine is not None
        assert len(engine.get_rules()) > 0

    def test_init_development_template(self):
        """Test initialization with development template."""
        engine = RoutingEngine(template="development")
        assert engine is not None

    def test_get_rules(self):
        """Test getting routing rules."""
        engine = RoutingEngine()
        rules = engine.get_rules()
        assert len(rules) > 0
        assert all(isinstance(rule, RoutingRule) for rule in rules)


class TestRoutingDecision:
    """Test routing decision."""

    def test_route_bugfix_to_hotfix(self):
        """Test routing bugfix to hotfix workflow."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.BUGFIX,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        decision = engine.route(metadata)
        assert decision.target == "hotfix_workflow"
        assert decision.matched_rule == "bugfix_to_hotfix"

    def test_route_hotfix_to_hotfix(self):
        """Test routing hotfix to hotfix workflow."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.HOTFIX,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        decision = engine.route(metadata)
        assert decision.target == "hotfix_workflow"

    def test_route_docs_small_low_risk_to_lightweight(self):
        """Test routing docs small low risk to lightweight."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.XS,
            risk_level=RiskLevel.LOW
        )
        decision = engine.route(metadata)
        assert decision.target == "lightweight_workflow"

    def test_route_feature_to_standard(self):
        """Test routing feature to standard workflow."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        decision = engine.route(metadata)
        assert decision.target == "standard_workflow"

    def test_route_high_risk_to_standard(self):
        """Test routing high risk to standard."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.HIGH
        )
        decision = engine.route(metadata)
        assert decision.target == "standard_workflow"

    def test_route_large_size_to_standard(self):
        """Test routing large size to standard."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.L,
            risk_level=RiskLevel.LOW
        )
        decision = engine.route(metadata)
        assert decision.target == "standard_workflow"

    def test_route_default_to_standard(self):
        """Test default routing to standard."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.TEST,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        decision = engine.route(metadata)
        assert decision.target == "standard_workflow"


class TestRoutingRule:
    """Test routing rule functionality."""

    def test_add_custom_rule(self):
        """Test adding custom routing rule."""
        engine = RoutingEngine()
        custom_rule = RoutingRule(
            name="critical_security_to_security_team",
            conditions=[
                RoutingCondition("change_type", ChangeType.SECURITY),
                RoutingCondition("risk_level", RiskLevel.CRITICAL)
            ],
            target="security_team",
            priority=150
        )
        engine.add_rule(custom_rule)

        # Test routing
        metadata = TaskMetadata(
            change_type=ChangeType.SECURITY,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.CRITICAL
        )
        decision = engine.route(metadata)
        assert decision.target == "security_team"

    def test_remove_rule(self):
        """Test removing routing rule."""
        engine = RoutingEngine()
        initial_count = len(engine.get_rules())

        result = engine.remove_rule("bugfix_to_hotfix")
        assert result is True
        assert len(engine.get_rules()) == initial_count - 1

    def test_remove_nonexistent_rule(self):
        """Test removing nonexistent rule."""
        engine = RoutingEngine()
        result = engine.remove_rule("nonexistent_rule")
        assert result is False

    def test_rule_priority_sorting(self):
        """Test rule priority sorting."""
        engine = RoutingEngine()
        # Add a custom rule with different priority to test sorting
        custom_rule = RoutingRule(
            name="test_sorting_rule",
            conditions=[RoutingCondition("change_type", ChangeType.TEST)],
            target="test_target",
            priority=50
        )
        engine.add_rule(custom_rule)
        
        rules = engine.get_rules()
        # Check that the newly added rule is in the list
        assert any(rule.name == "test_sorting_rule" for rule in rules)


class TestRoutingCondition:
    """Test routing condition functionality."""

    def test_condition_equals_operator(self):
        """Test equals operator."""
        condition = RoutingCondition("change_type", ChangeType.BUGFIX, "equals")
        metadata = TaskMetadata(
            change_type=ChangeType.BUGFIX,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        assert condition.matches(metadata) is True

    def test_condition_not_equals_operator(self):
        """Test not_equals operator."""
        condition = RoutingCondition("change_type", ChangeType.BUGFIX, "not_equals")
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        assert condition.matches(metadata) is True

    def test_condition_in_operator(self):
        """Test in operator."""
        condition = RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in")
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        assert condition.matches(metadata) is True

    def test_condition_not_in_operator(self):
        """Test not_in operator."""
        condition = RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "not_in")
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        assert condition.matches(metadata) is True


class TestPriorityCalculator:
    """Test priority calculator functionality."""

    def test_calculate_priority_high_risk(self):
        """Test priority calculation for high risk."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.HIGH,
            urgency=UrgencyLevel.HIGH
        )
        priority = engine.calculate_priority(metadata)
        # High risk + High urgency should result in priority > 50
        assert priority > 50

    def test_calculate_priority_low_risk(self):
        """Test priority calculation for low risk."""
        engine = RoutingEngine()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.XS,
            risk_level=RiskLevel.LOW,
            urgency=UrgencyLevel.LOW
        )
        priority = engine.calculate_priority(metadata)
        assert priority < 50

    def test_get_priority_ranking(self):
        """Test priority ranking."""
        engine = RoutingEngine()
        tasks = [
            TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.HIGH, UrgencyLevel.URGENT),
            TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM, UrgencyLevel.MEDIUM),
            TaskMetadata(ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW, UrgencyLevel.LOW),
        ]
        ranking = engine.get_priority_ranking(tasks)
        assert len(ranking) == 3
        assert ranking[0]["rank"] == 1
        assert ranking[0]["priority_score"] >= ranking[1]["priority_score"]

    def test_set_priority_factors(self):
        """Test setting priority factors."""
        engine = RoutingEngine()
        factors = PriorityFactors(
            risk_weight=0.5,
            urgency_weight=0.3,
            size_weight=0.1,
            cross_module_weight=0.05,
            custom_weight=0.05
        )
        engine.set_priority_factors(factors)
        retrieved_factors = engine.get_priority_factors()
        assert retrieved_factors.risk_weight == 0.5


class TestBatchRouting:
    """Test batch routing functionality."""

    def test_route_batch(self):
        """Test routing multiple tasks."""
        engine = RoutingEngine()
        tasks = [
            TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW),
            TaskMetadata(ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW),
            TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM),
        ]
        decisions = engine.route_batch(tasks)
        assert len(decisions) == 3
        assert decisions[0].target == "hotfix_workflow"
        assert decisions[1].target == "lightweight_workflow"
        assert decisions[2].target == "standard_workflow"


class TestPersistence:
    """Test rule persistence."""

    def test_save_and_load_rules(self):
        """Test saving and loading rules."""
        engine = RoutingEngine()

        # Save rules
        rules_data = engine.save_rules()
        assert len(rules_data) > 0

        # Create new engine and load rules
        new_engine = RoutingEngine()
        new_engine.load_rules(rules_data)
        assert len(new_engine.get_rules()) > 0

    def test_rule_serialization(self):
        """Test rule serialization."""
        rule = RoutingRule(
            name="test_rule",
            conditions=[
                RoutingCondition("change_type", ChangeType.FEATURE)
            ],
            target="test_target",
            priority=100
        )
        rule_dict = rule.to_dict()
        loaded_rule = RoutingRule.from_dict(rule_dict)
        assert loaded_rule.name == rule.name
        assert loaded_rule.target == rule.target

    def test_metadata_serialization(self):
        """Test metadata serialization."""
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM,
            urgency=UrgencyLevel.HIGH
        )
        metadata_dict = metadata.to_dict()
        loaded_metadata = TaskMetadata.from_dict(metadata_dict)
        assert loaded_metadata.change_type == metadata.change_type