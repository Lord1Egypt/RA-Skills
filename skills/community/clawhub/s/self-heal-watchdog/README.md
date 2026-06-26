# OpenClaw Self-Heal Watchdog 🛡️

Automated self-healing system for OpenClaw gateway with **model failover support**.

## Features

### Three-Layer Protection

| Layer | Detection | Action | Auto? |
|-------|-----------|--------|-------|
| **Process Watchdog** | Gateway process crash | Auto-restart | ✅ |
| **Config Guard** | Config corruption | Rollback + restart | ✅ |
| **Model Health Check** | Model API failure (2 consecutive) | Switch to fallback model | ✅ |

### Key Improvements over basic watchdogs

- **Model failover** — Detects when a model stops responding and auto-switches to fallback
- **State tracking** — Remembers current model, fail count, and failover history
- **Config backup** — Automatic backup before any config change
- **Dry-run mode** — Test without actually restarting anything
- **macOS launchd** — Native macOS scheduling (not just cron)

## Quick Install

```bash
bash scripts/setup.sh
```

This will:
1. Create `~/.openclaw/watchdog/` directory
2. Copy scripts to `~/.openclaw/watchdog/`
3. Register as launchd service (every 60 seconds)
4. Create initial config backup

## Manual Commands

```bash
# Check status
bash ~/.openclaw/watchdog/status.sh

# Full status with complete log
bash ~/.openclaw/watchdog/status.sh --full

# Dry-run test (no actual restart)
DRY_RUN=1 bash ~/.openclaw/watchdog/watchdog.sh

# View logs
tail -20 ~/.openclaw/watchdog/watchdog.log

# Disable watchdog
launchctl unload ~/Library/LaunchAgents/com.openclaw.watchdog.plist
```

## Configuration

Default settings in `scripts/watchdog.sh`:

| Variable | Default | Description |
|----------|---------|-------------|
| `HEALTH_ENDPOINT` | `http://localhost:18789/health` | Gateway health check URL |
| `FAIL_THRESHOLD` | `2` | Consecutive failures before failover |
| `CURRENT_MODEL` | Read from config | Current AI model |
| `FALLBACK_MODEL` | `openrouter/hunter-alpha` | Fallback model on failure |
| `OPENCLAW_CONFIG` | `~/.openclaw/openclaw.json` | Config file path |

## State File

`~/.openclaw/watchdog-state.json`:

```json
{
  "current_model": "openrouter/hunter-alpha",
  "original_model": "openrouter/healer-alpha",
  "fail_count": 0,
  "last_check": "2026-03-16T11:00:00-07:00",
  "last_failover": null,
  "failed_models": []
}
```

## Recovery Levels

| Level | Condition | Action | Auto? |
|-------|-----------|--------|-------|
| 1 | Process dead, config OK | Restart gateway | ✅ |
| 2 | Process alive, health check fail | Rollback config + restart | ✅ |
| 3 | Model unresponsive (2x) | Switch to fallback model | ✅ |
| 4 | No valid backup exists | Log alert | ⚠️ Manual |

## Log Format

```
[2026-03-16 11:00:00] ✅ Health check passed (model: hunter-alpha, response: 234ms)
[2026-03-16 11:01:00] ❌ Health check failed (model: healer-alpha, error: timeout) [1/2]
[2026-03-16 11:02:00] ❌ Health check failed (model: healer-alpha, error: timeout) [2/2]
[2026-03-16 11:02:01] 🔄 FAILOVER: healer-alpha → hunter-alpha
[2026-03-16 11:02:15] ✅ Gateway restarted with fallback model
```

## Uninstall

```bash
# Stop watchdog
launchctl unload ~/Library/LaunchAgents/com.openclaw.watchdog.plist

# Remove files
rm -rf ~/.openclaw/watchdog
rm ~/Library/LaunchAgents/com.openclaw.watchdog.plist
```

## Platform Support

- **macOS** — launchd (recommended) or cron
- **Linux** — cron or systemd (see `references/`)
- **Docker** — Use HEALTHCHECK directive

## License

MIT
