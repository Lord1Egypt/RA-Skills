---
name: session-guardian
description: |
  Never lose a conversation again. Auto-backup, smart recovery, and health monitoring for OpenClaw sessions. Protects against gateway crashes, model disconnections, and token overflow.

  Use this skill when:
  - User worries about losing conversations after gateway restart or model crash
  - User mentions session backup, conversation recovery, session protection, or data loss
  - User's agent is slow or timing out (likely token overflow from large sessions)
  - User runs multiple agents and needs to track collaboration across sessions
  - User asks about session health, backup strategy, or disaster recovery
  - User mentions "对话丢失", "会话备份", "上下文溢出", "token超限", "Gateway重启后记忆丢失"
  - Even if user just says "my agent lost everything after a restart" — this is the skill
---

# Session Guardian 🛡️

Never lose a conversation again.

```
  Without Guardian                    With Guardian
┌──────────────────┐            ┌──────────────────────────┐
│ Gateway crashes  │            │  Auto-backup every 5 min │
│ → conversation   │            │  Hourly snapshots        │
│   gone forever   │            │  Health monitoring       │
│                  │            │  One-command recovery    │
│ Token overflow   │            │                          │
│ → agent frozen   │            │  Gateway crash?          │
│                  │            │  → Restore in seconds    │
│ No way back. 😱  │            │                          │
└──────────────────┘            │  Token overflow?         │
                                │  → Auto-detected + alert │
                                │                          │
                                │  Always protected. 🛡️    │
                                └──────────────────────────┘
```

## The Problem

Your OpenClaw conversations live in session files. When things go wrong — and they will — you lose everything:

- 🔴 **Gateway restart** → entire conversation history gone
- 🔴 **Model disconnection** → mid-task context wiped out
- 🔴 **Token overflow** → session too large, agent slows down or crashes
- 🔴 **Disk issues** → session files corrupted or lost

No built-in backup. No recovery. No warning before it's too late.

## The Fix

```bash
clawhub install session-guardian
bash ~/.openclaw/workspace/skills/session-guardian/scripts/install.sh
```

That's it. Five layers of protection, running automatically.

## How It Works

```
Layer 1: Incremental Backup    → Every 5 min   → New conversations saved
Layer 2: Hourly Snapshot       → Every hour     → Full session snapshots
Layer 3: Health Check          → Every 6 hours  → Detect problems early
Layer 4: Smart Summary         → Daily          → Key info extracted
Layer 5: Knowledge Extraction  → Daily          → Best practices saved
```

All automatic. All in the background. Zero manual work.

## Quick Start

```bash
# Install
clawhub install session-guardian

# Deploy (sets up all cron jobs automatically)
cd ~/.openclaw/workspace/skills/session-guardian
bash scripts/install.sh

# Check status
bash scripts/status.sh
```

## What You Get

- ✅ **Auto-backup** every 5 minutes — never lose more than 5 min of conversation
- ✅ **Hourly snapshots** — full point-in-time recovery
- ✅ **Health monitoring** — warns before token overflow crashes your agent
- ✅ **One-command recovery** — restore any session from any backup
- ✅ **Multi-agent support** — protects all your agents, not just main
- ✅ **Collaboration tracking** — see task flow across agents (King → Lead → Members)
- ✅ **Knowledge extraction** — auto-saves best practices from conversations
- ✅ **Minimal overhead** — ~10-15k tokens/day, ~1-2MB/agent/month

## Usage

### Check Status

```bash
bash ~/.openclaw/workspace/skills/session-guardian/scripts/status.sh
```

Shows: backup count, last backup time, snapshot count, cron jobs, disk usage.

### Run Health Check

```bash
bash ~/.openclaw/workspace/skills/session-guardian/scripts/health-check.sh
```

Detects: oversized sessions, missing configs, disk space issues, gateway problems.

### Restore a Session

```bash
# List available backups
bash ~/.openclaw/workspace/skills/session-guardian/scripts/restore.sh list

# Restore specific agent
bash ~/.openclaw/workspace/skills/session-guardian/scripts/restore.sh restore --agent main
```

### View Collaboration Health (Multi-Agent)

```bash
bash ~/.openclaw/workspace/skills/session-guardian/scripts/collaboration-health.sh report
```

### Track Task Flow

```bash
bash ~/.openclaw/workspace/skills/session-guardian/scripts/collaboration-tracker.sh trace "task name"
```

## Cron Jobs (Auto-Configured)

After `install.sh`, these run automatically:

| Schedule | Task | What it does |
|----------|------|-------------|
| Every 5 min | Incremental backup | Save new conversations |
| Every hour | Snapshot | Full session archive |
| Every 6 hours | Health check | Detect problems |
| Daily 2am | Smart summary | Extract key info |

## File Structure

```
Assets/SessionBackups/
├── incremental/     # Every-5-min backups
├── hourly/          # Hourly snapshots
├── collaboration/   # Task flow records
└── Knowledge/       # Extracted best practices
```

All backups stay local. Nothing leaves your machine.

## Who Is This For

### Solo Agent User
✅ Protect your main conversation from crashes
✅ Get warned before token overflow kills your agent
✅ Recover in seconds, not hours of re-explaining

### Multi-Agent Team
✅ Protect all agents (King + team leads + members)
✅ Track collaboration: who assigned what, who finished what
✅ Health scoring: monitor team communication quality
✅ Knowledge extraction: auto-save best practices from every agent

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Backups not running | Check `crontab -l \| grep session-guardian` |
| Agent slow/timing out | Run health-check — likely token overflow |
| Can't restore | Run `restore.sh list` to see available backups |
| Disk filling up | Check config retention settings (default: 7 days incremental, 30 days snapshots) |

## Configuration

Edit `scripts/config.sh` to customize:

```bash
BACKUP_DIR         # Where backups go (default: Assets/SessionBackups)
INCREMENTAL_KEEP   # Days to keep incremental backups (default: 7)
SNAPSHOT_KEEP      # Days to keep snapshots (default: 30)
MAX_SESSION_SIZE   # Alert threshold for session size (default: 5MB)
```

## Security

- All data stays local — no external services, no network requests
- No API keys required
- Backups are excluded from git (add to .gitignore)
- Does not modify your session files — only reads and copies

## Performance

| Operation | Tokens | Storage |
|-----------|--------|---------|
| Incremental backup | ~100/run | ~10KB/session/day |
| Hourly snapshot | ~500/run | ~100KB/session/day |
| Health check | ~200/run | ~2KB/report |
| Daily summary | ~5k/run | ~5KB/day |
| **Total** | **~10-15k/day** | **~1-2MB/agent/month** |

## Feedback

- Star: `clawhub star session-guardian`
- Update: `clawhub update session-guardian`

---

# 🇨🇳 中文说明

## Session Guardian 🛡️ — 再也不丢对话

你的 OpenClaw 对话存在 session 文件里。Gateway 一重启、模型一断连、token 一溢出——对话就没了。没有备份，没有恢复，没有预警。

## 痛点

- 🔴 **Gateway 重启** → 整个对话历史消失
- 🔴 **模型断连** → 做到一半的任务上下文全丢
- 🔴 **Token 溢出** → session 太大，Agent 变慢甚至崩溃
- 🔴 **磁盘问题** → session 文件损坏或丢失

## 解决方案

```bash
clawhub install session-guardian
bash ~/.openclaw/workspace/skills/session-guardian/scripts/install.sh
```

五层自动防护，后台运行，零手动操作。

## 五层防护

| 层级 | 频率 | 作用 |
|------|------|------|
| 增量备份 | 每 5 分钟 | 保存新对话，最多丢 5 分钟 |
| 快照备份 | 每小时 | 完整 session 存档，支持回滚 |
| 健康检查 | 每 6 小时 | 提前发现问题（token 溢出、磁盘不足） |
| 智能总结 | 每天 | 提取关键信息到 MEMORY.md |
| 知识沉淀 | 每天 | 自动保存最佳实践 |

## 你会得到

- ✅ **自动备份** — 每 5 分钟一次，最多丢 5 分钟对话
- ✅ **一键恢复** — 从任意备份点恢复 session
- ✅ **健康监控** — 在 token 溢出前预警
- ✅ **多 Agent 支持** — 保护所有 Agent，不只是 main
- ✅ **协作追踪** — 可视化任务流转（King → 团长 → 成员）
- ✅ **知识沉淀** — 自动从对话中提取最佳实践
- ✅ **极低开销** — 每天约 10-15k tokens，每月约 1-2MB/Agent

## 常用命令

```bash
# 查看状态
bash scripts/status.sh

# 健康检查
bash scripts/health-check.sh

# 恢复 session
bash scripts/restore.sh list
bash scripts/restore.sh restore --agent main

# 协作健康度（多 Agent）
bash scripts/collaboration-health.sh report
```

## 适用场景

**个人用户**：保护主对话不丢失，token 溢出前预警，秒级恢复

**多 Agent 团队**：保护所有 Agent，追踪协作链路，自动沉淀知识

## 安全性

- 所有数据本地存储，不联网，不需要 API Key
- 不修改 session 文件，只读取和复制
- 备份文件已排除 git 追踪
