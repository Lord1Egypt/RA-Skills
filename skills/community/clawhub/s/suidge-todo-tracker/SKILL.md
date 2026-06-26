---
name: Todo Tracker
slug: suidge-todo-tracker
version: 1.3.0
description: Manage follow-up items and remind users during heartbeat checks.
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# Todo Tracker

## When to Use

用户提到提醒、跟进、待办事项。心跳周期自动检查 pending 事项。

## Core Rules

1. **单一数据源** — 所有事项存储在 `memory/todo.json`
2. **心跳检查** — 每 30 分钟检查 `status=pending` 且 `follow_up_time` 已到 → 提醒用户（持续提醒直到完成）
3. **完成/取消必须设时间戳** — `completed` 设 `completed_at`，`cancelled` 设 `cancelled_at`（ISO 8601）
4. **24 小时自动清理** — 已完成/取消超过 24 小时的事项由 `scripts/todo-cleaner.py` 删除
5. **信息不全要追问** — 用户说"明天提醒我"但没说时间 → 追问"几点？"

## Quick Reference

```bash
# 添加事项 → 写入 memory/todo.json，status=pending
# 完成事项 → status=completed + completed_at
# 取消事项 → status=cancelled + cancelled_at
# 清理 → python3 scripts/todo-cleaner.py
```

## Data Storage

`memory/todo.json` — 所有事项。Schema 见 `data-structure.md`。

## Guides

| Topic | File |
|-------|------|
| 安装配置 | `setup.md` |
| 数据结构 | `data-structure.md` |
| 使用示例 | `examples.md` |
| 清理脚本 | `scripts/todo-cleaner.py` |
