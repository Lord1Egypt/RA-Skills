# task-watcher — Async Task Monitoring & Callback

> **Version**: 1.2.0  
> **Author**: sly (OpenClaw)  
> **License**: MIT  
> **Install**: `clawhub install task-watcher`

Monitor long-running async tasks (content review, CI/CD, deployments) and get Discord/Telegram notifications when states change.

## What It Does

Register tasks → Watcher polls for state changes → Sends notifications on change/completion.

Perfect for:
- **Content publishing**: Monitor XHS/社媒 review status after posting
- **CI/CD**: Track GitHub PR merges, build completions
- **Deployments**: Watch rollout status
- **Any async workflow**: Anything that takes time and you want to know when it's done

## Architecture

```
Agent registers task → tasks.jsonl (shared-context)
                            ↓
Cron (*/3 * * * *) → watcher.py → Adapter checks state → state changed?
                                                              ↓ Yes
                                              Policy decides → Notifier sends Discord
```

Plugin architecture:
- **Adapters**: Pluggable state checkers. Built-in: XHS, GitHub PR, Cron Job
- **Notifiers**: Discord (via `openclaw agent --deliver`), Telegram, Session, File
- **Policies**: Notification frequency, escalation, retry logic
- **Stores**: JSONL-based persistence with file locking
- **Protection**: `expires_at` timeout (default 6h), 3x delivery failure escalation

## Quick Start

### 1. Install

```bash
clawhub install task-watcher
```

### 2. Register a monitoring task

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
    current_state="submitted",
    expires_at="2026-03-08T12:00:00",  # 6h timeout recommended
)
store.create(task)
```

Or via CLI:

```bash
cd ~/.openclaw/workspace/skills/task-watcher
python3 scripts/register_task.py \
  --task-id tsk_my_001 \
  --system xiaohongshu \
  --object-id note_abc123 \
  --reply-to channel:1234567890 \
  --expires-hours 6
```

### 3. Run watcher (cron)

```bash
# Add to crontab - every 3 minutes
*/3 * * * * cd ~/.openclaw/workspace/skills/task-watcher && \
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

## File Structure

```
task-watcher/
├── SKILL.md                    # This file
├── _meta.json                  # ClawHub metadata
├── scripts/
│   ├── watcher.py              # Cron entry point
│   ├── register_task.py        # CLI task registration
│   └── lib/
│       ├── __init__.py         # Package exports
│       ├── models.py           # Data models (CallbackTask, StateResult, SendResult)
│       ├── stores.py           # JSONL TaskStore with file locking
│       ├── adapters.py         # State adapters (XHS, GitHub, Cron)
│       ├── notifiers.py        # Discord/Telegram/File notifiers
│       ├── policies.py         # Notification policies
│       └── bus.py              # WatcherBus orchestrator
└── tests/
    ├── test_models.py
    ├── test_stores.py
    ├── test_adapters.py
    ├── test_notifiers.py
    ├── test_policies.py
    └── test_bus.py
```

## Data Paths

| File | Purpose |
|------|---------|
| `~/.openclaw/shared-context/monitor-tasks/tasks.jsonl` | Active tasks |
| `~/.openclaw/shared-context/monitor-tasks/audit.log` | Audit trail |
| `~/.openclaw/shared-context/monitor-tasks/notifications/` | Notification files |

## Built-in Adapters

| Adapter | System | How It Checks |
|---------|--------|---------------|
| `xiaohongshu-note-review` | XHS content review | Mock file / packet file |
| `github-pr-status` | GitHub PR merge | Skeleton (extend for your use) |
| `cron-job-completion` | Cron job tracking | File-based status check |

## Requirements

- Python 3.10+
- OpenClaw 2026.3+ (for `openclaw agent --deliver`)
- No external dependencies (stdlib only)
