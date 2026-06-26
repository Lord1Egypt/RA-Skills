#!/usr/bin/env python3
"""
Error Recovery - Execution Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Retry strategies and fallback mechanisms.
"""

import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
import threading
import uuid

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryStrategy(Enum):
    RETRY = "retry"
    ROLLBACK = "rollback"
    FALLBACK = "fallback"
    DEGRADE = "degrade"
    ESCALATE = "escalate"
    ABORT = "abort"

@dataclass
class ErrorContext:
    """Context information about an error."""
    error_id: str
    error_type: str
    error_message: str
    stack_trace: str
    timestamp: datetime
    operation: str
    parameters: Dict[str, Any]
    system_state: Dict[str, Any]
    user_context: Dict[str, Any]
    severity: ErrorSeverity

@dataclass
class RecoveryAction:
    """Represents a recovery action."""
    id: str
    name: str
    description: str
    strategy: RecoveryStrategy
    estimated_duration: float
    success_probability: float
    risk_level: float
    prerequisites: List[str]
    rollback_plan: Optional[str] = None

@dataclass
class RecoveryResult:
    """Result of a recovery attempt."""
    recovery_id: str
    original_error: ErrorContext
    actions_taken: List[RecoveryAction]
    success: bool
    result_message: str
    recovery_time: float
    system_state_after: Dict[str, Any]
    follow_up_required: bool
    follow_up_actions: List[str]

class ErrorRecoveryMechanism:
    """Advanced error recovery system with multiple recovery strategies."""

    def __init__(self):
        # Recovery action registry
        self.recovery_actions: Dict[str, RecoveryAction] = {}
        self._register_default_recovery_actions()

        # Error pattern database
        self.error_patterns: Dict[str, List[Dict[str, Any]]] = {}

        # Recovery history
        self.recovery_history: List[RecoveryResult] = []

        # Active recoveries tracking
        self.active_recoveries: Dict[str, RecoveryResult] = {}

        # Recovery configuration
        self.max_recovery_attempts = 3
        self.recovery_timeout = 300  # 5 minutes
        self.escalation_threshold = 2

        # Thread safety
        self.recovery_lock = threading.RLock()

    def _register_default_recovery_actions(self):
        """Register default recovery actions."""

        default_actions = [
            RecoveryAction(
                id="retry_with_backoff",
                name="Retry with Exponential Backoff",
                description="Retry the operation with increasing delays",
                strategy=RecoveryStrategy.RETRY,
                estimated_duration=30.0,
                success_probability=0.7,
                risk_level=0.1,
                prerequisites=["operation_idempotent"]
            ),
            RecoveryAction(
                id="rollback_transaction",
                name="Rollback Transaction",
                description="Rollback to previous stable state",
                strategy=RecoveryStrategy.ROLLBACK,
                estimated_duration=60.0,
                success_probability=0.9,
                risk_level=0.3,
                prerequisites=["rollback_point_available"],
                rollback_plan="Restore from backup if rollback fails"
            ),
            RecoveryAction(
                id="switch_to_fallback",
                name="Switch to Fallback Service",
                description="Use alternative service or method",
                strategy=RecoveryStrategy.FALLBACK,
                estimated_duration=45.0,
                success_probability=0.8,
                risk_level=0.2,
                prerequisites=["fallback_service_available"]
            ),
            RecoveryAction(
                id="degrade_functionality",
                name="Degrade Functionality",
                description="Provide reduced functionality mode",
                strategy=RecoveryStrategy.DEGRADE,
                estimated_duration=20.0,
                success_probability=0.95,
                risk_level=0.1,
                prerequisites=["degraded_mode_available"]
            ),
            RecoveryAction(
                id="escalate_to_human",
                name="Escalate to Human Operator",
                description="Notify human operator for manual intervention",
                strategy=RecoveryStrategy.ESCALATE,
                estimated_duration=120.0,
                success_probability=0.99,
                risk_level=0.0,
                prerequisites=["human_operator_available"]
            ),
            RecoveryAction(
                id="abort_operation",
                name="Abort Operation",
                description="Safely abort the current operation",
                strategy=RecoveryStrategy.ABORT,
                estimated_duration=10.0,
                success_probability=1.0,
                risk_level=0.5,
                prerequisites=["safe_abort_possible"]
            )
        ]

        for action in default_actions:
            self.recovery_actions[action.id] = action

    def detect_error(self, error: Exception, operation: str, parameters: Dict[str, Any],
                    system_state: Dict[str, Any], user_context: Dict[str, Any] = None) -> ErrorContext:
        """Detect and analyze an error to create error context."""

        error_id = str(uuid.uuid4())
        error_type = type(error).__name__
        error_message = str(error)
        stack_trace = traceback.format_exc()
        timestamp = datetime.now()

        # Determine error severity
        severity = self._assess_error_severity(error, operation, system_state)

        return ErrorContext(
            error_id=error_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            timestamp=timestamp,
            operation=operation,
            parameters=parameters or {},
            system_state=system_state or {},
            user_context=user_context or {},
            severity=severity
        )

    def _assess_error_severity(self, error: Exception, operation: str, system_state: Dict[str, Any]) -> ErrorSeverity:
        """Assess the severity of an error."""

        error_str = str(error).lower()
        operation_str = operation.lower()

        # Critical errors
        if any(keyword in error_str for keyword in ['critical', 'fatal', 'out of memory', 'disk full']):
            return ErrorSeverity.CRITICAL
        elif any(keyword in operation_str for keyword in ['payment', 'financial', 'security', 'authentication']):
            return ErrorSeverity.CRITICAL

        # High severity errors
        elif any(keyword in error_str for keyword in ['connection failed', 'timeout', 'permission denied']):
            return ErrorSeverity.HIGH
        elif any(keyword in operation_str for keyword in ['install', 'delete', 'modify', 'update']):
            return ErrorSeverity.HIGH

        # Medium severity errors
        elif any(keyword in error_str for keyword in ['retry', 'temporary', 'busy']):
            return ErrorSeverity.MEDIUM
        elif any(keyword in operation_str for keyword in ['read', 'fetch', 'query']):
            return ErrorSeverity.MEDIUM

        # Low severity errors
        else:
            return ErrorSeverity.LOW

    def select_recovery_strategy(self, error_context: ErrorContext) -> List[RecoveryAction]:
        """Select appropriate recovery strategies based on error context."""

        strategies = []

        # Check for known error patterns
        pattern_strategies = self._check_error_patterns(error_context)
        if pattern_strategies:
            strategies.extend(pattern_strategies)

        # Select strategies based on error severity
        severity_strategies = self._select_by_severity(error_context.severity)
        strategies.extend(severity_strategies)

        # Select strategies based on operation type
        operation_strategies = self._select_by_operation(error_context.operation)
        strategies.extend(operation_strategies)

        # Filter by prerequisites
        available_strategies = self._filter_by_prerequisites(strategies, error_context)

        # Sort by success probability and risk
        available_strategies.sort(key=lambda x: (x.success_probability, -x.risk_level), reverse=True)

        # Return top strategies
        return available_strategies[:3]  # Return top 3 strategies

    def _check_error_patterns(self, error_context: ErrorContext) -> List[RecoveryAction]:
        """Check for known error patterns and return appropriate strategies."""

        strategies = []
        error_signature = f"{error_context.error_type}:{error_context.operation}"

        if error_signature in self.error_patterns:
            pattern_data = self.error_patterns[error_signature]
            if pattern_data:
                # Get most successful strategy from history
                best_strategy = max(pattern_data, key=lambda x: x.get('success_rate', 0))
                strategy_id = best_strategy.get('strategy_id')
                if strategy_id in self.recovery_actions:
                    strategies.append(self.recovery_actions[strategy_id])

        return strategies

    def _select_by_severity(self, severity: ErrorSeverity) -> List[RecoveryAction]:
        """Select recovery strategies based on error severity."""

        if severity == ErrorSeverity.CRITICAL:
            return [
                self.recovery_actions['rollback_transaction'],
                self.recovery_actions['escalate_to_human'],
                self.recovery_actions['abort_operation']
            ]
        elif severity == ErrorSeverity.HIGH:
            return [
                self.recovery_actions['retry_with_backoff'],
                self.recovery_actions['switch_to_fallback'],
                self.recovery_actions['rollback_transaction']
            ]
        elif severity == ErrorSeverity.MEDIUM:
            return [
                self.recovery_actions['retry_with_backoff'],
                self.recovery_actions['degrade_functionality'],
                self.recovery_actions['switch_to_fallback']
            ]
        else:  # LOW
            return [
                self.recovery_actions['retry_with_backoff'],
                self.recovery_actions['degrade_functionality']
            ]

    def _select_by_operation(self, operation: str) -> List[RecoveryAction]:
        """Select recovery strategies based on operation type."""

        operation_lower = operation.lower()

        if any(keyword in operation_lower for keyword in ['install', 'update', 'modify']):
            return [self.recovery_actions['rollback_transaction']]
        elif any(keyword in operation_lower for keyword in ['network', 'api', 'service']):
            return [
                self.recovery_actions['retry_with_backoff'],
                self.recovery_actions['switch_to_fallback']
            ]
        elif any(keyword in operation_lower for keyword in ['read', 'query', 'fetch']):
            return [self.recovery_actions['degrade_functionality']]
        else:
            return [self.recovery_actions['retry_with_backoff']]

    def _filter_by_prerequisites(self, strategies: List[RecoveryAction], error_context: ErrorContext) -> List[RecoveryAction]:
        """Filter strategies based on available prerequisites."""

        available_strategies = []

        for strategy in strategies:
            if self._check_prerequisites(strategy.prerequisites, error_context):
                available_strategies.append(strategy)

        return available_strategies

    def _check_prerequisites(self, prerequisites: List[str], error_context: ErrorContext) -> bool:
        """Check if prerequisites are met for a recovery strategy."""

        for prerequisite in prerequisites:
            if prerequisite == "operation_idempotent":
                # Check if operation can be safely retried
                return error_context.operation.lower() not in ['payment', 'delete', 'financial']
            elif prerequisite == "rollback_point_available":
                # Check if system state supports rollback
                return error_context.system_state.get('rollback_available', False)
            elif prerequisite == "fallback_service_available":
                # Check if fallback services are available
                return error_context.system_state.get('fallback_available', True)
            elif prerequisite == "degraded_mode_available":
                # Check if degraded mode is available
                return True  # Assume always available for demo
            elif prerequisite == "human_operator_available":
                # Check if human operator can be notified
                return error_context.user_context.get('notifications_enabled', True)
            elif prerequisite == "safe_abort_possible":
                # Check if operation can be safely aborted
                return True  # Assume always possible for demo

        return True

    def execute_recovery(self, error_context: ErrorContext, strategies: List[RecoveryAction] = None) -> RecoveryResult:
        """Execute recovery using selected strategies."""

        with self.recovery_lock:
            recovery_id = str(uuid.uuid4())
            start_time = time.time()

            if not strategies:
                strategies = self.select_recovery_strategy(error_context)

            actions_taken = []
            success = False
            result_message = ""

            for strategy in strategies:
                try:
                    action_result = self._execute_recovery_action(strategy, error_context)
                    actions_taken.append(strategy)

                    if action_result['success']:
                        success = True
                        result_message = action_result['message']
                        break
                    else:
                        result_message = action_result['message']

                except Exception as e:
                    result_message = f"Recovery action {strategy.name} failed: {str(e)}"
                    continue

            recovery_time = time.time() - start_time

            # Create recovery result
            recovery_result = RecoveryResult(
                recovery_id=recovery_id,
                original_error=error_context,
                actions_taken=actions_taken,
                success=success,
                result_message=result_message,
                recovery_time=recovery_time,
                system_state_after=self._capture_system_state(),
                follow_up_required=not success,
                follow_up_actions=self._determine_follow_up_actions(success, error_context)
            )

            # Record recovery result
            self.recovery_history.append(recovery_result)
            if len(self.recovery_history) > 1000:
                self.recovery_history = self.recovery_history[-1000:]

            # Update error patterns
            self._update_error_patterns(error_context, strategies, success)

            return recovery_result

    def _execute_recovery_action(self, action: RecoveryAction, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute a specific recovery action."""

        action_handlers = {
            'retry_with_backoff': self._execute_retry_with_backoff,
            'rollback_transaction': self._execute_rollback,
            'switch_to_fallback': self._execute_fallback,
            'degrade_functionality': self._execute_degrade,
            'escalate_to_human': self._execute_escalate,
            'abort_operation': self._execute_abort
        }

        handler = action_handlers.get(action.id)
        if handler:
            return handler(error_context)
        else:
            return {'success': False, 'message': f'Unknown recovery action: {action.name}'}

    def _execute_retry_with_backoff(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute retry with exponential backoff."""
        # Simulate retry logic
        import random
        success_probability = 0.7

        if random.random() < success_probability:
            return {'success': True, 'message': 'Operation succeeded on retry'}
        else:
            return {'success': False, 'message': 'Retry failed, operation still not working'}

    def _execute_rollback(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute rollback to previous state."""
        # Simulate rollback logic
        return {'success': True, 'message': 'Successfully rolled back to previous stable state'}

    def _execute_fallback(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute fallback to alternative service."""
        # Simulate fallback logic
        return {'success': True, 'message': 'Switched to fallback service successfully'}

    def _execute_degrade(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute functionality degradation."""
        # Simulate degradation logic
        return {'success': True, 'message': 'Operating in degraded mode'}

    def _execute_escalate(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute escalation to human operator."""
        # Simulate escalation logic
        return {'success': True, 'message': 'Escalated to human operator for manual intervention'}

    def _execute_abort(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Execute safe abort of operation."""
        # Simulate abort logic
        return {'success': True, 'message': 'Operation safely aborted'}

    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state after recovery."""
        return {
            'timestamp': datetime.now().isoformat(),
            'recovery_status': 'completed',
            'system_health': 'stable'
        }

    def _determine_follow_up_actions(self, success: bool, error_context: ErrorContext) -> List[str]:
        """Determine required follow-up actions."""

        if success:
            return [
                "Monitor system stability",
                "Verify operation completion",
                "Update error pattern database"
            ]
        else:
            return [
                "Investigate root cause",
                "Review system logs",
                "Consider system maintenance",
                "Update recovery strategies"
            ]

    def _update_error_patterns(self, error_context: ErrorContext, strategies: List[RecoveryAction], success: bool):
        """Update error pattern database with recovery results."""

        error_signature = f"{error_context.error_type}:{error_context.operation}"

        if error_signature not in self.error_patterns:
            self.error_patterns[error_signature] = []

        for strategy in strategies:
            pattern_record = {
                'strategy_id': strategy.id,
                'timestamp': datetime.now(),
                'success': success,
                'severity': error_context.severity.value
            }

            self.error_patterns[error_signature].append(pattern_record)

            # Keep only recent patterns
            if len(self.error_patterns[error_signature]) > 50:
                self.error_patterns[error_signature] = self.error_patterns[error_signature][-50:]

    def get_recovery_statistics(self) -> Dict[str, Any]:
        """Get recovery statistics and insights."""

        if not self.recovery_history:
            return {'status': 'no_data'}

        total_recoveries = len(self.recovery_history)
        successful_recoveries = len([r for r in self.recovery_history if r.success])
        success_rate = successful_recoveries / total_recoveries if total_recoveries > 0 else 0

        # Calculate average recovery time
        recovery_times = [r.recovery_time for r in self.recovery_history if r.recovery_time]
        avg_recovery_time = sum(recovery_times) / len(recovery_times) if recovery_times else 0

        # Most common error types
        error_types = {}
        for recovery in self.recovery_history:
            error_type = recovery.original_error.error_type
            error_types[error_type] = error_types.get(error_type, 0) + 1

        # Most effective recovery actions
        action_effectiveness = {}
        for recovery in self.recovery_history:
            for action in recovery.actions_taken:
                if action.id not in action_effectiveness:
                    action_effectiveness[action.id] = {'total': 0, 'successful': 0}
                action_effectiveness[action.id]['total'] += 1
                if recovery.success:
                    action_effectiveness[action.id]['successful'] += 1

        return {
            'total_recoveries': total_recoveries,
            'successful_recoveries': successful_recoveries,
            'success_rate': success_rate,
            'average_recovery_time': avg_recovery_time,
            'most_common_errors': error_types,
            'action_effectiveness': action_effectiveness,
            'error_patterns_count': len(self.error_patterns)
        }

def demo_error_recovery():
    """Demonstrate the error recovery mechanism."""
    recovery_system = ErrorRecoveryMechanism()

    print("Error Recovery Mechanism Demo")
    print("=" * 50)

    # Simulate different types of errors
    test_errors = [
        (ConnectionError("Network connection failed"), "download_files", {}),
        (ValueError("Invalid configuration"), "load_config", {}),
        (MemoryError("Out of memory"), "process_large_dataset", {}),
        (PermissionError("Access denied"), "write_to_file", {})
    ]

    for i, (error, operation, params) in enumerate(test_errors, 1):
        print(f"\n--- Test {i}: {type(error).__name__} ---")

        # Create error context
        error_context = recovery_system.detect_error(
            error=error,
            operation=operation,
            parameters=params,
            system_state={'rollback_available': True, 'fallback_available': True}
        )

        print(f"Error: {error_context.error_message}")
        print(f"Severity: {error_context.severity.value}")
        print(f"Operation: {error_context.operation}")

        # Select recovery strategies
        strategies = recovery_system.select_recovery_strategy(error_context)
        print(f"Selected strategies: {[s.name for s in strategies]}")

        # Execute recovery
        result = recovery_system.execute_recovery(error_context, strategies)

        print(f"Recovery result: {'SUCCESS' if result.success else 'FAILED'}")
        print(f"Recovery time: {result.recovery_time:.2f}s")
        print(f"Message: {result.result_message}")

        if result.follow_up_actions:
            print(f"Follow-up actions: {result.follow_up_actions}")

    # Show statistics
    stats = recovery_system.get_recovery_statistics()
    print(f"\n" + "=" * 50)
    print("Recovery Statistics:")
    print(f"Total recoveries: {stats['total_recoveries']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    print(f"Average recovery time: {stats['average_recovery_time']:.2f}s")

if __name__ == "__main__":
    demo_error_recovery()
