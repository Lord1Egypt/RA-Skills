# termux-persistent-gateway 📱

Keep your AI agent gateway running persistently on Android/Termux — no systemd needed.

## Features

- **tmux session** — gateway survives screen-off and app-switching
- **Wake lock** — prevents CPU from sleeping
- **Auto-start on boot** — via Termux:Boot
- **Health monitoring** — auto-restart if gateway goes down
- **Configurable** — set your gateway command, session name, log paths

## Installation

```bash
clawhub install termux-persistent-gateway
```

## Quick Start

```bash
# Edit config at top of scripts/run-gateway.sh to set your gateway command
bash <skill_dir>/scripts/run-gateway.sh
```

## Requirements

- Termux (Android)
- `pkg install tmux termux-api termux-boot`
- Android: Settings > Apps > Termux > Battery > **Unrestricted**

## License

MIT
