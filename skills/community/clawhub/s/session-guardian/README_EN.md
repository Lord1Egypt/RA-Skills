# Session Guardian 🛡️

**Never Lose Your Conversations, Never Mix Up Your Tasks** - Enterprise-grade Session Backup + Project Management

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/cyber-axin/session-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-0.9.0+-orange.svg)](https://openclaw.ai)

[中文文档](README_CN.md) | English

---

## Use Cases

Are you facing these problems? Session Guardian solves them:

- 🔴 **Model crashes frequently**, conversations lost, work wasted
- 🔴 **Gateway restarts**, forgot what you were doing, task state lost
- 🔴 **Cross-channel confusion**, sent private info to group chat or vice versa
- 🔴 **Complex tasks hard to track**, tasks span multiple sessions, state forgotten
- 🔴 **Multi-agent chaos**, multiple agents working, don't know who's doing what
- 🔴 **Session files too large**, causing timeouts, slow responses, high token costs

---

## Quick Start

```bash
# 1. Install
clawhub install session-guardian

# 2. One-click deployment (auto-configure all cron jobs)
cd ~/.openclaw/workspace/skills/session-guardian
bash scripts/install.sh

# 3. Verify installation
crontab -l | grep session-guardian
openclaw cron list
```

**That's it!** Your conversations and task states are now protected.

---

## Core Features

### 1. Never Lose Conversations 📦

```bash
# Incremental backup (every 5 minutes) - max 5 minutes data loss
# Snapshot (every hour) - restore to any point in time
# Smart summary (daily) - AI extracts key content

# Restore data
bash scripts/restore.sh --source incremental
bash scripts/restore.sh --source hourly --timestamp 2026-03-03-14
```

**Zero token cost, runs independently, doesn't affect main conversations**

---

### 2. Persistent Task State 📋

```bash
# Create task plan
bash scripts/plan-manager.sh create "Develop new feature"

# Update progress
bash scripts/plan-manager.sh update "Develop new feature" "1.1"

# List all tasks
bash scripts/plan-manager.sh list

# Archive completed tasks
bash scripts/plan-manager.sh archive "Develop new feature"
```

**Auto-creates plan files, updates progress in real-time, trackable across sessions**

---

### 3. Prevent Cross-Channel Leaks 🔒

```bash
# Check session isolation status
bash scripts/session-isolation-check.sh check

# Generate detailed report
bash scripts/session-isolation-check.sh report
```

**Enforces channel and user checks, prevents private info leaking to group chats**

---

### 4. Auto-Recover from Gateway Restart 🔄

```bash
# Health check (runs every 6 hours automatically)
bash scripts/health-check.sh
```

**Auto-detects restarts, recovers all unfinished tasks, proactively reports**

---

### 5. Auto-Maintain Health 🏥

**Auto-cleans >1MB session files, fixes missing configs, monitors disk space**

---

## Five-Layer Protection

| Layer | Frequency | Function | Token Cost |
|-------|-----------|----------|------------|
| Incremental Backup | Every 5 min | Max 5 min data loss | 0 |
| Snapshot | Every hour | Restore to any time | 0 |
| Smart Summary | Daily | AI extracts key content | Minimal |
| Health Check | Every 6 hours | Clean, fix, monitor | 0 |
| Project Management | Real-time | Task tracking, session isolation | 0 |

---

## Real-World Example

### Multi-Agent Collaboration Project

```bash
# 1. Create project plan
bash scripts/plan-manager.sh create "Smart Inspection Product v1.0"

# 2. Assign tasks to different agents
# - Security AI Product Corps: Process design
# - Dev Corps UI Designer: Interface design
# - Dev Corps Full-stack: Code implementation

# 3. Update progress after each agent completes tasks
bash scripts/plan-manager.sh update "Smart Inspection Product v1.0" "1.1"

# 4. Regularly check session isolation
bash scripts/session-isolation-check.sh check

# 5. Archive after project completion
bash scripts/plan-manager.sh archive "Smart Inspection Product v1.0"
```

---

## Core Advantages

- ✅ **Zero Token Cost** - Backup and snapshots don't call LLM
- ✅ **No Impact on Main Conversations** - Uses system crontab, runs independently
- ✅ **Auto-Cleanup** - Intelligently manages disk space
- ✅ **One-Click Restore** - Quickly rollback to any point in time
- ✅ **Complete Documentation** - Examples, real cases, troubleshooting

---

## Use Cases

| Scenario | Pain Point | Solution |
|----------|------------|----------|
| Multi-agent collaboration | Hard to track task state | Plan file mechanism |
| Multi-channel operations | Cross-channel confusion | Session isolation check |
| Long-term projects | Data loss risk | Five-layer protection |
| Unstable models | Frequent crashes | Incremental backup + snapshot |
| Gateway restarts | Task state lost | Auto-recovery mechanism |

---

## Documentation

- [Complete Documentation](SKILL.md) - Detailed features and configuration
- [Usage Examples](EXAMPLES.md) - Real cases and FAQs
- [Release Notes](RELEASE-v1.0.md) - Complete feature details

---

## Changelog

### v1.0.1 (2026-03-03)
- 📝 Optimized documentation structure
- 📝 Highlighted use cases and pain points
- 📝 Updated contact information

### v1.0.0 (2026-03-03)
- ✨ Five-layer protection system
- ✨ Plan file mechanism
- ✨ Session isolation check
- ✨ GatewayRestart forced recovery
- 🔧 Health check and auto-repair
- 📝 Complete documentation

[View Complete Changelog](RELEASE-v1.0.md)

---

## Author

**Cyber Axin (赛博阿昕)** 🦞
- Founder of Lobster Studio
- King (Lobster King) - Master AI Agent, orchestrating five intelligent agent corps

Built from real-world experience with Lobster Studio's multi-agent collaboration.

---

## 📞 Contact

- **Email**: zhuangxin@szbit.cn
- **WeChat**: sixsixsix_666-
- **GitHub**: https://github.com/cyber-axin/session-guardian

---

## License

MIT License - See [LICENSE](LICENSE) file for details

---

**Session Guardian v1.0** - Never lose your AI conversations, never mix up task states 🛡️
