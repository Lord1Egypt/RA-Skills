"""
Priority calculator for task ranking.
"""

from typing import Dict, List
from .models import TaskMetadata, PriorityFactors, RiskLevel, UrgencyLevel, SizeLevel


class PriorityCalculator:
    """Priority calculator for task prioritization."""

    def __init__(self, factors: PriorityFactors = None):
        self.factors = factors or PriorityFactors()

    def calculate_priority(self, task_metadata: TaskMetadata) -> float:
        """Calculate priority score (0-100)."""
        # Risk score
        risk_scores = {
            RiskLevel.LOW: 20,
            RiskLevel.MEDIUM: 50,
            RiskLevel.HIGH: 80,
            RiskLevel.CRITICAL: 100
        }
        risk_score = risk_scores[task_metadata.risk_level]

        # Urgency score
        urgency_scores = {
            UrgencyLevel.LOW: 20,
            UrgencyLevel.MEDIUM: 50,
            UrgencyLevel.HIGH: 80,
            UrgencyLevel.URGENT: 100
        }
        urgency_score = urgency_scores[task_metadata.urgency]

        # Size score (inverse - smaller tasks get higher priority for quick completion)
        size_scores = {
            SizeLevel.XS: 100,
            SizeLevel.S: 80,
            SizeLevel.M: 60,
            SizeLevel.L: 40,
            SizeLevel.XL: 20
        }
        size_score = size_scores[task_metadata.change_size]

        # Cross-module score
        cross_module_score = 80 if task_metadata.cross_module else 20

        # Calculate weighted priority
        priority = (
            risk_score * self.factors.risk_weight +
            urgency_score * self.factors.urgency_weight +
            size_score * self.factors.size_weight +
            cross_module_score * self.factors.cross_module_weight
        )

        return min(100, max(0, priority))

    def get_priority_ranking(self, tasks: List[TaskMetadata]) -> List[Dict]:
        """Get priority ranking for multiple tasks."""
        ranked_tasks = []

        for task in tasks:
            priority_score = self.calculate_priority(task)
            ranked_tasks.append({
                "task": task.to_dict(),
                "priority_score": priority_score,
                "rank": 0  # Will be set after sorting
            })

        # Sort by priority score (descending)
        ranked_tasks.sort(key=lambda x: x["priority_score"], reverse=True)

        # Set ranks
        for i, task in enumerate(ranked_tasks):
            task["rank"] = i + 1

        return ranked_tasks

    def set_factors(self, factors: PriorityFactors) -> None:
        """Set priority factors."""
        self.factors = factors

    def get_factors(self) -> PriorityFactors:
        """Get priority factors."""
        return self.factors