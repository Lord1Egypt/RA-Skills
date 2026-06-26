# Synapse Brain — Architecture Reference

## Brain/Hands Architecture

This document describes the v2.0 architecture where Synapse Brain acts as the persistent orchestrator for synapse-code and synapse-wiki.

### Architecture Overview

```
┌─────────────────────────────────────────┐
│           User (Telegram/CLI)            │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Synapse Brain (持久调度)          │
│                                         │
│  SOUL.md: Agent 角色定义                  │
│  SKILL.md: 技能接口定义                   │
│  Scripts:                                │
│    - state_manager.py (持久化)            │
│    - task_router.py (路由)               │
│    - session_init.py (会话管理)           │
│    - subagent_dispatch.py (子代理调度)    │
└────┬───────────┬──────────┬─────────────┘
     │           │          │
     ▼           ▼          ▼
┌────────┐ ┌────────┐ ┌──────────┐
│ code   │ │ wiki   │ │ 子代理    │
│ Skill  │ │ Skill  │ │ (dev/qa) │
└────────┘ └────────┘ └──────────┘
```

### State Persistence

Session state is stored in `~/.openclaw/brain-state/{project}.json`:

```json
{
  "session_id": "unique_id",
  "project": "name",
  "title": "description",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "tasks": [
    {
      "id": "task-001",
      "title": "task description",
      "status": "completed|in_progress|failed|interrupted|pending",
      "skill": "synapse-code|synapse-wiki",
      "mode": "standalone|lite|full|parallel",
      "stage": "REQ|ARCH|DEV|INT|QA|DEPLOY",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ],
  "subagents": {
    "active": 0,
    "completed": 0,
    "failed": 0
  },
  "knowledge": {
    "wiki_initialized": false,
    "wiki_root": null,
    "last_ingest": null
  },
  "log": ["[timestamp] event description"]
}
```

### Intent Routing Pipeline

1. **Input**: User natural language
2. **Classification**: task_router.py matches keywords → intent
3. **Routing**: Intent maps to skill + command + mode
4. **Dispatch**: Brain invokes the target skill
5. **Result**: Output aggregated and state updated

### Task Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Planned, not started |
| `in_progress` | Actively being worked on |
| `interrupted` | Session ended before completion |
| `completed` | Done and verified |
| `failed` | Failed with error |

### Migration from v1.x

v1.x used external `pipeline.py` for orchestration. v2.0 replaces this with:

| v1.x | v2.0 |
|------|------|
| `pipeline.py` | Brain Agent + subagents |
| `config.json` pipeline.workspace | `state.json` per project |
| External ContractBoard | Brain internal state tracking |
| Manual mode selection | Automatic intent routing |

The `legacy` mode is still supported for backward compatibility with existing `pipeline.py` installations.
