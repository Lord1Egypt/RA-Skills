"""Task callback event bus package.

A company-wide event bus for task monitoring and callbacks.

Components:
- models: Data models (CallbackTask, StateResult, SendResult)
- stores: Task persistence (JsonlTaskStore)
- adapters: State checking adapters (XiaohongshuNoteReviewAdapter)
- notifiers: Notification channels (DiscordNotifier, SessionNotifier)
- policies: Callback policies (DefaultCallbackPolicy)
- bus: Main orchestrator (WatcherBus)
"""

from .models import (
    CallbackTask,
    StateResult,
    SendResult,
    TaskType,
    TaskPriority,
    TaskState,
)

from .stores import (
    TaskStore,
    JsonlTaskStore,
)

from .adapters import (
    StateAdapter,
    XiaohongshuNoteReviewAdapter,
    GitHubPRStatusAdapter,
    CronJobCompletionAdapter,
    AdapterRegistry,
    create_default_adapter_registry,
)

from .notifiers import (
    Notifier,
    DirectNotifier,
    DiscordNotifier,
    TelegramNotifier,
    SessionNotifier,
    NotifierRegistry,
    create_default_notifier_registry,
)

from .policies import (
    CallbackPolicy,
    DefaultCallbackPolicy,
    AggressiveNotifyPolicy,
    ConservativePolicy,
    DictPolicyAdapter,
)

from .bus import (
    WatcherBus,
    create_default_bus,
)

__version__ = "1.0.0"

__all__ = [
    # Models
    "CallbackTask",
    "StateResult",
    "SendResult",
    "TaskType",
    "TaskPriority",
    "TaskState",
    # Stores
    "TaskStore",
    "JsonlTaskStore",
    # Adapters
    "StateAdapter",
    "XiaohongshuNoteReviewAdapter",
    "GitHubPRStatusAdapter",
    "CronJobCompletionAdapter",
    "AdapterRegistry",
    "create_default_adapter_registry",
    # Notifiers
    "Notifier",
    "DirectNotifier",
    "DiscordNotifier",
    "TelegramNotifier",
    "SessionNotifier",
    "NotifierRegistry",
    "create_default_notifier_registry",
    # Policies
    "CallbackPolicy",
    "DefaultCallbackPolicy",
    "AggressiveNotifyPolicy",
    "ConservativePolicy",
    "DictPolicyAdapter",
    # Bus
    "WatcherBus",
    "create_default_bus",
]
