# windows-healing-gateway

OpenClaw Gateway Self-Healing System for Windows

Windows 环境下的 OpenClaw 网关自愈系统，使用 Task Scheduler 实现自动监控、故障修复和告警通知。

## Description

This skill provides a complete self-healing solution for OpenClaw Gateway on Windows:

- **Auto-Monitor**: Continuously monitors Gateway health every 30 seconds
- **Auto-Repair**: Automatically fixes crashes (JSON errors, port conflicts, plugin issues)
- **AI Diagnosis**: Analyzes logs and applies intelligent fixes
- **Alert Notification**: Sends alerts via Telegram when manual intervention needed
- **Secure**: All sensitive credentials isolated in environment files

## Tools

- `healing.deploy` - Deploy the healing system
- `healing.status` - Check system status
- `healing.repair` - Manual trigger repair
- `healing.logs` - View logs

## Installation

```powershell
# Via ClawHub
clawhub install windows-healing-gateway

# Manual
clawhub install https://github.com/yourusername/windows-healing-gateway
```

## Usage

### Deploy

```powershell
# Run deployment script
python skills/windows-healing-gateway/scripts/deploy-windows-healing.ps1
```

### Check Status

```powershell
# View Task Scheduler status
schtasks /Query /TN "OpenClaw\*" /FO LIST

# View logs
Get-Content ~/.openclaw/logs/monitor.log -Tail 20
```

### Manual Repair

```powershell
# Trigger manual repair
~/.openclaw/scripts/openclaw-fix.ps1

# Test mode (diagnose only)
~/.openclaw/scripts/openclaw-fix.ps1 -TestMode
```

## Configuration

Edit `~/.config/openclaw/gateway.env`:

```
MOONSHOT_API_KEY=your_key
CODING_PLAN_KEY=your_key
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Features

- ✅ Task Scheduler integration
- ✅ Process monitoring
- ✅ JSON repair
- ✅ Port conflict resolution
- ✅ Plugin error handling
- ✅ Telegram alerts
- ✅ Windows Event Log
- ✅ Secure credential storage

## Requirements

- Windows 10/11
- PowerShell 5.1+
- OpenClaw CLI
- Task Scheduler access

## Author

Franco

## License

MIT-0
