# task-watcher

> Async Task Monitoring & Callback for OpenClaw Agents

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests: 130 passed](https://img.shields.io/badge/tests-130%20passed-brightgreen.svg)]()

Monitor long-running async tasks (content review, CI/CD, deployments) and get Discord notifications when states change. Zero external dependencies — stdlib only.

## How It Works

```
Agent registers task --> tasks.jsonl (shared-context)
                              |
Cron (*/5 * * * *) --> watcher.py --> Adapter checks state --> state changed?
                                                                    | Yes
                                                      Policy decides --> Notifier sends Discord
```

## Quick Start

### 1. Install

```bash
# OpenClaw ClawHub
clawhub install task-watcher

# Or clone directly
git clone https://github.com/lanyasheng/task-watcher.git ~/.openclaw/workspace/skills/task-watcher
```

### 2. Register a task

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/skills/task-watcher/scripts/lib"))

from models import CallbackTask
from stores import JsonlTaskStore

store = JsonlTaskStore("~/.openclaw/shared-context/monitor-tasks/tasks.jsonl")
task = CallbackTask(
    task_id="tsk_my_task_001",
    owner_agent="content",
    target_system="xiaohongshu",
    target_object_id="note_id_here",
    reply_channel="discord",
    reply_to="channel:YOUR_CHANNEL_ID",
    expires_at="2026-03-08T12:00:00",
)
store.create(task)
```

Or via CLI:

```bash
python3 scripts/register_task.py \
  --task-id tsk_my_001 \
  --system xiaohongshu \
  --object-id note_abc123 \
  --reply-to channel:1234567890 \
  --expires-hours 6
```

### 3. Set up cron

```bash
*/5 * * * * cd ~/.openclaw/workspace/skills/task-watcher && \
  python3 scripts/watcher.py --once >> ~/.openclaw/logs/watcher.log 2>&1
```

### 4. Custom adapter

```python
from adapters import StateAdapter, StateResult

class MyAdapter(StateAdapter):
    @property
    def name(self): return "my-system"
    def supports(self, task): return task.target_system == "my-system"
    def health_check(self): return True

    def check(self, task):
        status = check_my_system(task.target_object_id)
        return StateResult(state=status, terminal=(status == "done"))
```

## Architecture

Plugin-based design with clear separation of concerns:

| Component | Purpose | Built-in |
|-----------|---------|----------|
| **Adapters** | Check task state from external systems | XHS, GitHub PR (skeleton), Cron Job |
| **Notifiers** | Deliver state-change notifications | Discord, Telegram (skeleton), Session |
| **Policies** | Decide when/how to notify | Default, Aggressive, Conservative |
| **Stores** | Persist task data | JSONL with file locking |

### Safety Features

- **Auto-expiry**: Tasks expire after configurable timeout (default 6h)
- **Escalation**: 3 consecutive delivery failures trigger escalation callback
- **Audit trail**: Every state change logged to `audit.log`
- **File locking**: Safe for concurrent cron execution

## Project Structure

```
task-watcher/
├── SKILL.md              # OpenClaw skill definition
├── _meta.json            # ClawHub metadata
├── README.md             # This file
├── scripts/
│   ├── watcher.py        # Cron entry point
│   ├── register_task.py  # CLI task registration
│   └── lib/
│       ├── models.py     # Data models
│       ├── stores.py     # JSONL persistence
│       ├── adapters.py   # State adapters
│       ├── notifiers.py  # Notification channels
│       ├── policies.py   # Notification policies
│       └── bus.py        # WatcherBus orchestrator
└── tests/
    ├── conftest.py       # Test path setup
    ├── test_models.py
    ├── test_stores.py
    ├── test_adapters.py
    ├── test_notifiers.py
    ├── test_policies.py
    └── test_bus.py
```

## Running Tests

```bash
cd task-watcher
python3 -m pytest tests/ -v
# 130 tests, 0 dependencies
```

## Requirements

- Python 3.10+
- OpenClaw 2026.3+ (for Discord delivery via `openclaw agent --deliver`)
- No external pip packages required

## License

MIT
