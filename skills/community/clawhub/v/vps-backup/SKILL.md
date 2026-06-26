---
name: vps-backup
description: Automated daily VPS backup using restic — backs up OpenClaw workspace, SSH keys, project code, and session transcripts. Configures encrypted incremental snapshots with retention policies and optional offsite push via rclone. Use when setting up a new VPS backup system, verifying existing backups, restoring files, or scheduling periodic automated backups.
---

# VPS Backup Skill

Automated daily backup for OpenClaw VPS deployments using [restic](https://restic.net) — encrypted, incremental, deduplicating snapshots with retention management and optional offsite push.

## What Gets Backed Up

| Path | Contents | Why |
|------|----------|-----|
| `~/.openclaw` | Workspace, memory, sessions, configs | Core agent state |
| `~/.config/opencode` | Agents, skills, OpenCode models | Agentic coding setup |
| `~/.ssh` | SSH keys | Access to all services |
| `~/.npm-global` | Global npm packages | Tools installed |
| `~/workspace/projects` | All project source code | Your work |
| Session transcripts | Exported via `export_sessions.py` | Human-readable chat history |

**Excluded** (reconstructable): `node_modules/`, `__pycache__/`, `*.pyc`, `*.log`, `tmp/`, `*.sqlite`, `.cache/`

## Setup

### 1. Install restic

```bash
# Linux (others: https://restic.net/install/)
curl -LO https://github.com/restic/restic/releases/latest/download/restic_linux_amd64.tar.gz
tar xzf restic_linux_amd64.tar.gz
sudo mv restic /usr/local/bin/
restic version
```

### 2. Install rclone (for offsite push — optional)

```bash
curl -LO https://downloads.rclone.org/rclone-current-linux-amd64.zip
unzip rclone-current-linux-amd64.zip
sudo cp rclone-linux-amd64/rclone /usr/local/bin/
rclone version
```

### 3. Configure the script

Edit the top config section of `scripts/vps-backup.sh`:

```bash
BACKUP_ROOT="/home/dev/backup/vps-daily"    # local backup root
BACKUP_PATHS=(                                    # what to back up
    "/home/dev/.openclaw"
    "/home/dev/.config/opencode"
    "/home/dev/.ssh"
    "/home/dev/.npm-global/lib/node_modules"
    "/workspace/projects"
)
SESSION_EXPORT="/home/dev/.openclaw/workspace/scripts/export_sessions.py"
```

### 4. Set encryption password

```bash
# Generate a strong password
openssl rand -base64 32 > ~/.backup-password
chmod 600 ~/.backup-password
```

### 5. (Optional) Configure rclone for offsite push

```bash
rclone config
# Follow prompts to add your cloud storage (Backblaze B2, Google Drive, etc.)
```

### 6. Schedule daily run

```bash
# Add to crontab (runs at 3am UTC daily)
0 3 * * * export BACKUP_PASSWORD=$(cat ~/.backup-password) && export PATH="$HOME/bin:$PATH" && bash /path/to/vps-backup.sh >> /var/log/vps-backup.log 2>&1
```

Or schedule via OpenClaw cron:

```
every: 24h | sessionTarget: isolated | model: glm-5
message: "Run: export BACKUP_PASSWORD=$(cat ~/.backup-password) && export PATH=\"$HOME/bin:$PATH\" && bash /home/dev/scripts/vps-backup.sh"
```

---

## Daily Usage

```bash
# Run backup manually
export BACKUP_PASSWORD=$(cat ~/.backup-password)
export PATH="$HOME/bin:$PATH"
bash /home/dev/scripts/vps-backup.sh

# Check snapshot count
export RESTIC_PASSWORD=$(cat ~/.backup-password)
export PATH="$HOME/bin:$PATH"
restic snapshots --repo /home/dev/backup/vps-daily/restic-repo

# Verify backup integrity
restic check --repo /home/dev/backup/vps-daily/restic-repo

# List repo size
du -sh /home/dev/backup/vps-daily/
```

---

## Restore

```bash
# Restore latest snapshot of a specific path
export RESTIC_PASSWORD=$(cat ~/.backup-password)
export PATH="$HOME/bin:$PATH"
restic restore latest \
  --repo /home/dev/backup/vps-daily/restic-repo \
  --target /tmp/restore \
  --path /home/dev/.openclaw

# List snapshots for a specific date
restic snapshots --repo /home/dev/backup/vps-daily/restic-repo \
  --tag date-2026-03-31

# Restore a specific snapshot by ID
restic restore abc123 \
  --repo /home/dev/backup/vps-daily/restic-repo \
  --target /tmp/restore
```

---

## Offsite Push

Set the `RCLONE_DEST` environment variable before running:

```bash
# Backblaze B2 example:
export RCLONE_DEST="b2:my-bucket/vps-backups"
export BACKUP_PASSWORD=$(cat ~/.backup-password)
export PATH="$HOME/bin:$PATH"
bash /home/dev/scripts/vps-backup.sh
# Output includes: "Offsite push done ✓"

# Google Drive:
export RCLONE_DEST="gcache:openclaw-backups"
```

The script automatically detects `rclone` and `RCLONE_DEST` and syncs after each backup.

---

## Retention Policy

| Level | Keep |
|-------|------|
| Daily | 7 |
| Weekly | 4 |
| Monthly | 6 |

Old snapshots are pruned automatically after each run.

---

## Health Check

The script checks for at least one snapshot in the last 26 hours. If missing, it logs a `HEALTH FAILED` error.

Add a monitoring check to your alerting:

```bash
# Alert if no recent backup
RECENT=$(RESTIC_PASSWORD=$(cat ~/.backup-password) restic snapshots \
  --repo /home/dev/backup/vps-daily/restic-repo \
  --json 2>/dev/null | python3 -c "
import sys,json,datetime
cutoff=datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=26)
print(sum(1 for s in json.load(sys.stdin)
  if datetime.datetime.fromisoformat(s['time'].replace('Z','+00:00'))>cutoff))
")
if [ "$RECENT" -eq 0 ]; then
  echo "ALERT: No backup in 26h!"
fi
```

---

## Files

- `scripts/vps-backup.sh` — the backup script
- `scripts/export_sessions.py` — session transcript exporter (optional but recommended)
- `docs/config.md` — environment variable reference
