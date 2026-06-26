# 🛡️ SysGuard - System Guardian for OpenClaw

> Zero-dependency, ultra-lightweight, IM-friendly system monitoring

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Shell](https://img.shields.io/badge/Shell-Bash-green.svg)]()

**SysGuard** is a pure Shell-based system guardian for OpenClaw. It provides real-time monitoring, intelligent diagnostics, and transparent notifications — all within your IM client.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏥 **Health Check** | Real-time CPU, Memory, Disk, Gateway monitoring |
| 🔔 **Transparent Notification** | Alerts on anomalies, user decides restart (no auto-restart) |
| 📊 **Visualization** | Text-based trend charts, viewable directly in IM |
| 🔍 **Smart Diagnostics** | 8 hidden events auto-detection |
| 🧹 **Safe Cleaning** | Cache cleanup to free disk space |
| ⚡ **Zero Dependencies** | Pure Shell, no external packages needed |

---

## 📋 Commands

| Command | Description |
|---------|-------------|
| `sg` | System status + command hints |
| `sgc` | Clean cache |
| `sgch` | Health check |
| `sgd` | Diagnostic report |
| `sgt [hours]` | Trend chart (default: 12h) |
| `sgm` | Daemon monitor |

> 💡 **Every `sg` displays all available commands** — build muscle memory fast

---

## 🚀 Quick Start

### Installation (For OpenClaw Admins)

```bash
# One-click install via ClawHub (recommended)
clawhub install sysguard

# Or clone from GitHub
git clone https://github.com/Steventsang18/sysguard.git
```

Once installed, **all users** can use SysGuard in any IM conversation — Feishu, WeChat Work, DingTalk, WeChat, etc. — by simply talking to the bot:

```
User: sg
Bot: 📊 SysGuard Status
     CPU   █████░░░░░ 54% ✅
     ...
```

### Usage

### Configuration (Optional)

```bash
vim ~/.openclaw/workspace/skills/sysguard/config/sysguard.conf
```

```bash
NOTIFY_CHANNEL=feishu
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

---

## 📊 Examples

### Status Panel

```
📊 SysGuard Status
━━━━━━━━━━━━━━━━━━━━━━
🕐 2026-03-24 00:40 | up 5d 12h
━━━━━━━━━━━━━━━━━━━━━━
CPU   █████░░░░░ 54% ✅
Memory ████░░░░░░ 40% ✅
Disk   ███████░░░ 74% ✅
Gateway ✅ Running (PID:3338082)
━━━━━━━━━━━━━━━━━━━━━━
💡 sgc | sgch | sgd | sgt | sgm
```

### Alert Notification

```
🚨 SysGuard Alert

⏰ Time: 2026-03-24 00:40
🔴 Status: Gateway unresponsive

📋 Possible Causes:
• Process crash or OOM
• High system load

🔧 Suggested Action:
• Run 'sgm' to start daemon monitor
```

---

## 🔍 8 Hidden Events

| # | Event | Impact |
|---|-------|--------|
| 1 | Gateway unresponsive | Total failure |
| 2 | Disk space low | Backup fails |
| 3 | Memory leak | Degrading performance |
| 4 | API timeout | Slow replies |
| 5 | Process overflow | High system load |
| 6 | Log explosion | Disk exhaustion |
| 7 | Cron buildup | Tasks stuck |
| 8 | Network packet loss | Timeouts |

---

## 🏗️ Project Structure

```
sysguard/
├── scripts/
│   ├── sysguard.sh          # Main entry
│   ├── health_check.sh      # Health check
│   ├── diagnostics.sh       # Diagnostics engine
│   ├── trend.sh             # Trend charts
│   ├── clean.sh             # Cache cleaner
│   ├── monitor.sh           # Daemon monitor
│   ├── ui.sh                # UI formatter
│   └── notifier.sh          # Notification module
├── config/
│   └── sysguard.conf        # Configuration
├── data/
│   └── history/             # JSON history data
└── lib/                     # Shared libraries
```

---

## 🎯 Comparison with AgentFlow

| Dimension | AgentFlow | SysGuard |
|-----------|-----------|----------|
| Process healing | ❌ | ✅ Transparent notification |
| Gateway RPC integration | ❌ | ✅ Deep probe |
| Trend charts | ❌ | ✅ Historical visualization |
| IM-friendly output | ⚠️ Basic | ✅ Optimized |
| Diagnostic knowledge base | ❌ | ✅ 8 hidden events |

---

## 📄 License

[MIT License](LICENSE)

---

## 👤 Author

**Zeng Pengxiang (曾鹏祥)**

- GitHub: [Steventsang18](https://github.com/Steventsang18)
- Home: https://github.com/Steventsang18/sysguard

---

**🛡️ SysGuard — Guardian for your system**
