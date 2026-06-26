"""Unit tests for task callback bus policies."""

import pytest
from datetime import datetime, timedelta

from models import CallbackTask, StateResult, TaskState
from policies import (
    DefaultCallbackPolicy,
    AggressiveNotifyPolicy,
    ConservativePolicy,
)


class TestDefaultCallbackPolicy:
    """Tests for DefaultCallbackPolicy."""

    @pytest.fixture
    def policy(self):
        """Create policy instance."""
        return DefaultCallbackPolicy()

    @pytest.fixture
    def sample_task(self):
        """Create sample task."""
        return CallbackTask(
            task_id="tsk_test",
            current_state=TaskState.REVIEWING,
            last_notified_state=TaskState.SUBMITTED,
            delivery_attempts=1
        )

    def test_should_notify_first_time(self, policy):
        """Test should notify on first check (delivery_attempts=0)."""
        task = CallbackTask(
            task_id="tsk_test",
            current_state=TaskState.SUBMITTED,
            delivery_attempts=0
        )
        state_result = StateResult(state=TaskState.SUBMITTED)

        assert policy.should_notify(task, state_result) is True

    def test_should_notify_state_changed(self, policy, sample_task):
        """Test should notify when state changed."""
        state_result = StateResult(state=TaskState.REVIEWING)

        assert policy.should_notify(sample_task, state_result) is True

    def test_should_not_notify_same_state(self, policy):
        """Test should not notify when state unchanged."""
        task = CallbackTask(
            task_id="tsk_test",
            current_state=TaskState.REVIEWING,
            last_notified_state=TaskState.REVIEWING,
            delivery_attempts=1
        )
        state_result = StateResult(state=TaskState.REVIEWING)

        assert policy.should_notify(task, state_result) is False

    def test_should_notify_terminal_not_delivered(self, policy):
        """Test should notify when terminal and not delivered."""
        task = CallbackTask(
            task_id="tsk_test",
            current_state=TaskState.APPROVED,
            last_notified_state=TaskState.REVIEWING,
            terminal=True,
            callback_delivered=False,
            delivery_attempts=1
        )
        state_result = StateResult(state=TaskState.APPROVED, terminal=True)

        assert policy.should_notify(task, state_result) is True

    def test_should_close_terminal_state(self, policy):
        """Test should close when state result indicates terminal."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.APPROVED, terminal=True)

        assert policy.should_close(task, state_result) is True

    def test_should_close_expired(self, policy):
        """Test should close when task expired."""
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        task = CallbackTask(
            task_id="tsk_test",
            expires_at=past_time
        )
        state_result = StateResult(state=TaskState.SUBMITTED)

        assert policy.should_close(task, state_result) is True

    def test_should_close_already_delivered(self, policy):
        """Test should close when already delivered."""
        task = CallbackTask(
            task_id="tsk_test",
            terminal=True,
            callback_delivered=True
        )
        state_result = StateResult(state=TaskState.APPROVED)

        assert policy.should_close(task, state_result) is True

    def test_should_retry_delivery_not_delivered(self, policy):
        """Test should retry when not delivered."""
        task = CallbackTask(
            task_id="tsk_test",
            callback_delivered=False,
            delivery_attempts=0
        )

        assert policy.should_retry_delivery(task) is True

    def test_should_not_retry_already_delivered(self, policy):
        """Test should not retry when already delivered."""
        task = CallbackTask(
            task_id="tsk_test",
            callback_delivered=True,
            delivery_attempts=1
        )

        assert policy.should_retry_delivery(task) is False

    def test_should_not_retry_max_attempts(self, policy):
        """Test should not retry when max attempts reached."""
        task = CallbackTask(
            task_id="tsk_test",
            callback_delivered=False,
            delivery_attempts=3
        )

        assert policy.should_retry_delivery(task) is False

    def test_should_retry_terminal(self, policy):
        """Test should retry for terminal state."""
        task = CallbackTask(
            task_id="tsk_test",
            terminal=True,
            callback_delivered=False,
            delivery_attempts=2
        )

        assert policy.should_retry_delivery(task) is True

    def test_should_escalate_max_failures(self, policy):
        """Test should escalate after max delivery failures."""
        task = CallbackTask(
            task_id="tsk_test",
            callback_delivered=False,
            delivery_attempts=3
        )

        assert policy.should_escalate(task) is True

    def test_should_escalate_expired(self, policy):
        """Test should escalate when expired."""
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        task = CallbackTask(
            task_id="tsk_test",
            expires_at=past_time,
            terminal=False
        )

        assert policy.should_escalate(task) is True

    def test_should_not_escalate_healthy_task(self, policy):
        """Test should not escalate healthy task."""
        future_time = (datetime.now() + timedelta(hours=1)).isoformat()
        task = CallbackTask(
            task_id="tsk_test",
            expires_at=future_time,
            delivery_attempts=1,
            callback_delivered=False
        )

        assert policy.should_escalate(task) is False

    def test_next_interval_terminal_delivered(self, policy):
        """Test next interval for terminal delivered task."""
        task = CallbackTask(
            task_id="tsk_test",
            terminal=True,
            callback_delivered=True
        )

        assert policy.next_interval(task) == 0

    def test_next_interval_terminal_not_delivered(self, policy):
        """Test next interval for terminal not delivered task."""
        task = CallbackTask(
            task_id="tsk_test",
            terminal=True,
            callback_delivered=False
        )

        assert policy.next_interval(task) == 60

    def test_next_interval_critical_priority(self, policy):
        """Test next interval for critical priority."""
        task = CallbackTask(
            task_id="tsk_test",
            priority="critical"
        )

        assert policy.next_interval(task) == 60

    def test_next_interval_high_priority(self, policy):
        """Test next interval for high priority."""
        task = CallbackTask(
            task_id="tsk_test",
            priority="high"
        )

        assert policy.next_interval(task) == 120

    def test_next_interval_normal_priority(self, policy):
        """Test next interval for normal priority."""
        task = CallbackTask(
            task_id="tsk_test",
            priority="normal"
        )

        assert policy.next_interval(task) == 180  # Default interval


class TestAggressiveNotifyPolicy:
    """Tests for AggressiveNotifyPolicy."""

    @pytest.fixture
    def policy(self):
        """Create policy instance."""
        return AggressiveNotifyPolicy()

    def test_should_notify_always(self, policy):
        """Test should always notify."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.SUBMITTED)

        assert policy.should_notify(task, state_result) is True

    def test_should_close_terminal(self, policy):
        """Test should close when terminal."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.APPROVED, terminal=True)

        assert policy.should_close(task, state_result) is True

    def test_should_not_close_non_terminal(self, policy):
        """Test should not close when not terminal."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.REVIEWING, terminal=False)

        assert policy.should_close(task, state_result) is False

    def test_next_interval(self, policy):
        """Test next interval."""
        task = CallbackTask(task_id="tsk_test")

        assert policy.next_interval(task) == 60


class TestConservativePolicy:
    """Tests for ConservativePolicy."""

    @pytest.fixture
    def policy(self):
        """Create policy instance."""
        return ConservativePolicy()

    def test_should_notify_only_terminal(self, policy):
        """Test should only notify on terminal states."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.REVIEWING, terminal=False)

        assert policy.should_notify(task, state_result) is False

        state_result = StateResult(state=TaskState.APPROVED, terminal=True)
        assert policy.should_notify(task, state_result) is True

    def test_should_close_terminal(self, policy):
        """Test should close when terminal."""
        task = CallbackTask(task_id="tsk_test")
        state_result = StateResult(state=TaskState.APPROVED, terminal=True)

        assert policy.should_close(task, state_result) is True

    def test_should_close_expired(self, policy):
        """Test should close when expired."""
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        task = CallbackTask(task_id="tsk_test", expires_at=past_time)
        state_result = StateResult(state=TaskState.SUBMITTED)

        assert policy.should_close(task, state_result) is True

    def test_should_retry_only_terminal(self, policy):
        """Test should only retry for terminal states."""
        task = CallbackTask(
            task_id="tsk_test",
            terminal=False,
            callback_delivered=False
        )

        assert policy.should_retry_delivery(task) is False

        task.terminal = True
        assert policy.should_retry_delivery(task) is True

    def test_next_interval_terminal(self, policy):
        """Test next interval for terminal task."""
        task = CallbackTask(task_id="tsk_test", terminal=True)

        assert policy.next_interval(task) == 300

    def test_next_interval_active(self, policy):
        """Test next interval for active task."""
        task = CallbackTask(task_id="tsk_test", terminal=False)

        assert policy.next_interval(task) == 600

    def test_should_escalate_max_failures(self, policy):
        """Test should escalate after max failures."""
        task = CallbackTask(
            task_id="tsk_test",
            delivery_attempts=5
        )

        assert policy.should_escalate(task) is True

    def test_should_not_escalate_under_max(self, policy):
        """Test should not escalate under max failures."""
        task = CallbackTask(
            task_id="tsk_test",
            delivery_attempts=3
        )

        assert policy.should_escalate(task) is False
