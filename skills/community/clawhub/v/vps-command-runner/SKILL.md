---
name: vps-command-runner
description: Run commands across multiple VPS simultaneously. Execute SSH commands, deploy updates, check logs, manage Docker services, and check health across all your servers from one place. Use when managing multiple VPS, running commands across all hosts, checking status of distributed services, or deploying changes to multiple servers.
---

# VPS Command Runner

Execute commands across your VPS fleet simultaneously using SSH key auth.

## Requirements

- SSH key-based auth configured in `~/.ssh/config` with host aliases
- `~/.openclaw/vps-inventory.conf` listing your hosts (see `inventory.example.conf`)
- No passwords stored anywhere — keys only

## Setup

1. Add each VPS to `~/.ssh/config`:

```
Host vps1-de
    HostName 1.2.3.4
    User deploy
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking yes
```

2. Copy `inventory.example.conf` to `~/.openclaw/vps-inventory.conf` and list your host aliases:

```
vps1-de
vps2-us
internal
```

3. First connection: run `ssh <alias> true` once manually to accept the host key.

## Quick Usage

```bash
# Run command on all VPS
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker ps"

# Run on specific host
~/.openclaw/workspace/skills/vps-command-runner/scripts/run.sh vps1-de "systemctl status docker"

# Health check all hosts
~/.openclaw/workspace/skills/vps-command-runner/scripts/status.sh

# Pull latest image everywhere
~/.openclaw/workspace/skills/vps-command-runner/scripts/update.sh bringyour/community-provider:g4-latest

# Tail logs across fleet
~/.openclaw/workspace/skills/vps-command-runner/scripts/logs.sh urnetwork 100

# Docker helpers
~/.openclaw/workspace/skills/vps-command-runner/scripts/docker.sh ps
~/.openclaw/workspace/skills/vps-command-runner/scripts/docker.sh restart urnetwork
```

## Scripts

- `run.sh <host> <command>` — Execute on one host
- `run-all.sh <command>` — Execute on all hosts (with confirmation)
- `status.sh` — Health check: uptime, load, disk, docker, memory
- `update.sh <image>` — Pull + restart a container across fleet
- `logs.sh <container> [lines]` — Tail logs on all hosts
- `docker.sh <action> [args]` — Docker helper (ps, restart, stop, logs, exec)
- `lib.sh` — Shared config/loader, not called directly

## Security notes

- Never put IPs, usernames, or passwords in this skill's files
- All auth via `~/.ssh/config` + keys
- `run-all.sh` requires explicit confirmation before executing
- Host key checking is enforced (`StrictHostKeyChecking=yes` via ssh config)
