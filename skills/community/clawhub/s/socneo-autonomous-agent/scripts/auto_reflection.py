#!/usr/bin/env python3
"""
Auto Reflection - Reflection Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Automatic outcome analysis and learning.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics
import uuid

class ReflectionType(Enum):
    TASK_COMPLETION = "task_completion"
    ERROR_ANALYSIS = "error_analysis"
    PERFORMANCE_REVIEW = "performance_review"
    PATTERN_DISCOVERY = "pattern_discovery"
    SYSTEM_HEALTH = "system_health"

class ReflectionOutcome(Enum):
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    LEARNING_OPPORTUNITY = "learning_opportunity"

@dataclass
class TaskResult:
    """Represents the result of a completed task."""
    task_id: str
    task_name: str
    execution_start: datetime
    execution_end: datetime
    status: str
    success_metrics: Dict[str, Any]
    performance_metrics: Dict[str, float]
    resource_usage: Dict[str, float]
    errors: List[str]
    user_feedback: Optional[str] = None
    confidence_score: float = 0.0

@dataclass
class ReflectionInsight:
    """An insight generated from reflection analysis."""
    insight_id: str
    category: str
    description: str
    confidence: float
    impact_level: str  # low, medium, high
    action_items: List[str]
    evidence: List[str]
    created_at: datetime

@dataclass
class ReflectionReport:
    """Complete reflection report for a task or session."""
    report_id: str
    reflection_type: ReflectionType
    subject_id: str  # task_id or session_id
    timestamp: datetime
    outcome: ReflectionOutcome
    insights: List[ReflectionInsight]
    recommendations: List[str]
    metrics_summary: Dict[str, Any]
    learning_points: List[str]
    follow_up_actions: List[str]

class AutoReflection:
    """Automated reflection system for continuous learning and improvement."""

    def __init__(self):
        self.reflection_criteria = {
            'success_rate_threshold': 0.8,
            'efficiency_threshold': 0.7,
            'user_satisfaction_threshold': 0.8,
            'performance_variance_threshold': 0.2
        }

        # Reflection patterns and templates
        self.reflection_patterns = {
            'success_analysis': [
                'goal_achievement',
                'efficiency_evaluation',
                'quality_assessment',
                'user_satisfaction'
            ],
            'failure_analysis': [
                'root_cause_identification',
                'error_pattern_recognition',
                'prevention_strategies',
                'recovery_improvements'
            ],
            'performance_optimization': [
                'bottleneck_identification',
                'resource_optimization',
                'process_improvement',
                'tool_enhancement'
            ]
        }

        # Learning templates
        self.learning_templates = {
            'process_improvement': 'Consider optimizing {process} by {improvement}',
            'error_prevention': 'Implement {prevention} to avoid {error_type}',
            'efficiency_gain': 'Apply {technique} to improve {metric} by {percentage}%',
            'quality_enhancement': 'Enhance {aspect} through {method}'
        }

    def conduct_reflection(self, task_result: TaskResult) -> ReflectionReport:
        """Conduct comprehensive reflection on task execution."""

        # Generate insights
        insights = self._generate_insights(task_result)

        # Evaluate outcome
        outcome = self._evaluate_outcome(task_result, insights)

        # Generate recommendations
        recommendations = self._generate_recommendations(task_result, insights)

        # Create metrics summary
        metrics_summary = self._create_metrics_summary(task_result)

        # Extract learning points
        learning_points = self._extract_learning_points(task_result, insights)

        # Determine follow-up actions
        follow_up_actions = self._determine_follow_up_actions(task_result, insights)

        return ReflectionReport(
            report_id=str(uuid.uuid4()),
            reflection_type=ReflectionType.TASK_COMPLETION,
            subject_id=task_result.task_id,
            timestamp=datetime.now(),
            outcome=outcome,
            insights=insights,
            recommendations=recommendations,
            metrics_summary=metrics_summary,
            learning_points=learning_points,
            follow_up_actions=follow_up_actions
        )

    def _generate_insights(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Generate insights from task execution data."""
        insights = []

        # Performance insights
        performance_insights = self._analyze_performance(task_result)
        insights.extend(performance_insights)

        # Success/failure insights
        if task_result.status == 'completed':
            success_insights = self._analyze_success(task_result)
            insights.extend(success_insights)
        else:
            failure_insights = self._analyze_failure(task_result)
            insights.extend(failure_insights)

        # Resource usage insights
        resource_insights = self._analyze_resource_usage(task_result)
        insights.extend(resource_insights)

        # Efficiency insights
        efficiency_insights = self._analyze_efficiency(task_result)
        insights.extend(efficiency_insights)

        return insights

    def _analyze_performance(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Analyze task performance metrics."""
        insights = []

        # Execution time analysis
        execution_time = (task_result.execution_end - task_result.execution_start).total_seconds()
        if 'expected_duration' in task_result.performance_metrics:
            expected_time = task_result.performance_metrics['expected_duration']
            time_ratio = execution_time / expected_time if expected_time > 0 else 1

            if time_ratio > 1.5:
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='performance',
                    description=f'Task took {time_ratio:.1f}x longer than expected',
                    confidence=0.8,
                    impact_level='medium',
                    action_items=['Review execution bottlenecks', 'Optimize slow operations'],
                    evidence=[f'Actual: {execution_time}s', f'Expected: {expected_time}s'],
                    created_at=datetime.now()
                ))
            elif time_ratio < 0.7:
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='efficiency',
                    description=f'Task completed {((1/time_ratio - 1) * 100):.0f}% faster than expected',
                    confidence=0.9,
                    impact_level='low',
                    action_items=['Document optimization techniques', 'Share best practices'],
                    evidence=[f'Actual: {execution_time}s', f'Expected: {expected_time}s'],
                    created_at=datetime.now()
                ))

        # Quality metrics analysis
        if 'quality_score' in task_result.success_metrics:
            quality_score = task_result.success_metrics['quality_score']
            if quality_score < self.reflection_criteria['success_rate_threshold']:
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='quality',
                    description=f'Task quality score ({quality_score:.2f}) below threshold',
                    confidence=0.85,
                    impact_level='high',
                    action_items=['Review quality criteria', 'Improve execution standards'],
                    evidence=[f'Quality score: {quality_score:.2f}'],
                    created_at=datetime.now()
                ))

        return insights

    def _analyze_success(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Analyze successful task execution."""
        insights = []

        # Goal achievement analysis
        if task_result.success_metrics:
            achieved_goals = sum(1 for metric, value in task_result.success_metrics.items()
                               if isinstance(value, bool) and value)
            total_goals = len([metric for metric, value in task_result.success_metrics.items()
                             if isinstance(value, bool)])

            if total_goals > 0:
                achievement_rate = achieved_goals / total_goals

                if achievement_rate >= 0.9:
                    insights.append(ReflectionInsight(
                        insight_id=str(uuid.uuid4()),
                        category='success',
                        description=f'High goal achievement rate ({achievement_rate:.1%})',
                        confidence=0.9,
                        impact_level='low',
                        action_items=['Document successful approach', 'Identify key success factors'],
                        evidence=[f'Achieved: {achieved_goals}/{total_goals} goals'],
                        created_at=datetime.now()
                    ))

        # Confidence analysis
        if task_result.confidence_score > 0.8:
            insights.append(ReflectionInsight(
                insight_id=str(uuid.uuid4()),
                category='confidence',
                description=f'High confidence execution ({task_result.confidence_score:.2f})',
                confidence=0.85,
                impact_level='low',
                action_items=['Validate confidence calibration', 'Document decision factors'],
                evidence=[f'Confidence score: {task_result.confidence_score:.2f}'],
                created_at=datetime.now()
            ))

        return insights

    def _analyze_failure(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Analyze task failures and errors."""
        insights = []

        # Error pattern analysis
        if task_result.errors:
            error_categories = self._categorize_errors(task_result.errors)

            for category, errors in error_categories.items():
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='failure_analysis',
                    description=f'{len(errors)} {category} errors encountered',
                    confidence=0.9,
                    impact_level='high',
                    action_items=[
                        f'Implement {category} error handling',
                        f'Add {category} validation checks',
                        f'Improve {category} error recovery'
                    ],
                    evidence=[f'Errors: {"; ".join(errors[:3])}'],
                    created_at=datetime.now()
                ))

        # Root cause analysis
        root_causes = self._identify_root_causes(task_result)
        for cause in root_causes:
            insights.append(ReflectionInsight(
                insight_id=str(uuid.uuid4()),
                category='root_cause',
                description=f'Root cause identified: {cause}',
                confidence=0.75,
                impact_level='high',
                action_items=[
                    f'Address {cause}',
                    f'Implement preventive measures for {cause}',
                    f'Monitor {cause} in future executions'
                ],
                evidence=['Task execution analysis'],
                created_at=datetime.now()
            ))

        return insights

    def _analyze_resource_usage(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Analyze resource usage patterns."""
        insights = []

        if not task_result.resource_usage:
            return insights

        # Memory usage analysis
        if 'memory_usage' in task_result.resource_usage:
            memory_usage = task_result.resource_usage['memory_usage']
            if memory_usage > 100:  # MB
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='resource_optimization',
                    description=f'High memory usage detected ({memory_usage:.1f} MB)',
                    confidence=0.8,
                    impact_level='medium',
                    action_items=[
                        'Optimize memory-intensive operations',
                        'Implement memory pooling',
                        'Review data structure efficiency'
                    ],
                    evidence=[f'Memory usage: {memory_usage:.1f} MB'],
                    created_at=datetime.now()
                ))

        # CPU usage analysis
        if 'cpu_usage' in task_result.resource_usage:
            cpu_usage = task_result.resource_usage['cpu_usage']
            if cpu_usage > 80:  # Percentage
                insights.append(ReflectionInsight(
                    insight_id=str(uuid.uuid4()),
                    category='performance',
                    description=f'High CPU usage detected ({cpu_usage:.1f}%)',
                    confidence=0.8,
                    impact_level='medium',
                    action_items=[
                        'Optimize CPU-intensive algorithms',
                        'Implement parallel processing',
                        'Review computational complexity'
                    ],
                    evidence=[f'CPU usage: {cpu_usage:.1f}%'],
                    created_at=datetime.now()
                ))

        return insights

    def _analyze_efficiency(self, task_result: TaskResult) -> List[ReflectionInsight]:
        """Analyze task efficiency and optimization opportunities."""
        insights = []

        # Efficiency score calculation
        efficiency_score = self._calculate_efficiency_score(task_result)

        if efficiency_score < self.reflection_criteria['efficiency_threshold']:
            insights.append(ReflectionInsight(
                insight_id=str(uuid.uuid4()),
                category='efficiency',
                description=f'Low efficiency score ({efficiency_score:.2f})',
                confidence=0.8,
                impact_level='medium',
                action_items=[
                    'Identify process bottlenecks',
                    'Optimize workflow steps',
                    'Review tool selection'
                ],
                evidence=[f'Efficiency score: {efficiency_score:.2f}'],
                created_at=datetime.now()
            ))

        return insights

    def _categorize_errors(self, errors: List[str]) -> Dict[str, List[str]]:
        """Categorize errors by type."""
        categories = {
            'network': [],
            'permission': [],
            'validation': [],
            'resource': [],
            'logic': [],
            'timeout': [],
            'other': []
        }

        for error in errors:
            error_lower = error.lower()
            if any(keyword in error_lower for keyword in ['network', 'connection', 'timeout']):
                categories['network'].append(error)
            elif any(keyword in error_lower for keyword in ['permission', 'access', 'denied']):
                categories['permission'].append(error)
            elif any(keyword in error_lower for keyword in ['validation', 'invalid', 'format']):
                categories['validation'].append(error)
            elif any(keyword in error_lower for keyword in ['memory', 'cpu', 'disk']):
                categories['resource'].append(error)
            elif any(keyword in error_lower for keyword in ['logic', 'algorithm', 'calculation']):
                categories['logic'].append(error)
            elif 'timeout' in error_lower:
                categories['timeout'].append(error)
            else:
                categories['other'].append(error)

        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

    def _identify_root_causes(self, task_result: TaskResult) -> List[str]:
        """Identify potential root causes of task failure."""
        root_causes = []

        if task_result.errors:
            # Analyze error patterns
            error_text = ' '.join(task_result.errors).lower()

            if 'network' in error_text or 'connection' in error_text:
                root_causes.append('Network connectivity issues')

            if 'permission' in error_text or 'access' in error_text:
                root_causes.append('Insufficient permissions or access rights')

            if 'memory' in error_text or 'cpu' in error_text:
                root_causes.append('Resource constraints')

            if 'validation' in error_text or 'format' in error_text:
                root_causes.append('Input validation failures')

            if 'timeout' in error_text:
                root_causes.append('Operation timeouts')

        # Analyze performance metrics for potential causes
        if 'execution_time' in task_result.performance_metrics:
            exec_time = task_result.performance_metrics['execution_time']
            if exec_time > 300:  # 5 minutes
                root_causes.append('Excessive execution time')

        return list(set(root_causes))  # Remove duplicates

    def _calculate_efficiency_score(self, task_result: TaskResult) -> float:
        """Calculate overall efficiency score."""
        score = 0.0
        factors = 0

        # Time efficiency
        if 'expected_duration' in task_result.performance_metrics:
            actual_time = (task_result.execution_end - task_result.execution_start).total_seconds()
            expected_time = task_result.performance_metrics['expected_duration']
            if expected_time > 0:
                time_efficiency = min(expected_time / actual_time, 2.0)  # Cap at 2x efficiency
                score += time_efficiency * 0.4
                factors += 0.4

        # Resource efficiency
        if task_result.resource_usage:
            # Normalize resource usage (lower is better)
            resource_efficiency = 1.0
            if 'memory_usage' in task_result.resource_usage:
                memory_usage = task_result.resource_usage['memory_usage']
                resource_efficiency *= max(0.1, 1 - (memory_usage / 1000))  # Normalize to 1GB

            if 'cpu_usage' in task_result.resource_usage:
                cpu_usage = task_result.resource_usage['cpu_usage']
                resource_efficiency *= max(0.1, 1 - (cpu_usage / 100))

            score += resource_efficiency * 0.3
            factors += 0.3

        # Success rate
        if task_result.success_metrics:
            success_count = sum(1 for v in task_result.success_metrics.values() if v is True)
            total_metrics = len(task_result.success_metrics)
            if total_metrics > 0:
                success_rate = success_count / total_metrics
                score += success_rate * 0.3
                factors += 0.3

        return score / factors if factors > 0 else 0.0

    def _evaluate_outcome(self, task_result: TaskResult, insights: List[ReflectionInsight]) -> ReflectionOutcome:
        """Evaluate the overall outcome of the task."""

        # Count insight impact levels
        high_impact_insights = [i for i in insights if i.impact_level == 'high']
        medium_impact_insights = [i for i in insights if i.impact_level == 'medium']

        # Determine outcome based on task status and insights
        if task_result.status == 'completed':
            if not high_impact_insights and len(medium_impact_insights) <= 1:
                return ReflectionOutcome.SUCCESS
            elif len(high_impact_insights) <= 1:
                return ReflectionOutcome.PARTIAL_SUCCESS
            else:
                return ReflectionOutcome.LEARNING_OPPORTUNITY
        else:
            if high_impact_insights:
                return ReflectionOutcome.FAILURE
            else:
                return ReflectionOutcome.LEARNING_OPPORTUNITY

    def _generate_recommendations(self, task_result: TaskResult, insights: List[ReflectionInsight]) -> List[str]:
        """Generate actionable recommendations based on insights."""
        recommendations = []

        # Collect action items from high-impact insights
        high_impact_insights = [i for i in insights if i.impact_level == 'high']
        for insight in high_impact_insights:
            recommendations.extend(insight.action_items)

        # Add general recommendations based on task outcome
        if task_result.status != 'completed':
            recommendations.append('Review and improve error handling procedures')
            recommendations.append('Implement additional validation checks')

        if any('efficiency' in insight.category for insight in insights):
            recommendations.append('Optimize task execution workflow')

        if any('resource' in insight.category for insight in insights):
            recommendations.append('Monitor and optimize resource usage')

        return list(set(recommendations))  # Remove duplicates

    def _create_metrics_summary(self, task_result: TaskResult) -> Dict[str, Any]:
        """Create a summary of key metrics."""
        summary = {
            'execution_time': (task_result.execution_end - task_result.execution_start).total_seconds(),
            'status': task_result.status,
            'error_count': len(task_result.errors),
            'confidence_score': task_result.confidence_score
        }

        if task_result.success_metrics:
            summary['success_metrics'] = task_result.success_metrics

        if task_result.performance_metrics:
            summary['performance_metrics'] = task_result.performance_metrics

        if task_result.resource_usage:
            summary['resource_usage'] = task_result.resource_usage

        return summary

    def _extract_learning_points(self, task_result: TaskResult, insights: List[ReflectionInsight]) -> List[str]:
        """Extract key learning points from the reflection."""
        learning_points = []

        # Extract from insights
        for insight in insights:
            if insight.impact_level in ['high', 'medium']:
                learning_points.append(f"{insight.category}: {insight.description}")

        # Add general learnings
        if task_result.status == 'completed':
            learning_points.append('Successful task completion patterns identified')

        if task_result.errors:
            learning_points.append('Error handling improvements needed')

        if task_result.confidence_score < 0.7:
            learning_points.append('Confidence calibration requires attention')

        return learning_points

    def _determine_follow_up_actions(self, task_result: TaskResult, insights: List[ReflectionInsight]) -> List[str]:
        """Determine required follow-up actions."""
        actions = []

        # High-impact insights require immediate follow-up
        high_impact_insights = [i for i in insights if i.impact_level == 'high']
        if high_impact_insights:
            actions.append('Schedule immediate review of high-impact issues')

        # Failed tasks require re-execution planning
        if task_result.status != 'completed':
            actions.append('Plan task re-execution with improvements')

        # Performance issues require optimization
        performance_insights = [i for i in insights if 'performance' in i.category]
        if performance_insights:
            actions.append('Implement performance optimizations')

        # Learning opportunities require documentation
        if insights:
            actions.append('Document lessons learned for future reference')

        return actions

def demo_auto_reflection():
    """Demonstrate the auto reflection system."""
    reflection = AutoReflection()

    # Create a sample task result
    task_result = TaskResult(
        task_id="task_123",
        task_name="Install New Skill",
        execution_start=datetime.now() - timedelta(minutes=10),
        execution_end=datetime.now(),
        status="completed",
        success_metrics={
            "skill_installed": True,
            "configuration_valid": True,
            "tests_passed": True,
            "quality_score": 0.85
        },
        performance_metrics={
            "expected_duration": 300,  # 5 minutes
            "actual_duration": 600,    # 10 minutes
            "steps_completed": 5
        },
        resource_usage={
            "memory_usage": 150.5,  # MB
            "cpu_usage": 65.2      # Percentage
        },
        errors=[],
        confidence_score=0.8
    )

    # Conduct reflection
    report = reflection.conduct_reflection(task_result)

    print("Auto Reflection Demo")
    print("=" * 60)
    print(f"Task: {task_result.task_name}")
    print(f"Status: {task_result.status}")
    print(f"Outcome: {report.outcome.value}")
    print(f"Insights Generated: {len(report.insights)}")

    print(f"\nKey Insights:")
    for i, insight in enumerate(report.insights, 1):
        print(f"{i}. {insight.category}: {insight.description}")
        print(f"   Impact: {insight.impact_level}, Confidence: {insight.confidence:.2f}")

    print(f"\nRecommendations:")
    for i, rec in enumerate(report.recommendations, 1):
        print(f"{i}. {rec}")

    print(f"\nFollow-up Actions:")
    for i, action in enumerate(report.follow_up_actions, 1):
        print(f"{i}. {action}")

if __name__ == "__main__":
    demo_auto_reflection()
