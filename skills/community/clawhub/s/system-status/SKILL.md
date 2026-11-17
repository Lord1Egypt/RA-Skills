---
name: system-status
description: Reports Windows system health including disk usage, memory, CPU, and top space consumers. Use when the user asks about disk space, storage, system resources, computer health, or wants a quick system overview.
---

# System Status

Quick system health report for Windows machines.

## Usage

Run the checker directly:

```bash
node skills/system-status/index.js
```

Or import as module:

```javascript
const { report, getDiskInfo, getMemoryInfo, getCPUInfo } = require('./skills/system-status');
report();
```

## What It Reports

- CPU model, core count, thread count
- RAM usage (free/total/percentage)
- C: drive usage (free/total/percentage)
- Top-level C:\ directories ranked by file count
- System uptime

## Output

Plain text report printed to stdout. Suitable for copy-paste into chat.
