---
name: uptime-tool
description: Show system uptime, load average, active user count, and boot time. Use for system health checks, monitoring, and diagnostics.
---

# Uptime Tool — System Uptime & Load Monitor

Display how long the system has been running since last boot, current user sessions, and CPU load averages. Essential for health checks, reboot verification, and capacity monitoring.

## Quick Start

```bash
# Show system uptime
uptime-tool

# Show uptime plus JSON output for monitoring
uptime-tool --json
```

## Usage

```bash
uptime-tool [OPTIONS]

Options:
  --json       Output as structured JSON
  --pretty     Human-readable format with emojis (default)
  --since      Show boot time timestamp
  --seconds    Show uptime in seconds only
  --compare    Compare with last-known value (requires --state-file)
  --watch N    Monitor continuously, N second intervals
  --alert N    Alert if uptime < N seconds (short uptime = recent reboot)
```

## Examples

```bash
# Standard uptime output
uptime-tool

# Machine-readable JSON for monitoring
uptime-tool --json

# Show boot time
uptime-tool --since

# Watch every 30 seconds
uptime-tool --watch 30

# Alert if system just rebooted (< 60 seconds uptime)
uptime-tool --alert 60

# Uptime in seconds for scripts
uptime-tool --seconds
```

## Features

- **Standard uptime display** with load averages
- **JSON output** for monitoring pipelines
- **Boot time** detection (when did the system start?)
- **Continuous watch** mode for real-time monitoring
- **Alert thresholds** for restart detection
- **Compare mode** detects unexpected reboots
- **Cross-platform** — works on Linux, macOS, BSD
