---
name: syspeek
description: Display a compact ASCII dashboard of system health: uptime, CPU load, memory usage, disk usage, and top open network ports. Use when the user asks to "peek" at the system, check system status, or view a quick system overview.
---

# syspeek — System Peek

Displays a compact ASCII dashboard of system health: uptime, CPU load, memory, disk, and top network connections.

## Usage

```bash
~/.openclaw/workspace/skills/syspeek/scripts/syspeek.sh
```

## Output

```
╔══════════════════════════════════════╗
║           SYSTEM PEEK                ║
╠══════════════════════════════════════╣
║ uptime    │ 15:42:38 up 3 days ...   ║
║ CPU load  │ 0.12 0.08 0.01 (1/4)    ║
║ memory    │ 6.2G / 15G (41%)         ║
║ disk root │ 22G / 100G (22%)         ║
║ top ports │ tcp 22,443,3306,6379     ║
╚══════════════════════════════════════╝
```

## Implementation

- `scripts/syspeek.sh` — POSIX shell script, no external dependencies beyond standard Linux tools
