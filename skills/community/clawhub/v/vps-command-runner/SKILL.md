---
name: vps-command-runner
description: Run commands across multiple VPS simultaneously. Execute SSH commands, deploy updates, check logs, and manage services across all your servers from one place. Use when managing multiple VPS, running commands across all hosts, checking status of distributed services, or deploying changes to multiple servers.
---

# VPS Command Runner

Execute commands across your VPS fleet simultaneously.

## VPS Inventory

| Host | IP | Username | Services |
|------|-----|----------|----------|
| Internal | [REDACTED] | [REDACTED] | Gateway, Nextcloud, Providers |
| VPS1 (DE) | [REDACTED] | [REDACTED] | Provider, Nextcloud |
| VPS2 (US) | [REDACTED] | [REDACTED] | WireGuard, Providers, Nextcloud |

## Setup

Edit scripts to add your credentials:

```bash
# Set these variables in each script:
USER="your-username"
PASS="your-password"

# Or use SSH keys:
# Add keys to ~/.ssh/ and modify scripts to use key auth
```

## Quick Usage

```bash
# Run command on all VPS
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker ps"

# Run command on specific VPS
~/.openclaw/workspace/skills/vps-command-runner/scripts/run.sh [IP] "systemctl status docker"

# Check provider status everywhere
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker ps --filter name=urnetwork --format \"{{.Names}}\" | wc -l"

# Update all providers
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker pull bringyour/community-provider:g4-latest"
```

## Scripts

- `run-all.sh <command>` — Execute on all VPS
- `run.sh <ip> <command>` — Execute on specific VPS
- `status.sh` — Quick health check of all VPS

## SSH Setup

Default: password authentication (edit scripts to change)

For key-based auth:
1. Add keys to `~/.ssh/`
2. Modify scripts to use: `ssh -i ~/.ssh/key ...` instead of `sshpass`