#!/usr/bin/env python3
"""
Uncertainty Handler - Judgment Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Low-confidence situation management.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

class UncertaintyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class HandlingStrategy(Enum):
    PROCEED_WITH_CAUTION = "proceed_with_caution"
    REQUEST_ADDITIONAL_INFO = "request_additional_info"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    DEFER_DECISION = "defer_decision"
    USE_CONSERVATIVE_APPROACH = "use_conservative_approach"

@dataclass
class UncertaintyContext:
    """Context information for uncertainty assessment."""
    task_id: str
    task_description: str
    confidence_score: float
    available_information: Dict[str, Any]
    missing_information: List[str]
    potential_risks: List[str]
    user_preferences: Dict[str, Any]
    system_capabilities: Dict[str, Any]
    timestamp: datetime

@dataclass
class UncertaintyResult:
    """Result of uncertainty handling."""
    uncertainty_level: UncertaintyLevel
    handling_strategy: HandlingStrategy
    confidence_assessment: str
    required_actions: List[str]
    escalation_required: bool
    alternatives: List[Dict[str, Any]]
    risk_mitigation: List[str]
    follow_up_plan: Optional[Dict[str, Any]] = None

class UncertaintyHandler:
    """Advanced uncertainty handling system for autonomous decision making."""

    def __init__(self):
        # Confidence thresholds
        self.confidence_thresholds = {
            UncertaintyLevel.LOW: 0.8,
            UncertaintyLevel.MEDIUM: 0.6,
            UncertaintyLevel.HIGH: 0.4,
            UncertaintyLevel.CRITICAL: 0.2
        }

        # Uncertainty patterns and their handling strategies
        self.uncertainty_patterns = {
            'missing_critical_info': {
                'strategy': HandlingStrategy.REQUEST_ADDITIONAL_INFO,
                'priority': 'high',
                'escalation_threshold': 0.3
            },
            'conflicting_information': {
                'strategy': HandlingStrategy.USE_CONSERVATIVE_APPROACH,
                'priority': 'medium',
                'escalation_threshold': 0.4
            },
            'novel_situation': {
                'strategy': HandlingStrategy.ESCALATE_TO_HUMAN,
                'priority': 'high',
                'escalation_threshold': 0.5
            },
            'high_risk_operation': {
                'strategy': HandlingStrategy.ESCALATE_TO_HUMAN,
                'priority': 'critical',
                'escalation_threshold': 0.6
            },
            'ambiguous_objectives': {
                'strategy': HandlingStrategy.REQUEST_ADDITIONAL_INFO,
                'priority': 'medium',
                'escalation_threshold': 0.4
            }
        }

        # Historical uncertainty resolution patterns
        self.resolution_history = []
        self.successful_strategies = {}

        # User tolerance levels for different types of uncertainty
        self.user_tolerance_levels = {
            'automation_risk': 0.7,
            'information_gaps': 0.5,
            'novel_situations': 0.3,
            'safety_concerns': 0.1
        }

    def assess_uncertainty(self, context: UncertaintyContext) -> UncertaintyResult:
        """Assess uncertainty level and determine handling strategy."""

        # Determine uncertainty level
        uncertainty_level = self._determine_uncertainty_level(context.confidence_score)

        # Identify uncertainty patterns
        patterns = self._identify_uncertainty_patterns(context)

        # Select handling strategy
        strategy = self._select_handling_strategy(context, patterns, uncertainty_level)

        # Generate confidence assessment
        confidence_assessment = self._generate_confidence_assessment(context, uncertainty_level)

        # Determine required actions
        required_actions = self._determine_required_actions(strategy, context, patterns)

        # Check if escalation is required
        escalation_required = self._check_escalation_requirement(context, uncertainty_level, patterns)

        # Generate alternatives
        alternatives = self._generate_alternatives(context, strategy)

        # Create risk mitigation plan
        risk_mitigation = self._create_risk_mitigation_plan(context, strategy, uncertainty_level)

        # Create follow-up plan
        follow_up_plan = self._create_follow_up_plan(context, strategy)

        # Record uncertainty assessment for learning
        self._record_uncertainty_assessment(context, uncertainty_level, strategy)

        return UncertaintyResult(
            uncertainty_level=uncertainty_level,
            handling_strategy=strategy,
            confidence_assessment=confidence_assessment,
            required_actions=required_actions,
            escalation_required=escalation_required,
            alternatives=alternatives,
            risk_mitigation=risk_mitigation,
            follow_up_plan=follow_up_plan
        )

    def _determine_uncertainty_level(self, confidence_score: float) -> UncertaintyLevel:
        """Determine uncertainty level based on confidence score."""
        if confidence_score >= self.confidence_thresholds[UncertaintyLevel.LOW]:
            return UncertaintyLevel.LOW
        elif confidence_score >= self.confidence_thresholds[UncertaintyLevel.MEDIUM]:
            return UncertaintyLevel.MEDIUM
        elif confidence_score >= self.confidence_thresholds[UncertaintyLevel.HIGH]:
            return UncertaintyLevel.HIGH
        else:
            return UncertaintyLevel.CRITICAL

    def _identify_uncertainty_patterns(self, context: UncertaintyContext) -> List[str]:
        """Identify patterns that contribute to uncertainty."""
        patterns = []

        # Check for missing critical information
        if len(context.missing_information) > 0:
            critical_missing = [info for info in context.missing_information if 'critical' in info.lower()]
            if critical_missing:
                patterns.append('missing_critical_info')

        # Check for conflicting information
        if 'conflicts' in context.available_information:
            if context.available_information['conflicts']:
                patterns.append('conflicting_information')

        # Check for novel situations
        if self._is_novel_situation(context):
            patterns.append('novel_situation')

        # Check for high-risk operations
        if self._is_high_risk_operation(context):
            patterns.append('high_risk_operation')

        # Check for ambiguous objectives
        if self._has_ambiguous_objectives(context):
            patterns.append('ambiguous_objectives')

        return patterns

    def _is_novel_situation(self, context: UncertaintyContext) -> bool:
        """Determine if this is a novel situation."""
        # Check if similar situations have been encountered before
        task_description = context.task_description.lower()

        # Look for novelty indicators
        novelty_indicators = [
            'first time', 'new', 'unprecedented', 'never before',
            'unknown', 'unclear', 'ambiguous'
        ]

        for indicator in novelty_indicators:
            if indicator in task_description:
                return True

        # Check against historical patterns
        similar_tasks = self._find_similar_historical_tasks(context.task_description)
        return len(similar_tasks) == 0

    def _is_high_risk_operation(self, context: UncertaintyContext) -> bool:
        """Determine if this is a high-risk operation."""
        risk_indicators = [
            'delete', 'remove', 'uninstall', 'reboot', 'restart',
            'financial', 'payment', 'sensitive', 'critical'
        ]

        task_description = context.task_description.lower()

        for indicator in risk_indicators:
            if indicator in task_description:
                return True

        # Check explicit risk list
        high_risk_keywords = ['critical', 'high risk', 'dangerous', 'irreversible']
        for risk in context.potential_risks:
            for keyword in high_risk_keywords:
                if keyword in risk.lower():
                    return True

        return False

    def _has_ambiguous_objectives(self, context: UncertaintyContext) -> bool:
        """Determine if objectives are ambiguous."""
        ambiguous_indicators = [
            'optimize', 'improve', 'better', 'enhance',
            'suitable', 'appropriate', 'best'
        ]

        task_description = context.task_description.lower()

        for indicator in ambiguous_indicators:
            if indicator in task_description:
                return True

        return False

    def _select_handling_strategy(self, context: UncertaintyContext, patterns: List[str], uncertainty_level: UncertaintyLevel) -> HandlingStrategy:
        """Select appropriate handling strategy based on patterns and uncertainty level."""

        # If multiple patterns, prioritize by severity
        if patterns:
            # Find the most critical pattern
            critical_pattern = None
            highest_priority = 'low'

            for pattern in patterns:
                if pattern in self.uncertainty_patterns:
                    pattern_priority = self.uncertainty_patterns[pattern]['priority']
                    priority_levels = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

                    if priority_levels.get(pattern_priority, 0) > priority_levels.get(highest_priority, 0):
                        highest_priority = pattern_priority
                        critical_pattern = pattern

            if critical_pattern:
                return self.uncertainty_patterns[critical_pattern]['strategy']

        # Default strategy based on uncertainty level
        if uncertainty_level == UncertaintyLevel.CRITICAL:
            return HandlingStrategy.ESCALATE_TO_HUMAN
        elif uncertainty_level == UncertaintyLevel.HIGH:
            return HandlingStrategy.REQUEST_ADDITIONAL_INFO
        elif uncertainty_level == UncertaintyLevel.MEDIUM:
            return HandlingStrategy.PROCEED_WITH_CAUTION
        else:
            return HandlingStrategy.PROCEED_WITH_CAUTION

    def _generate_confidence_assessment(self, context: UncertaintyContext, uncertainty_level: UncertaintyLevel) -> str:
        """Generate human-readable confidence assessment."""
        assessment_parts = []

        # Base confidence statement
        confidence_percentage = (1 - context.confidence_score) * 100
        assessment_parts.append(f"Confidence level: {context.confidence_score:.2f} ({confidence_percentage:.1f}% uncertainty)")

        # Uncertainty level description
        level_descriptions = {
            UncertaintyLevel.LOW: "Low uncertainty - system can proceed with normal operation",
            UncertaintyLevel.MEDIUM: "Medium uncertainty - proceed with caution and monitoring",
            UncertaintyLevel.HIGH: "High uncertainty - additional information or human input required",
            UncertaintyLevel.CRITICAL: "Critical uncertainty - immediate human intervention required"
        }
        assessment_parts.append(level_descriptions[uncertainty_level])

        # Contributing factors
        if context.missing_information:
            assessment_parts.append(f"Missing information: {', '.join(context.missing_information[:3])}")

        if context.potential_risks:
            assessment_parts.append(f"Potential risks: {', '.join(context.potential_risks[:3])}")

        return "; ".join(assessment_parts)

    def _determine_required_actions(self, strategy: HandlingStrategy, context: UncertaintyContext, patterns: List[str]) -> List[str]:
        """Determine required actions based on handling strategy."""
        actions = []

        strategy_actions = {
            HandlingStrategy.PROCEED_WITH_CAUTION: [
                "Implement additional monitoring",
                "Set up rollback mechanisms",
                "Prepare contingency plans"
            ],
            HandlingStrategy.REQUEST_ADDITIONAL_INFO: [
                "Identify missing information sources",
                "Formulate specific questions",
                "Determine optimal timing for information request"
            ],
            HandlingStrategy.ESCALATE_TO_HUMAN: [
                "Prepare comprehensive situation summary",
                "Highlight key decision points",
                "Suggest possible courses of action"
            ],
            HandlingStrategy.DEFER_DECISION: [
                "Set decision deferral timeline",
                "Monitor for changing conditions",
                "Prepare for re-evaluation"
            ],
            HandlingStrategy.USE_CONSERVATIVE_APPROACH: [
                "Identify safest course of action",
                "Implement minimal necessary changes",
                "Prepare for gradual escalation if needed"
            ]
        }

        actions.extend(strategy_actions.get(strategy, []))

        # Add pattern-specific actions
        for pattern in patterns:
            if pattern == 'missing_critical_info':
                actions.append("Prioritize gathering missing critical information")
            elif pattern == 'novel_situation':
                actions.append("Document situation for future reference")
            elif pattern == 'high_risk_operation':
                actions.append("Implement additional safety checks")

        return actions

    def _check_escalation_requirement(self, context: UncertaintyContext, uncertainty_level: UncertaintyLevel, patterns: List[str]) -> bool:
        """Check if escalation to human is required."""

        # Always escalate critical uncertainty
        if uncertainty_level == UncertaintyLevel.CRITICAL:
            return True

        # Check pattern escalation thresholds
        for pattern in patterns:
            if pattern in self.uncertainty_patterns:
                threshold = self.uncertainty_patterns[pattern]['escalation_threshold']
                if context.confidence_score < threshold:
                    return True

        # Check user tolerance levels
        for pattern in patterns:
            if pattern == 'novel_situation':
                if context.confidence_score < self.user_tolerance_levels['novel_situations']:
                    return True
            elif pattern == 'high_risk_operation':
                if context.confidence_score < self.user_tolerance_levels['safety_concerns']:
                    return True

        return False

    def _generate_alternatives(self, context: UncertaintyContext, primary_strategy: HandlingStrategy) -> List[Dict[str, Any]]:
        """Generate alternative approaches."""
        alternatives = []

        strategy_alternatives = {
            HandlingStrategy.ESCALATE_TO_HUMAN: [
                {
                    'strategy': HandlingStrategy.PROCEED_WITH_CAUTION.value,
                    'description': 'Proceed with enhanced monitoring and safety measures',
                    'risk_level': 'medium',
                    'requirements': ['Robust rollback plan', 'Real-time monitoring']
                },
                {
                    'strategy': HandlingStrategy.USE_CONSERVATIVE_APPROACH.value,
                    'description': 'Take minimal necessary action with conservative approach',
                    'risk_level': 'low',
                    'requirements': ['Conservative implementation', 'Gradual rollout']
                }
            ],
            HandlingStrategy.PROCEED_WITH_CAUTION: [
                {
                    'strategy': HandlingStrategy.REQUEST_ADDITIONAL_INFO.value,
                    'description': 'Gather more information before proceeding',
                    'risk_level': 'low',
                    'requirements': ['Information sources identified', 'Clear questions formulated']
                }
            ],
            HandlingStrategy.REQUEST_ADDITIONAL_INFO: [
                {
                    'strategy': HandlingStrategy.DEFER_DECISION.value,
                    'description': 'Wait for better information or conditions',
                    'risk_level': 'low',
                    'requirements': ['Deferral timeline established', 'Monitoring plan in place']
                }
            ]
        }

        return strategy_alternatives.get(primary_strategy, [])

    def _create_risk_mitigation_plan(self, context: UncertaintyContext, strategy: HandlingStrategy, uncertainty_level: UncertaintyLevel) -> List[str]:
        """Create risk mitigation plan."""
        mitigation_measures = []

        # Base mitigation measures
        if uncertainty_level in [UncertaintyLevel.HIGH, UncertaintyLevel.CRITICAL]:
            mitigation_measures.extend([
                "Implement comprehensive logging",
                "Set up real-time monitoring",
                "Prepare immediate rollback capability"
            ])

        # Strategy-specific mitigation
        if strategy == HandlingStrategy.PROCEED_WITH_CAUTION:
            mitigation_measures.extend([
                "Implement circuit breaker pattern",
                "Set up automatic rollback triggers",
                "Establish manual override mechanisms"
            ])
        elif strategy == HandlingStrategy.USE_CONSERVATIVE_APPROACH:
            mitigation_measures.extend([
                "Implement feature flags",
                "Use canary deployment approach",
                "Establish kill switches"
            ])

        # Risk-specific mitigation
        for risk in context.potential_risks:
            if 'data' in risk.lower():
                mitigation_measures.append("Implement data backup and recovery procedures")
            elif 'system' in risk.lower():
                mitigation_measures.append("Prepare system restore points")
            elif 'financial' in risk.lower():
                mitigation_measures.append("Implement transaction rollback capabilities")

        return mitigation_measures

    def _create_follow_up_plan(self, context: UncertaintyContext, strategy: HandlingStrategy) -> Optional[Dict[str, Any]]:
        """Create follow-up plan for uncertainty resolution."""
        if strategy in [HandlingStrategy.PROCEED_WITH_CAUTION, HandlingStrategy.USE_CONSERVATIVE_APPROACH]:
            return {
                'monitoring_schedule': 'Every 5 minutes for first hour, then hourly',
                'success_criteria': [
                    'No errors or warnings generated',
                    'Performance within expected parameters',
                    'User satisfaction maintained'
                ],
                'escalation_triggers': [
                    'Error rate exceeds 5%',
                    'Performance degradation > 20%',
                    'User requests intervention'
                ],
                'review_timeline': 'Review after 24 hours and weekly thereafter'
            }

        return None

    def _find_similar_historical_tasks(self, task_description: str) -> List[Dict[str, Any]]:
        """Find similar historical tasks for comparison."""
        # This would implement similarity matching against historical data
        # For demonstration, return empty list
        return []

    def _record_uncertainty_assessment(self, context: UncertaintyContext, uncertainty_level: UncertaintyLevel, strategy: HandlingStrategy):
        """Record uncertainty assessment for learning."""
        assessment_record = {
            'timestamp': context.timestamp,
            'task_description': context.task_description,
            'confidence_score': context.confidence_score,
            'uncertainty_level': uncertainty_level.value,
            'handling_strategy': strategy.value,
            'missing_information_count': len(context.missing_information),
            'potential_risks_count': len(context.potential_risks)
        }

        self.resolution_history.append(assessment_record)

        # Keep only recent history
        if len(self.resolution_history) > 1000:
            self.resolution_history = self.resolution_history[-1000:]

def demo_uncertainty_handler():
    """Demonstrate the uncertainty handling system."""
    handler = UncertaintyHandler()

    # Create sample uncertainty context
    context = UncertaintyContext(
        task_id="demo_uncertainty_1",
        task_description="Install experimental AI skill with unknown compatibility",
        confidence_score=0.3,
        available_information={
            'skill_name': 'experimental-skill',
            'source': 'community_repository',
            'conflicts': True
        },
        missing_information=[
            'compatibility_with_current_system',
            'security_vulnerabilities',
            'performance_impact'
        ],
        potential_risks=[
            'system_instability',
            'security_vulnerabilities',
            'data_corruption'
        ],
        user_preferences={'autonomy_level': 'medium'},
        system_capabilities={'sandbox_available': True},
        timestamp=datetime.now()
    )

    print("Uncertainty Handler Demo")
    print("=" * 50)

    # Assess uncertainty
    result = handler.assess_uncertainty(context)

    print(f"Task: {context.task_description}")
    print(f"Confidence Score: {context.confidence_score:.2f}")
    print(f"Uncertainty Level: {result.uncertainty_level.value}")
    print(f"Handling Strategy: {result.handling_strategy.value}")
    print(f"Escalation Required: {result.escalation_required}")

    print(f"\nConfidence Assessment:")
    print(f"  {result.confidence_assessment}")

    print(f"\nRequired Actions:")
    for action in result.required_actions:
        print(f"  - {action}")

    print(f"\nRisk Mitigation:")
    for mitigation in result.risk_mitigation:
        print(f"  - {mitigation}")

    if result.alternatives:
        print(f"\nAlternatives:")
        for alt in result.alternatives:
            print(f"  - {alt['strategy']}: {alt['description']} (Risk: {alt['risk_level']})")

if __name__ == "__main__":
    demo_uncertainty_handler()
