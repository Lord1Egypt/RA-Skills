# Task Dispatch Configuration

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TASKBOARD_API_URL` | Task board API endpoint | `http://127.0.0.1:3000` |
| `TASKBOARD_ACCESS_TOKEN` | API authentication token | (required) |
| `TASK_DISPATCH_INTERVAL_MS` | Cron interval in milliseconds | `300000` (5 min) |

## Task Board Adapters

### ClawBoard (Default)

```json
{
  "type": "clawboard",
  "apiUrl": "http://127.0.0.1:3000",
  "endpoints": {
    "projects": "/api/tasks/projects",
    "tasks": "/api/tasks/projects/{projectId}/tasks",
    "updateTask": "/api/tasks/projects/{projectId}/tasks/{taskId}"
  }
}
```

### Custom Adapter

Implement these methods:
- `getProjects()`: Return list of projects
- `getTasks(projectId)`: Return tasks for a project
- `updateTask(projectId, taskId, updates)`: Update task status

## Priority Mapping

| Level | Name | Weight |
|-------|------|--------|
| P0 | Critical | 0 |
| P1 | High | 1 |
| P2 | Medium | 2 |
| P3 | Low | 3 |

## Execution Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `maxConcurrentTasks` | Max parallel subagents (1 = sequential) | 1 |
| `taskTimeoutMs` | Subagent execution timeout | 300000 (5 min) |
| `retryCount` | Retry attempts on failure | 2 |
| `retryDelayMs` | Delay between retries | 60000 (1 min) |
| `continueOnSuccess` | Continue to next task after success | true |
| `continueOnFailure` | Continue to next task after failure | true |

## Continuous Dispatch

**Recommended:** Sequential execution with continuous loop

```
while (has_dispatchable_tasks):
    task = select_next_task()
    result = execute_and_wait(task)
    verify_and_update(task, result)
    # 立即继续，不等待
```

**Alternative:** Parallel execution (advanced)

```
# 同时派发多个任务
tasks = select_n_tasks(max_concurrent)
for task in tasks:
    spawn_subagent(task)

# 等待所有完成
wait_all_complete()
verify_all()
```

## Cron Job Configuration

```json
{
  "name": "Task Dispatch",
  "schedule": {
    "kind": "every",
    "everyMs": 300000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行 task-dispatch 调度检查。检查任务看板 API，筛选可派发任务，执行调度。无任务时返回 HEARTBEAT_OK。"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "feishu"
  }
}
```

### Schedule Types

| Kind | Format | Example |
|------|--------|---------|
| `every` | `{ "kind": "every", "everyMs": 300000 }` | Every 5 minutes |
| `cron` | `{ "kind": "cron", "expr": "*/5 * * * *" }` | Cron expression |
| `at` | `{ "kind": "at", "at": "2026-03-25T15:00:00Z" }` | One-shot at time |

## Task Schema

Required fields for auto-dispatch:

```typescript
interface Task {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in-progress" | "review" | "done" | "failed";
  priority: "P0" | "P1" | "P2" | "P3";
  executionMode: "auto" | "manual";
  assignee?: string;
  claimedBy?: string;
  dependencies?: string[];
  deliverables?: string[];
  acceptanceCriteria?: string[];
  blockingReason?: string;
}
```

## Failure Handling

When a task fails:
1. Set `status: "failed"`
2. Set `blockingReason` with error details
3. Clear `claimedBy`
4. Log error for review

Retry logic:
1. Check `retryCount` remaining
2. If retries left, reset to `todo` after `retryDelayMs`
3. If no retries, keep `failed` for manual intervention