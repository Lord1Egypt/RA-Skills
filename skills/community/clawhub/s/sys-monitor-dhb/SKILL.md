---
name: system-monitor
description: Monitor system metrics like CPU, memory, disk, and network. Use when user needs to track server performance, set up alerts for high resource usage, monitor uptime, check process status, or create system health reports.
---

# System Monitor

Monitor system metrics like CPU, memory, disk, and network.

## Quick Start

```bash
# Check current status
python scripts/monitor.py --status

# Monitor continuously
python scripts/monitor.py --watch
```

## Usage

```bash
python scripts/monitor.py [OPTIONS]

Options:
  --status        Show current system status
  --watch         Monitor continuously
  --interval SECS Check interval (default: 5)
  --cpu           Show CPU usage
  --memory        Show memory usage
  --disk          Show disk usage
  --network       Show network stats
  --processes     Show top processes
  --alert VALUE   Alert threshold (e.g., cpu:90)
  --json          Output as JSON
```

## Examples

```bash
# Quick status check
python scripts/monitor.py --status

# Watch mode
python scripts/monitor.py --watch --interval 10

# Alert on high CPU
python scripts/monitor.py --watch --alert cpu:90

# Alert on low disk
python scripts/monitor.py --watch --alert disk:90

# JSON output for dashboards
python scripts/monitor.py --status --json
```

## Alert Examples

```bash
# CPU above 90%
python scripts/monitor.py --watch --alert cpu:90

# Memory above 80%
python scripts/monitor.py --watch --alert memory:80

# Disk above 85%
python scripts/monitor.py --watch --alert disk:85
```

## Metrics

- CPU usage per core
- Memory usage (used/free/total)
- Disk usage per partition
- Network I/O
- Top processes by CPU/memory
- Uptime
