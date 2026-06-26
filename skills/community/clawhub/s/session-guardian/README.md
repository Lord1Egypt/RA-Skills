# Session Guardian 🛡️

**Your Conversation Guardian** - Enterprise-grade session backup + project management solution for OpenClaw

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/1052326311/session-guardian)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-0.9.0+-orange.svg)](https://openclaw.ai)

## Features

- 🔄 **Five-Layer Protection**: Incremental backup (5min) + Snapshot (1hr) + Smart summary (daily) + Health check (6hr) + Project management
- 🤝 **Multi-Agent Collaboration**: Track collaboration chains, monitor health scores
- 🧠 **Knowledge Extraction**: Auto-extract best practices from conversations
- 📊 **Smart Backup Strategy**: Adaptive backup frequency based on agent activity
- 🔗 **Self-Improving-Agent Integration**: Complementary design, save 65% tokens
- 🛡️ **Session Isolation**: Prevent cross-agent information leakage

## Quick Start

```bash
# Install via ClawHub
clawhub install session-guardian

# One-click deployment
cd ~/.openclaw/workspace/skills/session-guardian
bash scripts/install.sh

# Verify
crontab -l | grep session-guardian
```

## Use Cases

### 1. Enterprise Multi-Agent Collaboration
Multiple agents working together (Main → Team Lead → Members)

### 2. Personal Assistant Team
Multiple specialized assistants (Research, Coding, Writing, Translation)

### 3. Single-Agent Deep Usage
One main agent handling all tasks with long-term memory

### 4. Enterprise Multi-Department
Different departments with separate agents (Sales, Support, Tech, Finance)

## Core Features

### Five-Layer Protection System

1. **Incremental Backup** (Every 5 minutes)
   - Auto-backup new conversations
   - Minimal storage, fast recovery

2. **Snapshot Backup** (Every 1 hour)
   - Complete session snapshots
   - Version control, rollback support

3. **Smart Summary** (Daily)
   - Extract key information
   - Auto-update MEMORY.md

4. **Health Check** (Every 6 hours)
   - Monitor session file size
   - Detect abnormal token consumption

5. **Project Management**
   - Task state tracking
   - Milestone management

### Multi-Agent Collaboration (v2.0)

- **Collaboration Tracking**: Visualize task flow
- **Smart Backup Strategy**: Adaptive backup frequency
- **Knowledge Extraction**: Auto-update AGENTS.md
- **Health Scoring**: Monitor collaboration quality

### Integration with Self-Improving-Agent

**Complementary Design**:
- Session Guardian: Macro perspective (overall progress)
- Self-Improving-Agent: Micro perspective (specific issues)

**Token Savings**:
- Before: ~30k tokens/day
- After: ~10.5k tokens/day
- **Save 65% tokens**

## Installation

### Method 1: ClawHub (Recommended)

```bash
clawhub install session-guardian
```

### Method 2: Manual

```bash
git clone https://github.com/1052326311/session-guardian.git ~/.openclaw/workspace/skills/session-guardian
cd ~/.openclaw/workspace/skills/session-guardian
bash scripts/install.sh
```

## Configuration

Edit `config.json`:

```json
{
  "backup": {
    "incremental": {
      "enabled": true,
      "interval": 5,
      "retention": 7
    },
    "snapshot": {
      "enabled": true,
      "interval": 60,
      "retention": 30
    }
  },
  "summary": {
    "enabled": true,
    "schedule": "0 0 * * *"
  },
  "healthCheck": {
    "enabled": true,
    "interval": 6
  },
  "collaboration": {
    "tracking": true,
    "healthScore": true
  },
  "integration": {
    "selfImprovingAgent": {
      "enabled": true,
      "readLearnings": true
    }
  }
}
```

## Usage

### Manual Backup

```bash
# Backup all sessions
openclaw skill run session-guardian backup

# Backup specific agent
openclaw skill run session-guardian backup --agent main
```

### Manual Summary

```bash
# Generate daily summary
openclaw skill run session-guardian summary

# Generate weekly summary
openclaw skill run session-guardian summary --weekly
```

### Health Check

```bash
# Run health check
openclaw skill run session-guardian health-check

# View report
cat ~/.openclaw/workspace/Assets/SessionBackups/health-reports/latest.md
```

### Restore Session

```bash
# List backups
openclaw skill run session-guardian list-backups

# Restore
openclaw skill run session-guardian restore --backup 2026-03-06-10-00
```

## Performance

### Token Consumption
- Incremental backup: ~100 tokens/run
- Snapshot backup: ~500 tokens/run
- Daily summary: ~8k tokens/run (with SI integration)
- Health check: ~200 tokens/run
- **Total**: ~10-15k tokens/day

### Storage
- ~1-2MB/agent/month

## Cron Jobs

Automatically configured after installation:

```bash
*/5 * * * *   # Incremental backup (every 5 min)
0 * * * *     # Snapshot backup (every hour)
0 0 * * *     # Daily summary (midnight)
0 */6 * * *   # Health check (every 6 hours)
*/30 * * * *  # Collaboration tracking (every 30 min)
```

## Best Practices

1. **Regular Monitoring**: Check health reports weekly
2. **Backup Management**: Keep 7 days incremental, 30 days snapshots
3. **Knowledge Extraction**: Review daily summaries, update MEMORY.md
4. **Integration**: Use with self-improving-agent for error learning

## Troubleshooting

### Backup Not Running
```bash
crontab -l | grep session-guardian
tail -f ~/.openclaw/workspace/skills/session-guardian/logs/backup.log
```

### Large Session Files
```bash
openclaw skill run session-guardian health-check
cat ~/.openclaw/workspace/Assets/SessionBackups/health-reports/latest.md
```

## Roadmap

### v2.1 (Planned)
- [ ] Web dashboard
- [ ] Real-time monitoring
- [ ] Advanced analytics
- [ ] Custom alerts

### v2.2 (Planned)
- [ ] Cloud backup
- [ ] Team features
- [ ] API integration
- [ ] Mobile app

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- **GitHub**: https://github.com/1052326311/session-guardian
- **Issues**: https://github.com/1052326311/session-guardian/issues
- **ClawHub**: https://clawhub.com/session-guardian

## Changelog

### v2.0.0 (2026-03-05)
- ✨ Added collaboration tracking
- ✨ Added smart backup strategy
- ✨ Added knowledge extraction
- ✨ Added collaboration health scoring
- ✨ Integration with self-improving-agent
- 🐛 Fixed session isolation issues

### v1.0.0 (2026-03-01)
- 🎉 Initial release

---

# 中文版 / Chinese Version

## 功能特性

- 🔄 **五层防护**：增量备份（5分钟）+ 快照（1小时）+ 智能总结（每日）+ 健康检查（6小时）+ 项目管理
- 🤝 **多智能体协作**：追踪协作链路，监控健康度评分
- 🧠 **知识提取**：自动从对话中提取最佳实践
- 📊 **智能备份策略**：根据agent活跃度自适应备份频率
- 🔗 **Self-Improving-Agent集成**：互补设计，节省65% tokens
- 🛡️ **Session隔离**：防止跨agent信息泄露

## 快速开始

```bash
# 通过ClawHub安装
clawhub install session-guardian

# 一键部署
cd ~/.openclaw/workspace/skills/session-guardian
bash scripts/install.sh

# 验证
crontab -l | grep session-guardian
```

## 使用场景

### 1. 企业多智能体协作
多个agent分工协作（主控 → 团长 → 成员）

### 2. 个人助手团队
多个专业助手（研究、编程、写作、翻译）

### 3. 单agent深度使用
一个主agent处理所有任务，长期记忆

### 4. 企业多部门
不同部门各有agent（销售、客服、技术、财务）

## 性能

### Token消耗
- 增量备份：~100 tokens/次
- 快照备份：~500 tokens/次
- 每日总结：~8k tokens/次（集成SI后）
- 健康检查：~200 tokens/次
- **总计**：~10-15k tokens/天

### 存储
- ~1-2MB/agent/月

## 支持

- **GitHub**: https://github.com/1052326311/session-guardian
- **Issues**: https://github.com/1052326311/session-guardian/issues
- **ClawHub**: https://clawhub.com/session-guardian
