# Release Notes: wip-ldm-os v0.4.58

Backup system fixes. New `ldm backup` command.

## What changed

- `ldm backup` command: run backups on demand (--dry-run, --pin)
- `ldm backup --pin "reason"`: mark a backup so rotation never deletes it
- Size guard: backup aborts if workspace tar would exceed 10GB
- Backup excludes _temp/_archive (was creating 219GB tars overnight)
- Rotation respects .pinned marker files
- Disabled broken cron entry (LDMDevTools.app PID error)
- Disabled old LaunchAgent (com.wipcomputer.daily-backup, pointed to deleted iCloud path)

## Why

Parker went to bed with 300GB free, woke up with 16GB. The backup was tarring 244GB of pre-migration archives every night. Three backup systems were competing (cron, old LaunchAgent, new LaunchAgent). Only one worked. No way to run a backup on demand. No way to protect important backups from rotation.

## Issues closed

- #233 (backup tar includes _archive)
- #234 (backup system overhaul, Phase 1)

## How to verify

```bash
ldm backup --dry-run     # preview backup
ldm backup               # run full backup
ldm backup --pin "safe"  # pin it
ldm status               # check disk
```
