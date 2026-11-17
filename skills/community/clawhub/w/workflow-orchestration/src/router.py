"""
Task router for routing tasks to workflows.
"""

from typing import Dict
from .models import TaskMetadata, ChangeType, SizeLevel, RiskLevel


class TaskRouter:
    """Task router for routing tasks to appropriate workflows."""

    def __init__(self):
        self._routing_rules = self._build_default_rules()

    def _build_default_rules(self) -> Dict:
        """Build default routing rules."""
        return {
            "bugfix_to_hotfix": {
                "change_types": [ChangeType.BUGFIX, ChangeType.HOTFIX],
                "workflow": "hotfix"
            },
            "low_risk_small_to_lightweight": {
                "change_types": [ChangeType.DOCS, ChangeType.CONFIG, ChangeType.PROMPT, ChangeType.CHORE],
                "max_size": SizeLevel.S,
                "max_risk": RiskLevel.LOW,
                "workflow": "lightweight"
            },
            "high_risk_force_standard": {
                "min_risk": RiskLevel.HIGH,
                "workflow": "standard"
            },
            "large_size_force_standard": {
                "min_size": SizeLevel.L,
                "workflow": "standard"
            },
            "feature_to_standard": {
                "change_types": [ChangeType.FEATURE, ChangeType.REFACTOR, ChangeType.PERF, ChangeType.SECURITY, ChangeType.MIGRATION],
                "workflow": "standard"
            },
            "default": {
                "workflow": "standard"
            }
        }

    def route_task(self, metadata: TaskMetadata) -> str:
        """Route a task to appropriate workflow."""
        # Check bugfix/hotfix routing
        if metadata.change_type in [ChangeType.BUGFIX, ChangeType.HOTFIX]:
            return "hotfix"

        # Check low-risk small routing
        if metadata.change_type in [ChangeType.DOCS, ChangeType.CONFIG, ChangeType.PROMPT, ChangeType.CHORE]:
            if metadata.change_size in [SizeLevel.XS, SizeLevel.S] and metadata.risk_level == RiskLevel.LOW:
                return "lightweight"

        # Check high-risk routing
        if metadata.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return "standard"

        # Check large-size routing
        if metadata.change_size in [SizeLevel.L, SizeLevel.XL]:
            return "standard"

        # Check feature/refactor routing
        if metadata.change_type in [ChangeType.FEATURE, ChangeType.REFACTOR, ChangeType.PERF, ChangeType.SECURITY, ChangeType.MIGRATION]:
            return "standard"

        # Default routing
        return "standard"

    def add_routing_rule(self, rule_name: str, rule: Dict) -> None:
        """Add a routing rule."""
        self._routing_rules[rule_name] = rule

    def get_routing_rules(self) -> Dict:
        """Get all routing rules."""
        return self._routing_rules