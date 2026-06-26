---
name: reboot-checker
description: Detect unexpected system reboots and alert when the system comes back online. Tracks boot history and flags suspicious restarts.
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["bash"]}}}
---

# Reboot Checker

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

Use with cron or heartbeat systems:
```bash
# Cron: check every hour
0 * * * * /path/to/check-reboot.sh >> /var/log/reboot-check.log

# Or in a heartbeat script
RESULT=$(bash check-reboot.sh)
[[ "$RESULT" == *"REBOOTED"* ]] && echo "ALERT: Unexpected reboot!"
```

## Options

- `--state FILE` — State file path (default: `~/.reboot-check-state`)
- `--history` — Show recorded boot history
- `--reset` — Reset state to current boot
- `--json` — Output as JSON
