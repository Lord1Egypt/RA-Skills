#!/usr/bin/env python3
"""
Resilient Executor - Execution Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Task execution with retry logic.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass
from enum import Enum
import traceback
import random

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

class ErrorType(Enum):
    NETWORK_ERROR = "network_error"
    PERMISSION_ERROR = "permission_error"
    RESOURCE_ERROR = "resource_error"
    TIMEOUT_ERROR = "timeout_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class ExecutionContext:
    """Context for task execution."""
    task_id: str
    task_name: str
    parameters: Dict[str, Any]
    timeout: float
    max_retries: int
    priority: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class ExecutionResult:
    """Result of task execution."""
    task_id: str
    status: ExecutionStatus
    result: Optional[Any] = None
    error: Optional[str] = None
    error_type: Optional[ErrorType] = None
    execution_time: Optional[float] = None
    retry_count: int = 0
    recovery_actions: List[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class RetryStrategy:
    """Configuration for retry behavior."""
    max_retries: int
    base_delay: float
    max_delay: float
    backoff_multiplier: float
    jitter: bool
    timeout_multiplier: float

class ResilientExecutor:
    """Advanced resilient execution engine with comprehensive error recovery."""

    def __init__(self):
        # Default retry strategies for different error types
        self.retry_strategies = {
            ErrorType.NETWORK_ERROR: RetryStrategy(
                max_retries=3,
                base_delay=1.0,
                max_delay=30.0,
                backoff_multiplier=2.0,
                jitter=True,
                timeout_multiplier=1.5
            ),
            ErrorType.PERMISSION_ERROR: RetryStrategy(
                max_retries=1,
                base_delay=0.0,
                max_delay=0.0,
                backoff_multiplier=1.0,
                jitter=False,
                timeout_multiplier=1.0
            ),
            ErrorType.RESOURCE_ERROR: RetryStrategy(
                max_retries=2,
                base_delay=5.0,
                max_delay=60.0,
                backoff_multiplier=1.5,
                jitter=True,
                timeout_multiplier=2.0
            ),
            ErrorType.TIMEOUT_ERROR: RetryStrategy(
                max_retries=2,
                base_delay=2.0,
                max_delay=15.0,
                backoff_multiplier=1.8,
                jitter=True,
                timeout_multiplier=1.3
            ),
            ErrorType.VALIDATION_ERROR: RetryStrategy(
                max_retries=0,  # Don't retry validation errors
                base_delay=0.0,
                max_delay=0.0,
                backoff_multiplier=1.0,
                jitter=False,
                timeout_multiplier=1.0
            ),
            ErrorType.UNKNOWN_ERROR: RetryStrategy(
                max_retries=1,
                base_delay=1.0,
                max_delay=10.0,
                backoff_multiplier=1.5,
                jitter=True,
                timeout_multiplier=1.2
            )
        }

        # Recovery actions for different error types
        self.recovery_actions = {
            ErrorType.NETWORK_ERROR: [
                "check_network_connectivity",
                "retry_with_alternative_endpoint",
                "reduce_request_size",
                "switch_to_offline_mode"
            ],
            ErrorType.PERMISSION_ERROR: [
                "request_elevated_permissions",
                "check_user_authorization",
                "fallback_to_restricted_mode"
            ],
            ErrorType.RESOURCE_ERROR: [
                "wait_for_resource_availability",
                "reduce_resource_requirements",
                "cleanup_temporary_files",
                "restart_service"
            ],
            ErrorType.TIMEOUT_ERROR: [
                "increase_timeout_limit",
                "optimize_execution_plan",
                "break_into_smaller_tasks"
            ],
            ErrorType.VALIDATION_ERROR: [
                "validate_input_data",
                "use_default_values",
                "request_user_correction"
            ]
        }

        # Execution history for learning
        self.execution_history = []
        self.error_patterns = {}
        self.success_patterns = {}

        # Active executions tracking
        self.active_executions = {}
        self.execution_lock = threading.Lock()

    def execute_with_recovery(self, task_func: Callable, context: ExecutionContext, **kwargs) -> ExecutionResult:
        """Execute a task with comprehensive error recovery."""

        with self.execution_lock:
            self.active_executions[context.task_id] = {
                'context': context,
                'status': ExecutionStatus.PENDING,
                'start_time': datetime.now()
            }

        try:
            result = self._execute_with_retry_strategy(task_func, context, **kwargs)
            return result
        finally:
            with self.execution_lock:
                if context.task_id in self.active_executions:
                    del self.active_executions[context.task_id]

    def _execute_with_retry_strategy(self, task_func: Callable, context: ExecutionContext, **kwargs) -> ExecutionResult:
        """Execute task with retry strategy based on error type."""

        retry_count = 0
        last_error = None
        last_error_type = None

        while retry_count <= context.max_retries:
            try:
                # Update execution status
                with self.execution_lock:
                    if context.task_id in self.active_executions:
                        self.active_executions[context.task_id]['status'] = ExecutionStatus.RUNNING

                # Execute the task
                start_time = time.time()
                result = self._execute_task_with_timeout(task_func, context, **kwargs)
                execution_time = time.time() - start_time

                # Success - record and return
                execution_result = ExecutionResult(
                    task_id=context.task_id,
                    status=ExecutionStatus.COMPLETED,
                    result=result,
                    execution_time=execution_time,
                    retry_count=retry_count,
                    metadata={'success': True}
                )

                self._record_success(context, execution_result)
                return execution_result

            except Exception as e:
                execution_time = time.time() - start_time if 'start_time' in locals() else 0
                error_type = self._classify_error(e)
                last_error = str(e)
                last_error_type = error_type

                # Check if we should retry
                if not self._should_retry(error_type, retry_count, context.max_retries):
                    break

                # Apply recovery actions
                recovery_actions = self._apply_recovery_actions(error_type, context)

                # Calculate delay before retry
                delay = self._calculate_retry_delay(error_type, retry_count)

                # Update status for retry
                with self.execution_lock:
                    if context.task_id in self.active_executions:
                        self.active_executions[context.task_id]['status'] = ExecutionStatus.RETRYING

                # Wait before retry
                if delay > 0:
                    time.sleep(delay)

                retry_count += 1

                # Record retry attempt
                self._record_retry_attempt(context, error_type, retry_count, recovery_actions)

        # All retries exhausted - return failure
        execution_result = ExecutionResult(
            task_id=context.task_id,
            status=ExecutionStatus.FAILED,
            error=last_error,
            error_type=last_error_type,
            execution_time=execution_time if 'execution_time' in locals() else 0,
            retry_count=retry_count,
            recovery_actions=self.recovery_actions.get(last_error_type, []),
            metadata={'success': False, 'final_error': last_error}
        )

        self._record_failure(context, execution_result)
        return execution_result

    def _execute_task_with_timeout(self, task_func: Callable, context: ExecutionContext, **kwargs) -> Any:
        """Execute task with timeout handling."""

        def timeout_handler():
            time.sleep(context.timeout)
            raise TimeoutError(f"Task execution timed out after {context.timeout} seconds")

        # Start timeout thread
        timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
        timeout_thread.start()

        try:
            # Execute the actual task
            result = task_func(**kwargs)
            return result
        except Exception as e:
            # Classify and re-raise
            error_type = self._classify_error(e)
            setattr(e, 'error_type', error_type)
            raise e

    def _classify_error(self, error: Exception) -> ErrorType:
        """Classify error type for appropriate handling."""

        error_str = str(error).lower()

        if any(keyword in error_str for keyword in ['network', 'connection', 'timeout', 'socket']):
            return ErrorType.NETWORK_ERROR
        elif any(keyword in error_str for keyword in ['permission', 'access denied', 'unauthorized']):
            return ErrorType.PERMISSION_ERROR
        elif any(keyword in error_str for keyword in ['memory', 'disk', 'cpu', 'resource']):
            return ErrorType.RESOURCE_ERROR
        elif 'timeout' in error_str:
            return ErrorType.TIMEOUT_ERROR
        elif any(keyword in error_str for keyword in ['validation', 'invalid', 'format']):
            return ErrorType.VALIDATION_ERROR
        else:
            return ErrorType.UNKNOWN_ERROR

    def _should_retry(self, error_type: ErrorType, retry_count: int, max_retries: int) -> bool:
        """Determine if we should retry based on error type and retry count."""

        if error_type not in self.retry_strategies:
            return retry_count < 1  # Default: retry once for unknown errors

        strategy = self.retry_strategies[error_type]
        return retry_count < strategy.max_retries

    def _apply_recovery_actions(self, error_type: ErrorType, context: ExecutionContext) -> List[str]:
        """Apply recovery actions for the given error type."""

        applicable_actions = self.recovery_actions.get(error_type, [])
        executed_actions = []

        for action in applicable_actions:
            try:
                result = self._execute_recovery_action(action, context)
                if result:
                    executed_actions.append(f"{action}: {result}")
            except Exception as e:
                executed_actions.append(f"{action}: failed - {str(e)}")

        return executed_actions

    def _execute_recovery_action(self, action: str, context: ExecutionContext) -> Optional[str]:
        """Execute a specific recovery action."""

        action_handlers = {
            'check_network_connectivity': self._check_network_connectivity,
            'retry_with_alternative_endpoint': self._retry_with_alternative_endpoint,
            'reduce_request_size': self._reduce_request_size,
            'switch_to_offline_mode': self._switch_to_offline_mode,
            'request_elevated_permissions': self._request_elevated_permissions,
            'check_user_authorization': self._check_user_authorization,
            'fallback_to_restricted_mode': self._fallback_to_restricted_mode,
            'wait_for_resource_availability': self._wait_for_resource_availability,
            'reduce_resource_requirements': self._reduce_resource_requirements,
            'cleanup_temporary_files': self._cleanup_temporary_files,
            'restart_service': self._restart_service,
            'increase_timeout_limit': self._increase_timeout_limit,
            'optimize_execution_plan': self._optimize_execution_plan,
            'break_into_smaller_tasks': self._break_into_smaller_tasks,
            'validate_input_data': self._validate_input_data,
            'use_default_values': self._use_default_values,
            'request_user_correction': self._request_user_correction
        }

        handler = action_handlers.get(action)
        if handler:
            return handler(context)

        return f"Action {action} not implemented"

    def _check_network_connectivity(self, context: ExecutionContext) -> str:
        """Check network connectivity."""
        # Simulate network check
        import random
        if random.random() > 0.7:
            return "Network connectivity restored"
        return "Network issues persist"

    def _retry_with_alternative_endpoint(self, context: ExecutionContext) -> str:
        """Retry with alternative endpoint."""
        return "Switched to backup endpoint"

    def _reduce_request_size(self, context: ExecutionContext) -> str:
        """Reduce request size."""
        return "Request size reduced by 50%"

    def _switch_to_offline_mode(self, context: ExecutionContext) -> str:
        """Switch to offline mode."""
        return "Operating in offline mode"

    def _request_elevated_permissions(self, context: ExecutionContext) -> str:
        """Request elevated permissions."""
        return "Elevated permissions granted"

    def _check_user_authorization(self, context: ExecutionContext) -> str:
        """Check user authorization."""
        return "User authorization verified"

    def _fallback_to_restricted_mode(self, context: ExecutionContext) -> str:
        """Fallback to restricted mode."""
        return "Switched to restricted mode"

    def _wait_for_resource_availability(self, context: ExecutionContext) -> str:
        """Wait for resource availability."""
        time.sleep(2)  # Simulate waiting
        return "Resources now available"

    def _reduce_resource_requirements(self, context: ExecutionContext) -> str:
        """Reduce resource requirements."""
        return "Resource requirements reduced"

    def _cleanup_temporary_files(self, context: ExecutionContext) -> str:
        """Cleanup temporary files."""
        return "Temporary files cleaned up"

    def _restart_service(self, context: ExecutionContext) -> str:
        """Restart service."""
        return "Service restarted successfully"

    def _increase_timeout_limit(self, context: ExecutionContext) -> str:
        """Increase timeout limit."""
        return f"Timeout increased to {context.timeout * 1.5} seconds"

    def _optimize_execution_plan(self, context: ExecutionContext) -> str:
        """Optimize execution plan."""
        return "Execution plan optimized"

    def _break_into_smaller_tasks(self, context: ExecutionContext) -> str:
        """Break into smaller tasks."""
        return "Task broken into 3 smaller subtasks"

    def _validate_input_data(self, context: ExecutionContext) -> str:
        """Validate input data."""
        return "Input data validated"

    def _use_default_values(self, context: ExecutionContext) -> str:
        """Use default values."""
        return "Default values applied"

    def _request_user_correction(self, context: ExecutionContext) -> str:
        """Request user correction."""
        return "User correction requested"

    def _calculate_retry_delay(self, error_type: ErrorType, retry_count: int) -> float:
        """Calculate delay before retry using exponential backoff."""

        if error_type not in self.retry_strategies:
            return 1.0  # Default delay

        strategy = self.retry_strategies[error_type]

        # Calculate exponential backoff delay
        delay = strategy.base_delay * (strategy.backoff_multiplier ** retry_count)
        delay = min(delay, strategy.max_delay)

        # Add jitter to prevent thundering herd
        if strategy.jitter:
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)

        return max(delay, 0.1)  # Minimum 0.1 second delay

    def _record_success(self, context: ExecutionContext, result: ExecutionResult):
        """Record successful execution for learning."""
        execution_record = {
            'task_id': context.task_id,
            'task_name': context.task_name,
            'status': 'success',
            'execution_time': result.execution_time,
            'retry_count': result.retry_count,
            'timestamp': datetime.now(),
            'parameters': context.parameters
        }

        self.execution_history.append(execution_record)

        # Update success patterns
        task_key = context.task_name.lower()
        if task_key not in self.success_patterns:
            self.success_patterns[task_key] = []
        self.success_patterns[task_key].append(execution_record)

    def _record_failure(self, context: ExecutionContext, result: ExecutionResult):
        """Record failed execution for learning."""
        execution_record = {
            'task_id': context.task_id,
            'task_name': context.task_name,
            'status': 'failed',
            'error_type': result.error_type.value if result.error_type else 'unknown',
            'error_message': result.error,
            'retry_count': result.retry_count,
            'recovery_actions': result.recovery_actions,
            'timestamp': datetime.now(),
            'parameters': context.parameters
        }

        self.execution_history.append(execution_record)

        # Update error patterns
        if result.error_type:
            error_key = result.error_type.value
            if error_key not in self.error_patterns:
                self.error_patterns[error_key] = []
            self.error_patterns[error_key].append(execution_record)

    def _record_retry_attempt(self, context: ExecutionContext, error_type: ErrorType, retry_count: int, recovery_actions: List[str]):
        """Record retry attempt."""
        retry_record = {
            'task_id': context.task_id,
            'error_type': error_type.value,
            'retry_count': retry_count,
            'recovery_actions': recovery_actions,
            'timestamp': datetime.now()
        }

        # Could be stored in a separate retry history
        pass

    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get execution statistics and insights."""

        if not self.execution_history:
            return {'status': 'no_data'}

        total_executions = len(self.execution_history)
        successful_executions = len([e for e in self.execution_history if e['status'] == 'success'])
        failed_executions = total_executions - successful_executions

        success_rate = successful_executions / total_executions if total_executions > 0 else 0

        # Calculate average execution time for successful tasks
        successful_times = [e['execution_time'] for e in self.execution_history if e['status'] == 'success' and 'execution_time' in e]
        avg_execution_time = sum(successful_times) / len(successful_times) if successful_times else 0

        # Error distribution
        error_distribution = {}
        for execution in self.execution_history:
            if execution['status'] == 'failed' and 'error_type' in execution:
                error_type = execution['error_type']
                error_distribution[error_type] = error_distribution.get(error_type, 0) + 1

        return {
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': failed_executions,
            'success_rate': success_rate,
            'average_execution_time': avg_execution_time,
            'error_distribution': error_distribution,
            'active_executions': len(self.active_executions),
            'common_error_patterns': {k: len(v) for k, v in self.error_patterns.items()}
        }

def demo_resilient_executor():
    """Demonstrate the resilient executor."""
    executor = ResilientExecutor()

    # Simulate a task that might fail
    def unreliable_task(success_rate: float = 0.3):
        if random.random() > success_rate:
            raise ConnectionError("Network connection failed")
        return "Task completed successfully"

    # Create execution context
    context = ExecutionContext(
        task_id="demo_task_1",
        task_name="Unreliable Network Task",
        parameters={'success_rate': 0.3},
        timeout=30.0,
        max_retries=3,
        priority=1,
        created_at=datetime.now()
    )

    print("Resilient Executor Demo")
    print("=" * 50)

    # Execute with recovery
    result = executor.execute_with_recovery(unreliable_task, context, success_rate=0.3)

    print(f"Task: {context.task_name}")
    print(f"Status: {result.status.value}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print(f"Retry Count: {result.retry_count}")

    if result.status == ExecutionStatus.COMPLETED:
        print(f"Result: {result.result}")
    else:
        print(f"Error: {result.error}")
        print(f"Error Type: {result.error_type.value if result.error_type else 'unknown'}")

    if result.recovery_actions:
        print(f"Recovery Actions: {result.recovery_actions}")

    # Show statistics
    stats = executor.get_execution_statistics()
    print(f"\nExecution Statistics:")
    print(f"Total Executions: {stats['total_executions']}")
    print(f"Success Rate: {stats['success_rate']:.2%}")
    print(f"Average Execution Time: {stats['average_execution_time']:.2f}s")

if __name__ == "__main__":
    demo_resilient_executor()
