# OpenClaw Self-Updater

[⭐ GitHub](https://github.com/GhostDragon124/openclaw-self-updater) | [📦 ClawHub](https://clawhub.ai/self-updater)

⭐ The ONLY OpenClaw updater with Cron-aware + Idle detection!

Intelligent auto-updater that checks for updates while respecting your scheduled tasks.

## Features

- 🔒 **Cron-aware**: Avoids disrupting your scheduled tasks
- ⏳ **Idle detection**: Waits for system idle before updating
- 🧠 **AI Risk Assessment**: Evaluates risk score (Low/Medium/High)
- ✅ **User Approval**: Confirms High-risk updates
- 📲 **Smart Notifications**: Auto-detects Telegram/Feishu
- 🔄 **Dual Updates**: Updates both OpenClaw core AND skills

## Quick Start

```powershell
# Check for updates
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1

# Auto-update with smart timing
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1 -AutoUpdate -SmartTiming
```

## Install

```bash
# Via ClawHub (recommended)
clawhub install self-updater

# Or clone manually
git clone https://github.com/your-username/openclaw-self-updater.git
```

## Documentation

See [SKILL.md](./SKILL.md) for full documentation.

## License

MIT
