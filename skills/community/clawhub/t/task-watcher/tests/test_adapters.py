"""Unit tests for task callback bus adapters."""

import pytest
import os
import json
import tempfile
import shutil

from models import CallbackTask, StateResult, TaskState
from adapters import (
    XiaohongshuNoteReviewAdapter,
    GitHubPRStatusAdapter,
    CronJobCompletionAdapter,
    AdapterRegistry,
    create_default_adapter_registry,
)


class TestXiaohongshuNoteReviewAdapter:
    """Tests for XiaohongshuNoteReviewAdapter."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test data."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def adapter(self, temp_dir):
        """Create adapter instance with temp paths."""
        tasks_path = os.path.join(temp_dir, "tasks.jsonl")
        mock_path = os.path.join(temp_dir, "mock-xhs-states.json")
        return XiaohongshuNoteReviewAdapter(
            monitor_tasks_path=tasks_path,
            mock_states_path=mock_path
        )

    @pytest.fixture
    def adapter_with_mock(self, temp_dir):
        """Create adapter with pre-populated mock states."""
        mock_states = {
            "note_approved": {"state": "approved", "confidence": 0.95},
            "note_rejected": {"state": "rejected", "confidence": 0.90},
            "note_reviewing": {"state": "reviewing", "confidence": 0.85},
        }

        mock_path = os.path.join(temp_dir, "mock-xhs-states.json")
        with open(mock_path, 'w') as f:
            json.dump(mock_states, f)

        tasks_path = os.path.join(temp_dir, "tasks.jsonl")

        return XiaohongshuNoteReviewAdapter(
            monitor_tasks_path=tasks_path,
            mock_states_path=mock_path
        )

    def test_name(self, adapter):
        """Test adapter name."""
        assert adapter.name == "xiaohongshu-note-review"

    def test_health_check(self, adapter):
        """Test health check."""
        assert adapter.health_check() is True

    def test_supports_by_adapter_name(self, adapter):
        """Test supports detection by adapter name."""
        task = CallbackTask(task_id="tsk_1", adapter="xiaohongshu-note-review")
        assert adapter.supports(task) is True

    def test_supports_by_target_system(self, adapter):
        """Test supports detection by target system."""
        task = CallbackTask(task_id="tsk_1", target_system="xiaohongshu")
        assert adapter.supports(task) is True

    def test_does_not_support(self, adapter):
        """Test that adapter doesn't support non-XHS tasks."""
        task = CallbackTask(task_id="tsk_1", target_system="github")
        assert adapter.supports(task) is False

    def test_check_no_target_object_id(self, adapter):
        """Test check with no target_object_id."""
        task = CallbackTask(task_id="tsk_1", target_system="xiaohongshu")
        result = adapter.check(task)

        assert result.is_success() is False
        assert "No target_object_id" in result.error

    def test_check_with_mock_state(self, adapter_with_mock):
        """Test check with mock state file."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="xiaohongshu-note-review",
            target_object_id="note_approved"
        )

        result = adapter_with_mock.check(task)

        assert result.is_success() is True
        assert result.state == "approved"
        assert result.terminal is True
        assert result.confidence == 0.95

    def test_check_no_mock_state_found(self, adapter):
        """Test check when no mock state exists."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="xiaohongshu-note-review",
            target_object_id="note_unknown",
            current_state=TaskState.SUBMITTED
        )

        result = adapter.check(task)

        assert result.state == TaskState.SUBMITTED
        assert result.terminal is False

    def test_check_rejected_state(self, adapter_with_mock):
        """Test check with rejected state."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="xiaohongshu-note-review",
            target_object_id="note_rejected"
        )

        result = adapter_with_mock.check(task)

        assert result.state == "rejected"
        assert result.terminal is True

    def test_check_reviewing_state(self, adapter_with_mock):
        """Test check with reviewing state."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="xiaohongshu-note-review",
            target_object_id="note_reviewing"
        )

        result = adapter_with_mock.check(task)

        assert result.state == "reviewing"
        assert result.terminal is False

    def test_parse_page_content_approved(self, adapter):
        """Test parsing approved page content."""
        html = "<div>审核通过</div><span>已发布</span>"
        result = adapter._parse_page_content(html)

        assert result.state == "approved"
        assert result.terminal is True

    def test_parse_page_content_rejected(self, adapter):
        """Test parsing rejected page content."""
        html = "<div>审核未通过</div><span>被驳回</span>"
        result = adapter._parse_page_content(html)

        assert result.state == "rejected"
        assert result.terminal is True

    def test_parse_page_content_reviewing(self, adapter):
        """Test parsing reviewing page content."""
        html = "<div>审核中</div><span>正在审核</span>"
        result = adapter._parse_page_content(html)

        assert result.state == "reviewing"
        assert result.terminal is False

    def test_parse_page_content_unknown(self, adapter):
        """Test parsing unknown page content."""
        html = "<div>some random content</div>"
        result = adapter._parse_page_content(html)

        assert result.state == TaskState.SUBMITTED
        assert result.terminal is False


class TestGitHubPRStatusAdapter:
    """Tests for GitHubPRStatusAdapter."""

    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        return GitHubPRStatusAdapter()

    def test_name(self, adapter):
        """Test adapter name."""
        assert adapter.name == "github-pr-status"

    def test_health_check_not_implemented(self, adapter):
        """Test health check (not implemented)."""
        assert adapter.health_check() is False

    def test_check_not_implemented(self, adapter):
        """Test check (not implemented)."""
        task = CallbackTask(task_id="tsk_1", adapter="github-pr-status")
        result = adapter.check(task)

        assert result.is_success() is False
        assert "not yet implemented" in result.error


class TestCronJobCompletionAdapter:
    """Tests for CronJobCompletionAdapter."""

    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        return CronJobCompletionAdapter()

    @pytest.fixture
    def job_status_dir(self, monkeypatch):
        """Create temporary job status directory with path patching."""
        temp_dir = tempfile.mkdtemp()
        shared_context = os.path.join(temp_dir, ".openclaw", "shared-context")
        job_dir = os.path.join(shared_context, "job-status")
        os.makedirs(job_dir, exist_ok=True)

        status = {
            "state": "completed",
            "finished_at": "2026-03-07T10:00:00+08:00"
        }
        status_file = os.path.join(job_dir, "job_001.json")
        with open(status_file, 'w') as f:
            json.dump(status, f)

        original_expanduser = os.path.expanduser

        def patched_expanduser(path):
            if "~/.openclaw/shared-context" in path:
                return path.replace("~", temp_dir)
            return original_expanduser(path)

        monkeypatch.setattr(os.path, "expanduser", patched_expanduser)

        yield job_dir

        shutil.rmtree(temp_dir)

    def test_name(self, adapter):
        """Test adapter name."""
        assert adapter.name == "cron-job-completion"

    def test_health_check(self, adapter):
        """Test health check."""
        assert adapter.health_check() is True

    def test_supports_by_adapter_name(self, adapter):
        """Test supports detection."""
        task = CallbackTask(task_id="tsk_1", adapter="cron-job-completion")
        assert adapter.supports(task) is True

    def test_check_no_job_id(self, adapter):
        """Test check with no job_id."""
        task = CallbackTask(task_id="tsk_1", adapter="cron-job-completion")
        result = adapter.check(task)

        assert result.is_success() is False
        assert "No job_id" in result.error

    def test_check_job_not_found(self, adapter):
        """Test check when job status file not found."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="cron-job-completion",
            target_object_id="nonexistent_job"
        )

        result = adapter.check(task)

        assert result.state == "running"
        assert result.terminal is False

    def test_check_job_completed(self, adapter, job_status_dir):
        """Test check with completed job."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="cron-job-completion",
            target_object_id="job_001"
        )

        result = adapter.check(task)

        assert result.state == "completed"
        assert result.terminal is True
        assert result.confidence == 0.95


class TestAdapterRegistry:
    """Tests for AdapterRegistry."""

    @pytest.fixture
    def registry(self):
        """Create registry with default adapters."""
        return create_default_adapter_registry()

    def test_register_adapter(self):
        """Test registering an adapter."""
        registry = AdapterRegistry()
        adapter = XiaohongshuNoteReviewAdapter()

        registry.register(adapter)

        assert registry.get("xiaohongshu-note-review") is adapter

    def test_find_for_task_by_adapter_name(self, registry):
        """Test finding adapter by task adapter name."""
        task = CallbackTask(
            task_id="tsk_1",
            adapter="xiaohongshu-note-review"
        )

        adapter = registry.find_for_task(task)
        assert adapter is not None
        assert adapter.name == "xiaohongshu-note-review"

    def test_find_for_task_by_supports(self, registry):
        """Test finding adapter by supports method."""
        task = CallbackTask(
            task_id="tsk_1",
            target_system="xiaohongshu"
        )

        adapter = registry.find_for_task(task)
        assert adapter is not None
        assert adapter.name == "xiaohongshu-note-review"

    def test_find_for_task_not_found(self, registry):
        """Test finding adapter when none supports task."""
        task = CallbackTask(
            task_id="tsk_1",
            target_system="unknown_system"
        )

        adapter = registry.find_for_task(task)
        assert adapter is None

    def test_list_adapters(self, registry):
        """Test listing registered adapters."""
        adapters = registry.list_adapters()

        assert "xiaohongshu-note-review" in adapters
        assert "github-pr-status" in adapters
        assert "cron-job-completion" in adapters

    def test_health_check_all(self, registry):
        """Test health check for all adapters."""
        health = registry.health_check_all()

        assert health["xiaohongshu-note-review"] is True
        assert health["github-pr-status"] is False
        assert health["cron-job-completion"] is True
