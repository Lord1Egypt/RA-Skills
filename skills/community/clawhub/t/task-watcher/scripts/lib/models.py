"""Data models for task callback event bus."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict
import json


class TaskType(str, Enum):
    """Types of callback tasks."""
    STATUS_MONITOR = "status_monitor"
    JOB_COMPLETION = "job_completion"
    APPROVAL_WORKFLOW = "approval_workflow"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskState(str, Enum):
    """Standard task states."""
    SUBMITTED = "submitted"
    PENDING = "pending"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class CallbackTask:
    """
    Unified callback task model.

    Represents a task that needs to be monitored and notified upon state changes.
    """
    task_id: str
    schema_version: str = "1.0"
    owner_agent: str = ""
    task_type: str = TaskType.STATUS_MONITOR
    target_system: str = ""
    adapter: str = ""  # Which StateAdapter to use
    target_object_id: str = ""  # e.g., note_id, pr_number
    source_of_truth: str = "browser_page"  # webhook/api/browser_page/local_file
    reply_channel: str = "discord"  # discord/telegram/session
    reply_to: str = ""  # e.g., "channel:1475430870318846048"
    requester_id: str = ""
    current_state: str = TaskState.SUBMITTED
    last_notified_state: str = ""
    last_state_hash: str = ""
    terminal: bool = False
    callback_delivered: bool = False
    delivery_attempts: int = 0
    confidence: float = 1.0
    priority: str = TaskPriority.NORMAL
    needs_human_input: bool = False
    last_error: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    expires_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.last_notified_state:
            self.last_notified_state = self.current_state

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CallbackTask":
        """Create from dictionary."""
        # Filter only known fields
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "CallbackTask":
        """Create from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def update_state(self, new_state: str, confidence: float = 1.0) -> bool:
        """
        Update state if changed.

        Returns True if state actually changed.
        """
        if self.current_state != new_state:
            self.last_notified_state = self.current_state
            self.current_state = new_state
            self.confidence = confidence
            self.updated_at = datetime.now().isoformat()
            return True
        return False

    def mark_terminal(self, final_state: str, delivered: bool = False) -> None:
        """Mark task as terminal."""
        self.current_state = final_state
        self.terminal = True
        self.callback_delivered = delivered
        self.updated_at = datetime.now().isoformat()

    def is_expired(self) -> bool:
        """Check if task has expired."""
        if not self.expires_at:
            return False
        try:
            expires = datetime.fromisoformat(self.expires_at)
            return datetime.now() > expires
        except (ValueError, TypeError):
            return False

    def should_notify(self) -> bool:
        """Check if notification should be sent."""
        return self.current_state != self.last_notified_state


@dataclass
class StateResult:
    """
    Result of a state check by adapter.

    This is the standardized output format for all StateAdapters.
    """
    state: str
    terminal: bool = False
    confidence: float = 1.0
    source_of_truth: str = "browser_page"
    raw_evidence: str = ""
    error: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        """Check if state check was successful."""
        return not self.error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StateResult":
        """Create from dictionary."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)


@dataclass
class SendResult:
    """
    Result of a notification send operation.

    This is the standardized output format for all Notifiers.
    """
    ok: bool = False
    delivered: bool = False
    provider_message_id: str = ""
    error: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        """Check if send was successful."""
        return self.ok and self.delivered

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SendResult":
        """Create from dictionary."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in known_fields}
        return cls(**filtered_data)
