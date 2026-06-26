"""Integration tests for task callback bus WatcherBus."""

import pytest
import os
import json
import tempfile
import shutil
from datetime import datetime, timedelta

from models import CallbackTask, StateResult, TaskState
from stores import JsonlTaskStore
from adapters import (
    StateAdapter, AdapterRegistry, XiaohongshuNoteReviewAdapter
)
from notifiers import NotifierRegistry, SessionNotifier
from policies import DefaultCallbackPolicy
from bus import WatcherBus, create_default_bus


class MockAdapter(StateAdapter):
    """Mock adapter for testing."""

    def __init__(self, name="mock", supported_states=None):
        self._name = name
        self.supported_states = supported_states or {}
        self.call_count = 0

    @property
    def name(self):
        return self._name

    def supports(self, task):
        return task.adapter == self._name

    def health_check(self):
        return True

    def check(self, task):
        self.call_count += 1
        if task.target_object_id in self.supported_states:
            state_info = self.supported_states[task.target_object_id]
            return StateResult(
                state=state_info.get("state", task.current_state),
                terminal=state_info.get("terminal", False),
                confidence=state_info.get("confidence", 0.95)
            )
        return StateResult(state=task.current_state)


class TestWatcherBus:
    """Tests for WatcherBus."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def bus_setup(self, temp_dir):
        """Create bus with test components."""
        # Create task store
        tasks_file = os.path.join(temp_dir, "tasks.jsonl")
        task_store = JsonlTaskStore(tasks_file)

        # Create mock adapter
        mock_adapter = MockAdapter(
            name="mock-adapter",
            supported_states={}
        )

        # Create adapter registry
        adapter_registry = AdapterRegistry()
        adapter_registry.register(mock_adapter)

        # Create notifier registry with session notifier
        notifier_registry = NotifierRegistry()
        notifier_registry.register(SessionNotifier())

        # Create policy
        policy = DefaultCallbackPolicy()

        # Create bus
        audit_file = os.path.join(temp_dir, "audit.log")
        bus = WatcherBus(
            task_store=task_store,
            adapter_registry=adapter_registry,
            notifier_registry=notifier_registry,
            policy=policy,
            audit_log_path=audit_file
        )

        return bus, task_store, mock_adapter

    def test_run_cycle_empty(self, bus_setup):
        """Test running cycle with no tasks."""
        bus, _, _ = bus_setup

        stats = bus.run_cycle()

        assert stats['tasks_checked'] == 0

    def test_run_cycle_with_task(self, bus_setup):
        """Test running cycle with active task."""
        bus, task_store, mock_adapter = bus_setup

        # Create a task
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            target_object_id="obj_1",
            reply_channel="session",
            current_state=TaskState.SUBMITTED
        )
        task_store.create(task)

        # Mock the state check
        mock_adapter.supported_states = {
            "obj_1": {"state": TaskState.REVIEWING, "terminal": False}
        }

        stats = bus.run_cycle()

        assert stats['tasks_checked'] == 1
        assert stats['states_changed'] == 1

    def test_run_cycle_no_state_change(self, bus_setup):
        """Test running cycle with no state change."""
        bus, task_store, mock_adapter = bus_setup

        # Create a task
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            target_object_id="obj_1",
            reply_channel="session",
            current_state=TaskState.SUBMITTED
        )
        task_store.create(task)

        # State stays the same
        mock_adapter.supported_states = {
            "obj_1": {"state": TaskState.SUBMITTED, "terminal": False}
        }

        stats = bus.run_cycle()

        assert stats['tasks_checked'] == 1
        assert stats['states_changed'] == 0

    def test_run_cycle_terminal_state(self, bus_setup):
        """Test running cycle with terminal state."""
        bus, task_store, mock_adapter = bus_setup

        # Create a task
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            target_object_id="obj_1",
            reply_channel="session",
            current_state=TaskState.REVIEWING
        )
        task_store.create(task)

        # State becomes terminal
        mock_adapter.supported_states = {
            "obj_1": {"state": TaskState.APPROVED, "terminal": True}
        }

        stats = bus.run_cycle()

        assert stats['tasks_checked'] == 1
        assert stats['states_changed'] == 1
        assert stats['tasks_closed'] == 1

        # Verify task is closed
        updated_task = task_store.get("tsk_1")
        assert updated_task.terminal is True
        assert updated_task.current_state == TaskState.APPROVED

    def test_run_cycle_task_expired(self, bus_setup):
        """Test running cycle with expired task."""
        bus, task_store, _ = bus_setup

        # Create an expired task
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            reply_channel="session",
            expires_at=past_time
        )
        task_store.create(task)

        stats = bus.run_cycle()

        assert stats['tasks_checked'] == 1
        assert stats['tasks_closed'] == 1

        # Verify task is closed with timeout
        updated_task = task_store.get("tsk_1")
        assert updated_task.terminal is True
        assert updated_task.current_state == TaskState.TIMEOUT

    def test_run_cycle_no_adapter(self, bus_setup):
        """Test running cycle with no matching adapter."""
        bus, task_store, _ = bus_setup

        # Create a task with unknown adapter
        task = CallbackTask(
            task_id="tsk_1",
            adapter="unknown-adapter",
            reply_channel="session"
        )
        task_store.create(task)

        stats = bus.run_cycle()

        # Should be checked but no state change
        assert stats['tasks_checked'] == 1
        assert stats['states_changed'] == 0

    def test_audit_log_written(self, bus_setup):
        """Test that audit log is written."""
        bus, task_store, _ = bus_setup

        # Create a task
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            target_object_id="obj_1",
            reply_channel="session",
            current_state=TaskState.SUBMITTED
        )
        task_store.create(task)

        bus.run_cycle()

        # Verify audit log exists
        assert os.path.exists(bus.audit_log_path)

    def test_escalation_callback(self, bus_setup):
        """Test escalation callback."""
        bus, task_store, _ = bus_setup

        escalated_tasks = []
        def on_escalate(task, reason):
            escalated_tasks.append((task.task_id, reason))

        bus.on_escalation = on_escalate

        # Create a task with max delivery failures
        task = CallbackTask(
            task_id="tsk_1",
            adapter="mock-adapter",
            reply_channel="session",
            delivery_attempts=3,
            callback_delivered=False
        )
        task_store.create(task)

        stats = bus.run_cycle()

        assert stats['tasks_escalated'] == 1
        assert len(escalated_tasks) == 1
        assert escalated_tasks[0][0] == "tsk_1"

    def test_get_health(self, bus_setup):
        """Test health check."""
        bus, _, _ = bus_setup

        health = bus.get_health()

        assert 'status' in health
        assert 'active_tasks' in health
        assert 'adapters' in health

    def test_run_cycle_limit(self, bus_setup):
        """Test running cycle with limit."""
        bus, task_store, _ = bus_setup

        # Create multiple tasks
        for i in range(5):
            task = CallbackTask(
                task_id=f"tsk_{i}",
                adapter="mock-adapter",
                reply_channel="session"
            )
            task_store.create(task)

        stats = bus.run_cycle(limit=3)

        assert stats['tasks_checked'] == 3


class TestCreateDefaultBus:
    """Tests for create_default_bus factory function."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_create_default_bus(self, temp_dir):
        """Test creating default bus."""
        tasks_file = os.path.join(temp_dir, "tasks.jsonl")
        audit_file = os.path.join(temp_dir, "audit.log")
        notify_dir = os.path.join(temp_dir, "notifications")

        bus = create_default_bus(
            tasks_file=tasks_file,
            audit_log=audit_file,
            notifications_dir=notify_dir
        )

        assert bus is not None
        assert isinstance(bus.task_store, JsonlTaskStore)
        assert bus.audit_log_path == audit_file

    def test_create_default_bus_creates_directories(self, temp_dir):
        """Test that create_default_bus creates necessary directories."""
        tasks_file = os.path.join(temp_dir, "subdir", "tasks.jsonl")
        audit_file = os.path.join(temp_dir, "subdir", "audit.log")
        notify_dir = os.path.join(temp_dir, "subdir", "notifications")

        bus = create_default_bus(
            tasks_file=tasks_file,
            audit_log=audit_file,
            notifications_dir=notify_dir
        )

        assert os.path.exists(os.path.dirname(tasks_file))
        assert os.path.exists(notify_dir)


class TestWatcherBusIntegration:
    """End-to-end integration tests."""

    @pytest.fixture
    def integration_setup(self):
        """Create full integration setup."""
        temp_dir = tempfile.mkdtemp()

        # Create default bus
        tasks_file = os.path.join(temp_dir, "tasks.jsonl")
        audit_file = os.path.join(temp_dir, "audit.log")
        notify_dir = os.path.join(temp_dir, "notifications")

        bus = create_default_bus(
            tasks_file=tasks_file,
            audit_log=audit_file,
            notifications_dir=notify_dir
        )

        yield bus, temp_dir

        shutil.rmtree(temp_dir)

    def test_full_workflow(self, integration_setup):
        """Test complete workflow from creation to notification."""
        bus, temp_dir = integration_setup

        # Create mock XHS states file
        mock_states = {
            "note_123": {"state": "reviewing", "confidence": 0.9}
        }
        monitor_dir = os.path.join(temp_dir, "monitor-tasks")
        os.makedirs(monitor_dir, exist_ok=True)
        mock_file = os.path.join(monitor_dir, "mock-xhs-states.json")
        with open(mock_file, 'w') as f:
            json.dump(mock_states, f)

        # Override the default path used by adapter
        # (In real test, we use the mock adapter, but here we're testing integration)

        # Create task
        task = CallbackTask(
            task_id="tsk_integration_001",
            owner_agent="content",
            target_system="xiaohongshu",
            adapter="xiaohongshu-note-review",
            target_object_id="note_123",
            reply_channel="session",
            reply_to="channel:test",
            requester_id="user_001",
            current_state="submitted"
        )
        bus.task_store.create(task)

        # Run cycle
        stats = bus.run_cycle()

        # Verify cycle ran
        assert stats['tasks_checked'] == 1

        # Verify audit log
        assert os.path.exists(bus.audit_log_path)
