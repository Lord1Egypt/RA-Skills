---
name: system-maintenance
description: Complete maintenance system for OpenClaw with unified architecture, filesystem governance, and cross-platform design
version: 1.3.2
metadata:
  openclaw:
    homepage: https://github.com/jazzqi/openclaw-system-maintenance
---

## 📖 Layer 1: Immediate Value (30-Second Overview)

### What You Get
The **System Maintenance Skill** provides a complete, unified maintenance solution for OpenClaw systems. It includes real-time monitoring, automated cleanup, log management, and health reporting - all in a modular, easy-to-maintain architecture.

**Key Benefits:**
- ✅ Automated monitoring every 5 minutes
- ✅ Auto-recovery of failed services
- ✅ 50% reduction in cron tasks
- ✅ Full backup and one-click rollback
- ✅ Weekly optimization reports

**Core Value:** Replaces fragmented maintenance scripts with a professional, unified system maintenance solution.

## 🚀 Layer 2: Quick Start (5-Minute Setup)

### Installation

#### Method 1: ClawHub Install (Recommended)
```bash
bunx clawhub@latest install system-maintenance
```

#### Method 2: GitHub Clone
```bash
git clone https://github.com/jazzqi/openclaw-system-maintenance.git \
  ~/.openclaw/skills/system-maintenance
cd ~/.openclaw/skills/system-maintenance
chmod +x scripts/*.sh
```

#### One-Click Setup
```bash
bash scripts/install-maintenance-system.sh
```

#### Verification
```bash
# Check cron tasks
crontab -l | grep -i openclaw

# Test monitoring
bash scripts/real-time-monitor.sh --test

# Quick health check
bash scripts/daily-maintenance.sh --quick-check
```

## 🏗️ Layer 3: Architecture & Components

### Maintenance Schedule

| Frequency | Task | Description | Script |
|-----------|------|-------------|--------|
| Every 5 min | Real-time Monitoring | Gateway monitoring & auto-recovery | `real-time-monitor.sh` |
| Daily 2:00 AM | Log Management | Log cleanup, rotation, compression | `log-management.sh` |
| Daily 3:30 AM | Daily Maintenance | Comprehensive cleanup & health checks | `daily-maintenance.sh` |
| Sunday 3:00 AM | Weekly Optimization | Deep system analysis & reporting | `weekly-optimization.sh` |

### Core Functions

#### 🏗️ Unified Architecture
- Modulardesign with 5 core scripts
- Configuration-driven management
- Safe migration from old systems
- Professional directory layout

#### ⏱️ Smart Monitoring & Recovery
- Real-time gateway monitoring
- Automatic service recovery
- Health scoring system (0-100)
- Resource tracking (CPU, memory, disk)
- macOS compatibility

#### 📊 Professional Reporting
- Weekly optimization reports (Markdown)
- Execution summaries
- Optimization suggestions
- Performance metrics tracking

#### 🛡️ Safety & Reliability
- Complete backup system
- One-click rollback
- Error recovery with graceful handling
- Security checks for sensitive info
- Proper permission management

#### 🔄 Maintenance Automation
- Log rotation & cleanup
- Temporary file cleanup
- Daily health checks
- Automatic .learnings/ updates

## 📚 Layer 4: Resources & Reference

### File Structure

```
system-maintenance/
├── 📄 entry.js                 # Skill entry point
├── 📄 package.json             # NPM configuration
├── 📄 SKILL.md                 # This file
├── 🛠️  scripts/                # Core scripts
│   ├── weekly-optimization.sh      # Weekly deep optimization
│   ├── real-time-monitor.sh        # Real-time monitoring (5 min)
│   ├── log-management.sh           # Log cleanup & rotation
│   ├── daily-maintenance.sh        # Daily maintenance (3:30 AM)
│   ├── install-maintenance-system.sh # Installation tool
│   └── check-before-commit.sh      # Pre-commit quality check
├── 📚  examples/               # Examples & templates
│   ├── setup-guide.md              # Quick setup guide
│   ├── migration-guide.md          # Safe migration guide
│   ├── final-status-template.md    # Status report template
│   └── optimization-suggestions.md # Optimization suggestions
├── 📝  docs/                   # Additional documentation
│   ├── FILE_SYSTEM_GOVERNANCE.md   # FS Governance Standard
│   └── cross-platform-architecture.md
└── 📁 assets/                  # Static resources
    └── README.md
```

### Command Reference

#### Real-time Monitor
```bash
# Test mode (no actual operations)
bash scripts/real-time-monitor.sh --test

# Force execution
bash scripts/real-time-monitor.sh --force

# View status
bash scripts/real-time-monitor.sh --status
```

#### Log Management
```bash
# Dry run (preview changes)
bash scripts/log-management.sh --dry-run

# Manual rotation
bash scripts/log-management.sh --rotate

# Cleanup only
bash scripts/log-management.sh --cleanup
```

#### Daily Maintenance
```bash
# Quick health check only
bash scripts/daily-maintenance.sh --quick-check

# Full maintenance cycle
bash scripts/daily-maintenance.sh --full

# Skip backup (emergency mode)
bash scripts/daily-maintenance.sh --no-backup
```

#### Weekly Optimization
```bash
# Generate report only (no optimization)
bash scripts/weekly-optimization.sh --report-only

# Analysis only (no changes)
bash scripts/weekly-optimization.sh --analyze-only

# Full optimization cycle
bash scripts/weekly-optimization.sh --optimize
```

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.3.2 | 2026-03-16 | Reorganized SKILL.md with progressive disclosure; cleaned up backup files |
| 1.3.1 | 2026-03-16 | Added FS Governance; improved error handling |
| 1.3.0 | 2026-03-12 | Archival version, initial ClawHub release |

## 🔧 Layer 5: Advanced Configuration

### Customization Options
- **Configuration file**: `scripts/config.json`
- **Monitoring intervals**: Adjust in `real-time-monitor.sh`
- **Log policies**: Modify in `log-management.sh`
- **Health thresholds**: Configure in health check scripts

### Integration Points
- **System Status API**: Emergency endpoints
- **Logging Forwarding**: External log aggregation
- **Metrics Export**: Prometheus/Grafana compatible
- **Webhook Notifications**: Slack, Discord, email

### Security Features
- **Encrypted Backups**: Optional GPG encryption
- **Access Controls**: File permission management
- **Audit Logging**: All maintenance actions logged
- **Secrets Management**: Integration with vault systems

## 🛠️ Usage Examples

### Quick Health Check
```bash
# Run all health checks in sequence
bash scripts/daily-maintenance.sh --quick-check
bash scripts/log-management.sh --status
bash scripts/real-time-monitor.sh --status
```

### Emergency Recovery
```bash
# Force restore from latest backup
bash scripts/install-maintenance-system.sh --restore-latest

# Manual service restart
pkill -f openclaw-gateway && openclaw gateway start
```

### Performance Tuning
```bash
# Adjust monitoring frequency (edit config)
# Default: 5 minutes, can be set to 1-60 minutes
# Example: Set to 2 minutes for critical systems
```

## 🤝 Contributing

Please read `CONTRIBUTING.md` before submitting pull requests.

## 📜 License

MIT License - see `LICENSE` file for details.

---
*Built with ❤️ for the OpenClaw community*
