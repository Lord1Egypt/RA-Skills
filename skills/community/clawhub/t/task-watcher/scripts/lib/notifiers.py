"""Notifier interface and implementations for sending notifications."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
import os

try:
    from .models import CallbackTask, SendResult, TaskState
except ImportError:
    from models import CallbackTask, SendResult, TaskState


class Notifier(ABC):
    """
    Abstract interface for sending notifications.

    Each notifier knows how to send messages to a specific channel.
    The output is standardized to SendResult.
    """

    @property
    @abstractmethod
    def channel(self) -> str:
        """Channel identifier (e.g., 'discord', 'telegram')."""
        pass

    @abstractmethod
    def send(self, task: CallbackTask, payload: Optional[Dict[str, Any]] = None) -> SendResult:
        """
        Send notification for a task.

        Args:
            task: Task to notify about
            payload: Optional custom payload (if None, generate from task)

        Returns:
            SendResult with delivery status
        """
        pass

    def format_message(self, task: CallbackTask, event_type: str = "state_change") -> str:
        """
        Format notification message.

        Args:
            task: Task to format message for
            event_type: Type of event (created, state_change, terminal)

        Returns:
            Formatted message string
        """
        if event_type == "created":
            return self._format_created_message(task)
        elif event_type == "terminal":
            return self._format_terminal_message(task)
        else:
            return self._format_state_change_message(task)

    def _format_created_message(self, task: CallbackTask) -> str:
        """Format message for task creation."""
        return f"""已开始监控任务。
- task_id: {task.task_id}
- 目标系统: {task.target_system}
- 当前状态: {task.current_state}
- 回报频道: {task.reply_to}
- 触发条件: 状态变化 / 终态完成"""

    def _format_state_change_message(self, task: CallbackTask) -> str:
        """Format message for state change."""
        return f"""任务状态更新。
- task_id: {task.task_id}
- 状态变化: {task.last_notified_state} -> {task.current_state}
- 置信度: {task.confidence:.0%}
- 时间: {task.updated_at}"""

    def _format_terminal_message(self, task: CallbackTask) -> str:
        """Format message for terminal state."""
        state_emoji = {
            TaskState.APPROVED: "✅",
            TaskState.REJECTED: "❌",
            TaskState.COMPLETED: "✅",
            TaskState.FAILED: "❌",
            TaskState.TIMEOUT: "⏰",
            TaskState.CANCELLED: "🚫"
        }.get(task.current_state, "📋")

        state_text = str(task.current_state).upper()
        return f"""{state_emoji} 监控任务已完成。
- task_id: {task.task_id}
- 最终状态: {state_text}
- 时间: {task.updated_at}
- 下次步骤: 可查看详细结果或继续后续操作"""


class DiscordNotifier(Notifier):
    """
    Discord channel notifier via OpenClaw agent CLI.

    Sends real Discord messages through `openclaw agent --deliver`.
    Also writes to file as audit trail.
    """

    def __init__(self, output_dir: Optional[str] = None, agent_id: str = "main",
                 openclaw_bin: Optional[str] = None, dry_run: bool = False):
        self.output_dir = output_dir or os.path.expanduser(
            "~/.openclaw/shared-context/monitor-tasks/notifications"
        )
        self.agent_id = agent_id
        self.openclaw_bin = openclaw_bin or self._find_openclaw_bin()
        self.dry_run = dry_run
        self._ensure_output_dir()

    def _find_openclaw_bin(self) -> str:
        """Locate openclaw binary."""
        candidates = [
            os.path.expanduser("~/.npm-global/bin/openclaw"),
            "/usr/local/bin/openclaw",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0]

    def _ensure_output_dir(self) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    @property
    def channel(self) -> str:
        return "discord"

    def send(self, task: CallbackTask, payload: Optional[Dict[str, Any]] = None) -> SendResult:
        """
        Send notification to Discord via openclaw agent --deliver.

        Also writes to file as audit trail.
        """
        try:
            if payload is None:
                if task.terminal:
                    event_type = "terminal"
                elif task.delivery_attempts == 0:
                    event_type = "created"
                else:
                    event_type = "state_change"
                message = self.format_message(task, event_type)
            else:
                message = payload.get('message') or payload.get('text', '')

            self._write_notification_file(task, message)

            if self.dry_run:
                return SendResult(
                    ok=True,
                    delivered=True,
                    provider_message_id="dry_run",
                    metadata={'dry_run': True}
                )

            return self._send_via_openclaw(task, message)

        except Exception as e:
            return SendResult(
                ok=False,
                delivered=False,
                error=str(e)
            )

    def _send_via_openclaw(self, task: CallbackTask, message: str) -> SendResult:
        """Send message through openclaw agent --deliver."""
        import subprocess

        node_path = "/opt/homebrew/bin/node"
        env = os.environ.copy()
        env["PATH"] = "/opt/homebrew/bin:" + env.get("PATH", "")

        reply_channel = task.reply_to or ""
        channel_id = reply_channel.replace("channel:", "") if reply_channel.startswith("channel:") else ""

        cmd = [
            node_path, self.openclaw_bin,
            "agent",
            "--agent", self.agent_id,
            "--channel", "discord",
            "--deliver",
            "--message", "[Watcher] " + message,
        ]
        if channel_id:
            cmd.extend(["--reply-to", "channel:" + channel_id])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120, env=env
            )
            if result.returncode == 0:
                return SendResult(
                    ok=True,
                    delivered=True,
                    provider_message_id="openclaw-agent-" + task.task_id,
                    metadata={'stdout': result.stdout[:500], 'method': 'openclaw_agent'}
                )
            else:
                return SendResult(
                    ok=False,
                    delivered=False,
                    error="openclaw agent exit " + str(result.returncode) + ": " + result.stderr[:300],
                    metadata={'method': 'openclaw_agent'}
                )
        except subprocess.TimeoutExpired:
            return SendResult(ok=False, delivered=False, error="openclaw agent timed out (120s)")
        except FileNotFoundError:
            return SendResult(ok=False, delivered=False, error="openclaw binary not found: " + self.openclaw_bin)

    def _write_notification_file(self, task: CallbackTask, message: str) -> None:
        """Write notification to file as audit trail."""
        notification_file = os.path.join(
            self.output_dir,
            task.task_id + "_" + task.updated_at.replace(':', '-') + ".json"
        )
        notification_data = {
            'task_id': task.task_id,
            'channel': self.channel,
            'reply_to': task.reply_to,
            'message': message,
            'timestamp': task.updated_at,
        }
        with open(notification_file, 'w', encoding='utf-8') as f:
            json.dump(notification_data, f, ensure_ascii=False, indent=2)


class TelegramNotifier(Notifier):
    """
    Telegram notifier (placeholder for future implementation).
    """

    @property
    def channel(self) -> str:
        return "telegram"

    def send(self, task: CallbackTask, payload: Optional[Dict[str, Any]] = None) -> SendResult:
        """Send notification to Telegram."""
        return SendResult(
            ok=False,
            delivered=False,
            error="Telegram notifier not yet implemented"
        )


class SessionNotifier(Notifier):
    """
    Notifier for current session/CLI context.

    Useful for testing and CLI usage.
    """

    def __init__(self):
        self.last_message: Optional[str] = None

    @property
    def channel(self) -> str:
        return "session"

    def send(self, task: CallbackTask, payload: Optional[Dict[str, Any]] = None) -> SendResult:
        """Send notification to session (prints to stdout)."""
        try:
            if payload is None:
                if task.terminal:
                    event_type = "terminal"
                elif task.delivery_attempts == 0:
                    event_type = "created"
                else:
                    event_type = "state_change"
                message = self.format_message(task, event_type)
            else:
                message = payload.get('message') or payload.get('text', '')

            self.last_message = message

            # Print to stdout
            print(f"\n{'='*50}")
            print(f"[TASK NOTIFICATION] {task.task_id}")
            print(f"{'='*50}")
            print(message)
            print(f"{'='*50}\n")

            return SendResult(
                ok=True,
                delivered=True,
                metadata={'channel': 'session'}
            )

        except Exception as e:
            return SendResult(
                ok=False,
                delivered=False,
                error=str(e)
            )

    def get_last_message(self) -> Optional[str]:
        """Get the last message sent (useful for testing)."""
        return self.last_message


class DirectNotifier(Notifier):
    """
    Direct file-based notifier for script-first, LLM-last approach.

    Writes notifications to a structured directory for external pickup:
    - Discord bot polls and sends
    - Webhook handlers read and forward
    - CLI tools display

    This is the preferred notifier for MVP as it:
    1. Requires no external API calls (scripts don't block)
    2. Provides durable notification queue
    3. Allows LLM to inspect before sending (LLM-last)
    4. Enables multiple consumers
    """

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize Direct notifier.

        Args:
            output_dir: Directory to write notification files
                       Default: ~/.openclaw/shared-context/monitor-tasks/notifications
        """
        self.output_dir = output_dir or os.path.expanduser(
            "~/.openclaw/shared-context/monitor-tasks/notifications"
        )
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    @property
    def channel(self) -> str:
        return "direct"

    def send(self, task: CallbackTask, payload: Optional[Dict[str, Any]] = None) -> SendResult:
        """
        Write notification to file for external pickup.

        File format: {task_id}_{timestamp}.json
        Contains: task_id, reply_to, message, timestamp, terminal flag

        Args:
            task: Task to notify about
            payload: Optional custom payload

        Returns:
            SendResult with file path as provider_message_id
        """
        try:
            # Determine event type and format message
            if payload is None:
                if task.terminal:
                    event_type = "terminal"
                elif task.delivery_attempts == 0:
                    event_type = "created"
                else:
                    event_type = "state_change"
                message = self.format_message(task, event_type)
            else:
                message = payload.get('message') or payload.get('text', '')
                event_type = payload.get('event_type', 'unknown')

            # Generate unique filename with timestamp
            import time
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            safe_task_id = task.task_id.replace('/', '_').replace(':', '_')
            filename = f"{safe_task_id}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)

            # Build notification envelope
            notification = {
                'schema_version': '1.0',
                'task_id': task.task_id,
                'event_type': event_type,
                'channel': 'direct',
                'reply_channel': task.reply_channel,
                'reply_to': task.reply_to,
                'requester_id': task.requester_id,
                'current_state': task.current_state,
                'terminal': task.terminal,
                'message': message,
                'timestamp': task.updated_at,
                'filepath': filepath,
                'metadata': {
                    'target_system': task.target_system,
                    'target_object_id': task.target_object_id,
                    'delivery_attempts': task.delivery_attempts,
                }
            }

            # Atomic write: write to temp then rename
            temp_path = filepath + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(notification, f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.rename(temp_path, filepath)

            return SendResult(
                ok=True,
                delivered=True,
                provider_message_id=filepath,
                metadata={
                    'filepath': filepath,
                    'filename': filename,
                    'event_type': event_type
                }
            )

        except Exception as e:
            return SendResult(
                ok=False,
                delivered=False,
                error=f"Direct notification failed: {e}"
            )

    def list_pending(self, limit: Optional[int] = None) -> list:
        """
        List pending notification files.

        Useful for consumers to poll for new notifications.

        Args:
            limit: Maximum number to return

        Returns:
            List of file paths, sorted by modification time (newest first)
        """
        if not os.path.exists(self.output_dir):
            return []

        files = [
            os.path.join(self.output_dir, f)
            for f in os.listdir(self.output_dir)
            if f.endswith('.json') and not f.endswith('.tmp')
        ]
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        if limit:
            return files[:limit]
        return files

    def read_notification(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Read a notification file.

        Args:
            filepath: Path to notification file

        Returns:
            Notification dict or None if error
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def ack(self, filepath: str) -> bool:
        """
        Acknowledge and remove a notification.

        Args:
            filepath: Path to notification file

        Returns:
            True if successfully removed
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except OSError:
            pass
        return False


class NotifierRegistry:
    """Registry for managing notifiers."""

    def __init__(self):
        self._notifiers: Dict[str, Notifier] = {}

    def register(self, notifier: Notifier) -> None:
        """Register a notifier."""
        self._notifiers[notifier.channel] = notifier

    def get(self, channel: str) -> Optional[Notifier]:
        """Get notifier by channel."""
        return self._notifiers.get(channel)

    def find_for_task(self, task: CallbackTask) -> Optional[Notifier]:
        """Find notifier for the given task's reply_channel."""
        if task.reply_channel and task.reply_channel in self._notifiers:
            return self._notifiers.get(task.reply_channel)
        return None

    def list_channels(self) -> list:
        """List all registered channel names."""
        return list(self._notifiers.keys())


def create_default_notifier_registry(output_dir: Optional[str] = None,
                                     dry_run: bool = False) -> NotifierRegistry:
    """Create registry with default notifiers."""
    registry = NotifierRegistry()
    registry.register(DirectNotifier(output_dir))
    registry.register(DiscordNotifier(output_dir, dry_run=dry_run))
    registry.register(TelegramNotifier())
    registry.register(SessionNotifier())
    return registry
