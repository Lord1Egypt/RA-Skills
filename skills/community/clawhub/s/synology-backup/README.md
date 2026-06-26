# Synology Backup

[![ClawHub](https://img.shields.io/badge/ClawHub-synology--backup-blue)](https://clawhub.ai/pfrederiksen/synology-backup)
[![Version](https://img.shields.io/badge/version-1.2.1-green)]()

An [OpenClaw](https://openclaw.ai) skill for backing up and restoring OpenClaw workspace, configs, and agent data to a Synology NAS via SMB or SSH/rsync. Supports Tailscale for secure remote VPS-to-NAS connectivity.

## Features

- 💾 **Incremental backup** — workspace, configs, agent data, cron jobs, sub-agent workspaces
- 🚫 **Smart exclusions** — `.git/`, `node_modules/`, `__pycache__/` excluded by default; configurable
- 🔄 **Safe restore** — automatically snapshots current state before restoring (undo in one command)
- 🔍 **Integrity verification** — checksums key files and counts directory contents
- 📊 **Status checks** — mount health, disk space, last success timestamp, snapshot inventory
- ✅ **State tracking** — records last successful backup timestamp + manifest checksum
- ⚠️ **Failure alerting** — Telegram alert on backup failure (optional success notification too)
- 🔒 **Tailscale support** — secure remote backup over WireGuard mesh
- 🔑 **SSH/rsync transport** — alternative to SMB; key-based auth, no credentials file needed
- 🧹 **Auto-pruning** — daily snapshots and pre-restore safety snapshots pruned automatically
- 🛡️ **Security-hardened** — all config values validated, no `eval`, no shell injection possible

## Scripts

| Script | Description |
|--------|-------------|
| `backup.sh [--dry-run]` | Run incremental backup |
| `restore.sh [date]` | Restore from snapshot (lists available if no date given) |
| `status.sh` | Show mount health, last backup, snapshot inventory |
| `verify.sh [date]` | Verify snapshot integrity via checksums |

## Installation

```bash
clawhub install synology-backup
```

## Quick Setup

1. Install dependencies: `apt-get install -y cifs-utils rsync`
2. Create a dedicated Synology user with access to one share only
3. Create credentials file: `touch ~/.openclaw/.smb-credentials && chmod 600 ~/.openclaw/.smb-credentials`
4. Create config at `~/.openclaw/synology-backup.json` (see SKILL.md for full reference)
5. Test: `bash scripts/backup.sh --dry-run`
6. Register cron: `openclaw cron add --name "Synology Backup" --cron "0 3 * * *" --tz "America/Los_Angeles" --agent main --message "exec bash ~/.openclaw/workspace/skills/synology-backup/scripts/backup.sh && exec bash ~/.openclaw/workspace/skills/synology-backup/scripts/verify.sh. Reply NO_REPLY."`

## Configuration

```json
{
  "host": "100.x.x.x",
  "share": "backups/openclaw",
  "mountPoint": "/mnt/synology",
  "credentialsFile": "~/.openclaw/.smb-credentials",
  "smbVersion": "3.0",
  "transport": "smb",
  "telegramTarget": "",
  "notifyOnSuccess": false,
  "backupPaths": [
    "~/.openclaw/workspace",
    "~/.openclaw/openclaw.json",
    "~/.openclaw/cron",
    "~/.openclaw/agents"
  ],
  "backupExclude": [],
  "includeSubAgentWorkspaces": true,
  "retention": 7,
  "preRestoreRetention": 3
}
```

For SSH transport, replace `"transport": "smb"` with `"transport": "ssh"` and add `sshUser`, `sshHost`, `sshPort`, `sshDest`.

## Requirements

- Synology NAS with SMB share (or SSH access)
- OpenClaw installed
- `cifs-utils` and `rsync` (`apt-get install -y cifs-utils rsync`)
- Tailscale (optional, recommended for remote backup)

## Security

- Credentials stored in a dedicated file with `chmod 600`, never inline
- All config values validated before use — no shell injection possible
- Restore uses an explicit allowlist of safe paths — no arbitrary writes
- Pre-restore safety snapshots automatically pruned after `preRestoreRetention` days
- Default exclusions prevent backing up `.git/`, `node_modules/`, temp files

## License

MIT

## Links

- [ClawHub](https://clawhub.ai/pfrederiksen/synology-backup)
- [OpenClaw](https://openclaw.ai)
- [SKILL.md](./SKILL.md) — full configuration reference
