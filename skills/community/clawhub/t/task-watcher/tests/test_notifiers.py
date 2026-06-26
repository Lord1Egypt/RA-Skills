"""Unit tests for task callback bus notifiers."""

import pytest
import os
import json
import tempfile
import shutil

from models import CallbackTask, TaskState
from notifiers import (
    DiscordNotifier,
    TelegramNotifier,
    SessionNotifier,
    NotifierRegistry,
    create_default_notifier_registry,
)


class TestDiscordNotifier:
    """Tests for DiscordNotifier."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def notifier(self, temp_dir):
        """Create notifier instance (dry_run for unit tests)."""
        return DiscordNotifier(output_dir=temp_dir, dry_run=True)

    @pytest.fixture
    def sample_task(self):
        """Create sample task."""
        return CallbackTask(
            task_id="tsk_test_001",
            owner_agent="content",
            target_system="xiaohongshu",
            reply_channel="discord",
            reply_to="channel:123456",
            current_state=TaskState.REVIEWING,
            last_notified_state=TaskState.SUBMITTED,
            confidence=0.95,
            delivery_attempts=1
        )

    def test_channel(self, notifier):
        """Test channel identifier."""
        assert notifier.channel == "discord"

    def test_send_state_change(self, notifier, sample_task, temp_dir):
        """Test sending state change notification."""
        result = notifier.send(sample_task)

        assert result.ok is True
        assert result.delivered is True
        assert result.metadata.get('dry_run') is True

        # Verify audit file was still created
        files = [f for f in os.listdir(temp_dir) if f.endswith('.json')]
        assert len(files) >= 1

        with open(os.path.join(temp_dir, files[0])) as f:
            data = json.load(f)
            assert data['task_id'] == "tsk_test_001"
            assert data['channel'] == "discord"
            assert "任务状态更新" in data['message']

    def test_send_terminal(self, notifier, temp_dir):
        """Test sending terminal state notification."""
        task = CallbackTask(
            task_id="tsk_test_002",
            reply_channel="discord",
            current_state=TaskState.APPROVED,
            terminal=True
        )

        result = notifier.send(task)

        assert result.ok is True

        files = [f for f in os.listdir(temp_dir) if 'tsk_test_002' in f]
        assert len(files) >= 1
        with open(os.path.join(temp_dir, files[0])) as f:
            data = json.load(f)
            assert "已完成" in data['message']
            assert "APPROVED" in data['message']

    def test_send_created(self, notifier, temp_dir):
        """Test sending created notification."""
        task = CallbackTask(
            task_id="tsk_test_003",
            reply_channel="discord",
            current_state=TaskState.SUBMITTED,
            delivery_attempts=0
        )

        result = notifier.send(task)

        assert result.ok is True

        files = [f for f in os.listdir(temp_dir) if 'tsk_test_003' in f]
        assert len(files) >= 1
        with open(os.path.join(temp_dir, files[0])) as f:
            data = json.load(f)
            assert "开始监控" in data['message']

    def test_send_with_custom_payload(self, notifier, sample_task):
        """Test sending with custom payload."""
        custom_payload = {"message": "Custom notification message"}
        result = notifier.send(sample_task, payload=custom_payload)

        assert result.ok is True

    def test_format_message_created(self, notifier):
        """Test message formatting for created event."""
        task = CallbackTask(
            task_id="tsk_1",
            owner_agent="content",
            target_system="xiaohongshu",
            reply_to="channel:123",
            current_state=TaskState.SUBMITTED
        )

        message = notifier.format_message(task, "created")
        assert "tsk_1" in message
        assert "xiaohongshu" in message
        assert "开始监控" in message

    def test_format_message_terminal(self, notifier):
        """Test message formatting for terminal event."""
        task = CallbackTask(
            task_id="tsk_1",
            current_state=TaskState.APPROVED,
            updated_at="2026-03-07T10:00:00"
        )

        message = notifier.format_message(task, "terminal")
        assert "已完成" in message
        assert "APPROVED" in message
        assert "✅" in message

    def test_ensure_output_dir(self, temp_dir):
        """Test that output directory is created."""
        new_dir = os.path.join(temp_dir, "new_subdir", "notifications")
        notifier = DiscordNotifier(output_dir=new_dir)

        assert os.path.exists(new_dir)


class TestTelegramNotifier:
    """Tests for TelegramNotifier."""

    @pytest.fixture
    def notifier(self):
        """Create notifier instance."""
        return TelegramNotifier()

    def test_channel(self, notifier):
        """Test channel identifier."""
        assert notifier.channel == "telegram"

    def test_send_not_implemented(self, notifier):
        """Test that send returns not implemented error."""
        task = CallbackTask(task_id="tsk_1")
        result = notifier.send(task)

        assert result.ok is False
        assert result.delivered is False
        assert "not yet implemented" in result.error


class TestSessionNotifier:
    """Tests for SessionNotifier."""

    @pytest.fixture
    def notifier(self):
        """Create notifier instance."""
        return SessionNotifier()

    @pytest.fixture
    def sample_task(self):
        """Create sample task."""
        return CallbackTask(
            task_id="tsk_test_001",
            current_state=TaskState.REVIEWING,
            last_notified_state=TaskState.SUBMITTED,
            delivery_attempts=1
        )

    def test_channel(self, notifier):
        """Test channel identifier."""
        assert notifier.channel == "session"

    def test_send(self, notifier, sample_task):
        """Test sending notification."""
        result = notifier.send(sample_task)

        assert result.ok is True
        assert result.delivered is True
        assert result.metadata['channel'] == "session"

    def test_get_last_message(self, notifier, sample_task):
        """Test getting last message."""
        notifier.send(sample_task)

        last_message = notifier.get_last_message()
        assert last_message is not None
        assert "tsk_test_001" in last_message

    def test_send_stores_message(self, notifier, sample_task):
        """Test that send stores the message."""
        notifier.send(sample_task)

        assert notifier.last_message is not None
        assert "任务状态更新" in notifier.last_message


class TestNotifierRegistry:
    """Tests for NotifierRegistry."""

    @pytest.fixture
    def registry(self):
        """Create registry with default notifiers."""
        return create_default_notifier_registry()

    def test_register_notifier(self):
        """Test registering a notifier."""
        registry = NotifierRegistry()
        notifier = SessionNotifier()

        registry.register(notifier)

        assert registry.get("session") is notifier

    def test_find_for_task(self, registry):
        """Test finding notifier for task."""
        task = CallbackTask(
            task_id="tsk_1",
            reply_channel="discord"
        )

        notifier = registry.find_for_task(task)
        assert notifier is not None
        assert notifier.channel == "discord"

    def test_find_for_task_not_found(self, registry):
        """Test finding notifier when not found."""
        task = CallbackTask(
            task_id="tsk_1",
            reply_channel="unknown_channel"
        )

        notifier = registry.find_for_task(task)
        assert notifier is None

    def test_list_channels(self, registry):
        """Test listing registered channels."""
        channels = registry.list_channels()

        assert "discord" in channels
        assert "telegram" in channels
        assert "session" in channels
