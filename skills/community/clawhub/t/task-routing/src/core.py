"""
Main routing engine orchestrator.
"""

from typing import Dict, List, Optional
from .models import TaskMetadata, RoutingRule, RoutingDecision, PriorityFactors
from .engine import RoutingExecutor
from .priority import PriorityCalculator


class RoutingEngine:
    """Main routing engine orchestrator."""

    def __init__(self, template: str = "development"):
        self.executor = RoutingExecutor()
        self.calculator = PriorityCalculator()
        self._template = template

    def route(self, task_metadata: TaskMetadata) -> RoutingDecision:
        """Route a task to target."""
        return self.executor.execute_routing(task_metadata)

    def route_batch(self, tasks: List[TaskMetadata]) -> List[RoutingDecision]:
        """Route multiple tasks."""
        return [self.route(task) for task in tasks]

    def add_rule(self, rule: RoutingRule) -> None:
        """Add a routing rule."""
        self.executor.add_rule(rule)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove a routing rule."""
        return self.executor.remove_rule(rule_name)

    def get_rules(self) -> List[RoutingRule]:
        """Get all routing rules."""
        return self.executor.get_rules()

    def calculate_priority(self, task_metadata: TaskMetadata) -> float:
        """Calculate task priority."""
        return self.calculator.calculate_priority(task_metadata)

    def get_priority_ranking(self, tasks: List[TaskMetadata]) -> List[Dict]:
        """Get priority ranking for tasks."""
        return self.calculator.get_priority_ranking(tasks)

    def set_priority_factors(self, factors: PriorityFactors) -> None:
        """Set priority calculation factors."""
        self.calculator.set_factors(factors)

    def get_priority_factors(self) -> PriorityFactors:
        """Get priority calculation factors."""
        return self.calculator.get_factors()

    def save_rules(self) -> List[Dict]:
        """Save rules to list of dicts."""
        return [rule.to_dict() for rule in self.executor.get_rules()]

    def load_rules(self, rules_data: List[Dict]) -> None:
        """Load rules from list of dicts."""
        # Clear existing rules first
        self.executor._rules = []
        
        for rule_dict in rules_data:
            rule = RoutingRule.from_dict(rule_dict)
            self.executor.add_rule(rule)