"""Unit tests for task callback bus models."""

import pytest
import json
from datetime import datetime, timedelta
from models import (
    CallbackTask,
    StateResult,
    SendResult,
    TaskType,
    TaskPriority,
    TaskState,
)


class TestCallbackTask:
    """Tests for CallbackTask model."""

    def test_basic_creation(self):
        """Test creating a basic callback task."""
        task = CallbackTask(
            task_id="tsk_test_001",
            owner_agent="content",
            target_system="xiaohongshu",
            adapter="xiaohongshu-note-review",
            target_object_id="note_abc123",
            reply_channel="discord",
            reply_to="channel:123456",
            requester_id="user_001",
        )

        assert task.task_id == "tsk_test_001"
        assert task.owner_agent == "content"
        assert task.target_system == "xiaohongshu"
        assert task.current_state == TaskState.SUBMITTED
        assert task.terminal is False
        assert task.callback_delivered is False

    def test_default_state(self):
        """Test that default state is SUBMITTED."""
        task = CallbackTask(task_id="tsk_test")
        assert task.current_state == TaskState.SUBMITTED
        assert task.last_notified_state == TaskState.SUBMITTED

    def test_update_state(self):
        """Test state update functionality."""
        task = CallbackTask(task_id="tsk_test", current_state=TaskState.SUBMITTED)

        # Update to new state
        changed = task.update_state(TaskState.REVIEWING, confidence=0.95)
        assert changed is True
        assert task.current_state == TaskState.REVIEWING
        assert task.last_notified_state == TaskState.SUBMITTED
        assert task.confidence == 0.95

        # Update to same state (no change)
        changed = task.update_state(TaskState.REVIEWING, confidence=0.90)
        assert changed is False
        assert task.confidence == 0.95  # Confidence not updated on no-change

    def test_mark_terminal(self):
        """Test marking task as terminal."""
        task = CallbackTask(task_id="tsk_test", current_state=TaskState.REVIEWING)

        task.mark_terminal(TaskState.APPROVED, delivered=True)

        assert task.terminal is True
        assert task.current_state == TaskState.APPROVED
        assert task.callback_delivered is True

    def test_is_expired(self):
        """Test expiration check."""
        # Task with past expiration
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        expired_task = CallbackTask(
            task_id="tsk_expired",
            expires_at=past_time
        )
        assert expired_task.is_expired() is True

        # Task with future expiration
        future_time = (datetime.now() + timedelta(hours=1)).isoformat()
        valid_task = CallbackTask(
            task_id="tsk_valid",
            expires_at=future_time
        )
        assert valid_task.is_expired() is False

        # Task with no expiration
        no_expire_task = CallbackTask(task_id="tsk_no_expire")
        assert no_expire_task.is_expired() is False

    def test_should_notify(self):
        """Test notification trigger detection."""
        # State changed
        task = CallbackTask(
            task_id="tsk_test",
            current_state=TaskState.REVIEWING,
            last_notified_state=TaskState.SUBMITTED
        )
        assert task.should_notify() is True

        # State unchanged
        task.last_notified_state = TaskState.REVIEWING
        assert task.should_notify() is False

    def test_to_dict(self):
        """Test conversion to dictionary."""
        task = CallbackTask(
            task_id="tsk_test",
            owner_agent="content",
            metadata={"key": "value"}
        )

        d = task.to_dict()
        assert d["task_id"] == "tsk_test"
        assert d["owner_agent"] == "content"
        assert d["metadata"] == {"key": "value"}

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "task_id": "tsk_test",
            "owner_agent": "content",
            "current_state": "reviewing",
            "unknown_field": "ignored"  # Should be ignored
        }

        task = CallbackTask.from_dict(data)
        assert task.task_id == "tsk_test"
        assert task.current_state == "reviewing"

    def test_to_json(self):
        """Test JSON serialization."""
        task = CallbackTask(task_id="tsk_test", owner_agent="content")
        json_str = task.to_json()

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["task_id"] == "tsk_test"
        assert parsed["owner_agent"] == "content"

    def test_from_json(self):
        """Test JSON deserialization."""
        json_str = '{"task_id": "tsk_test", "owner_agent": "content"}'
        task = CallbackTask.from_json(json_str)
        assert task.task_id == "tsk_test"
        assert task.owner_agent == "content"


class TestStateResult:
    """Tests for StateResult model."""

    def test_success_result(self):
        """Test successful state result."""
        result = StateResult(
            state=TaskState.APPROVED,
            terminal=True,
            confidence=0.95,
            source_of_truth="browser_page",
            raw_evidence="Status: approved"
        )

        assert result.is_success() is True
        assert result.state == TaskState.APPROVED
        assert result.terminal is True

    def test_error_result(self):
        """Test error state result."""
        result = StateResult(
            state=TaskState.SUBMITTED,
            error="Connection failed",
            source_of_truth="error"
        )

        assert result.is_success() is False
        assert result.error == "Connection failed"

    def test_to_from_dict(self):
        """Test dictionary conversion."""
        result = StateResult(
            state=TaskState.REVIEWING,
            terminal=False,
            confidence=0.85,
            metadata={"note_id": "abc123"}
        )

        d = result.to_dict()
        result2 = StateResult.from_dict(d)

        assert result2.state == TaskState.REVIEWING
        assert result2.confidence == 0.85
        assert result2.metadata == {"note_id": "abc123"}


class TestSendResult:
    """Tests for SendResult model."""

    def test_success(self):
        """Test successful send."""
        result = SendResult(
            ok=True,
            delivered=True,
            provider_message_id="msg_123"
        )
        assert result.is_success() is True

    def test_failure(self):
        """Test failed send."""
        result = SendResult(
            ok=False,
            delivered=False,
            error="Network error"
        )
        assert result.is_success() is False

    def test_partial_failure(self):
        """Test partial failure (ok but not delivered)."""
        result = SendResult(
            ok=True,
            delivered=False,
            error="Rate limited"
        )
        assert result.is_success() is False

    def test_to_from_dict(self):
        """Test dictionary conversion."""
        result = SendResult(
            ok=True,
            delivered=True,
            provider_message_id="msg_456"
        )

        d = result.to_dict()
        result2 = SendResult.from_dict(d)

        assert result2.ok is True
        assert result2.delivered is True
        assert result2.provider_message_id == "msg_456"


class TestTaskState:
    """Tests for TaskState enum."""

    def test_terminal_states(self):
        """Test identification of terminal states."""
        terminal_states = {
            TaskState.APPROVED,
            TaskState.REJECTED,
            TaskState.COMPLETED,
            TaskState.FAILED,
            TaskState.TIMEOUT,
            TaskState.CANCELLED,
        }

        non_terminal_states = {
            TaskState.SUBMITTED,
            TaskState.PENDING,
            TaskState.REVIEWING,
        }

        for state in terminal_states:
            # Terminal states should be identifiable
            assert state in terminal_states

        for state in non_terminal_states:
            assert state not in terminal_states


class TestTaskPriority:
    """Tests for TaskPriority enum."""

    def test_priority_order(self):
        """Test priority values."""
        assert TaskPriority.LOW == "low"
        assert TaskPriority.NORMAL == "normal"
        assert TaskPriority.HIGH == "high"
        assert TaskPriority.CRITICAL == "critical"


class TestTaskType:
    """Tests for TaskType enum."""

    def test_task_types(self):
        """Test task type values."""
        assert TaskType.STATUS_MONITOR == "status_monitor"
        assert TaskType.JOB_COMPLETION == "job_completion"
        assert TaskType.APPROVAL_WORKFLOW == "approval_workflow"
