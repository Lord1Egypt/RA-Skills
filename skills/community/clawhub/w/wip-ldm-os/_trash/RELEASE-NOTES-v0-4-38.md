# Release Notes: wip-ldm-os v0.4.38

## Unified Backup System (#119)

One script replaces three competing backup systems.

**`~/.ldm/bin/ldm-backup.sh`** backs up everything:
- `~/.ldm/` (crystal.db via sqlite3 .backup, agents, state, config)
- `~/.openclaw/` (main.sqlite, context-embeddings, workspace, sessions)
- `~/.claude/` (CLAUDE.md, settings.json, projects)
- Entire workspace (excludes node_modules, .git/objects, old backups, _trash)

iCloud offsite: compresses the backup to a single .tar.gz and copies to iCloud. One file per backup. Rotates to 7 days.

**`~/.ldm/bin/ldm-restore.sh`** restores from local or iCloud:
- `ldm-restore.sh` ... list available backups
- `ldm-restore.sh <backup>` ... restore everything
- `ldm-restore.sh --only ldm <backup>` ... restore just crystal.db + agents
- `ldm-restore.sh --from-icloud <file>` ... restore from iCloud tar
- `ldm-restore.sh --dry-run <backup>` ... preview

**`ldm install`** now deploys both scripts to `~/.ldm/bin/`.

Timestamps use `YYYY-MM-DD--HH-MM-SS` format so backups can run multiple times per day.

## What it replaces

- Lesa's `daily-backup.sh` (was broken, pointed to deleted iCloud path)
- Old `ldm-backup.sh` (only covered ~/.ldm/)
- Separate `verify-backup.sh` (verification built into the new script)
