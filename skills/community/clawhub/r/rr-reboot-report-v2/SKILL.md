---
name: rr-reboot-report-v2
description: Detect unexpected system reboots and alert when the system comes back online. Tracks boot history and flags suspicious restarts.
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["bash"],"files":["~/.rr-reboot-config"]}}}
---

# RR Reboot Report

Detect unexpected reboots and track boot history. Useful for security monitoring — flags when a system restarts unexpectedly.

## Quick Start

```bash
# Check for unexpected reboot (run at startup or on first heartbeat)
bash {baseDir}/scripts/check-reboot.sh

# View boot history
bash {baseDir}/scripts/check-reboot.sh --history

# Reset state (mark current boot as known)
bash {baseDir}/scripts/check-reboot.sh --reset
```

## How It Works

1. On first run, records current boot time to state file
2. On subsequent runs, compares current boot time with last known
3. If boot time changed unexpectedly → alerts
4. State file: `~/.reboot-check-state` (customizable with `--state`)

## Output

```
STATUS: CLEAN       — No reboot since last check
STATUS: REBOOTED    — System rebooted since last check
STATUS: FIRST_RUN   — First time running, recording boot time
```

## Integration

### Auto-Alert via Cron (Recommended)

For automatic Telegram alerts on reboot without needing the agent active:

**1. Create config file** (one-time setup):
```bash
cat > ~/.rr-reboot-config << 'EOF'
BOT_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
EOF
chmod 600 ~/.rr-reboot-config
```

**2. Add to crontab:**
```bash
@reboot /path/to/scripts/reboot-alert.sh
```

The `reboot-alert.sh` helper script:
- Detects reboots automatically
- Reads credentials from `~/.rr-reboot-config` (user-created, isolated config)
- Sends alert via Telegram Bot API directly
- Waits for network at boot
- Resets state after alert

No credentials stored in the script or skill files. All user-provided.

### Heartbeat Integration

```bash
# In heartbeat script
RESULT=$(bash check-reboot.sh)
[[ "$RESULT" == *"REBOOTED"* ]] && echo "ALERT: Unexpected reboot!"
```

## Options

- `--state FILE` — State file path (default: `~/.reboot-check-state`)
- `--history` — Show recorded boot history
- `--reset` — Reset state to current boot
- `--json` — Output as JSON
