---
name: sys-doctor
description: "Comprehensive system diagnostics and health check for Linux servers. Check disk usage, memory, CPU load, network interfaces, running services, and system info. Generate HTML health reports or JSON output. Use when the user wants to: (1) Check server health and resource usage, (2) Diagnose performance issues, (3) Generate system health reports for monitoring, (4) Check disk space on all mounted volumes, (5) Inspect memory and swap usage, (6) Troubleshoot network connectivity, (7) Audit running services."
---

# System Doctor (sys-doctor)

Run comprehensive system diagnostics with a single command.

## Quick start

```bash
python3 skills/sys-doctor/scripts/sys_doctor.py
```

Output example:
```
◆ System Health Report: myserver
2026-05-10 13:30:00
============================================================
========================== DISK ==========================
  🟢 /              60%  (30G/50G, avail: 20G)
  🟡 /var/log       85%  (4.3G/5G, avail: 0.7G)
  🟢 /home          45%  (90G/200G, avail: 110G)
========================== MEMORY ========================
  RAM:    4.2G / 16G  (26%)
  Swap:   0.1G / 2G  (5%)
========================== CPU ============================
  Load:     0.45 / 0.32 / 0.28
  Cores:    4 (8 logical)
========================== NETWORK ========================
  🟢 eth0       UP    192.168.1.100/24
  🟢 docker0    UP    172.17.0.1/16
========================== SERVICES ======================
  • systemd-journald  • cron  • sshd  • docker
  • nginx  • postgresql  • redis-server
```

## Commands

| Command | Action |
|---------|--------|
| `--check disk` | Check only disk usage |
| `--check memory` | Check only memory/swap |
| `--check cpu` | Check only CPU load |
| `--check network` | Check only network interfaces |
| `--check services` | List running services |
| `--report` | Generate HTML health report |
| `--json` | Output as JSON |
| `--output file.html` | Save to specific file |

## HTML Reports

Generate a styled HTML report for sharing or monitoring:

```bash
python3 skills/sys-doctor/scripts/sys_doctor.py --report
# Creates: sys-doctor-report-20260510-133000.html
```

## JSON Output

For programmatic consumption (API, monitoring, dashboards):

```bash
python3 skills/sys-doctor/scripts/sys_doctor.py --json
```

## Health Status Logic

- **Disk ≥ 90%** → `critical` (exit code 2)
- **Disk ≥ 80%** → `warning`
- **Disk < 80%** → `ok`

The report's color-coded badges reflect overall health status.

## Requirements

- **Linux** (primary) — uses `/proc/`, `df`, `free`, `ip`, `systemctl`
- **macOS** — partial support via `psutil` fallback (install: `pip install psutil`)
- No external API calls — fully offline
