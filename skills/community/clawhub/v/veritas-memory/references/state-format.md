# STATE.md Format Specification

## Purpose

STATE.md is the agent's memory index — not a database table, not a task list. It serves three functions:

1. **Event Timeline** — chronicle of who did what when (5-10 most recent events = instant context)
2. **Current State** — derived snapshot of system/user/project status
3. **Do-Not-Repeat** — explicit blacklist of verified-but-should-not-redo actions

## Format

```markdown
# {Agent} 的状态

> 最后更新: {timestamp} CST
> ⚠️ 本文件是日志的缓存。如有疑问，回溯日志。

---

## 事件时间线

### {YYYY-MM-DD}

| 时间 | 谁 | 做了什么 | 来源 |
|------|-----|---------|------|
| HH:MM | {agent/user/system} | {one-line action/decision} | [seq N] or [source] |

---

## 当前综合状态（从时间线推导）

- {status_key}: {value} [{timestamp} {source}]

---

## 禁止重做

| 事项 | 原因 | 来源 |
|------|------|------|
| ❌ {action} | {why} | [{timestamp}] |

---

## 未完成的长期事项

- {long-term todo}
```

## Field Specification

| Field | Required | Example |
|-------|----------|---------|
| 时间 | Yes | `07:35` or `2026-05-21 22:30` |
| 谁 | Yes | `user` / `agent-name` / `系统组件` |
| 做了什么 | Yes | `审计报告：ML过滤已修，V10未接入` |
| 来源 | Yes | `[seq 158]` / `[M-sessions_send]` / `[brain_rules DB]` |

## Source Reference Types

| Format | Meaning |
|--------|---------|
| `[seq N]` | Current session message sequence number |
| `[agent:id:channel: seq N]` | Cross-session full reference |
| `[X-sessions_send]` | Cross-agent communication |
| `[database/table]` | Database record |
| `[production.log]` | System log |

## Maintenance Rules

1. Each user decision/instruction → append event immediately (WAL)
2. Each task completion → append event immediately
3. Cross-agent message → append event immediately
4. Keep timeline at 40-60 events; Memory Tender merges older ones
5. Events >3 days old → merge to daily summary lines
