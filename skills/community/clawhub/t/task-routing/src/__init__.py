"""
Task Routing Skill
A lightweight task routing engine for intelligent task assignment and prioritization.
"""

from .core import RoutingEngine, RoutingDecision
from .models import TaskMetadata, RoutingRule, RoutingCondition, PriorityFactors
from .engine import RoutingExecutor
from .priority import PriorityCalculator

__version__ = "1.0.0"
__all__ = [
    "RoutingEngine",
    "RoutingDecision",
    "TaskMetadata",
    "RoutingRule",
    "RoutingCondition",
    "PriorityFactors",
    "RoutingExecutor",
    "PriorityCalculator",
]