"""Unit tests for task callback bus stores."""

import pytest
import os
import json
import tempfile
import shutil
from datetime import datetime, timedelta

from models import CallbackTask, TaskState
from stores import JsonlTaskStore, TaskStore


class TestJsonlTaskStore:
    """Tests for JsonlTaskStore."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def store(self, temp_dir):
        """Create a fresh JsonlTaskStore for each test."""
        file_path = os.path.join(temp_dir, "tasks.jsonl")
        return JsonlTaskStore(file_path)

    @pytest.fixture
    def sample_task(self):
        """Create a sample task for testing."""
        return CallbackTask(
            task_id="tsk_test_001",
            owner_agent="content",
            target_system="xiaohongshu",
            adapter="xiaohongshu-note-review",
            target_object_id="note_abc123",
            reply_channel="discord",
            reply_to="channel:123456",
            requester_id="user_001",
            current_state=TaskState.SUBMITTED
        )

    def test_create_task(self, store, sample_task):
        """Test creating a task."""
        created = store.create(sample_task)

        assert created.task_id == sample_task.task_id
        assert created.owner_agent == sample_task.owner_agent
        assert created.created_at is not None

    def test_create_duplicate_task(self, store, sample_task):
        """Test that creating duplicate task raises error."""
        store.create(sample_task)

        with pytest.raises(ValueError, match="already exists"):
            store.create(sample_task)

    def test_get_task(self, store, sample_task):
        """Test getting a task by ID."""
        store.create(sample_task)

        retrieved = store.get("tsk_test_001")
        assert retrieved is not None
        assert retrieved.task_id == "tsk_test_001"
        assert retrieved.owner_agent == "content"

    def test_get_nonexistent_task(self, store):
        """Test getting a non-existent task."""
        retrieved = store.get("nonexistent")
        assert retrieved is None

    def test_list_active(self, store, sample_task):
        """Test listing active tasks."""
        # Create active task
        store.create(sample_task)

        # Create terminal task
        terminal_task = CallbackTask(
            task_id="tsk_terminal",
            owner_agent="content",
            current_state=TaskState.APPROVED,
            terminal=True
        )
        store.create(terminal_task)

        active = store.list_active()
        assert len(active) == 1
        assert active[0].task_id == "tsk_test_001"

    def test_list_by_owner(self, store):
        """Test listing tasks by owner."""
        # Create tasks for different owners
        task1 = CallbackTask(task_id="tsk_content_1", owner_agent="content")
        task2 = CallbackTask(task_id="tsk_trading_1", owner_agent="trading")
        task3 = CallbackTask(task_id="tsk_content_2", owner_agent="content")

        store.create(task1)
        store.create(task2)
        store.create(task3)

        content_tasks = store.list_by_owner("content")
        assert len(content_tasks) == 2
        assert all(t.owner_agent == "content" for t in content_tasks)

    def test_list_by_adapter(self, store):
        """Test listing tasks by adapter."""
        task1 = CallbackTask(task_id="tsk_1", adapter="xiaohongshu-note-review")
        task2 = CallbackTask(task_id="tsk_2", adapter="github-pr-status")
        task3 = CallbackTask(task_id="tsk_3", adapter="xiaohongshu-note-review")

        store.create(task1)
        store.create(task2)
        store.create(task3)

        xhs_tasks = store.list_by_adapter("xiaohongshu-note-review")
        assert len(xhs_tasks) == 2

    def test_update_task(self, store, sample_task):
        """Test updating a task."""
        store.create(sample_task)

        updated = store.update("tsk_test_001", {
            "current_state": TaskState.REVIEWING,
            "confidence": 0.95
        })

        assert updated is not None
        assert updated.current_state == TaskState.REVIEWING
        assert updated.confidence == 0.95
        assert updated.owner_agent == "content"  # Unchanged field

    def test_update_nonexistent_task(self, store):
        """Test updating a non-existent task."""
        result = store.update("nonexistent", {"current_state": TaskState.REVIEWING})
        assert result is None

    def test_close_task(self, store, sample_task):
        """Test closing a task."""
        store.create(sample_task)

        closed = store.close("tsk_test_001", TaskState.APPROVED)

        assert closed is not None
        assert closed.terminal is True
        assert closed.current_state == TaskState.APPROVED

    def test_delete_task(self, store, sample_task):
        """Test deleting a task."""
        store.create(sample_task)

        deleted = store.delete("tsk_test_001")
        assert deleted is True

        # Should not be found anymore
        assert store.get("tsk_test_001") is None

    def test_delete_nonexistent_task(self, store):
        """Test deleting a non-existent task."""
        deleted = store.delete("nonexistent")
        assert deleted is False

    def test_count_active(self, store):
        """Test counting active tasks."""
        # Initially empty
        assert store.count_active() == 0

        # Add active task
        store.create(sample_task := CallbackTask(task_id="tsk_1"))
        assert store.count_active() == 1

        # Add terminal task (should not count)
        store.create(CallbackTask(task_id="tsk_2", terminal=True))
        assert store.count_active() == 1

    def test_persistence(self, temp_dir, sample_task):
        """Test that tasks persist across store instances."""
        file_path = os.path.join(temp_dir, "tasks.jsonl")

        # Create store and task
        store1 = JsonlTaskStore(file_path)
        store1.create(sample_task)

        # Create new store instance with same file
        store2 = JsonlTaskStore(file_path)
        retrieved = store2.get("tsk_test_001")

        assert retrieved is not None
        assert retrieved.task_id == "tsk_test_001"

    def test_latest_version_wins(self, store, sample_task):
        """Test that latest version of task is returned."""
        store.create(sample_task)

        # Update task multiple times
        store.update("tsk_test_001", {"current_state": TaskState.REVIEWING})
        store.update("tsk_test_001", {"current_state": TaskState.APPROVED})

        # Should get latest version
        retrieved = store.get("tsk_test_001")
        assert retrieved.current_state == TaskState.APPROVED

    def test_list_active_limit(self, store):
        """Test limit parameter for list_active."""
        # Create multiple tasks
        for i in range(5):
            store.create(CallbackTask(task_id=f"tsk_{i}"))

        # Get limited results
        limited = store.list_active(limit=3)
        assert len(limited) == 3

    def test_list_priority_order(self, store):
        """Test that active tasks are sorted by priority."""
        # Create tasks with different priorities
        task_low = CallbackTask(task_id="tsk_low", priority="low")
        task_high = CallbackTask(task_id="tsk_high", priority="high")
        task_normal = CallbackTask(task_id="tsk_normal", priority="normal")

        store.create(task_low)
        store.create(task_high)
        store.create(task_normal)

        # Should be sorted: high, normal, low
        active = store.list_active()
        assert active[0].task_id == "tsk_high"
        assert active[1].task_id == "tsk_normal"
        assert active[2].task_id == "tsk_low"

    def test_compact(self, store):
        """Test file compaction."""
        # Create and update task multiple times
        store.create(CallbackTask(task_id="tsk_1"))
        store.update("tsk_1", {"current_state": TaskState.REVIEWING})
        store.update("tsk_1", {"current_state": TaskState.APPROVED})

        # Get file size before compact
        file_size_before = os.path.getsize(store.file_path)

        # Compact
        lines_removed = store.compact()

        # File should be smaller or have same size
        file_size_after = os.path.getsize(store.file_path)
        assert file_size_after <= file_size_before

        # Task should still be retrievable
        task = store.get("tsk_1")
        assert task is not None
        assert task.current_state == TaskState.APPROVED


class TestTaskStoreInterface:
    """Tests for TaskStore abstract interface compliance."""

    def test_jsonl_implements_interface(self):
        """Test that JsonlTaskStore implements TaskStore interface."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "tasks.jsonl")
            store = JsonlTaskStore(file_path)

            # Should be instance of TaskStore
            assert isinstance(store, TaskStore)

            # Should have all required methods
            assert hasattr(store, 'create')
            assert hasattr(store, 'get')
            assert hasattr(store, 'list_active')
            assert hasattr(store, 'update')
            assert hasattr(store, 'close')
            assert hasattr(store, 'delete')
