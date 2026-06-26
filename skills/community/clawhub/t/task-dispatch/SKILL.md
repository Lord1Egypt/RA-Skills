---
name: task-dispatch
description: "Task scheduling and dispatching for task boards. Use when setting up periodic task dispatch, checking for dispatchable tasks, creating subagents to execute tasks, or verifying task completion. Supports task board APIs like ClawBoard."
---

# Task Dispatch

Automated task scheduling and execution for task management systems.

## Quick Start

用户说"设置任务调度"或"部署 ClawBoard"时，按以下流程引导：

### Step 1: 检测环境

```bash
# 检查 Node.js
node --version  # 需要 >= 18

# 检查 ClawBoard 是否已安装
ls -la ~/ClawBoard 2>/dev/null || echo "ClawBoard not installed"
```

### Step 2: 部署 ClawBoard（如未安装）

```bash
# 克隆仓库
git clone https://github.com/CCCaptain0129/ClawBoard.git ~/ClawBoard
cd ~/ClawBoard

# 安装依赖并初始化
./clawboard install

# 生成访问 token（自动保存到 .env）
./clawboard token --generate
```

### Step 3: 启动服务

```bash
cd ~/ClawBoard
./clawboard start

# 检查状态
./clawboard status
```

### Step 4: 配置 Agent 环境

在 Agent 工作目录创建 `.env` 文件：

```bash
# 获取 token
TOKEN=$(cat ~/ClawBoard/.env | grep BOARD_ACCESS_TOKEN | cut -d= -f2)

# 写入 Agent 工作目录
echo "TASKBOARD_API_URL=http://127.0.0.1:3000" >> ~/.openclaw/workspace-<name>/.env
echo "TASKBOARD_ACCESS_TOKEN=$TOKEN" >> ~/.openclaw/workspace-<name>/.env
```

### Step 5: 打开看板

- **前端看板**: http://127.0.0.1:5173
- **后端 API**: http://127.0.0.1:3000
- 输入 `.env` 中的 `BOARD_ACCESS_TOKEN` 登录

### Step 6: 设置定时调度（可选）

用户说"设置定时调度"时：

```json
{
  "name": "ClawBoard 调度巡检",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "payload": {
    "kind": "agentTurn",
    "message": "执行 task-dispatch 调度检查。无任务时返回 HEARTBEAT_OK。"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "none" }
}
```

---

## Agent Role

**You are a dispatcher, not an executor.**

- Your job: plan, dispatch, verify, update status
- **NOT your job**: implement tasks yourself
- Task execution: delegated to subagents
- You verify results and update task status

## Data Source of Truth

| What | Source |
|------|--------|
| Task data | API endpoint (e.g., `http://127.0.0.1:3000/api/tasks/...`) |
| Task files | `tasks/*.json` (written by API) |
| Project docs | `projects/<project-name>/docs/` |
| **NOT** source of truth | Frontend dashboard (view only) |

## ClawBoard Deployment Guide

### Prerequisites

- Node.js >= 18
- Git
- PM2 (auto-installed by `./clawboard install`)

### Installation Commands

| Command | Description |
|---------|-------------|
| `./clawboard install` | Install dependencies, create .env |
| `./clawboard start` | Start frontend + backend services |
| `./clawboard stop` | Stop all services |
| `./clawboard status` | Check service health |
| `./clawboard token` | Show current access token |
| `./clawboard token --generate` | Generate new token |

### Verification Checklist

After deployment, verify:

1. ✅ Backend API responds: `curl http://127.0.0.1:3000/health`
2. ✅ Frontend loads: open http://127.0.0.1:5173
3. ✅ Token works: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:3000/api/tasks/projects`
4. ✅ Agent .env configured with token

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `lsof -i :3000` then kill process |
| Port 5173 in use | `lsof -i :5173` then kill process |
| Token not working | Regenerate with `./clawboard token --generate` |
| Services not starting | Check logs in `~/ClawBoard/logs/` |

---

## Dispatch Operations

### Overview

This skill enables agents to:
1. Check task boards for dispatchable tasks
2. Spawn subagents to execute tasks
3. Verify completion and update task status
4. **Continue dispatching until no tasks remain** (no waiting for next cron)

### Key Principle: Continuous Dispatch

```
触发一次 → 循环执行直到无任务 → 结束

而不是：

触发一次 → 派发一个任务 → 等待下次触发
```

### Dispatch Loop

```python
def dispatch_loop():
    while True:
        task = select_dispatchable_task()
        if not task:
            return HEARTBEAT_OK  # 本轮结束
        
        # 派发并等待完成
        result = spawn_and_wait(task)
        
        # 验收
        if result.success:
            update_task(task.id, status="review")
        else:
            update_task(task.id, status="failed", blockingReason=result.error)
        
        # 【关键】立即继续下一轮，不返回
        # 循环会自动检查下一个任务
```

---

## API Reference

### Get Projects
```
GET {TASKBOARD_API_URL}/api/tasks/projects
Authorization: Bearer {TOKEN}
```

### Get Tasks
```
GET {TASKBOARD_API_URL}/api/tasks/projects/{projectId}/tasks
Authorization: Bearer {TOKEN}
```

### Create Project
```
POST {TASKBOARD_API_URL}/api/tasks/projects
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "id": "my-project",
  "name": "My Project",
  "description": "...",
  "taskPrefix": "MP",
  "color": "#3B82F6",
  "icon": "📁"
}
```

### Create Task
```
POST {TASKBOARD_API_URL}/api/tasks/projects/{projectId}/tasks
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "title": "Task title",
  "description": "...",
  "status": "todo",
  "priority": "P1",
  "executionMode": "auto",
  "assignee": "agent-id"
}
```

### Update Task
```
PUT {TASKBOARD_API_URL}/api/tasks/projects/{projectId}/tasks/{taskId}
Authorization: Bearer {TOKEN}
Content-Type: application/json

{
  "status": "in-progress",
  "claimedBy": "agent-id"
}
```

---

## Task Selection Rules

A task is dispatchable if ALL conditions are met:

| Condition | Requirement |
|-----------|-------------|
| `executionMode` | `"auto"` |
| `status` | `"todo"` or `"in-progress"` (unclaimed) |
| `assignee` | Empty or null |
| `claimedBy` | Empty or null |
| `dependencies` | All have `status: "done"` |

### Priority Order

1. `P0` > `P1` > `P2` > `P3`
2. Same priority: earlier `createdAt` first

---

## Subagent Execution

### Prepare Dispatch Context

Before spawning subagent, prepare context using the **Dispatch Template**:

See [references/dispatch-template.md](references/dispatch-template.md) for full template.

**Required fields to fill:**
- Task Identity (from task data)
- Goal (one sentence)
- Hard Constraints (what NOT to do)
- Deliverables (from task.deliverables)
- Acceptance Criteria (from task.acceptanceCriteria)
- Output Format (completion_signal block)

### Spawn with Wait

Use `sessions_spawn` with the dispatch context:

```json
{
  "runtime": "subagent",
  "mode": "run",
  "task": "<filled dispatch template>",
  "timeoutSeconds": 300
}
```

The main agent should:
1. Fill dispatch template with task context
2. Spawn subagent with the template
3. **Wait for completion** (blocking or polling)
4. Parse `completion_signal` from response
5. Verify deliverables and update status
6. **Immediately continue to next task**

### Completion Signal

Subagent must return a `completion_signal` block:

```completion_signal
task_id: <taskId>
status: done | blocked
summary: <one sentence summary>
deliverables: <comma-separated paths>
next_step: <N/A if done; blocking reason if blocked>
```

Parse this block to determine task outcome:
- `status: done` → Verify deliverables, update to `review`
- `status: blocked` → Update to `failed` with `blockingReason`

---

## Status Transitions

```
todo → in-progress → review → done
                ↓         ↓
              failed    failed
```

**Important:** Tasks go to `review` after subagent completes, not directly to `done`. User or main agent verifies before `done`.

---

## Verification Checklist

After subagent completes, verify:

1. **Deliverables exist**
   - Check all paths in `deliverables` array
   - Files should be non-empty

2. **Acceptance criteria met**
   - Review each criterion
   - Mark pass/fail

3. **Update status**
   - All pass → `review`
   - Any fail → `failed` with `blockingReason`

---

## Heartbeat Response

When triggered by cron/heartbeat:

- **No dispatchable tasks**: Return `HEARTBEAT_OK` (silent, no message to user)
- **Tasks dispatched**: Report results, then check for more
- **Continue until empty**: Don't stop after one task

---

## Failure Handling

When a task fails or has no valid execution:

1. **Record the reason** in `blockingReason` field
2. **Clear invalid occupation** (`claimedBy`)
3. **Return task to actionable state** (`todo` or `in-progress`)
4. **Never fail silently** - always log or report

### Common Failure Scenarios

| Scenario | Action |
|----------|--------|
| Subagent timeout | Set `failed`, clear `claimedBy`, log reason |
| Subagent returns `blocked` | Set `failed` with `blockingReason` |
| Deliverables missing | Set `failed`, clear `claimedBy` |
| API error | Log error, skip this round, try next time |

---

## Dispatch Principles

1. **Only dispatch `executionMode=auto` tasks**
2. **Priority order**: `todo` first, then unclaimed `in-progress`
3. **Respect assignee**: Don't re-dispatch if `assignee` is set
4. **Verify before done**: Tasks go to `review` first, then `done` after verification

---

## Configuration

See [references/config.md](references/config.md) for:
- Task board adapters
- Priority mappings
- Execution timeouts
- Retry policies

---

## Example Usage

### Deploy ClawBoard
```
"部署 ClawBoard 看板"
```

### Setup with User Guidance
```
"帮我设置任务调度系统"
```

### Manual Dispatch (runs until empty)
```
"检查任务看板，派发所有待执行任务"
```

### Setup Periodic Check
```
"设置每10分钟自动检查任务"
```

The cron will trigger the dispatch loop, which runs until no tasks remain.