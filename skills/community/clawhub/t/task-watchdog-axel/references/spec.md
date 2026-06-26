# Task Watchdog 详细规格

本文档是 SKILL.md 的详细参考，补充脚本参数、权限检查流程、GRACE 参数、状态流转、Cron 配置和测试场景。

## 1. Lock JSON Schema

```json
{
  "task_id": "string (required) - 唯一标识，格式: task-{name}-{seq}",
  "agent_id": "string (required) - lock 创建者",
  "session_id": "string (required) - 创建者的当前 session",
  "status": "string - in_progress | done | timeout | abandoned",
  "created_at": "ISO8601 (required)",
  "last_heartbeat": "ISO8601 (lock-self-check 更新，隔5分钟)",
  "last_progress": "ISO8601 (lock-update --progress 时更新，标记真实进展)",
  "description": "string (required) - 任务描述",
  "progress": "string (optional) - 当前进度描述",
  "parent_task_id": "string (optional) - 父任务",
  "done_at": "ISO8601 (optional) - 标记完成时间"
}
```

**判断 abandoned 用 `last_progress`，不看 `last_heartbeat`**：
- `last_heartbeat` 超时 → 可能是网络抖动，不归档
- `last_progress` 超 GRACE×3 → 真正 abandoned

## 2. 脚本参数

### lock-self-check.sh

**功能**：Agent 自检，在 HEARTBEAT 触发时调用

```
--agent-id     必填（或设置 AGENT_NAME 环境变量）
--session-id  选填（默认从 AGENT_SESSION_ID 读取）
```

**行为**：
1. 找到 `active/` 下该 agent 的所有 lock
2. owner session 存活 → 更新 last_heartbeat
3. owner session 已死 → 接管（更新 session_id + heartbeat）

### lock-create.sh
```
--task-id          必填
--agent-id        必填
--session-id      必填
--description     必填
--parent-task-id  选填
```

### lock-update.sh
```
--task-id     必填
--progress    选填
--heartbeat   选填（默认 now）
```

### lock-done.sh
```
--task-id     必填
--agent-id   选填
```

### lock-status.sh
```
--task-id     必填
--agent-id   选填
--json        选填
```

### lock-archive.sh
```
--list              列出活跃任务
--status            各 agent 统计
--archive-days N    归档 N 天前完成的任务
--cleanup-days N    清理 N 天前归档
```

## 3. 写权限检查流程

```
收到写请求 (lock-update / lock-done)
  │
  ├── 读取 lock 中的 session_id
  │
  ├── effective_session = 传参 > AGENT_SESSION_ID > 空
  │
  ├── effective_session == lock.session_id
  │     → ✅ 允许（owner）
  │
  ├── effective_session == dispatcher | main
  │     → ✅ 允许（可接管）
  │
  └── 否则
        ├── 检查 owner session 是否仍活跃
        │     活跃 → ❌ 拒绝
        │     不活跃 → ✅ 允许接管
```

**说明**：Owner session 消失后，任何人都可接管该 lock。

## 4. Session 存活检查

```bash
openclaw sessions list --agent {agent_id} --format json | grep "{session_id}"
```

找不到 → session 已死。

## 5. GRACE 参数

| 参数 | 值 | 说明 |
|------|-----|------|
| GRACE_MINUTES | 8 | 心跳容忍范围（分钟），last_progress 无关 |
| GRACE×3 | 24 | abandoned 判定阈值（last_progress 超限 + session 死） |

心跳更新建议频率：**每 5 分钟一次**（留 3 分钟余量）。

## 6. 状态流转

```
active/{task_id}.lock (in_progress)
    │
    ├── agent 调用 lock-done
    │     → done_at = now
    │     → 移动到 archive/今天/
    │
    ├── scan 发现 session 死 + last_progress 超 GRACE×3
    │     → 移动到 archive/今天/
    │     → status = abandoned
    │
    └── agent 重启后发现自己的 abandoned lock
          → 决定继续或放弃
```

## 7. Cron 配置

```bash
# 每 10 分钟扫描异常并归档
*/10 * * * * $HOME/.openclaw/workspace/skills/task-watchdog/scripts/scan-locks.sh

# 每天归档 7 天前完成的任务
0 0 * * * $HOME/.openclaw/workspace/skills/task-watchdog/scripts/lock-archive.sh --archive-days 7

# 每天清理 30 天前的归档
0 0 * * * $HOME/.openclaw/workspace/skills/task-watchdog/scripts/lock-archive.sh --cleanup-days 30

# 每周一生成状态报告
0 9 * * 1 $HOME/.openclaw/workspace/skills/task-watchdog/scripts/lock-report.sh
```

## 8. 测试场景

| 场景 | 预期行为 |
|------|---------|
| 正常创建→心跳→完成 | active/ → archive/今天/，流程干净 |
| session 消失 + hb 超 GRACE×3 | 归档为 abandoned |
| 另一 agent 想改你的 lock | 报错拒绝（owner session 仍活跃） |
| lock 已 done 再调用 | 提示已是 done，不报错 |
| 查已归档任务 | lock-status 能从 archive/ 找到 |
| owner session 死后的接管 | 新 session 可写，接管逻辑正确 |
| 接管 abandoned 任务 | 新 session 可写，原 session 已死则允许 |
