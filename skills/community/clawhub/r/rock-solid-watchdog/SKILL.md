# Rock-Solid Watchdog

A self-healing supervisor for local LLM inference servers (llama.cpp).
Monitors health, auto-restarts on failure, escalates to recovery.

## Type

Plugin — runs alongside OpenClaw gateway

## How it works

```bash
# 1. Clone / download
git clone https://github.com/gutchapa/rock-solid-watchdog.git
cd rock-solid-watchdog

# 2. Configure (optional env vars)
export LLAMA_PORT=8085
export LLAMA_SERVER=~/llama.cpp/build/bin/llama-server

# 3. Run
bash rock-solid-watchdog.sh
```

## Features

- Configurable health check interval and retry limits
- macOS notifications on failure (optional)
- Consecutive failure tracking with rate-limited escalation
- Graceful restart with full logging
- Custom hook system (pre-start, post-start, post-fail, escalate)

## Requirements

- bash 4+
- curl
- pkill/pgrep
- macOS (Linux-compatible with notify-send)

## Files

```
rock-solid-watchdog/
├── rock-solid-watchdog.sh   # Main script
├── README.md                # This file
└── hooks/                   # Optional custom hooks
    ├── 00-notify-post-start.sh.example
    └── 00-log-post-fail.sh.example
```

## Env vars

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMA_SERVER` | `~/llama.cpp/build/bin/llama-server` | Path to server binary |
| `LLAMA_PORT` | `8084` | Watchdog port |
| `LLAMA_HOST` | `127.0.0.1` | Bind address |
| `MAX_CONSECUTIVE_FAILS` | `5` | Auto-restart threshold |
| `ENABLE_LLAMA_WATCH` | `1` | Enable/disable |
| `LOG_FILE` | `~/.openclaw/logs/watchdog.log` | Log path |
| `HOOK_DIR` | `./hooks/` | Custom hook scripts directory |

## License

Apache 2.0
