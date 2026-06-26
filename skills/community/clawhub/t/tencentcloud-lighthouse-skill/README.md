# Tencent Cloud Lighthouse Skill

An OpenClaw Skill for managing Tencent Cloud Lighthouse instances via tccli CLI.

Supports instance management, monitoring & alerting, firewall configuration, remote command execution (TAT), snapshots, and traffic package management.

## Structure

```
SKILL.md                              # Main skill definition
references/
  instance-management.md              # Instance query, start/stop/reboot, password reset
  monitoring-alerting.md              # CPU/memory/bandwidth metrics, alarm policies
  firewall-management.md              # Firewall rule CRUD, security best practices
  remote-command-tat.md               # TAT remote command execution
  snapshot-blueprint.md               # Snapshot and custom image management
  traffic-package.md                  # Traffic package usage query
```

## Quick Start

1. Install tccli: `pip install tccli`
2. Configure credentials via OAuth login or AK/SK
3. Refer to SKILL.md for usage
