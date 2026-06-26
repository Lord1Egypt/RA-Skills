#!/usr/bin/env python3
"""
Risk Decision Matrix - Judgment Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Risk-based decision making.
"""

from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ImpactLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ConfidenceLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ActionType(Enum):
    EXECUTE = "execute"
    EXECUTE_NOTIFY = "execute_notify"
    EXECUTE_REPORT = "execute_report"
    REQUEST_APPROVAL = "request_approval"
    DEFER = "defer"
    ESCALATE = "escalate"

@dataclass
class DecisionContext:
    """Context information for decision making."""
    task_id: str
    task_name: str
    impact_level: ImpactLevel
    confidence_level: ConfidenceLevel
    user_context: Dict[str, Any]
    system_state: Dict[str, Any]
    historical_data: Dict[str, Any]
    timestamp: datetime

@dataclass
class DecisionResult:
    """Result of a risk-based decision."""
    action: ActionType
    requires_approval: bool
    confidence_score: float
    reasoning: str
    alternatives: list
    risk_assessment: Dict[str, Any]
    execution_plan: Optional[Dict[str, Any]] = None

class RiskDecisionMatrix:
    """Advanced risk-based decision making system."""

    def __init__(self):
        # Risk thresholds configuration
        self.risk_thresholds = {
            (ImpactLevel.LOW, ConfidenceLevel.HIGH): {
                'action': ActionType.EXECUTE,
                'approval': False,
                'confidence_threshold': 0.7
            },
            (ImpactLevel.MEDIUM, ConfidenceLevel.HIGH): {
                'action': ActionType.EXECUTE_NOTIFY,
                'approval': False,
                'confidence_threshold': 0.8
            },
            (ImpactLevel.HIGH, ConfidenceLevel.HIGH): {
                'action': ActionType.EXECUTE_NOTIFY,
                'approval': False,
                'confidence_threshold': 0.9
            },
            (ImpactLevel.LOW, ConfidenceLevel.MEDIUM): {
                'action': ActionType.EXECUTE_REPORT,
                'approval': False,
                'confidence_threshold': 0.6
            },
            (ImpactLevel.MEDIUM, ConfidenceLevel.MEDIUM): {
                'action': ActionType.REQUEST_APPROVAL,
                'approval': True,
                'confidence_threshold': 0.7
            },
            (ImpactLevel.HIGH, ConfidenceLevel.MEDIUM): {
                'action': ActionType.REQUEST_APPROVAL,
                'approval': True,
                'confidence_threshold': 0.8
            },
            (ImpactLevel.LOW, ConfidenceLevel.LOW): {
                'action': ActionType.REQUEST_APPROVAL,
                'approval': True,
                'confidence_threshold': 0.5
            },
            (ImpactLevel.MEDIUM, ConfidenceLevel.LOW): {
                'action': ActionType.ESCALATE,
                'approval': True,
                'confidence_threshold': 0.6
            },
            (ImpactLevel.HIGH, ConfidenceLevel.LOW): {
                'action': ActionType.ESCALATE,
                'approval': True,
                'confidence_threshold': 0.7
            },
            (ImpactLevel.CRITICAL, ConfidenceLevel.LOW): {
                'action': ActionType.ESCALATE,
                'approval': True,
                'confidence_threshold': 0.9
            },
            (ImpactLevel.CRITICAL, ConfidenceLevel.MEDIUM): {
                'action': ActionType.ESCALATE,
                'approval': True,
                'confidence_threshold': 0.95
            },
            (ImpactLevel.CRITICAL, ConfidenceLevel.HIGH): {
                'action': ActionType.REQUEST_APPROVAL,
                'approval': True,
                'confidence_threshold': 0.95
            }
        }

        # Risk categories and their weights
        self.risk_categories = {
            'data_security': 0.25,
            'system_stability': 0.20,
            'user_privacy': 0.20,
            'financial_impact': 0.15,
            'reputation': 0.10,
            'compliance': 0.10
        }

        # Historical decision outcomes
        self.decision_history = []
        self.success_patterns = {}

    def make_decision(self, context: DecisionContext) -> DecisionResult:
        """Make a risk-based decision for the given context."""

        # Get base decision from risk matrix
        risk_key = (context.impact_level, context.confidence_level)
        base_decision = self.risk_thresholds.get(risk_key, {
            'action': ActionType.REQUEST_APPROVAL,
            'approval': True,
            'confidence_threshold': 0.8
        })

        # Calculate actual confidence score
        confidence_score = self._calculate_confidence_score(context)

        # Adjust decision based on confidence score
        final_action = self._adjust_action_by_confidence(
            base_decision['action'],
            confidence_score,
            base_decision['confidence_threshold']
        )

        # Generate reasoning and alternatives
        reasoning = self._generate_reasoning(context, final_action, confidence_score)
        alternatives = self._generate_alternatives(context, final_action)
        risk_assessment = self._assess_risks(context)
        execution_plan = self._create_execution_plan(context, final_action)

        # Create decision result
        result = DecisionResult(
            action=final_action,
            requires_approval=base_decision['approval'],
            confidence_score=confidence_score,
            reasoning=reasoning,
            alternatives=alternatives,
            risk_assessment=risk_assessment,
            execution_plan=execution_plan
        )

        # Record decision for learning
        self._record_decision(context, result)

        return result

    def _calculate_confidence_score(self, context: DecisionContext) -> float:
        """Calculate confidence score based on available information."""
        base_confidence = self._get_base_confidence(context.confidence_level)

        # Adjust based on user context
        user_context_factor = self._evaluate_user_context(context.user_context)

        # Adjust based on system state
        system_state_factor = self._evaluate_system_state(context.system_state)

        # Adjust based on historical data
        historical_factor = self._evaluate_historical_data(context)

        # Calculate final confidence score
        confidence = (
            base_confidence * 0.4 +
            user_context_factor * 0.3 +
            system_state_factor * 0.2 +
            historical_factor * 0.1
        )

        return min(max(confidence, 0.0), 1.0)

    def _get_base_confidence(self, confidence_level: ConfidenceLevel) -> float:
        """Get base confidence value from confidence level."""
        confidence_map = {
            ConfidenceLevel.HIGH: 0.9,
            ConfidenceLevel.MEDIUM: 0.6,
            ConfidenceLevel.LOW: 0.3
        }
        return confidence_map.get(confidence_level, 0.5)

    def _evaluate_user_context(self, user_context: Dict[str, Any]) -> float:
        """Evaluate confidence based on user context."""
        if not user_context:
            return 0.5

        confidence_factors = []

        # Check user expertise level
        if user_context.get('expertise_level') == 'expert':
            confidence_factors.append(0.9)
        elif user_context.get('expertise_level') == 'intermediate':
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)

        # Check user availability
        if user_context.get('availability') == 'available':
            confidence_factors.append(0.8)
        elif user_context.get('availability') == 'busy':
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.4)

        # Check user preferences
        if user_context.get('autonomy_preference') == 'high':
            confidence_factors.append(0.9)
        elif user_context.get('autonomy_preference') == 'low':
            confidence_factors.append(0.6)
        else:
            confidence_factors.append(0.7)

        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5

    def _evaluate_system_state(self, system_state: Dict[str, Any]) -> float:
        """Evaluate confidence based on system state."""
        if not system_state:
            return 0.5

        confidence_factors = []

        # Check system load
        cpu_usage = system_state.get('cpu_usage', 0)
        if cpu_usage < 50:
            confidence_factors.append(0.9)
        elif cpu_usage < 80:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)

        # Check available memory
        memory_available = system_state.get('memory_available_gb', 0)
        if memory_available > 4:
            confidence_factors.append(0.9)
        elif memory_available > 1:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)

        # Check recent errors
        recent_errors = system_state.get('recent_errors', 0)
        if recent_errors == 0:
            confidence_factors.append(0.9)
        elif recent_errors < 5:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)

        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5

    def _evaluate_historical_data(self, context: DecisionContext) -> float:
        """Evaluate confidence based on historical performance."""
        task_type = context.task_name.lower()

        if task_type in self.success_patterns:
            success_rate = self.success_patterns[task_type].get('success_rate', 0.5)
            return success_rate

        return 0.6  # Default confidence for unknown tasks

    def _adjust_action_by_confidence(self, base_action: ActionType, confidence: float, threshold: float) -> ActionType:
        """Adjust action based on actual confidence score."""
        if confidence < threshold * 0.7:  # Significantly below threshold
            if base_action == ActionType.EXECUTE:
                return ActionType.REQUEST_APPROVAL
            elif base_action == ActionType.EXECUTE_NOTIFY:
                return ActionType.REQUEST_APPROVAL
            elif base_action == ActionType.EXECUTE_REPORT:
                return ActionType.REQUEST_APPROVAL

        elif confidence > threshold * 1.2:  # Significantly above threshold
            if base_action == ActionType.REQUEST_APPROVAL:
                return ActionType.EXECUTE_NOTIFY
            elif base_action == ActionType.EXECUTE_REPORT:
                return ActionType.EXECUTE

        return base_action

    def _generate_reasoning(self, context: DecisionContext, action: ActionType, confidence: float) -> str:
        """Generate human-readable reasoning for the decision."""
        reasoning_parts = []

        # Impact assessment
        reasoning_parts.append(f"Impact level: {context.impact_level.value}")

        # Confidence assessment
        reasoning_parts.append(f"Confidence level: {context.confidence_level.value} (actual: {confidence:.2f})")

        # Action justification
        action_reasons = {
            ActionType.EXECUTE: "Low impact and high confidence allow direct execution",
            ActionType.EXECUTE_NOTIFY: "Medium to high impact requires execution with notification",
            ActionType.EXECUTE_REPORT: "Lower confidence requires execution with detailed reporting",
            ActionType.REQUEST_APPROVAL: "High impact or low confidence requires human approval",
            ActionType.ESCALATE: "Critical situation requires escalation to higher authority",
            ActionType.DEFER: "Better to defer until more information is available"
        }

        reasoning_parts.append(f"Decision rationale: {action_reasons.get(action, 'Standard risk assessment applied')}")

        # Context considerations
        if context.user_context.get('availability') == 'busy':
            reasoning_parts.append("User is currently busy, minimizing interruptions")

        if context.system_state.get('cpu_usage', 0) > 80:
            reasoning_parts.append("High system load detected, considering resource constraints")

        return "; ".join(reasoning_parts)

    def _generate_alternatives(self, context: DecisionContext, primary_action: ActionType) -> list:
        """Generate alternative actions for consideration."""
        alternatives = []

        if primary_action == ActionType.REQUEST_APPROVAL:
            alternatives.append({
                'action': ActionType.EXECUTE_REPORT.value,
                'description': 'Execute with detailed monitoring and reporting',
                'risk_level': 'medium'
            })
            alternatives.append({
                'action': ActionType.DEFER.value,
                'description': 'Wait for better conditions or more information',
                'risk_level': 'low'
            })

        elif primary_action == ActionType.EXECUTE:
            alternatives.append({
                'action': ActionType.EXECUTE_NOTIFY.value,
                'description': 'Execute but notify user of the action',
                'risk_level': 'low'
            })

        return alternatives

    def _assess_risks(self, context: DecisionContext) -> Dict[str, Any]:
        """Assess various risk categories for the decision."""
        risks = {}

        for category, weight in self.risk_categories.items():
            risk_score = self._calculate_category_risk(category, context)
            risks[category] = {
                'score': risk_score,
                'weight': weight,
                'weighted_score': risk_score * weight
            }

        # Calculate overall risk
        overall_risk = sum(r['weighted_score'] for r in risks.values())
        risks['overall_risk'] = overall_risk
        risks['risk_level'] = self._categorize_risk_level(overall_risk)

        return risks

    def _calculate_category_risk(self, category: str, context: DecisionContext) -> float:
        """Calculate risk score for a specific category."""
        # This would implement specific risk calculations for each category
        # For demonstration, using simplified calculations

        if category == 'data_security':
            if context.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]:
                return 0.8
            elif context.impact_level == ImpactLevel.MEDIUM:
                return 0.5
            else:
                return 0.2

        elif category == 'system_stability':
            if 'restart' in context.task_name.lower() or 'reboot' in context.task_name.lower():
                return 0.9
            elif 'update' in context.task_name.lower() or 'install' in context.task_name.lower():
                return 0.6
            else:
                return 0.3

        elif category == 'user_privacy':
            if 'user' in context.task_name.lower() and 'data' in context.task_name.lower():
                return 0.7
            else:
                return 0.3

        elif category == 'financial_impact':
            if context.impact_level in [ImpactLevel.HIGH, ImpactLevel.CRITICAL]:
                return 0.8
            else:
                return 0.2

        elif category == 'reputation':
            return 0.4  # Moderate reputation risk for most actions

        elif category == 'compliance':
            if 'policy' in context.task_name.lower() or 'regulation' in context.task_name.lower():
                return 0.9
            else:
                return 0.3

        return 0.5  # Default moderate risk

    def _categorize_risk_level(self, risk_score: float) -> str:
        """Categorize overall risk level."""
        if risk_score >= 0.8:
            return 'critical'
        elif risk_score >= 0.6:
            return 'high'
        elif risk_score >= 0.4:
            return 'medium'
        else:
            return 'low'

    def _create_execution_plan(self, context: DecisionContext, action: ActionType) -> Optional[Dict[str, Any]]:
        """Create execution plan for the decision."""
        if action in [ActionType.EXECUTE, ActionType.EXECUTE_NOTIFY, ActionType.EXECUTE_REPORT]:
            return {
                'phases': [
                    {
                        'name': 'preparation',
                        'description': 'Prepare execution environment',
                        'estimated_duration': '2 minutes'
                    },
                    {
                        'name': 'execution',
                        'description': 'Execute the main task',
                        'estimated_duration': '5 minutes'
                    },
                    {
                        'name': 'verification',
                        'description': 'Verify successful completion',
                        'estimated_duration': '2 minutes'
                    },
                    {
                        'name': 'notification',
                        'description': 'Notify relevant parties',
                        'estimated_duration': '1 minute'
                    }
                ],
                'rollback_plan': 'Automated rollback available',
                'monitoring_requirements': ['resource_usage', 'error_rates', 'completion_status']
            }

        return None

    def _record_decision(self, context: DecisionContext, result: DecisionResult):
        """Record decision for learning and analysis."""
        decision_record = {
            'timestamp': context.timestamp,
            'task_type': context.task_name,
            'impact_level': context.impact_level.value,
            'confidence_level': context.confidence_level.value,
            'action_taken': result.action.value,
            'confidence_score': result.confidence_score,
            'risk_assessment': result.risk_assessment
        }

        self.decision_history.append(decision_record)

        # Keep only recent history
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-1000:]

def demo_risk_decision():
    """Demonstrate the risk decision matrix."""
    matrix = RiskDecisionMatrix()

    # Create sample decision context
    context = DecisionContext(
        task_id="demo_task_1",
        task_name="Install security update",
        impact_level=ImpactLevel.MEDIUM,
        confidence_level=ConfidenceLevel.HIGH,
        user_context={
            'expertise_level': 'intermediate',
            'availability': 'available',
            'autonomy_preference': 'high'
        },
        system_state={
            'cpu_usage': 45,
            'memory_available_gb': 8,
            'recent_errors': 0
        },
        historical_data={},
        timestamp=datetime.now()
    )

    print("Risk Decision Matrix Demo")
    print("=" * 50)

    # Make decision
    result = matrix.make_decision(context)

    print(f"Task: {context.task_name}")
    print(f"Impact Level: {context.impact_level.value}")
    print(f"Confidence Level: {context.confidence_level.value}")
    print(f"Decision: {result.action.value}")
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"Requires Approval: {result.requires_approval}")
    print(f"\nReasoning: {result.reasoning}")

    print(f"\nRisk Assessment:")
    for category, assessment in result.risk_assessment.items():
        if category not in ['overall_risk', 'risk_level']:
            print(f"  {category}: {assessment['score']:.2f} (weight: {assessment['weight']:.2f})")

    print(f"\nOverall Risk: {result.risk_assessment['overall_risk']:.2f} ({result.risk_assessment['risk_level']})")

if __name__ == "__main__":
    demo_risk_decision()
