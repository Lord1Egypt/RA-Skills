---
name: vps-guardian
description: Autonomous VPS monitoring and auto-remediation — kills runaway procs, frees disk, restarts dead services, hardens security. Not alerts. Action.
tags:
  - vps
  - monitoring
  - remediation
  - security
  - automation
  - devops
  - self-healing
category: devops
---

# VPS Guardian — Self-Healing Server Agent

## What It Does

VPS Guardian doesn't just alert you when something's wrong — it fixes it. An autonomous agent that monitors your VPS and takes action: killing runaway processes, freeing disk space, restarting dead services, and hardening security.

**Philosophy: Alerts are for humans. Guardians act.**

## Quick Start

### Install

```bash
# Download
sudo curl -o /usr/local/bin/vps-guardian https://raw.githubusercontent.com/vps-guardian/guardian/main/src/guardian.py
sudo chmod +x /usr/local/bin/vps-guardian

# Configure (optional — defaults are sensible)
sudo cp /usr/local/bin/vps-guardian.conf.example /etc/vps-guardian.conf
```

### Run

```bash
# One-shot scan + remediate
vps-guardian --scan

# Daemon mode (continuous monitoring)
vps-guardian --daemon

# Dry run (report only, no action)
vps-guardian --dry-run
```

### Schedule with Cron

```bash
# Every 5 minutes
*/5 * * * * /usr/local/bin/vps-guardian --scan >> /var/log/vps-guardian.log 2>&1
```

## What It Fixes

### 1. Runaway Processes
- Detects processes consuming >90% CPU for 5+ minutes
- Identifies zombie processes (state Z)
- Finds OOM candidates (highest RSS on low memory)
- **Action**: SIGTERM, then SIGKILL after 10s if unresponsive
- Logs PID, command, CPU%, memory%, and duration before killing

### 2. Disk Space Recovery
- Warns at 80% usage, acts at 90%
- Rotates logs older than 7 days (gzip)
- Clears /tmp files older than 3 days
- Removes orphaned apt caches
- Truncates journal logs >500MB
- **Action**: Sequential cleanup until below threshold
- Logs bytes freed and what was cleaned

### 3. Dead Service Restart
- Monitors critical systemd services
- Detects failed/inactive states
- Attempts `systemctl restart` up to 3 times
- Escalates to alert after 3 failures
- **Action**: Auto-restart with exponential backoff (5s, 30s, 120s)

### 4. Security Hardening
- Detects unexpected listening ports (diffs against baseline)
- Identifies brute-force SSH attempts (fail2ban integration)
- Flags world-writable files in /etc, /root
- Checks for suspicious processes (crypto miners, reverse shells)
- **Action**: Blocks IPs via iptables, chmods files, kills suspicious processes
- Never auto-blocks — always requires approval (prevents lockout)

### 5. Memory Recovery
- Detects memory pressure (available <10%)
- Identifies top memory consumers
- Clears page cache, dentries, inodes
- **Action**: Cache drop first, process kill as last resort

## Configuration

```ini
# /etc/vps-guardian.conf

[thresholds]
cpu_kill_percent = 90
cpu_kill_duration = 300
disk_warn_percent = 80
disk_act_percent = 90
memory_act_percent = 90
zombie_kill = true

[services]
# Services to auto-restart when down
critical = ssh, cron, systemd-resolved, rsyslog
# Services to monitor but NOT auto-restart
watched = nginx, docker, fail2ban

[security]
block_bruteforce = true
max_ssh_failures = 10
scan_suspicious_procs = true
auto_block = false    # Always requires approval

[cleanup]
rotate_logs_days = 7
tmp_max_age_days = 3
journal_max_size_mb = 500
apt_cache_clean = true

[alerts]
telegram_bot_token =
telegram_chat_id =
webhook_url =
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Healthy — no issues found |
| 1 | Remediated — fixed issues, all clear now |
| 2 | Critical — unrecoverable issues remain |
| 3 | Error — guardian itself failed |

## Logging

All actions are logged with before/after state:

```
[2026-04-17T06:30:00Z] RUNAWAY pid=4523 cmd="node server.js" cpu=94.2% mem=1.2G duration=420s → SIGTERM → exited
[2026-04-17T06:30:05Z] DISK / 92% → rotated /var/log/syslog.1 (freed 340MB) → 87%
[2026-04-17T06:30:10Z] SERVICE ssh: inactive → restarted → active
[2026-04-17T06:30:15Z] SECURITY 5 SSH failures from 45.33.xx.xx → blocked via iptables
```

## Safety Mechanisms

- **Protected processes**: Never kills pid 1, kernel threads, or self
- **Protected services**: Never restarts systemd itself
- **Rate limiting**: Max 5 process kills per scan cycle
- **Dry run mode**: `--dry-run` shows what would happen without acting
- **Whitelist**: Exclude processes/services from remediation
- **Approval gate**: Security actions always require confirmation

## Requirements

- Linux (systemd-based)
- Python 3.8+
- Root or sudo access
- No external dependencies (stdlib only)

## Differences from Monitoring Tools

| Feature | Traditional Monitoring | VPS Guardian |
|---------|----------------------|--------------|
| Detects issues | Yes | Yes |
| Sends alerts | Yes | Yes |
| Fixes issues | No | Yes |
| Requires human | Yes | No (configurable) |
| Runs autonomously | No | Yes |
| Learns baselines | Sometimes | Yes (over time) |

## Support

- Issues: https://github.com/vps-guardian/guardian/issues
- Docs: https://vps-guardian.io/docs
