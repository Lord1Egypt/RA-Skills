"""StateAdapter interface and implementations for checking task states."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json
import re

try:
    from .models import CallbackTask, StateResult, TaskState
except ImportError:
    from models import CallbackTask, StateResult, TaskState


class StateAdapter(ABC):
    """
    Abstract interface for checking task states.

    Each adapter knows how to check the state of a specific target system.
    The output is standardized to StateResult.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Adapter name/identifier."""
        pass

    @abstractmethod
    def supports(self, task: CallbackTask) -> bool:
        """
        Check if this adapter supports the given task.

        Args:
            task: Task to check

        Returns:
            True if this adapter can handle the task
        """
        pass

    @abstractmethod
    def check(self, task: CallbackTask) -> StateResult:
        """
        Check the current state of the task.

        Args:
            task: Task to check

        Returns:
            StateResult with current state information
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if adapter is healthy and ready to use.

        Returns:
            True if adapter is operational
        """
        pass


class XiaohongshuNoteReviewAdapter(StateAdapter):
    """
    Adapter for checking Xiaohongshu note review status.

    Real-State-First Implementation:
    1. Monitor tasks registry (real task state from one-click-posting)
    2. Packet file (script-first: reads publish.status from packet)
    3. Mock state file (fallback for testing only)

    States:
    - submitted: Note created, pending review
    - reviewing: Under review (publishing in packet)
    - approved: Published/approved
    - rejected: Rejected
    - failed: Error state
    """

    VALID_STATES = {
        "submitted", "reviewing", "approved", "rejected", "failed", "published"
    }

    # Terminal states for XHS note review
    TERMINAL_STATES = {"approved", "rejected", "failed", "published"}

    # Default paths for real state sources
    DEFAULT_MONITOR_TASKS_PATH = "~/.openclaw/shared-context/monitor-tasks/tasks.jsonl"
    DEFAULT_MOCK_STATES_PATH = "~/.openclaw/shared-context/monitor-tasks/mock-xhs-states.json"

    def __init__(self, monitor_tasks_path: Optional[str] = None, mock_states_path: Optional[str] = None):
        """
        Initialize adapter with configurable paths.

        Args:
            monitor_tasks_path: Path to monitor tasks registry (real state source)
            mock_states_path: Path to mock states file (testing only)
        """
        self._monitor_tasks_path = monitor_tasks_path or self.DEFAULT_MONITOR_TASKS_PATH
        self._mock_states_path = mock_states_path or self.DEFAULT_MOCK_STATES_PATH

    @property
    def name(self) -> str:
        return "xiaohongshu-note-review"

    def supports(self, task: CallbackTask) -> bool:
        """Check if task is a XHS note review task."""
        return (
            task.adapter == self.name or
            task.target_system == "xiaohongshu"
        )

    def health_check(self) -> bool:
        """Check if XHS adapter is healthy."""
        import os
        # Check if real state sources are accessible
        monitor_path = os.path.expanduser(self._monitor_tasks_path)
        return os.path.exists(os.path.dirname(monitor_path))

    def check(self, task: CallbackTask) -> StateResult:
        """
        Check XHS note review status with real-state-first priority.

        Priority:
        1. Monitor tasks registry (real state from one-click-posting system)
        2. Packet file (publish.status from packet JSON)
        3. Mock state file (testing fallback only)
        4. Assumed state (last resort)

        Args:
            task: Task with target_object_id = note_id/packet_id

        Returns:
            StateResult with review status
        """
        try:
            note_id = task.target_object_id
            # Ensure we use string value for state, not enum
            current_state = str(task.current_state.value if hasattr(task.current_state, 'value') else task.current_state)

            if not note_id:
                return StateResult(
                    state=current_state,
                    terminal=False,
                    confidence=0.0,
                    error="No target_object_id (note_id/packet_id) specified",
                    source_of_truth="error"
                )

            # Priority 1: Check monitor tasks registry (real state source)
            result = self._check_monitor_registry(note_id, task)
            # Return if found (confidence > 0), even with lower confidence due to errors
            # because monitor registry is the primary source of truth
            if result.confidence > 0:
                return result

            # Priority 2: Check packet file (if packet_path in metadata)
            if task.metadata and task.metadata.get("packet_path"):
                result = self._check_packet_file(task)
                if result.confidence >= 0.9:
                    return result

            # Priority 3: Try to find packet from monitor registry and check it
            packet_path = self._find_packet_path_from_registry(note_id)
            if packet_path:
                result = self._check_packet_at_path(packet_path, note_id)
                if result.confidence >= 0.9:
                    return result

            # Priority 4: Check mock state file (testing only)
            result = self._check_mock_file(note_id, task)
            if result.confidence > 0:
                return result

            # Priority 5: Return assumed state with low confidence
            return StateResult(
                state=current_state or TaskState.SUBMITTED.value,
                terminal=False,
                confidence=0.3,
                source_of_truth="assumed",
                raw_evidence="No real state source found",
                metadata={'note_id': note_id, 'assumed': True}
            )

        except Exception as e:
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                error=str(e),
                source_of_truth="error"
            )

    def _check_monitor_registry(self, note_id: str, task: CallbackTask) -> StateResult:
        """
        Check state from monitor tasks registry (real state source).

        This is the primary source of truth - it contains the actual task state
        as tracked by the one-click-posting monitoring system.
        """
        import os

        # Ensure we use string value for state
        current_state = str(task.current_state.value if hasattr(task.current_state, 'value') else task.current_state)

        registry_path = os.path.expanduser(self._monitor_tasks_path)
        if not os.path.exists(registry_path):
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="monitor_registry",
                error=f"Registry not found: {registry_path}"
            )

        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        task_entry = json.loads(line)
                        # Match by target_object_id or packet_id
                        if (task_entry.get('target_object_id') == note_id or
                            task_entry.get('packet_id') == note_id):

                            state = task_entry.get('current_state', 'submitted')
                            terminal = task_entry.get('terminal', False) or state in self.TERMINAL_STATES
                            confidence = 0.98 if not task_entry.get('last_error') else 0.85

                            return StateResult(
                                state=state,
                                terminal=terminal,
                                confidence=confidence,
                                source_of_truth="monitor_registry",
                                raw_evidence=json.dumps({
                                    'task_id': task_entry.get('task_id'),
                                    'current_state': state,
                                    'terminal': terminal,
                                    'updated_at': task_entry.get('updated_at')
                                }),
                                metadata={
                                    'task_id': task_entry.get('task_id'),
                                    'packet_id': task_entry.get('packet_id'),
                                    'packet_path': task_entry.get('packet_path'),
                                    'registry_path': registry_path
                                }
                            )
                    except json.JSONDecodeError:
                        continue

            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="monitor_registry",
                error=f"No entry found for note_id: {note_id}"
            )

        except IOError as e:
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="monitor_registry",
                error=f"Failed to read registry: {e}"
            )

    def _find_packet_path_from_registry(self, note_id: str) -> Optional[str]:
        """Find packet_path from monitor registry by note_id."""
        import os

        registry_path = os.path.expanduser(self._monitor_tasks_path)
        if not os.path.exists(registry_path):
            return None

        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        task_entry = json.loads(line)
                        if (task_entry.get('target_object_id') == note_id or
                            task_entry.get('packet_id') == note_id):
                            return task_entry.get('packet_path')
                    except json.JSONDecodeError:
                        continue
        except IOError:
            pass

        return None

    def _check_packet_file(self, task: CallbackTask) -> StateResult:
        """
        Check state from one-click-posting packet file.

        Reads publish.status from packet JSON.
        Maps: draft->submitted, publishing->reviewing, published->approved
        """
        # Ensure we use string value for state
        current_state = str(task.current_state.value if hasattr(task.current_state, 'value') else task.current_state)

        packet_path = task.metadata.get("packet_path") if task.metadata else None
        if not packet_path:
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="packet_file",
                error="No packet_path in task metadata"
            )

        note_id = task.target_object_id
        return self._check_packet_at_path(packet_path, note_id)

    def _check_packet_at_path(self, packet_path: str, note_id: str) -> StateResult:
        """Check packet file at specific path."""
        import os

        if not os.path.exists(packet_path):
            return StateResult(
                state="submitted",
                terminal=False,
                confidence=0.0,
                source_of_truth="packet_file",
                error=f"Packet file not found: {packet_path}"
            )

        try:
            with open(packet_path, 'r', encoding='utf-8') as f:
                packet = json.load(f)

            # Verify packet_id matches note_id if possible
            packet_id = packet.get("packet_id", "")
            if note_id and packet_id and packet_id != note_id:
                # This might be a different packet, but we still check it
                pass

            publish = packet.get("publish", {})
            status = publish.get("status", "draft")

            # Map packet status to standardized task state
            state_mapping = {
                "draft": "submitted",
                "publishing": "reviewing",
                "reviewing": "reviewing",
                "published": "approved",
                "failed": "failed"
            }

            task_state = state_mapping.get(status, status)
            terminal = task_state in self.TERMINAL_STATES

            # Check if monitor section has more recent info
            monitor = packet.get("monitor", {})
            if monitor.get("current_state"):
                task_state = monitor.get("current_state")
                terminal = task_state in self.TERMINAL_STATES

            return StateResult(
                state=task_state,
                terminal=terminal,
                confidence=0.95,
                source_of_truth="packet_file",
                raw_evidence=json.dumps({
                    "packet_id": packet_id,
                    "packet_status": status,
                    "mapped_state": task_state,
                    "monitor_state": monitor.get("current_state")
                }),
                metadata={
                    "packet_path": packet_path,
                    "packet_status": status,
                    "packet_id": packet_id
                }
            )

        except (json.JSONDecodeError, IOError) as e:
            return StateResult(
                state="submitted",
                terminal=False,
                confidence=0.0,
                source_of_truth="packet_file",
                error=f"Failed to read packet: {e}"
            )

    def _check_mock_file(self, note_id: str, task: CallbackTask) -> StateResult:
        """
        Check state from mock file (testing only, lowest priority).

        This is only used when no real state sources are available.
        """
        import os

        # Ensure we use string value for state
        current_state = str(task.current_state.value if hasattr(task.current_state, 'value') else task.current_state)

        mock_file = os.path.expanduser(self._mock_states_path)

        if not os.path.exists(mock_file):
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="mock_file",
                error="Mock file not found"
            )

        try:
            with open(mock_file, 'r', encoding='utf-8') as f:
                mock_states = json.load(f)

            if note_id not in mock_states:
                return StateResult(
                    state=current_state,
                    terminal=False,
                    confidence=0.0,
                    source_of_truth="mock_file",
                    error=f"No mock state for note_id: {note_id}"
                )

            mock_state = mock_states[note_id]
            state = mock_state.get('state', 'submitted')
            terminal = state in self.TERMINAL_STATES

            return StateResult(
                state=state,
                terminal=terminal,
                confidence=mock_state.get('confidence', 0.7),
                source_of_truth="mock_file",
                raw_evidence=json.dumps(mock_state),
                metadata={'mock': True, 'note_id': note_id}
            )

        except (json.JSONDecodeError, IOError) as e:
            return StateResult(
                state=current_state,
                terminal=False,
                confidence=0.0,
                source_of_truth="mock_file",
                error=f"Failed to read mock file: {e}"
            )

    def _parse_page_content(self, html_content: str) -> StateResult:
        """
        Parse XHS page content to determine review status.

        NOTE: This method is kept for compatibility but is NOT used in the
        script-first implementation. Browser checking should be done via
        external scripts, not LLM parsing.

        Kept for: backward compatibility, potential future use with structured
        browser automation output.
        """
        # Look for status indicators in page
        patterns = {
            'approved': [
                r'审核通过',
                r'已发布',
                r'published',
                r'status.*approved'
            ],
            'rejected': [
                r'审核未通过',
                r'被驳回',
                r'rejected',
                r'未通过'
            ],
            'reviewing': [
                r'审核中',
                r'正在审核',
                r'reviewing',
                r'processing'
            ]
        }

        for state, regex_list in patterns.items():
            for pattern in regex_list:
                if re.search(pattern, html_content, re.IGNORECASE):
                    return StateResult(
                        state=state,
                        terminal=(state in ['approved', 'rejected']),
                        confidence=0.85,
                        source_of_truth="browser_page",
                        raw_evidence=f"Matched pattern: {pattern}"
                    )

        return StateResult(
            state=TaskState.SUBMITTED,
            terminal=False,
            confidence=0.5,
            source_of_truth="browser_page",
            raw_evidence="No clear status pattern found"
        )


class GitHubPRStatusAdapter(StateAdapter):
    """
    Adapter for checking GitHub PR status.

    Future implementation for GitHub PR monitoring.
    """

    @property
    def name(self) -> str:
        return "github-pr-status"

    def supports(self, task: CallbackTask) -> bool:
        return task.adapter == self.name or task.target_system == "github"

    def health_check(self) -> bool:
        # MVP: Not fully implemented
        return False

    def check(self, task: CallbackTask) -> StateResult:
        return StateResult(
            state=task.current_state,
            terminal=False,
            confidence=0.0,
            error="GitHub adapter not yet implemented",
            source_of_truth="error"
        )


class CronJobCompletionAdapter(StateAdapter):
    """
    Adapter for checking cron job completion status.

    Checks if a cron job has completed by looking at:
    - Job status files
    - Log files
    - Process status
    """

    @property
    def name(self) -> str:
        return "cron-job-completion"

    def supports(self, task: CallbackTask) -> bool:
        return task.adapter == self.name or task.task_type == "job_completion"

    def health_check(self) -> bool:
        return True

    def check(self, task: CallbackTask) -> StateResult:
        """Check cron job completion status."""
        import os

        job_id = task.target_object_id
        if not job_id:
            return StateResult(
                state=task.current_state,
                error="No job_id specified",
                source_of_truth="error"
            )

        # Check for status file
        status_file = os.path.expanduser(
            f"~/.openclaw/shared-context/job-status/{job_id}.json"
        )

        if os.path.exists(status_file):
            try:
                with open(status_file, 'r') as f:
                    status = json.load(f)

                state = status.get('state', 'running')
                terminal = state in ['completed', 'failed', 'timeout']

                return StateResult(
                    state=state,
                    terminal=terminal,
                    confidence=0.95,
                    source_of_truth="local_file",
                    raw_evidence=json.dumps(status),
                    metadata={'job_id': job_id}
                )
            except (json.JSONDecodeError, IOError) as e:
                return StateResult(
                    state=task.current_state,
                    error=f"Failed to read status file: {e}",
                    source_of_truth="error"
                )

        # Job still running or status file not created yet
        return StateResult(
            state='running',
            terminal=False,
            confidence=0.7,
            source_of_truth="local_file",
            raw_evidence="Status file not found",
            metadata={'job_id': job_id}
        )


class AdapterRegistry:
    """Registry for managing state adapters."""

    def __init__(self):
        self._adapters: Dict[str, StateAdapter] = {}

    def register(self, adapter: StateAdapter) -> None:
        """Register an adapter."""
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> Optional[StateAdapter]:
        """Get adapter by name."""
        return self._adapters.get(name)

    def find_for_task(self, task: CallbackTask) -> Optional[StateAdapter]:
        """Find adapter that supports the given task."""
        # First try by explicit adapter name
        if task.adapter and task.adapter in self._adapters:
            adapter = self._adapters[task.adapter]
            if adapter.supports(task):
                return adapter

        # Then try to find any supporting adapter
        for adapter in self._adapters.values():
            if adapter.supports(task):
                return adapter

        return None

    def list_adapters(self) -> list:
        """List all registered adapter names."""
        return list(self._adapters.keys())

    def health_check_all(self) -> Dict[str, bool]:
        """Run health check on all adapters."""
        return {name: adapter.health_check() for name, adapter in self._adapters.items()}


def create_default_adapter_registry() -> AdapterRegistry:
    """Create registry with default adapters."""
    registry = AdapterRegistry()
    registry.register(XiaohongshuNoteReviewAdapter())
    registry.register(GitHubPRStatusAdapter())
    registry.register(CronJobCompletionAdapter())
    return registry
