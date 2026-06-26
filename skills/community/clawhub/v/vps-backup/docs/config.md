# VPS Backup — Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BACKUP_PASSWORD` | Yes* | — | Encryption password for restic repo. \*Or set via `~/.backup-password` file |
| `BACKUP_ROOT` | No | `/home/dev/backup/vps-daily` | Local root directory for backups |
| `RESTIC_REPO` | No | `$BACKUP_ROOT/restic-repo` | Path to the restic repository |
| `SESSION_EXPORT` | No | — | Path to `export_sessions.py` (session archiver script) |
| `RETENTION_DAILY` | No | `7` | Number of daily snapshots to keep |
| `RETENTION_WEEKLY` | No | `4` | Number of weekly snapshots to keep |
| `RETENTION_MONTHLY` | No | `6` | Number of monthly snapshots to keep |
| `RCLONE_DEST` | No | — | rclone remote for offsite push (e.g. `b2:bucket/path`) |

## Quick Setup Commands

```bash
# 1. Generate encryption password
openssl rand -base64 32 > ~/.backup-password
chmod 600 ~/.backup-password

# 2. Verify restic repo (after first backup)
export RESTIC_PASSWORD=$(cat ~/.backup-password)
restic check --repo /home/dev/backup/vps-daily/restic-repo

# 3. List all snapshots
restic snapshots --repo /home/dev/backup/vps-daily/restic-repo

# 4. Offsite push to Backblaze B2
export RCLONE_DEST="b2:my-bucket/vps-backups"
export BACKUP_PASSWORD=$(cat ~/.backup-password)
bash /path/to/vps-backup.sh

# 5. Change retention policy
export RETENTION_DAILY=14
export RETENTION_WEEKLY=8
export RETENTION_MONTHLY=12
bash /path/to/vps-backup.sh
```

## Adding the Session Archiver

Download `export_sessions.py` from:
https://github.com/codaire/openclaw-session-archiver

```bash
# Install the session archiver
curl -LO https://raw.githubusercontent.com/codaire/openclaw-session-archiver/main/export_sessions.py
chmod +x export_sessions.py

# Point to it in the backup script config:
SESSION_EXPORT="/home/dev/scripts/export_sessions.py"
```

Or integrate it into the backup cron line:

```bash
0 3 * * * \
  python3 /home/dev/scripts/export_sessions.py && \
  export BACKUP_PASSWORD=$(cat ~/.backup-password) && \
  bash /home/dev/scripts/vps-backup.sh \
  >> /var/log/vps-backup.log 2>&1
```
