#!/usr/bin/env python3
"""
Pattern Recognizer - Reflection Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Pattern detection and analysis.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
import uuid
from collections import defaultdict, Counter

class PatternType(Enum):
    FREQUENCY = "frequency"
    TEMPORAL = "temporal"
    PERFORMANCE = "performance"
    ERROR = "error"
    RESOURCE = "resource"
    USER_BEHAVIOR = "user_behavior"
    SKILL_INTERACTION = "skill_interaction"

@dataclass
class Pattern:
    """Represents a discovered pattern."""
    pattern_id: str
    pattern_type: PatternType
    name: str
    description: str
    confidence: float
    frequency: int
    first_observed: datetime
    last_observed: datetime
    data_points: List[Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    actionable: bool = True

class PatternRecognizer:
    """Advanced pattern recognition system for autonomous learning."""

    def __init__(self):
        self.pattern_database = {}
        self.recognition_threshold = 0.6
        self.min_frequency = 3
        self.max_pattern_age = timedelta(days=30)

    def identify_patterns(self, task_history: List[Dict]) -> List[Pattern]:
        """Identify patterns from task execution history."""
        patterns = []

        # Frequency analysis
        frequency_patterns = self._analyze_frequency(task_history)
        patterns.extend(frequency_patterns)

        # Temporal analysis
        temporal_patterns = self._analyze_temporal(task_history)
        patterns.extend(temporal_patterns)

        # Performance analysis
        performance_patterns = self._analyze_performance(task_history)
        patterns.extend(performance_patterns)

        # Error analysis
        error_patterns = self._analyze_errors(task_history)
        patterns.extend(error_patterns)

        # Filter and rank patterns
        filtered_patterns = self._filter_patterns(patterns)
        ranked_patterns = self._rank_patterns(filtered_patterns)

        return ranked_patterns

    def _analyze_frequency(self, task_history: List[Dict]) -> List[Pattern]:
        """Analyze frequency-based patterns."""
        patterns = []

        # Group tasks by type
        task_types = defaultdict(list)
        for task in task_history:
            task_type = task.get('task_type', 'unknown')
            task_types[task_type].append(task)

        # Find frequent task patterns
        for task_type, tasks in task_types.items():
            if len(tasks) >= 3:
                frequency = len(tasks)
                avg_interval = self._calculate_average_interval(tasks)

                patterns.append(Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.FREQUENCY,
                    name=f"Frequent {task_type} tasks",
                    description=f"{task_type} tasks occur {frequency} times with average interval of {avg_interval:.1f} hours",
                    confidence=min(0.9, frequency / 10.0),
                    frequency=frequency,
                    first_observed=min(task['timestamp'] for task in tasks),
                    last_observed=max(task['timestamp'] for task in tasks),
                    data_points=[task['timestamp'] for task in tasks],
                    metadata={'task_type': task_type, 'avg_interval_hours': avg_interval}
                ))

        return patterns

    def _analyze_temporal(self, task_history: List[Dict]) -> List[Pattern]:
        """Analyze time-based patterns."""
        patterns = []

        # Extract temporal features
        hourly_distribution = defaultdict(int)
        weekly_distribution = defaultdict(int)

        for task in task_history:
            timestamp = task['timestamp']
            hourly_distribution[timestamp.hour] += 1
            weekly_distribution[timestamp.weekday()] += 1

        # Find peak activity hours
        peak_hours = [hour for hour, count in hourly_distribution.items()
                     if count >= 5 and count == max(hourly_distribution.values())]

        if peak_hours:
            patterns.append(Pattern(
                pattern_id=str(uuid.uuid4()),
                pattern_type=PatternType.TEMPORAL,
                name="Peak Activity Hours",
                description=f"Highest activity during hours: {', '.join(map(str, peak_hours))}",
                confidence=0.8,
                frequency=max(hourly_distribution.values()),
                first_observed=min(task['timestamp'] for task in task_history),
                last_observed=max(task['timestamp'] for task in task_history),
                data_points=list(hourly_distribution.items()),
                metadata={'peak_hours': peak_hours}
            ))

        return patterns

    def _analyze_performance(self, task_history: List[Dict]) -> List[Pattern]:
        """Analyze performance-related patterns."""
        patterns = []

        # Analyze execution time trends
        execution_times = []
        for task in task_history:
            if 'execution_time' in task and task['execution_time'] is not None:
                execution_times.append((task['timestamp'], task['execution_time']))

        if len(execution_times) >= 5:
            times = [et[1] for et in execution_times]
            trend = self._calculate_trend(times)

            if trend > 0.1:  # Increasing trend
                patterns.append(Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.PERFORMANCE,
                    name="Performance Degradation",
                    description=f"Execution time increasing by {trend*100:.1f}% over time",
                    confidence=0.8,
                    frequency=len(execution_times),
                    first_observed=execution_times[0][0],
                    last_observed=execution_times[-1][0],
                    data_points=execution_times,
                    metadata={'trend_percentage': trend * 100}
                ))

        return patterns

    def _analyze_errors(self, task_history: List[Dict]) -> List[Pattern]:
        """Analyze error patterns."""
        patterns = []

        # Group errors by type
        error_types = defaultdict(list)
        for task in task_history:
            if 'errors' in task and task['errors']:
                for error in task['errors']:
                    error_type = self._categorize_error(error)
                    error_types[error_type].append((task['timestamp'], error))

        # Find frequent error patterns
        for error_type, errors in error_types.items():
            if len(errors) >= 3:
                frequency = len(errors)
                error_rate = frequency / len(task_history)

                patterns.append(Pattern(
                    pattern_id=str(uuid.uuid4()),
                    pattern_type=PatternType.ERROR,
                    name=f"Frequent {error_type} Errors",
                    description=f"{error_type} errors occur {frequency} times ({error_rate*100:.1f}% error rate)",
                    confidence=min(0.95, error_rate * 2),
                    frequency=frequency,
                    first_observed=errors[0][0],
                    last_observed=errors[-1][0],
                    data_points=errors,
                    metadata={'error_type': error_type, 'error_rate': error_rate}
                ))

        return patterns

    def _calculate_average_interval(self, tasks: List[Dict]) -> float:
        """Calculate average time interval between tasks."""
        if len(tasks) < 2:
            return 0.0

        intervals = []
        sorted_tasks = sorted(tasks, key=lambda t: t['timestamp'])

        for i in range(1, len(sorted_tasks)):
            interval = (sorted_tasks[i]['timestamp'] - sorted_tasks[i-1]['timestamp']).total_seconds() / 3600
            intervals.append(interval)

        return statistics.mean(intervals) if intervals else 0.0

    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate linear trend of values."""
        if len(values) < 2:
            return 0.0

        n = len(values)
        x_values = list(range(n))

        # Simple linear regression
        sum_x = sum(x_values)
        sum_y = sum(values)
        sum_xy = sum(x * y for x, y in zip(x_values, values))
        sum_x2 = sum(x * x for x in x_values)

        denominator = n * sum_x2 - sum_x * sum_x
        if denominator == 0:
            return 0.0

        slope = (n * sum_xy - sum_x * sum_y) / denominator

        # Return relative trend (slope / mean)
        mean_value = statistics.mean(values)
        return slope / mean_value if mean_value != 0 else 0.0

    def _categorize_error(self, error: str) -> str:
        """Categorize error by type."""
        error_lower = error.lower()

        if any(keyword in error_lower for keyword in ['network', 'connection', 'timeout']):
            return 'network'
        elif any(keyword in error_lower for keyword in ['permission', 'access', 'denied']):
            return 'permission'
        elif any(keyword in error_lower for keyword in ['memory', 'cpu', 'disk']):
            return 'resource'
        elif any(keyword in error_lower for keyword in ['validation', 'format', 'invalid']):
            return 'validation'
        else:
            return 'general'

    def _filter_patterns(self, patterns: List[Pattern]) -> List[Pattern]:
        """Filter patterns based on confidence and frequency thresholds."""
        filtered = []

        for pattern in patterns:
            if pattern.confidence < self.recognition_threshold:
                continue
            if pattern.frequency < self.min_frequency:
                continue
            if datetime.now() - pattern.last_observed > self.max_pattern_age:
                continue
            filtered.append(pattern)

        return filtered

    def _rank_patterns(self, patterns: List[Pattern]) -> List[Pattern]:
        """Rank patterns by importance and actionability."""
        return sorted(patterns, key=lambda p: (
            p.confidence,
            p.frequency,
            -((datetime.now() - p.last_observed).total_seconds())
        ), reverse=True)

    def generate_optimization_suggestions(self, patterns: List[Pattern]) -> List[Dict]:
        """Generate optimization suggestions based on discovered patterns."""
        suggestions = []

        for pattern in patterns:
            if not pattern.actionable:
                continue

            suggestion = {
                'pattern_id': pattern.pattern_id,
                'pattern_name': pattern.name,
                'suggestion_type': self._determine_suggestion_type(pattern),
                'description': self._generate_suggestion_description(pattern),
                'priority': self._calculate_priority(pattern),
                'implementation_effort': self._estimate_effort(pattern),
                'expected_benefit': self._estimate_benefit(pattern)
            }

            suggestions.append(suggestion)

        return sorted(suggestions, key=lambda s: s['priority'], reverse=True)

    def _determine_suggestion_type(self, pattern: Pattern) -> str:
        """Determine the type of optimization suggestion."""
        type_mapping = {
            PatternType.ERROR: 'error_prevention',
            PatternType.PERFORMANCE: 'performance_optimization',
            PatternType.RESOURCE: 'resource_management',
            PatternType.USER_BEHAVIOR: 'workflow_optimization',
            PatternType.SKILL_INTERACTION: 'integration_opportunity',
            PatternType.TEMPORAL: 'scheduling_optimization'
        }
        return type_mapping.get(pattern.pattern_type, 'general_optimization')

    def _generate_suggestion_description(self, pattern: Pattern) -> str:
        """Generate a human-readable description of the optimization suggestion."""
        if pattern.pattern_type == PatternType.ERROR:
            return f"Address recurring {pattern.name} errors to improve system reliability"
        elif pattern.pattern_type == PatternType.PERFORMANCE:
            return f"Optimize {pattern.name} to enhance system performance"
        elif pattern.pattern_type == PatternType.RESOURCE:
            return f"Manage {pattern.name} to improve resource efficiency"
        elif pattern.pattern_type == PatternType.USER_BEHAVIOR:
            return f"Streamline {pattern.name} workflow based on usage patterns"
        elif pattern.pattern_type == PatternType.SKILL_INTERACTION:
            return f"Integrate skills involved in {pattern.name} for better efficiency"
        else:
            return f"Optimize {pattern.name} based on observed patterns"

    def _calculate_priority(self, pattern: Pattern) -> float:
        """Calculate priority score for the pattern."""
        base_score = pattern.confidence * 0.4
        frequency_score = min(pattern.frequency / 10.0, 1.0) * 0.3
        recency_score = (1 - min((datetime.now() - pattern.last_observed).days / 30.0, 1.0)) * 0.3

        return base_score + frequency_score + recency_score

    def _estimate_effort(self, pattern: Pattern) -> str:
        """Estimate implementation effort."""
        if pattern.pattern_type == PatternType.ERROR:
            return 'low'
        elif pattern.pattern_type == PatternType.PERFORMANCE:
            return 'medium'
        elif pattern.pattern_type == PatternType.RESOURCE:
            return 'medium'
        elif pattern.pattern_type == PatternType.SKILL_INTERACTION:
            return 'high'
        else:
            return 'low'

    def _estimate_benefit(self, pattern: Pattern) -> str:
        """Estimate expected benefit."""
        if pattern.frequency > 10 and pattern.confidence > 0.8:
            return 'high'
        elif pattern.frequency > 5 and pattern.confidence > 0.6:
            return 'medium'
        else:
            return 'low'

def demo_pattern_recognition():
    """Demonstrate the pattern recognition system."""
    recognizer = PatternRecognizer()

    # Create sample task history
    task_history = [
        {
            'timestamp': datetime.now() - timedelta(days=5),
            'task_type': 'skill_installation',
            'execution_time': 120,
            'success': True,
            'errors': [],
            'used_skills': ['skill-vetter', 'skill-finder']
        },
        {
            'timestamp': datetime.now() - timedelta(days=4),
            'task_type': 'skill_installation',
            'execution_time': 150,
            'success': True,
            'errors': [],
            'used_skills': ['skill-vetter', 'skill-finder']
        },
        {
            'timestamp': datetime.now() - timedelta(days=3),
            'task_type': 'skill_installation',
            'execution_time': 180,
            'success': False,
            'errors': ['Network timeout', 'Connection failed'],
            'used_skills': ['skill-vetter']
        },
        {
            'timestamp': datetime.now() - timedelta(days=2),
            'task_type': 'skill_audit',
            'execution_time': 90,
            'success': True,
            'errors': [],
            'used_skills': ['skill-vetter', 'autonomous-agent']
        },
        {
            'timestamp': datetime.now() - timedelta(days=1),
            'task_type': 'skill_installation',
            'execution_time': 200,
            'success': False,
            'errors': ['Network timeout'],
            'used_skills': ['skill-vetter', 'skill-finder']
        }
    ]

    # Identify patterns
    patterns = recognizer.identify_patterns(task_history)

    print("Pattern Recognition Demo")
    print("=" * 60)
    print(f"Patterns identified: {len(patterns)}")

    for i, pattern in enumerate(patterns, 1):
        print(f"\n{i}. {pattern.name}")
        print(f"   Type: {pattern.pattern_type.value}")
        print(f"   Description: {pattern.description}")
        print(f"   Confidence: {pattern.confidence:.2f}")
        print(f"   Frequency: {pattern.frequency}")
        print(f"   Actionable: {pattern.actionable}")

    # Generate optimization suggestions
    suggestions = recognizer.generate_optimization_suggestions(patterns)

    print(f"\nOptimization Suggestions:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['pattern_name']}")
        print(f"   Type: {suggestion['suggestion_type']}")
        print(f"   Description: {suggestion['description']}")
        print(f"   Priority: {suggestion['priority']:.2f}")
        print(f"   Effort: {suggestion['implementation_effort']}")
        print(f"   Benefit: {suggestion['expected_benefit']}")

if __name__ == "__main__":
    demo_pattern_recognition()
