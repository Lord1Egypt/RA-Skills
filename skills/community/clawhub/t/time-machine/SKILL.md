---
name: time-machine
description: Git-style incremental snapshots and instant rollback for OpenClaw. Use when user needs to: (1) Create manual snapshots (save, backup, snapshot, 时光机), (2) List existing backups, (3) Rollback to a previous state, (4) Auto-snapshot before dangerous changes, (5) Configure scheduled backups with retention policies.
---

# ⏰ Time Machine

> Git-style version control for your OpenClaw configuration. Backup, rollback, restore confidence.

## Why Time Machine?

Ever made a config change and broken everything? Yeah, we all have.

Time Machine automatically snapshots your OpenClaw workspace—so you can roll back instantly when things go wrong. Think of it as Git for your assistant's brain.

## Quick Start

```bash
# Create a snapshot
/snap save

# See all snapshots
/snap list

# Rollback to previous version
/snap rollback

# Rollback to specific version
/snap rollback v15

# See what's in a snapshot
/snap view v15
```

## What Gets Backed Up?

**Core Configs:**
- `openclaw.json` - Main configuration
- `config.yaml` - System config
- `agents/*.json` - Agent definitions
- `channels/*` - Channel setups
- `skills/*` - Skill configurations
- `credentials/*` - Secrets (encrypted)
- `.env` - Environment variables

**Your Memory:**
- `MEMORY.md` - Long-term memory
- `memory/*.md` - Daily notes

## How It Works

### Incremental Snapshots

First snapshot = full backup (all files)
Later snapshots = only changed files (patches)

```
v1_full/    → Complete copy of everything
v2_inc/     → Only what changed since v1
v3_inc/     → Only what changed since v2
```

**Result:** Fast, lightweight backups that save disk space.

### Smart Recovery

When you rollback:
1. Load the last full snapshot
2. Apply each incremental patch in order
3. Done ✓

## Commands

### `/snap save`
Create snapshot. Triggers: "save snapshot", "backup now", "create backup", "保存快照"

### `/snap list`
Show all snapshots with timestamps. Triggers: "list snapshots", "show backups", "查看快照"

### `/snap view vX`
Preview what's in a snapshot. Triggers: "view snapshot", "show backup details"

### `/snap rollback`
Rollback to previous version. Shows preview first, asks for confirmation.

Variants:
- `rollback v15` - Go to specific version
- `rollback --only memory` - Restore only memory files
- `rollback --only config` - Restore only config files
- `rollback openclaw.json to v10` - Single file restore

### `/snap delete vX`
Delete a snapshot. Triggers: "delete snapshot", "remove backup"

## Auto-Snapshot

Enable automatic backups in `openclaw.json`:

```json
{
  "timeMachine": {
    "enabled": true,
    "autoSnapshot": {
      "onChange": true,
      "schedule": "0 3 * * *",
      "retentionDays": 7,
      "maxCount": 50
    }
  }
}
```

- `onChange`: Create snapshot before risky config changes
- `schedule`: Cron job for automatic backups (default: 3 AM daily)
- `retentionDays`: Auto-delete backups older than X days
- `maxCount`: Keep only last X snapshots

## Danger Zone Protection

When user tries to modify critical config files, Time Machine prompts:

> "⏰ Create a snapshot before making changes?"

This gives you a safe restore point—automatically.

## Output Examples

### Snapshot Created
```
✅ Created snapshot v15_inc (incremental)
📝 Based on v10_full
📁 Changed: openclaw.json, channels/telegram.json
💾 Saved: Only 2 patches (2.3KB)
```

### Rollback Preview
```
⚠️ About to rollback to v14_inc
📄 Will restore: openclaw.json
❓ Confirm? (yes/no)
```

### Rollback Complete
```
✅ Rolled back to v14_inc
📦 Auto-created v15 as rollback point
```

## Edge Cases

- **First use:** Auto-creates initial full snapshot
- **Corrupted snapshot:** Skips bad ones, restores from last valid
- **Disk full:** Warns user, pauses creation, keeps existing
- **Single file:** Supports partial rollback (one file)

## Scripts

Python scripts in `scripts/`:
- `snapshot.py` - Create snapshots
- `restore.py` - Restore from snapshots  
- `list.py` - List all snapshots
- `cleanup.py` - Auto-cleanup old snapshots

Run: `python scripts/snapshot.py`, etc.

---

**TL;DR:** Install Time Machine, forget about config disasters. Your assistant has your back.
