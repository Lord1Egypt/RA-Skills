---
name: system-monitor-pro
version: 1.0.0
description: Real-time OpenClaw system monitoring with beautiful terminal UI. CPU, memory, disk, GPU, Gateway, cron jobs, model quota, and multi-machine support. Works on macOS and Linux.
author: dagangtj
tags: [monitoring, system, dashboard, devops, gpu, openclaw]
triggers:
  - system status
  - 系统状态
  - monitor
  - 监控
  - dashboard
  - health check
  - 健康检查
---

# System Monitor Pro 🖥️

Real-time OpenClaw system monitoring skill. Beautiful formatted output directly in your chat.

## Features

- 🖥️ CPU / Memory / Disk usage with visual bars
- 🎮 GPU monitoring (NVIDIA) — utilization + VRAM
- 🌐 Gateway status + uptime
- ⏰ Cron job status overview
- 🤖 Model & quota tracking
- 💻 Multi-machine support (SSH remote monitoring)
- 📊 Beautiful terminal-style formatted output
- 🔔 Alert thresholds (CPU>80%, Memory>85%, Disk>90%)

## Usage

Just say any of these:
- "system status" / "系统状态"
- "monitor" / "监控"  
- "health check" / "健康检查"
- "dashboard"

## How It Works

When triggered, run the monitor script:

```bash
node <skill_dir>/monitor.js [--remote user@host] [--json] [--alert-only]
```

### Options
- `--remote user@host` — Monitor a remote machine via SSH
- `--json` — Output raw JSON instead of formatted text
- `--alert-only` — Only show items that need attention

### Output Format

The script outputs a beautifully formatted system status card like:

```
🦞 OpenClaw System Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖥️ CPU    ██░░░░░░░░  18%
💾 Memory ████░░░░░░  42%  6.8/16.0 GB
💿 Disk   █░░░░░░░░░   7%  14/228 GB
🌐 Gateway ● Running (pid 1234)
⏰ Crons   6/6 OK
🤖 Model   claude-opus-4-6 (yunyi)
💰 Quota   ████████████ 100% ⚠️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Multi-Machine Example

```bash
# Local machine
node monitor.js

# Remote machine via SSH
node monitor.js --remote macmini2001-01@100.104.241.24

# Both machines
node monitor.js && node monitor.js --remote macmini2001-01@100.104.241.24
```

### Integration

Add to your HEARTBEAT.md for periodic monitoring:
```markdown
## System Monitor (every 30 min)
Run: node ~/.openclaw/workspace/skills/system-monitor-pro/monitor.js --alert-only
If alerts found → notify user
```

## Requirements

- Node.js 18+
- macOS or Linux
- SSH access for remote monitoring (optional)
- `nvidia-smi` for GPU monitoring (optional)

## Files

| File | Description |
|------|-------------|
| SKILL.md | This file |
| monitor.js | Main monitoring script |
