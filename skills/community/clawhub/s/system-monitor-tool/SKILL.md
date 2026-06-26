---
name: system-monitor
description: System resource monitoring (CPU, memory, disk, network). Use when user asks "system status", "CPU usage", "memory usage", "disk space", or wants to monitor system resources.
---

# System Monitor

Monitor system resources in real-time.

## Commands

### System Overview
When user says: "system status", "how's the system"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh status
```

### CPU Usage
When user says: "CPU usage", "how's CPU"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh cpu
```

### Memory Usage
When user says: "memory usage", "RAM status"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh memory
```

### Disk Usage
When user says: "disk space", "storage status"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh disk
```

### Network Status
When user says: "network status", "connection info"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh network
```

### Process List
When user says: "top processes", "what's using CPU"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh processes [--top 10]
```

### Temperature (if available)
When user says: "CPU temperature", "system temp"
```bash
bash skills/system-monitor-1.0.0/scripts/monitor.sh temp
```

## Examples

```bash
# Full system status
bash skills/system-monitor-1.0.0/scripts/monitor.sh status

# Check disk space
bash skills/system-monitor-1.0.0/scripts/monitor.sh disk

# Top 5 processes
bash skills/system-monitor-1.0.0/scripts/monitor.sh processes --top 5

# Monitor mode (continuous)
bash skills/system-monitor-1.0.0/scripts/monitor.sh watch --interval 5
```

## Response Format

```
🖥️  **System Status** (2026-03-10 12:30:00)

**CPU:** 25% (4 cores)
**Memory:** 8.2GB / 16GB (51%)
**Disk:** 256GB / 512GB (50%)
**Network:** 🟢 Connected (WiFi)
**Uptime:** 3 days, 4 hours
```
