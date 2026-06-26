# Backup: Technical Details

## Config Schema

All backup settings are in `~/.ldm/config.json`. The backup script reads these at runtime.

```json
{
  "org": "wipcomputerinc",
  "paths": {
    "workspace": "~/wipcomputerinc",
    "ldm": "~/.ldm",
    "claude": "~/.claude",
    "openclaw": "~/.openclaw",
    "icloudBackup": "~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputerinc-icloud/backups"
  },
  "backup": {
    "keep": 7,
    "includeSecrets": false
  }
}
```

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `paths.workspace` | string | required | Root workspace directory to back up |
| `paths.icloudBackup` | string | optional | iCloud destination for offsite copies |
| `backup.keep` | number | 7 | Days of backups to keep before rotation |
| `backup.includeSecrets` | boolean | false | Whether to include `~/.ldm/secrets/` |
| `org` | string | required | Used as prefix in iCloud tar filenames |

## Script Location

- **Source:** `scripts/ldm-backup.sh` in the wip-ldm-os-private repo
- **Deployed to:** `~/.ldm/bin/ldm-backup.sh`
- **Deployed by:** `deployScripts()` in `bin/ldm.js`, called during both `ldm init` and `ldm install`
- **Restore script:** `scripts/ldm-restore.sh` deployed to `~/.ldm/bin/ldm-restore.sh`

All `.sh` files in the repo's `scripts/` directory are deployed to `~/.ldm/bin/` on every `ldm install`. This means script fixes land automatically on the next update without requiring a full `ldm init`.

## LaunchAgent

**Label:** `ai.openclaw.ldm-backup`
**Plist source:** `shared/launchagents/ai.openclaw.ldm-backup.plist`
**Deployed to:** `~/Library/LaunchAgents/ai.openclaw.ldm-backup.plist`

```xml
<key>StartCalendarInterval</key>
<dict>
  <key>Hour</key>
  <integer>3</integer>
  <key>Minute</key>
  <integer>0</integer>
</dict>
```

The plist uses `{{HOME}}` placeholders that are replaced at deploy time by `ldm init`.

**Logs:** stdout and stderr both go to `~/.ldm/logs/backup.log`.

**No Full Disk Access (FDA):** The LaunchAgent runs at 3:00 AM without FDA. Some paths (like `~/Library/Messages/`) are inaccessible without FDA. The target is to move the trigger to midnight via LDMDevTools.app (which has FDA) once the PID error is resolved.

### Dead Triggers (Cleaned Automatically)

The `cleanDeadBackupTriggers()` function in `ldm.js` removes old competing triggers on every `ldm init`:
- Old cron entries referencing `LDMDevTools.app`
- `com.wipcomputer.daily-backup` LaunchAgent
- OpenClaw `backup-verify` cron entries

Only `ai.openclaw.ldm-backup` should exist.

## Rotation Logic

The backup script handles rotation after a successful backup:

1. List all dated directories in `~/.ldm/backups/` (format: `YYYY-MM-DD--HH-MM-SS`)
2. Sort by name (which sorts chronologically)
3. Skip any directory containing a `.pinned` marker file
4. Delete directories beyond the `keep` count (oldest first)
5. Same rotation logic applies to iCloud tars at `paths.icloudBackup`

**Pinning:** `ldm backup --pin "reason"` creates a `.pinned` file in the latest backup directory. Pinned backups are never rotated.

## iCloud Offsite Details

After the local backup completes:

1. Tar + gzip the entire dated backup directory
2. Filename format: `<org>-<machine>-<timestamp>.tar.gz`
3. Copy to `paths.icloudBackup` (from config.json)
4. Apply the same rotation (keep N, skip pinned)
5. iCloud syncs the file to all devices automatically

The iCloud path must exist. The script does not create it. `ldm init` does not create it either. Create it manually if it does not exist.

## SQLite Safety

SQLite files are backed up using `sqlite3 .backup`, not `cp`. This ensures a consistent snapshot even if the database is being written to. The script checks for the `sqlite3` binary and skips database backup with a warning if it is not found.

Files backed up this way:
- `~/.ldm/memory/crystal.db`
- `~/.openclaw/memory/main.sqlite`
- `~/.openclaw/memory/context-embeddings.sqlite`

## Excludes

The workspace tar excludes:
- `node_modules/` ... reconstructable via npm install
- `.git/objects/` ... reconstructable via git fetch
- `backups/` ... avoids recursive backup
- `_trash/` ... already deleted content
- `*.tar.gz` ... avoids backing up old backup archives
