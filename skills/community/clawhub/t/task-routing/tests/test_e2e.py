"""
End-to-end tests for task routing.
"""

import pytest
from src import RoutingEngine
from src.models import (
    TaskMetadata, RoutingRule, RoutingCondition, PriorityFactors,
    ChangeType, SizeLevel, RiskLevel, UrgencyLevel
)


class TestTaskRoutingE2E:
    """Test complete task routing scenarios."""

    def test_development_workflow_routing_complete(self):
        """Test complete development workflow routing."""
        engine = RoutingEngine(template="development")

        # Scenario 1: Critical security issue
        security_task = TaskMetadata(
            ChangeType.SECURITY,
            SizeLevel.M,
            RiskLevel.CRITICAL,
            UrgencyLevel.URGENT
        )
        decision = engine.route(security_task)
        assert decision.target == "standard_workflow"

        # Scenario 2: Quick documentation fix
        docs_task = TaskMetadata(
            ChangeType.DOCS,
            SizeLevel.XS,
            RiskLevel.LOW,
            UrgencyLevel.LOW
        )
        decision = engine.route(docs_task)
        assert decision.target == "lightweight_workflow"

        # Scenario 3: Bug fix
        bugfix_task = TaskMetadata(
            ChangeType.BUGFIX,
            SizeLevel.S,
            RiskLevel.MEDIUM,
            UrgencyLevel.HIGH
        )
        decision = engine.route(bugfix_task)
        assert decision.target == "hotfix_workflow"

        # Scenario 4: Large feature
        feature_task = TaskMetadata(
            ChangeType.FEATURE,
            SizeLevel.XL,
            RiskLevel.HIGH,
            UrgencyLevel.MEDIUM
        )
        decision = engine.route(feature_task)
        assert decision.target == "standard_workflow"

    def test_priority_ranking_complete_workflow(self):
        """Test complete priority ranking workflow."""
        engine = RoutingEngine()

        # Create 10 tasks with different priorities
        tasks = [
            TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.CRITICAL, UrgencyLevel.URGENT),
            TaskMetadata(ChangeType.BUGFIX, SizeLevel.S, RiskLevel.HIGH, UrgencyLevel.HIGH),
            TaskMetadata(ChangeType.HOTFIX, SizeLevel.M, RiskLevel.CRITICAL, UrgencyLevel.MEDIUM),
            TaskMetadata(ChangeType.FEATURE, SizeLevel.L, RiskLevel.HIGH, UrgencyLevel.MEDIUM),
            TaskMetadata(ChangeType.PERF, SizeLevel.M, RiskLevel.MEDIUM, UrgencyLevel.HIGH),
            TaskMetadata(ChangeType.REFACTOR, SizeLevel.L, RiskLevel.MEDIUM, UrgencyLevel.MEDIUM),
            TaskMetadata(ChangeType.TEST, SizeLevel.S, RiskLevel.MEDIUM, UrgencyLevel.LOW),
            TaskMetadata(ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW, UrgencyLevel.LOW),
            TaskMetadata(ChangeType.CONFIG, SizeLevel.S, RiskLevel.LOW, UrgencyLevel.MEDIUM),
            TaskMetadata(ChangeType.CHORE, SizeLevel.XS, RiskLevel.LOW, UrgencyLevel.LOW),
        ]

        # Get priority ranking
        ranking = engine.get_priority_ranking(tasks)

        # Verify ranking
        assert len(ranking) == 10
        assert ranking[0]["rank"] == 1
        assert ranking[9]["rank"] == 10

        # Security urgent should be highest priority
        assert ranking[0]["task"]["change_type"] == "security"

        # Docs low should be lowest priority
        assert ranking[9]["task"]["change_type"] in ["docs", "chore"]


class TestCustomRoutingE2E:
    """Test custom routing scenarios."""

    def test_custom_team_routing_complete(self):
        """Test complete custom team routing."""
        engine = RoutingEngine()

        # Add team-specific routing rules
        team_rules = [
            RoutingRule(
                name="security_to_security_team",
                conditions=[RoutingCondition("change_type", ChangeType.SECURITY)],
                target="security_team",
                priority=200
            ),
            RoutingRule(
                name="perf_to_perf_team",
                conditions=[RoutingCondition("change_type", ChangeType.PERF)],
                target="perf_team",
                priority=190
            ),
            RoutingRule(
                name="critical_to_senior_team",
                conditions=[RoutingCondition("risk_level", RiskLevel.CRITICAL)],
                target="senior_team",
                priority=195
            ),
        ]

        for rule in team_rules:
            engine.add_rule(rule)

        # Test routing
        security_task = TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.MEDIUM)
        decision = engine.route(security_task)
        assert decision.target == "security_team"

        perf_task = TaskMetadata(ChangeType.PERF, SizeLevel.M, RiskLevel.MEDIUM)
        decision = engine.route(perf_task)
        assert decision.target == "perf_team"

        # Critical task should go to senior team (highest priority for critical)
        critical_task = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.CRITICAL)
        decision = engine.route(critical_task)
        assert decision.target == "senior_team"

    def test_custom_routing_with_exclusions(self):
        """Test custom routing with exclusions."""
        engine = RoutingEngine()

        # Add exclusion rule
        exclusion_rule = RoutingRule(
            name="exclude_large_refactor_from_junior",
            conditions=[
                RoutingCondition("change_type", ChangeType.REFACTOR),
                RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "in"),
                RoutingCondition("risk_level", RiskLevel.HIGH, "not_equals")  # Exclude high risk
            ],
            target="intermediate_team",
            priority=180
        )
        engine.add_rule(exclusion_rule)

        # Test large refactor (should go to intermediate)
        large_refactor = TaskMetadata(ChangeType.REFACTOR, SizeLevel.L, RiskLevel.MEDIUM)
        decision = engine.route(large_refactor)
        assert decision.target == "intermediate_team"

        # Test large refactor with high risk (should NOT go to intermediate)
        large_refactor_high_risk = TaskMetadata(ChangeType.REFACTOR, SizeLevel.L, RiskLevel.HIGH)
        decision = engine.route(large_refactor_high_risk)
        # Should go to standard_workflow due to high risk rule
        assert decision.target == "standard_workflow"


class TestRealWorldScenariosE2E:
    """Test real-world scenarios."""

    def test_enterprise_task_routing(self):
        """Test enterprise task routing scenario."""
        engine = RoutingEngine()

        # Add enterprise-specific rules
        enterprise_rules = [
            RoutingRule(
                name="production_hotfix",
                conditions=[
                    RoutingCondition("change_type", ChangeType.HOTFIX),
                    RoutingCondition("urgency", UrgencyLevel.URGENT)
                ],
                target="production_hotfix_pipeline",
                priority=300
            ),
            RoutingRule(
                name="compliance_security",
                conditions=[
                    RoutingCondition("change_type", ChangeType.SECURITY),
                    RoutingCondition("cross_module", True)
                ],
                target="compliance_review_pipeline",
                priority=250
            ),
        ]

        for rule in enterprise_rules:
            engine.add_rule(rule)

        # Scenario 1: Production hotfix
        prod_hotfix = TaskMetadata(
            ChangeType.HOTFIX,
            SizeLevel.S,
            RiskLevel.HIGH,
            UrgencyLevel.URGENT
        )
        decision = engine.route(prod_hotfix)
        assert decision.target == "production_hotfix_pipeline"

        # Scenario 2: Cross-module security change
        cross_security = TaskMetadata(
            ChangeType.SECURITY,
            SizeLevel.M,
            RiskLevel.HIGH,
            UrgencyLevel.MEDIUM,
            cross_module=True
        )
        decision = engine.route(cross_security)
        assert decision.target == "compliance_review_pipeline"

    def test_team_capacity_routing(self):
        """Test team capacity-based routing."""
        engine = RoutingEngine()

        # Add capacity-based rules
        capacity_rules = [
            RoutingRule(
                name="small_tasks_to_junior",
                conditions=[
                    RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in"),
                    RoutingCondition("risk_level", RiskLevel.LOW)
                ],
                target="junior_team",
                priority=100
            ),
            RoutingRule(
                name="medium_tasks_to_intermediate",
                conditions=[
                    RoutingCondition("change_size", SizeLevel.M),
                    RoutingCondition("risk_level", [RiskLevel.LOW, RiskLevel.MEDIUM], "in")
                ],
                target="intermediate_team",
                priority=110
            ),
            RoutingRule(
                name="large_tasks_to_senior",
                conditions=[
                    RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "in")
                ],
                target="senior_team",
                priority=120
            ),
        ]

        for rule in capacity_rules:
            engine.add_rule(rule)

        # Test different sizes
        small_task = TaskMetadata(ChangeType.FEATURE, SizeLevel.XS, RiskLevel.LOW)
        decision = engine.route(small_task)
        assert decision.target == "junior_team"

        medium_task = TaskMetadata(ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM)
        decision = engine.route(medium_task)
        assert decision.target == "intermediate_team"

        large_task = TaskMetadata(ChangeType.FEATURE, SizeLevel.L, RiskLevel.MEDIUM)
        decision = engine.route(large_task)
        assert decision.target == "senior_team"


class TestRoutingPerformanceE2E:
    """Test routing performance."""

    def test_large_batch_routing(self):
        """Test large batch routing."""
        engine = RoutingEngine()

        # Create 100 tasks
        tasks = [
            TaskMetadata(
                ChangeType.FEATURE if i % 3 == 0 else (ChangeType.BUGFIX if i % 3 == 1 else ChangeType.DOCS),
                SizeLevel.M,
                RiskLevel.MEDIUM
            )
            for i in range(100)
        ]

        # Route all
        decisions = engine.route_batch(tasks)
        assert len(decisions) == 100

        # All should have valid targets
        assert all(decision.target is not None for decision in decisions)

    def test_large_priority_ranking(self):
        """Test large priority ranking."""
        engine = RoutingEngine()

        # Create 50 tasks
        tasks = [
            TaskMetadata(
                ChangeType.FEATURE,
                SizeLevel.M,
                RiskLevel.LOW if i < 25 else (RiskLevel.MEDIUM if i < 40 else RiskLevel.HIGH),
                UrgencyLevel.MEDIUM
            )
            for i in range(50)
        ]

        # Get ranking
        ranking = engine.get_priority_ranking(tasks)
        assert len(ranking) == 50

        # Verify ranking order
        priorities = [r["priority_score"] for r in ranking]
        assert priorities == sorted(priorities, reverse=True)


class TestRoutingPersistenceE2E:
    """Test routing persistence end-to-end."""

    def test_full_persistence_workflow(self):
        """Test full persistence workflow."""
        engine = RoutingEngine()

        # Add custom rules with high priority
        custom_rules = [
            RoutingRule(
                name="custom_rule1",
                conditions=[RoutingCondition("change_type", ChangeType.SECURITY)],
                target="security_pipeline",
                priority=300  # High priority
            ),
            RoutingRule(
                name="custom_rule2",
                conditions=[RoutingCondition("change_type", ChangeType.PERF)],
                target="perf_pipeline",
                priority=290  # High priority
            ),
        ]

        for rule in custom_rules:
            engine.add_rule(rule)

        # Save rules
        rules_data = engine.save_rules()

        # Create new engine and load
        new_engine = RoutingEngine()
        new_engine.load_rules(rules_data)

        # Test routing in new engine
        security_task = TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.MEDIUM)
        decision = new_engine.route(security_task)
        assert decision.target == "security_pipeline"

        perf_task = TaskMetadata(ChangeType.PERF, SizeLevel.M, RiskLevel.MEDIUM)
        decision = new_engine.route(perf_task)
        assert decision.target == "perf_pipeline"

    def test_persistence_with_priority_factors(self):
        """Test persistence with priority factors."""
        engine = RoutingEngine()

        # Set custom factors
        factors = PriorityFactors(
            risk_weight=0.5,
            urgency_weight=0.3,
            size_weight=0.1,
            cross_module_weight=0.05,
            custom_weight=0.05
        )
        engine.set_priority_factors(factors)

        # Calculate priority
        metadata = TaskMetadata(ChangeType.SECURITY, SizeLevel.M, RiskLevel.CRITICAL)
        priority1 = engine.calculate_priority(metadata)

        # Get factors and create new engine
        saved_factors = engine.get_priority_factors()
        new_engine = RoutingEngine()
        new_engine.set_priority_factors(saved_factors)

        # Verify same priority calculation
        priority2 = new_engine.calculate_priority(metadata)
        assert priority1 == priority2