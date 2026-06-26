---
name: task-watchdog
version: 1.0.0
description: 任务锁与超时监控系统。外部文件承载任务状态，不污染 agent 上下文，纯靠 heartbeat + GRACE 判断，不发即时告警。
---

# Task Watchdog

## 核心概念

Lock 文件是任务的外部状态载体，放于 `~/.openclaw/agents/{agent_id}/locks/`：
- `active/` — 正在执行的任务
- `archive/YYYY-MM-DD/` — 归档（done / abandoned / timeout）

**两个时间字段，职责不同：**
```
last_heartbeat  — lock-self-check 更新（纯心跳维持，不说明任务有进展）
last_progress   — lock-update --progress 时更新（标记真实进展）
```

**状态判断（用 last_progress，不看 last_heartbeat）：**
```
✅ 正常      session 存在，last_progress 正常
⚠️ SESSION_DEAD  session 已消失
⚠️ STALLED      session 存在，但 last_progress 超 GRACE×3
⚠️ HEARTBEAT_DELAY  心跳延迟
🚫 abandoned  session 消失 + last_progress 超 GRACE×3
📦 done       任务完成，立即归档
```

## 脚本

| 脚本 | 用途 |
|------|------|
| `lock-create.sh` | 创建 lock → active/ |
| `lock-update.sh` | 更新 heartbeat；`--progress` 时同时更新 last_progress |
| `lock-done.sh` | 标记完成 → 归档 |
| `lock-status.sh` | 查询状态 |
| `scan-locks.sh` | 扫描 active/，异常归档 |
| `lock-archive.sh` | 归档N天前 / 清理N天前 / 统计 |
| `lock-report.sh` | 查看所有活跃任务状态 |
| `lock-self-check.sh` | Agent 自检：更新心跳 + 处理 abandoned |

## 推荐用法

**关键节点调用：**
```
任务开始 → lock-create
每个关键步骤完成 → lock-update --progress "X完成，开始Y"
任务全部完成 → lock-done
```

**HEARTBEAT 触发时调用自检：**
```
收到心跳轮询时
  → 调用 lock-self-check.sh
  → 自动完成：
      无活跃任务 → 无输出，agent 回复 HEARTBEAT_OK
      owner session 存活 → 只更新 last_heartbeat
      owner session 已死 → 接管任务（更新 session_id + last_heartbeat）
  → 无需判断逻辑，脚本自动处理
```

## 设计目标

**任务续做保障系统**，不是即时告警系统：
- 中断后 lock 留在 active/，Supervisor 扫描归档
- 自检机制让 agent 自动继续被中断的任务
- 定期报告让负责人知道哪些任务需要接管或放弃

## 常用命令

```bash
./lock-self-check.sh --agent-id xxx --session-id xxx   # HEARTBEAT 触发时调用
./lock-report.sh                                        # 查看所有活跃任务状态
./lock-archive.sh --list                              # 同上
./lock-archive.sh --archive-days 7                   # 归档7天前完成的任务
./lock-archive.sh --cleanup-days 30                   # 清理30天前的归档
```
