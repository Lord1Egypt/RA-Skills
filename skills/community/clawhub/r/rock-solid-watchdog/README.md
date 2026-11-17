# 🔒 Rock-Solid Watchdog for llama.cpp

![macOS](https://img.shields.io/badge/macOS-✓-brightgreen)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-orange)

A self-healing supervisor for local LLM inference servers. Monitors
health, auto-restarts on failure, escalates to recovery.

## ⚡ Quick Start

```bash
git clone https://github.com/gutchapa/rock-solid-watchdog.git
cd rock-solid-watchdog
bash rock-solid-watchdog.sh
```

## ✨ Features

- **Self-healing** — auto-restarts crashed llama-server
- **Configurable** — retry limits, check intervals, logging
- **Smart alerts** — macOS notifications on failure
- **Hook system** — custom scripts on start, fail, escalate
- **Zero deps** — pure bash + curl, no pip/npm install
- **Mac Mini ready** — tested on M-series, 16 GB RAM

## 📋 Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMA_PORT` | 8084 | Watchdog port |
| `LLAMA_HOST` | 127.0.0.1 | Bind address |
| `MAX_CONSECUTIVE_FAILS` | 5 | Auto-restart threshold |
| `LOG_FILE` | `~/.openclaw/logs/watchdog.log` | Log path |

## 🤝 Contributing

PRs welcome! See [openclaw/clawhub](https://github.com/openclaw/clawhub) for plugin registry.

## 📄 License

Apache 2.0
