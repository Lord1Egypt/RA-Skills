#!/usr/bin/env python3
"""
Priority Evaluator - Judgment Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Task priority calculation.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import math

class TaskType(Enum):
    SYSTEM_MAINTENANCE = "system_maintenance"
    USER_REQUEST = "user_request"
    SKILL_INSTALLATION = "skill_installation"
    ERROR_HANDLING = "error_handling"
    MONITORING = "monitoring"
    OPTIMIZATION = "optimization"
    COMMUNICATION = "communication"

class PriorityLevel(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    BACKGROUND = 1

@dataclass
class Task:
    """Represents a task to be prioritized."""
    id: str
    name: str
    task_type: TaskType
    description: str
    urgency: float  # 0.0 to 1.0
    importance: float  # 0.0 to 1.0
    user_relevance: float  # 0.0 to 1.0
    resource_cost: float  # 0.0 to 1.0
    estimated_duration: float  # in minutes
    dependencies: List[str]
    created_at: datetime
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = None

class PriorityEvaluator:
    """Advanced priority evaluation system for autonomous decision making."""

    def __init__(self):
        # Default priority factors (can be customized)
        self.priority_factors = {
            'urgency': 0.4,
            'importance': 0.3,
            'user_relevance': 0.2,
            'resource_cost': 0.1
        }

        # Task type modifiers
        self.task_type_modifiers = {
            TaskType.ERROR_HANDLING: 1.5,
            TaskType.SYSTEM_MAINTENANCE: 1.2,
            TaskType.USER_REQUEST: 1.3,
            TaskType.SKILL_INSTALLATION: 1.1,
            TaskType.MONITORING: 0.9,
            TaskType.OPTIMIZATION: 0.8,
            TaskType.COMMUNICATION: 1.0
        }

        # Time-based urgency modifiers
        self.urgency_time_thresholds = {
            'immediate': timedelta(minutes=5),
            'soon': timedelta(hours=1),
            'today': timedelta(hours=8),
            'this_week': timedelta(days=7)
        }

        # Historical performance data
        self.performance_history = {}
        self.user_preferences = {}

    def calculate_priority_score(self, task: Task) -> float:
        """Calculate comprehensive priority score for a task."""

        # Base priority calculation
        base_score = (
            task.urgency * self.priority_factors['urgency'] +
            task.importance * self.priority_factors['importance'] +
            task.user_relevance * self.priority_factors['user_relevance'] +
            (1 - task.resource_cost) * self.priority_factors['resource_cost']
        )

        # Apply task type modifier
        type_modifier = self.task_type_modifiers.get(task.task_type, 1.0)
        modified_score = base_score * type_modifier

        # Apply time-based urgency boost
        time_modifier = self._calculate_time_modifier(task)
        time_adjusted_score = modified_score * time_modifier

        # Apply deadline pressure
        deadline_modifier = self._calculate_deadline_modifier(task)
        final_score = time_adjusted_score * deadline_modifier

        # Apply learning-based adjustments
        learning_modifier = self._calculate_learning_modifier(task)
        final_score *= learning_modifier

        return min(final_score, 1.0)  # Cap at 1.0

    def _calculate_time_modifier(self, task: Task) -> float:
        """Calculate time-based urgency modifier."""
        now = datetime.now()
        time_since_creation = now - task.created_at

        # More recent tasks get a slight boost
        if time_since_creation < timedelta(minutes=5):
            return 1.2
        elif time_since_creation < timedelta(hours=1):
            return 1.1
        elif time_since_creation < timedelta(hours=8):
            return 1.0
        else:
            return 0.9

    def _calculate_deadline_modifier(self, task: Task) -> float:
        """Calculate deadline pressure modifier."""
        if not task.deadline:
            return 1.0

        time_to_deadline = task.deadline - datetime.now()

        if time_to_deadline < timedelta(minutes=30):
            return 2.0  # Critical deadline
        elif time_to_deadline < timedelta(hours=2):
            return 1.5  # Urgent deadline
        elif time_to_deadline < timedelta(hours=24):
            return 1.2  # Soon deadline
        else:
            return 1.0  # No immediate pressure

    def _calculate_learning_modifier(self, task: Task) -> float:
        """Calculate modifier based on learned patterns."""
        modifier = 1.0

        # Check if similar tasks were successful in the past
        if task.task_type.value in self.performance_history:
            success_rate = self.performance_history[task.task_type.value].get('success_rate', 0.5)
            if success_rate > 0.8:
                modifier *= 1.1  # Boost for historically successful task types
            elif success_rate < 0.3:
                modifier *= 0.9  # Reduce for historically problematic task types

        # Apply user preferences
        if task.task_type.value in self.user_preferences:
            preference = self.user_preferences[task.task_type.value]
            modifier *= preference

        return modifier

    def determine_priority_level(self, score: float) -> PriorityLevel:
        """Convert priority score to priority level."""
        if score >= 0.8:
            return PriorityLevel.CRITICAL
        elif score >= 0.6:
            return PriorityLevel.HIGH
        elif score >= 0.4:
            return PriorityLevel.MEDIUM
        elif score >= 0.2:
            return PriorityLevel.LOW
        else:
            return PriorityLevel.BACKGROUND

    def prioritize_task_list(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority score."""
        task_scores = []

        for task in tasks:
            score = self.calculate_priority_score(task)
            priority_level = self.determine_priority_level(score)
            task_scores.append((task, score, priority_level))

        # Sort by score (descending)
        task_scores.sort(key=lambda x: x[1], reverse=True)

        # Update tasks with priority information
        for task, score, level in task_scores:
            if not hasattr(task, 'priority_score'):
                task.priority_score = score
            if not hasattr(task, 'priority_level'):
                task.priority_level = level

        return [task for task, _, _ in task_scores]

    def get_execution_recommendation(self, task: Task) -> Dict[str, Any]:
        """Get execution recommendation based on priority analysis."""
        score = self.calculate_priority_score(task)
        level = self.determine_priority_level(score)

        recommendation = {
            'task_id': task.id,
            'priority_score': score,
            'priority_level': level.value,
            'recommendation': self._get_recommendation_action(level),
            'estimated_impact': self._estimate_impact(task),
            'resource_requirement': self._assess_resource_requirement(task),
            'execution_timing': self._suggest_execution_timing(task)
        }

        return recommendation

    def _get_recommendation_action(self, level: PriorityLevel) -> str:
        """Get recommended action based on priority level."""
        actions = {
            PriorityLevel.CRITICAL: "execute_immediately",
            PriorityLevel.HIGH: "execute_soon",
            PriorityLevel.MEDIUM: "schedule_execution",
            PriorityLevel.LOW: "queue_for_later",
            PriorityLevel.BACKGROUND: "execute_when_idle"
        }
        return actions.get(level, "schedule_execution")

    def _estimate_impact(self, task: Task) -> Dict[str, float]:
        """Estimate the impact of executing this task."""
        return {
            'user_satisfaction': task.user_relevance * task.importance,
            'system_improvement': task.importance * (1 - task.resource_cost),
            'urgency_resolution': task.urgency,
            'resource_efficiency': 1 - task.resource_cost
        }

    def _assess_resource_requirement(self, task: Task) -> str:
        """Assess resource requirements for the task."""
        if task.resource_cost > 0.8:
            return "high"
        elif task.resource_cost > 0.5:
            return "medium"
        else:
            return "low"

    def _suggest_execution_timing(self, task: Task) -> str:
        """Suggest optimal execution timing."""
        if task.deadline:
            time_to_deadline = task.deadline - datetime.now()
            if time_to_deadline < timedelta(hours=1):
                return "immediate"
            elif time_to_deadline < timedelta(hours=4):
                return "within_4_hours"
            else:
                return "before_deadline"
        else:
            score = self.calculate_priority_score(task)
            if score > 0.7:
                return "as_soon_as_possible"
            elif score > 0.4:
                return "during_next_window"
            else:
                return "when_resources_available"

    def update_performance_history(self, task: Task, success: bool, execution_time: float):
        """Update performance history for learning."""
        task_type = task.task_type.value

        if task_type not in self.performance_history:
            self.performance_history[task_type] = {
                'total_executions': 0,
                'successful_executions': 0,
                'success_rate': 0.0,
                'average_execution_time': 0.0
            }

        history = self.performance_history[task_type]
        history['total_executions'] += 1

        if success:
            history['successful_executions'] += 1

        history['success_rate'] = history['successful_executions'] / history['total_executions']

        # Update average execution time
        current_avg = history['average_execution_time']
        new_count = history['total_executions']
        history['average_execution_time'] = ((current_avg * (new_count - 1)) + execution_time) / new_count

    def set_user_preference(self, task_type: TaskType, preference_score: float):
        """Set user preference for a task type (0.5 to 1.5)."""
        self.user_preferences[task_type.value] = max(0.5, min(1.5, preference_score))

    def get_priority_statistics(self) -> Dict[str, Any]:
        """Get statistics about priority evaluations."""
        total_tasks = sum(h['total_executions'] for h in self.performance_history.values())

        return {
            'total_tasks_evaluated': total_tasks,
            'task_type_performance': self.performance_history,
            'user_preferences': self.user_preferences,
            'priority_factors': self.priority_factors
        }

def demo_priority_evaluation():
    """Demonstrate the priority evaluation system."""
    evaluator = PriorityEvaluator()

    # Create sample tasks
    tasks = [
        Task(
            id="task_1",
            name="Fix critical system error",
            task_type=TaskType.ERROR_HANDLING,
            description="System is experiencing high memory usage",
            urgency=0.9,
            importance=0.8,
            user_relevance=0.7,
            resource_cost=0.3,
            estimated_duration=15,
            dependencies=[],
            created_at=datetime.now() - timedelta(minutes=10),
            deadline=datetime.now() + timedelta(minutes=30)
        ),
        Task(
            id="task_2",
            name="Install new skill",
            task_type=TaskType.SKILL_INSTALLATION,
            description="User requested installation of document processing skill",
            urgency=0.4,
            importance=0.6,
            user_relevance=0.8,
            resource_cost=0.2,
            estimated_duration=10,
            dependencies=[],
            created_at=datetime.now() - timedelta(hours=2)
        ),
        Task(
            id="task_3",
            name="System monitoring",
            task_type=TaskType.MONITORING,
            description="Regular system health check",
            urgency=0.3,
            importance=0.5,
            user_relevance=0.4,
            resource_cost=0.1,
            estimated_duration=5,
            dependencies=[],
            created_at=datetime.now() - timedelta(hours=6)
        )
    ]

    print("Priority Evaluation Demo")
    print("=" * 50)

    # Evaluate each task
    for task in tasks:
        recommendation = evaluator.get_execution_recommendation(task)
        print(f"\nTask: {task.name}")
        print(f"Priority Score: {recommendation['priority_score']:.3f}")
        print(f"Priority Level: {PriorityLevel(recommendation['priority_level']).name}")
        print(f"Recommendation: {recommendation['recommendation']}")
        print(f"Execution Timing: {recommendation['execution_timing']}")
        print(f"Resource Requirement: {recommendation['resource_requirement']}")

    # Sort tasks by priority
    print("\n" + "=" * 50)
    print("Task Priority Ranking:")
    print("=" * 50)

    prioritized_tasks = evaluator.prioritize_task_list(tasks)
    for i, task in enumerate(prioritized_tasks, 1):
        print(f"{i}. {task.name} (Score: {task.priority_score:.3f}, Level: {task.priority_level.name})")

if __name__ == "__main__":
    demo_priority_evaluation()
