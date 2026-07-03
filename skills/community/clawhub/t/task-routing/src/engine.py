"""
Routing engine implementation.
"""

from typing import Dict, List, Optional
from .models import TaskMetadata, RoutingRule, RoutingCondition, RoutingDecision


class RoutingExecutor:
    """Routing executor for executing routing rules."""

    def __init__(self):
        self._rules: List[RoutingRule] = []
        self._load_default_rules()

    def _load_default_rules(self):
        """Load default routing rules."""
        from .models import ChangeType, SizeLevel, RiskLevel

        # Development workflow routing rules
        default_rules = [
            RoutingRule(
                name="bugfix_to_hotfix",
                conditions=[
                    RoutingCondition("change_type", ChangeType.BUGFIX),
                ],
                target="hotfix_workflow",
                priority=100
            ),
            RoutingRule(
                name="hotfix_to_hotfix",
                conditions=[
                    RoutingCondition("change_type", ChangeType.HOTFIX),
                ],
                target="hotfix_workflow",
                priority=100
            ),
            RoutingRule(
                name="docs_small_low_risk_to_lightweight",
                conditions=[
                    RoutingCondition("change_type", ChangeType.DOCS),
                    RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in"),
                    RoutingCondition("risk_level", RiskLevel.LOW),
                ],
                target="lightweight_workflow",
                priority=90
            ),
            RoutingRule(
                name="config_small_low_risk_to_lightweight",
                conditions=[
                    RoutingCondition("change_type", ChangeType.CONFIG),
                    RoutingCondition("change_size", [SizeLevel.XS, SizeLevel.S], "in"),
                    RoutingCondition("risk_level", RiskLevel.LOW),
                ],
                target="lightweight_workflow",
                priority=90
            ),
            RoutingRule(
                name="high_risk_to_standard",
                conditions=[
                    RoutingCondition("risk_level", [RiskLevel.HIGH, RiskLevel.CRITICAL], "in"),
                ],
                target="standard_workflow",
                priority=95
            ),
            RoutingRule(
                name="large_size_to_standard",
                conditions=[
                    RoutingCondition("change_size", [SizeLevel.L, SizeLevel.XL], "in"),
                ],
                target="standard_workflow",
                priority=85
            ),
            RoutingRule(
                name="feature_to_standard",
                conditions=[
                    RoutingCondition("change_type", [ChangeType.FEATURE, ChangeType.REFACTOR, ChangeType.PERF, ChangeType.SECURITY, ChangeType.MIGRATION], "in"),
                ],
                target="standard_workflow",
                priority=80
            ),
            RoutingRule(
                name="default_to_standard",
                conditions=[],
                target="standard_workflow",
                priority=1
            ),
        ]

        self._rules = default_rules

    def add_rule(self, rule: RoutingRule) -> None:
        """Add a routing rule."""
        self._rules.append(rule)
        # Sort by priority (highest first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove a routing rule."""
        for i, rule in enumerate(self._rules):
            if rule.name == rule_name:
                self._rules.pop(i)
                return True
        return False

    def get_rules(self) -> List[RoutingRule]:
        """Get all routing rules."""
        return self._rules

    def execute_routing(self, task_metadata: TaskMetadata) -> RoutingDecision:
        """Execute routing logic."""
        matched_rules = []
        alternatives = []

        for rule in self._rules:
            if not rule.enabled:
                continue

            if rule.matches(task_metadata):
                matched_rules.append(rule)
            elif rule.conditions:  # Has conditions but doesn't fully match
                # Partial match for alternatives
                partial_matches = sum(1 for cond in rule.conditions if cond.matches(task_metadata))
                if partial_matches > 0:
                    alternatives.append((rule.target, partial_matches / len(rule.conditions)))

        if matched_rules:
            # Return highest priority match
            best_match = matched_rules[0]
            confidence = best_match.confidence_weight

            return RoutingDecision(
                target=best_match.target,
                matched_rule=best_match.name,
                confidence=confidence,
                alternatives=[alt[0] for alt in sorted(alternatives, key=lambda x: x[1], reverse=True)[:3]],
                metadata={"total_matches": len(matched_rules)}
            )

        # Return default
        return RoutingDecision(
            target="standard_workflow",
            matched_rule="default",
            confidence=0.5,
            alternatives=[],
            metadata={}
        )