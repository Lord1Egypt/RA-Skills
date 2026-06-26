"""WatcherBus - Main orchestrator for task monitoring and callbacks."""

from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
import logging
import json
import os

try:
    from .models import CallbackTask, StateResult, SendResult, TaskState
except ImportError:
    from models import CallbackTask, StateResult, SendResult, TaskState
try:
    from .stores import TaskStore, JsonlTaskStore
except ImportError:
    from stores import TaskStore, JsonlTaskStore
try:
    from .adapters import StateAdapter, AdapterRegistry, create_default_adapter_registry
except ImportError:
    from adapters import StateAdapter, AdapterRegistry, create_default_adapter_registry
try:
    from .notifiers import Notifier, NotifierRegistry, create_default_notifier_registry
except ImportError:
    from notifiers import Notifier, NotifierRegistry, create_default_notifier_registry
try:
    from .policies import CallbackPolicy, DefaultCallbackPolicy
except ImportError:
    from policies import CallbackPolicy, DefaultCallbackPolicy


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('WatcherBus')


class WatcherBus:
    """
    Main orchestrator for task monitoring and callbacks.

    Flow:
    1. Load active tasks from TaskStore
    2. For each task, find appropriate StateAdapter
    3. Check current state
    4. Apply Policy to decide action
    5. Notify if needed
    6. Update TaskStore
    """

    def __init__(
        self,
        task_store: TaskStore,
        adapter_registry: AdapterRegistry,
        notifier_registry: NotifierRegistry,
        policy: Optional[CallbackPolicy] = None,
        on_escalation: Optional[Callable[[CallbackTask, str], None]] = None,
        audit_log_path: Optional[str] = None
    ):
        """
        Initialize WatcherBus.

        Args:
            task_store: Storage for tasks
            adapter_registry: Registry of state adapters
            notifier_registry: Registry of notifiers
            policy: Callback policy (default: DefaultCallbackPolicy)
            on_escalation: Callback for escalation events
            audit_log_path: Path for audit log file
        """
        self.task_store = task_store
        self.adapter_registry = adapter_registry
        self.notifier_registry = notifier_registry
        self.policy = policy or DefaultCallbackPolicy()
        self.on_escalation = on_escalation
        self.audit_log_path = audit_log_path

        # Statistics
        self.stats = {
            'tasks_checked': 0,
            'states_changed': 0,
            'notifications_sent': 0,
            'notifications_failed': 0,
            'tasks_closed': 0,
            'tasks_escalated': 0,
            'errors': 0
        }

    def _log_audit(self, event: str, task: CallbackTask, details: Optional[Dict] = None) -> None:
        """Write audit log entry."""
        if not self.audit_log_path:
            return

        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'event': event,
                'task_id': task.task_id,
                'owner_agent': task.owner_agent,
                'current_state': task.current_state,
                'terminal': task.terminal,
                'details': details or {}
            }

            # Append to audit log
            with open(self.audit_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception as e:
            logger.warning(f"Failed to write audit log: {e}")

    def run_cycle(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Run one watcher cycle.

        Args:
            limit: Max tasks to process (None = all active)

        Returns:
            Statistics dict
        """
        logger.info("Starting watcher cycle")

        # Reset stats for this cycle
        self.stats = {
            'tasks_checked': 0,
            'states_changed': 0,
            'notifications_sent': 0,
            'notifications_failed': 0,
            'tasks_closed': 0,
            'tasks_escalated': 0,
            'errors': 0
        }

        # Get active tasks
        active_tasks = self.task_store.list_active(limit=limit)
        logger.info(f"Found {len(active_tasks)} active tasks")

        for task in active_tasks:
            try:
                self._process_task(task)
            except Exception as e:
                logger.error(f"Error processing task {task.task_id}: {e}")
                self.stats['errors'] += 1
                self._log_audit('error', task, {'error': str(e)})

        logger.info(f"Cycle complete: {self.stats}")
        return self.stats

    # Backward compatibility alias
    run_once = run_cycle

    def _process_task(self, task: CallbackTask) -> None:
        """Process a single task."""
        self.stats['tasks_checked'] += 1

        # Check for expiration
        if task.is_expired():
            logger.info(f"Task {task.task_id} expired, closing")
            self._close_task(task, TaskState.TIMEOUT)
            self.stats['tasks_closed'] += 1
            return

        # Find adapter
        adapter = self.adapter_registry.find_for_task(task)
        if not adapter:
            logger.warning(f"No adapter found for task {task.task_id}")
            self._log_audit('adapter_not_found', task)
            return

        # Check state
        state_result = adapter.check(task)
        logger.debug(f"Task {task.task_id} state: {state_result.state} (terminal={state_result.terminal})")

        # Update task with new state info
        state_changed = task.current_state != state_result.state
        if state_changed:
            logger.info(f"Task {task.task_id} state changed: {task.current_state} -> {state_result.state}")
            task.last_notified_state = task.current_state
            task.current_state = state_result.state
            task.confidence = state_result.confidence
            task.updated_at = datetime.now().isoformat()
            self.stats['states_changed'] += 1

        # Check if should close
        if self.policy.should_close(task, state_result):
            logger.info(f"Closing task {task.task_id} with state {state_result.state}")
            self._close_task(task, state_result.state)
            self.stats['tasks_closed'] += 1
            return

        # Check if should notify
        if self.policy.should_notify(task, state_result):
            logger.info(f"Notifying for task {task.task_id}")
            self._notify_task(task)

        # Check if should escalate
        if self.policy.should_escalate(task):
            logger.info(f"Escalating task {task.task_id}")
            self._escalate_task(task)
            self.stats['tasks_escalated'] += 1

        # Update task in store
        self.task_store.update(task.task_id, task.to_dict())

    def _close_task(self, task: CallbackTask, final_state: str) -> None:
        """Close a task with final state."""
        task.terminal = True
        task.current_state = final_state
        task.updated_at = datetime.now().isoformat()

        # Always send terminal notification (regardless of previous delivery)
        task.callback_delivered = False
        self._notify_task(task)

        # Update in store
        self.task_store.close(task.task_id, final_state)
        self._log_audit('task_closed', task, {'final_state': final_state})

    def _notify_task(self, task: CallbackTask) -> bool:
        """
        Send notification for a task.

        Returns:
            True if notification was sent successfully
        """
        # Find notifier
        notifier = self.notifier_registry.find_for_task(task)
        if not notifier:
            logger.warning(f"No notifier found for task {task.task_id} channel {task.reply_channel}")
            task.last_error = f"No notifier for channel: {task.reply_channel}"
            task.delivery_attempts += 1
            self.stats['notifications_failed'] += 1
            return False

        # Send notification
        try:
            result = notifier.send(task)
            task.delivery_attempts += 1

            if result.is_success():
                task.callback_delivered = True
                task.last_notified_state = task.current_state
                self.stats['notifications_sent'] += 1
                self._log_audit('notification_sent', task, {
                    'channel': task.reply_channel,
                    'message_id': result.provider_message_id
                })
                return True
            else:
                task.last_error = result.error
                self.stats['notifications_failed'] += 1
                self._log_audit('notification_failed', task, {
                    'channel': task.reply_channel,
                    'error': result.error
                })
                return False

        except Exception as e:
            task.last_error = str(e)
            task.delivery_attempts += 1
            self.stats['notifications_failed'] += 1
            self._log_audit('notification_error', task, {'error': str(e)})
            return False

    def _escalate_task(self, task: CallbackTask) -> None:
        """Escalate task to main agent."""
        self._log_audit('escalated', task)

        if self.on_escalation:
            try:
                reason = self._get_escalation_reason(task)
                self.on_escalation(task, reason)
            except Exception as e:
                logger.error(f"Escalation callback failed: {e}")

    def _get_escalation_reason(self, task: CallbackTask) -> str:
        """Get reason for escalation."""
        if task.delivery_attempts >= 3 and not task.callback_delivered:
            return f"Delivery failed {task.delivery_attempts} times"
        if task.is_expired():
            return "Task expired"
        return "Policy escalation"

    def get_health(self) -> Dict[str, Any]:
        """
        Get health status of the bus.

        Returns:
            Health status dict
        """
        active_count = self.task_store.count_active()
        adapter_health = self.adapter_registry.health_check_all()

        return {
            'status': 'healthy' if all(adapter_health.values()) else 'degraded',
            'active_tasks': active_count,
            'adapters': adapter_health,
            'last_cycle_stats': self.stats
        }


def create_default_bus(
    tasks_file: Optional[str] = None,
    audit_log: Optional[str] = None,
    notifications_dir: Optional[str] = None
) -> WatcherBus:
    """
    Create a WatcherBus with default configuration.

    Args:
        tasks_file: Path to tasks JSONL file
        audit_log: Path to audit log file
        notifications_dir: Directory for notification output

    Returns:
        Configured WatcherBus instance
    """
    # Default paths
    base_dir = os.path.expanduser("~/.openclaw/shared-context/monitor-tasks")

    if tasks_file is None:
        tasks_file = os.path.join(base_dir, "tasks.jsonl")
    if audit_log is None:
        audit_log = os.path.join(base_dir, "audit.log")
    if notifications_dir is None:
        notifications_dir = os.path.join(base_dir, "notifications")

    # Ensure directories exist
    os.makedirs(os.path.dirname(tasks_file) or base_dir, exist_ok=True)
    os.makedirs(os.path.dirname(audit_log) or base_dir, exist_ok=True)
    os.makedirs(notifications_dir, exist_ok=True)

    # Create components
    task_store = JsonlTaskStore(tasks_file)
    adapter_registry = create_default_adapter_registry()
    notifier_registry = create_default_notifier_registry(notifications_dir)
    policy = DefaultCallbackPolicy()

    return WatcherBus(
        task_store=task_store,
        adapter_registry=adapter_registry,
        notifier_registry=notifier_registry,
        policy=policy,
        audit_log_path=audit_log
    )
