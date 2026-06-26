# Windows Healing Gateway

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)

OpenClaw Gateway Self-Healing System for Windows

## ✨ Features

- 🔄 **Auto-Monitor** - Continuous health checks every 30 seconds
- 🔧 **Auto-Repair** - Fixes JSON errors, port conflicts, plugin issues
- 🤖 **AI Diagnosis** - Intelligent log analysis and repair
- 🚨 **Alert System** - Telegram notifications for failures
- 🔒 **Secure** - Credentials isolated in environment files
- 📊 **Logging** - Comprehensive Windows Event Log integration

## 📦 Installation

### Via ClawHub

```powershell
clawhub install windows-healing-gateway
```

### Manual

```powershell
git clone https://github.com/franco-user/windows-healing-gateway.git
cd windows-healing-gateway
```

## 🚀 Quick Start

### 1. Deploy

```powershell
# Run deployment
python skills/windows-healing-gateway/scripts/deploy-windows-healing.ps1

# Or manually
powershell -ExecutionPolicy Bypass -File scripts/deploy-windows-healing.ps1
```

### 2. Configure

Edit `~/.config/openclaw/gateway.env`:

```
# Required
MOONSHOT_API_KEY=your_moonshot_key
CODING_PLAN_KEY=your_coding_plan_key

# Optional (for alerts)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. Verify

```powershell
# Check Task Scheduler tasks
schtasks /Query /TN "OpenClaw\*" /FO LIST

# View logs
Get-Content ~/.openclaw/logs/monitor.log -Tail 20
```

## 🛠️ Components

| Component | Purpose |
|-----------|---------|
| `openclaw-fix.ps1` | AI-powered repair script |
| `openclaw-monitor.ps1` | Continuous monitoring service |
| `openclaw-gateway-starter.ps1` | Gateway startup script |
| `OpenClaw-Gateway-AutoStart.xml` | Task Scheduler config |
| `OpenClaw-Monitor-Service.xml` | Monitor service config |

## 📊 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Task Scheduler │────▶│  Monitor Script │────▶│  Health Check   │
│  (Every 30s)    │     │  (PowerShell)   │     │  (Process+Port) │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                            ┌───────────────────────────┘
                            ▼
                    ┌─────────────────┐
                    │  Gateway OK?    │
                    └─────────────────┘
                          │        │
                         Yes      No
                          │        │
                          ▼        ▼
                   ┌──────────┐  ┌─────────────────┐
                   │ Continue │  │  Collect Logs   │
                   │ Monitor  │  │  AI Diagnosis   │
                   └──────────┘  │  Auto-Repair    │
                                 │  Health Check   │
                                 └─────────────────┘
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                        ┌──────────┐            ┌──────────┐
                        │  Fixed   │            │  Failed  │
                        │  Continue│            │  Alert   │
                        └──────────┘            └──────────┘
```

## 🔧 Repair Capabilities

| Issue | Fix Method |
|-------|-----------|
| JSON syntax error | Auto-remove trailing commas, fix quotes |
| Port conflict | Kill conflicting process |
| Plugin error | Disable problematic plugin |
| Memory exhaustion | Restart with cleanup |
| Process crash | Full restart with health check |

## 🚨 Alert Channels

- **Telegram** - Instant message alerts
- **Windows Notification** - System tray popup
- **Windows Event Log** - System event viewer

## 📋 Requirements

- Windows 10/11
- PowerShell 5.1 or higher
- OpenClaw CLI installed
- Task Scheduler access
- Administrator privileges (for Task Scheduler)

## 🤝 Contributing

Contributions welcome! Please submit Pull Requests.

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- OpenClaw Team
- Windows Task Scheduler
- PowerShell Community
