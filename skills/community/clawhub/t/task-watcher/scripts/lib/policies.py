"""Policy interface and implementations for notification decisions."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime

try:
    from .models import CallbackTask, StateResult, TaskState
except ImportError:
    from models import CallbackTask, StateResult, TaskState


class CallbackPolicy(ABC):
    """
    Abstract interface for callback policies.

    Policies decide:
    - When to notify
    - When to close tasks
    - When to retry delivery
    - When to escalate
    - Next check interval
    """

    @abstractmethod
    def should_notify(self, task: CallbackTask, state_result: StateResult) -> bool:
        """
        Decide if notification should be sent.

        Args:
            task: Current task state
            state_result: Latest state check result

        Returns:
            True if notification should be sent
        """
        pass

    @abstractmethod
    def should_close(self, task: CallbackTask, state_result: StateResult) -> bool:
        """
        Decide if task should be closed (terminal state).

        Args:
            task: Current task state
            state_result: Latest state check result

        Returns:
            True if task should be closed
        """
        pass

    @abstractmethod
    def should_retry_delivery(self, task: CallbackTask) -> bool:
        """
        Decide if delivery should be retried.

        Args:
            task: Current task state

        Returns:
            True if delivery should be retried
        """
        pass

    @abstractmethod
    def should_escalate(self, task: CallbackTask) -> bool:
        """
        Decide if task should be escalated to main agent.

        Args:
            task: Current task state

        Returns:
            True if task should be escalated
        """
        pass

    @abstractmethod
    def next_interval(self, task: CallbackTask) -> int:
        """
        Get next check interval in seconds.

        Args:
            task: Current task state

        Returns:
            Seconds until next check
        """
        pass


class DefaultCallbackPolicy(CallbackPolicy):
    """
    Default callback policy implementation.

    Rules:
    - Notify on state changes
    - Notify on terminal states
    - Don't notify for same state twice
    - Retry delivery up to max_attempts
    - Escalate after max_delivery_failures or timeout
    - Fixed 3-minute interval (MVP simplification)
    """

    def __init__(
        self,
        max_delivery_attempts: int = 3,
        max_task_age_hours: int = 24,
        default_interval_seconds: int = 180  # 3 minutes
    ):
        """
        Initialize default policy.

        Args:
            max_delivery_attempts: Max delivery retries before escalation
            max_task_age_hours: Max task age before timeout
            default_interval_seconds: Default check interval
        """
        self.max_delivery_attempts = max_delivery_attempts
        self.max_task_age_hours = max_task_age_hours
        self.default_interval_seconds = default_interval_seconds

    def should_notify(self, task: CallbackTask, state_result: StateResult) -> bool:
        """
        Decide if notification should be sent.

        Notify when:
        1. State changed from last notification
        2. Task is terminal and not yet delivered
        3. This is first check (delivery_attempts == 0)
        """
        # First notification on task creation
        if task.delivery_attempts == 0:
            return True

        # State changed
        if task.current_state != task.last_notified_state:
            return True

        # Terminal state not yet delivered
        if task.terminal and not task.callback_delivered:
            return True

        return False

    def should_close(self, task: CallbackTask, state_result: StateResult) -> bool:
        """
        Decide if task should be closed.

        Close when:
        1. State result indicates terminal state
        2. Task is expired (timeout)
        3. Max delivery attempts exceeded
        """
        # State adapter says it's terminal
        if state_result.terminal:
            return True

        # Task is expired
        if task.is_expired():
            return True

        # Terminal state already delivered
        if task.terminal and task.callback_delivered:
            return True

        return False

    def should_retry_delivery(self, task: CallbackTask) -> bool:
        """
        Decide if delivery should be retried.

        Retry when:
        1. Not yet delivered
        2. Under max attempts
        3. Not terminal (keep trying for terminal states)
        """
        if task.callback_delivered:
            return False

        if task.delivery_attempts >= self.max_delivery_attempts:
            return False

        # Always retry for terminal states up to max attempts
        if task.terminal:
            return True

        # Retry state change notifications once
        if task.delivery_attempts == 0:
            return True

        return False

    def should_escalate(self, task: CallbackTask) -> bool:
        """
        Decide if task should be escalated.

        Escalate when:
        1. Delivery failed max times
        2. Task expired and not properly closed
        3. State check repeatedly fails
        """
        # Delivery failed too many times
        if task.delivery_attempts >= self.max_delivery_attempts and not task.callback_delivered:
            return True

        # Task expired but not closed
        if task.is_expired() and not task.terminal:
            return True

        # Check for old tasks that are stuck
        if task.expires_at:
            try:
                expires = datetime.fromisoformat(task.expires_at)
                now = datetime.now()
                # Escalate if expired by more than 1 hour
                if (now - expires).total_seconds() > 3600 and not task.terminal:
                    return True
            except (ValueError, TypeError):
                pass

        return False

    def next_interval(self, task: CallbackTask) -> int:
        """
        Get next check interval.

        MVP: Fixed interval, no backoff.
        Future: Could implement backoff based on task age/priority.
        """
        # Terminal and delivered - no more checks needed
        if task.terminal and task.callback_delivered:
            return 0

        # Terminal but not delivered - check sooner
        if task.terminal and not task.callback_delivered:
            return 60  # 1 minute

        # High priority tasks check more frequently
        if task.priority == "critical":
            return 60  # 1 minute
        if task.priority == "high":
            return 120  # 2 minutes

        return self.default_interval_seconds

    def build_payload(self, task: CallbackTask, state_result: StateResult) -> Dict[str, Any]:
        """
        Build notification payload.

        Compatible with policy.py pattern.

        Args:
            task: Current task state
            state_result: Latest state check result

        Returns:
            Payload dict with 'text' and 'terminal' keys
        """
        next_state = state_result.state
        if state_result.terminal:
            text = (
                "监控任务已完成。\n"
                f"- task_id: {task.task_id}\n"
                f"- 最终状态: {next_state}\n"
                f"- 下一步: {self._next_action(next_state)}"
            )
            return {"text": text, "terminal": True}

        text = (
            "监控状态更新。\n"
            f"- task_id: {task.task_id}\n"
            f"- 状态变化: {task.current_state} -> {next_state}"
        )
        return {"text": text, "terminal": False}

    def _next_action(self, state: str) -> str:
        """Get recommended next action for terminal state."""
        if state == "approved":
            return "可继续跟首评/首小时数据"
        if state == "rejected":
            return "建议人工检查原因并改稿后重发"
        if state == "timeout":
            return "建议人工检查平台状态或登录态"
        return "请查看任务详情"


class AggressiveNotifyPolicy(CallbackPolicy):
    """
    Policy that notifies on every check (useful for testing).
    """

    def __init__(self, max_delivery_attempts: int = 10):
        self.max_delivery_attempts = max_delivery_attempts

    def should_notify(self, task: CallbackTask, state_result: StateResult) -> bool:
        return True

    def should_close(self, task: CallbackTask, state_result: StateResult) -> bool:
        return state_result.terminal

    def should_retry_delivery(self, task: CallbackTask) -> bool:
        return not task.callback_delivered and task.delivery_attempts < self.max_delivery_attempts

    def should_escalate(self, task: CallbackTask) -> bool:
        return task.delivery_attempts >= self.max_delivery_attempts

    def next_interval(self, task: CallbackTask) -> int:
        return 60  # 1 minute


class ConservativePolicy(CallbackPolicy):
    """
    Conservative policy that only notifies on terminal states.
    """

    def __init__(
        self,
        max_delivery_attempts: int = 5,
        max_task_age_hours: int = 48
    ):
        self.max_delivery_attempts = max_delivery_attempts
        self.max_task_age_hours = max_task_age_hours

    def should_notify(self, task: CallbackTask, state_result: StateResult) -> bool:
        # Only notify on terminal states
        return state_result.terminal or (task.terminal and not task.callback_delivered)

    def should_close(self, task: CallbackTask, state_result: StateResult) -> bool:
        return state_result.terminal or task.is_expired()

    def should_retry_delivery(self, task: CallbackTask) -> bool:
        return (
            task.terminal
            and not task.callback_delivered
            and task.delivery_attempts < self.max_delivery_attempts
        )

    def should_escalate(self, task: CallbackTask) -> bool:
        return task.delivery_attempts >= self.max_delivery_attempts

    def next_interval(self, task: CallbackTask) -> int:
        if task.terminal:
            return 300  # 5 minutes for terminal tasks
        return 600  # 10 minutes for active tasks


class DictPolicyAdapter:
    """
    Adapter for using policies with plain dicts (monitor script compatibility).

    Wraps a CallbackPolicy to work with dict-based tasks from monitor scripts.
    """

    def __init__(self, policy: Optional[CallbackPolicy] = None):
        """
        Initialize with optional policy.

        Args:
            policy: CallbackPolicy to wrap (default: DefaultCallbackPolicy)
        """
        self.policy = policy or DefaultCallbackPolicy()

    def should_notify(self, task_dict: Dict[str, Any], state_result_dict: Dict[str, Any]) -> bool:
        """
        Decide if notification should be sent.

        Args:
            task_dict: Task as plain dict
            state_result_dict: State result as plain dict

        Returns:
            True if notification should be sent
        """
        task = CallbackTask.from_dict(task_dict)
        state_result = StateResult.from_dict(state_result_dict)
        return self.policy.should_notify(task, state_result)

    def should_close(self, task_dict: Dict[str, Any], state_result_dict: Dict[str, Any]) -> bool:
        """
        Decide if task should be closed.

        Args:
            task_dict: Task as plain dict
            state_result_dict: State result as plain dict

        Returns:
            True if task should be closed
        """
        task = CallbackTask.from_dict(task_dict)
        state_result = StateResult.from_dict(state_result_dict)
        return self.policy.should_close(task, state_result)

    def build_payload(self, task_dict: Dict[str, Any], state_result_dict: Dict[str, Any]) -> Dict[str, str]:
        """
        Build notification payload.

        Args:
            task_dict: Task as plain dict
            state_result_dict: State result as plain dict

        Returns:
            Payload dict with 'text' and 'terminal' keys
        """
        task = CallbackTask.from_dict(task_dict)
        state_result = StateResult.from_dict(state_result_dict)
        return self.policy.build_payload(task, state_result)
