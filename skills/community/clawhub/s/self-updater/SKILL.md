---
name: self-updater
version: 1.4.2
description: |
  ⭐ OPEN SOURCE! GitHub: github.com/GhostDragon124/openclaw-self-updater
  ⭐ ONLY skill with Cron-aware + Idle detection! Auto-updates OpenClaw core & skills, analyzes cron schedules to avoid user tasks, waits for idle time, AI-powered risk assessment, user approval for high-risk updates, and smart notifications.
  Use for: auto-update, maintenance, cron, smart-schedule, skills, gateway, restart, healthcheck, monitoring, ops
repository:
  type: git
  url: https://github.com/GhostDragon124/openclaw-self-updater
homepage: https://github.com/GhostDragon124/openclaw-self-updater#readme
required_binaries:
  - pwsh (PowerShell 5.1+)
  - npm
  - clawhub
optional_envs:
  - TELEGRAM_BOT_TOKEN
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
---

# Self Updater

⭐ **The ONLY OpenClaw updater with Cron-aware + Idle detection!**

Intelligent auto-updater that checks for updates while respecting your scheduled tasks.

## Why This Skill?

| Feature | Other Updaters | This Skill |
|---------|---------------|------------|
| Cron-aware | ❌ | ✅ Avoids your scheduled tasks |
| Idle detection | ❌ | ✅ Waits for system idle |
| AI Risk Assessment | ❌ | ✅ Evaluates update impact |
| User Approval | ❌ | ✅ Confirms High-risk updates |
| Smart Notifications | ⚠️ Basic | ✅ Concise, channel-aware |

## Features

- **🔒 Cron-aware**: Reads ~/.openclaw/cron/jobs.json to avoid disrupting your scheduled tasks
- **⏳ Idle detection**: Waits for system idle before updating (no interruption!)
- **🧠 AI Impact Assessment**: Evaluates risk score (Low/Medium/High) before updating
- **✅ User Approval**: Pauses and asks before High-risk updates
- **📲 Smart Notifications**: Auto-detects Telegram/Feishu, sends concise reports
- **🔄 Dual Updates**: Updates both OpenClaw core AND installed skills
- **🛡️ Auto-restart**: Ensures gateway comes back up after updates
- **🌐 Port Auto-detect**: Reads gateway port from config automatically

## Quick Start

```powershell
# Check for updates
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1

# Auto-update with smart timing
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1 -AutoUpdate -SmartTiming

# Full automation (for cron)
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1 -AutoUpdate -SmartTiming -AutoApprove -Quiet
```

## AI Risk Assessment

Evaluates 5 factors to calculate risk score:

| Factor | Weight | Description |
|--------|--------|-------------|
| Version Impact | 30% | Major/Minor/Patch |
| Skills Count | 25% | Number of skills to update |
| Gateway Restart | 20% | Restart impact |
| Time Since Update | 15% | Hours since last update |
| Cron Proximity | 10% | Distance to next task |

**Risk Levels**:
- 🟢 **Low** (Score <50): Auto-update
- 🟡 **Medium** (Score 50-74): Warning but auto-update
- 🔴 **High** (Score ≥75): Requires YOUR approval

## User Approval Flow

When risk is **High**:
1. Shows warning with assessment details
2. Waits for your confirmation (60s timeout)
3. If approved → proceeds with update
4. If rejected/skipped → cancels gracefully

Use `-AutoApprove` for unattended runs.

## Smart Notifications

**Pre-update** (concise):
```
🔄 OpenClaw Update Check
• Core: 1.2.3 → 1.3.0 (Minor)
• Skills: 3 to update
• Risk: 🟡 Medium
```

**Post-update**:
```
✅ OpenClaw Updated
• Core: v1.3.0
• Skills: 3 updated
• Gateway: ✅ OK
```

Auto-detects: Telegram, Feishu

## Use Cases

- ✅ Weekly maintenance automation
- ✅ Keep OpenClaw always up-to-date
- ✅ Never interrupt scheduled crawler tasks
- ✅ Get notified of updates
- ✅ Safe auto-updates with risk control

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| AutoUpdate | false | Apply updates automatically |
| SmartTiming | false | Wait for idle + check cron |
| AutoApprove | false | Skip approval (for cron) |
| NoNotify | false | Skip notifications |
| UpdateSkillsOnly | false | Update skills only |
| Port | auto | Gateway port |
| IdleThreshold | 5 | Minutes of idle to wait |
| CronLookAhead | 60 | Minutes to look ahead for tasks |
| MaxWait | 30 | Max wait time (minutes) |

## Requirements

- PowerShell 5.1+ (pwsh)
- npm + clawhub CLI
- Windows (idle detection)
- Reads: `~/.openclaw/openclaw.json` (port only), `~/.openclaw/cron/jobs.json`

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications |
| `FEISHU_APP_ID` | Feishu app ID for notifications |
| `FEISHU_APP_SECRET` | Feishu app secret for notifications |

> **Note:** This skill only reads the `gateway.port` from config. No credentials are transmitted externally.

## Tags

auto-update, maintenance, cron, smart-schedule, skills, gateway, restart, healthcheck, monitoring, ops, openclaw, updater, self-maintenance, ai-assessment, user-approval, notification
