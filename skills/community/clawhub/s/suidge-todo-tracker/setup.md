# Setup Guide

## Installation Steps

### 1. Copy Template File

```bash
cp skills/todo-tracker/templates/todo.json memory/todo.json
```

### 2. Update HEARTBEAT.md

Add this to your heartbeat checklist:

```markdown
3. **待跟进事项检查** — 读取 `memory/todo.json`：
   - 检查 `status=pending` 且 `follow_up_time` 已到的事项 → 提醒用户
   - 检查 `status=completed/cancelled` 且超过 24 小时的事项 → 删除
```

### 3. Update AGENTS.md

Add trigger keywords to your tool routing table:

```markdown
| 提醒我 / 跟进 / 别忘了 / 待办 / todo | `todo-tracker` 技能 |
```

## Verification

After installation, verify:

1. `memory/todo.json` exists and contains `{"items": []}`
2. Heartbeat check includes todo check step
3. Trigger keywords are registered

## Uninstall

Remove:
- `memory/todo.json`
- Heartbeat check step from HEARTBEAT.md
- Trigger keywords from AGENTS.md
- `skills/todo-tracker/` directory