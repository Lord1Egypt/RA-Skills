---
name: trash-manager
version: 1.0.0
description: Trash management with index tracking for all agents. Use when deleting files to ensure proper index registration and 7-day auto-cleanup.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
---

# Trash Manager 🗑️

Trash management with index tracking. All agents must use this for file deletion — no bare `rm` or `mv` to trash.

## Core Rule

**Always move files to trash and update the index before "deleting" anything.**

```
Bare rm = forbidden ❌
mv ~/.openclaw/trash/ = forbidden ❌ (no index)
trash-manager.sh add <file> = correct ✅
```

## Workflow

```
User/Agent requests file deletion
    ↓
Check if file is truly no longer needed
    ↓
Call trash-manager.sh add <file>
    ↓
Auto: moves to ~/.openclaw/trash/ + updates index.json
    ↓
Auto-clean: files in trash >7 days cleared every Monday 3 AM
```

## Index File

- Path: `~/.openclaw/trash/index.json`
- Fields:
  - `original_path`: original file path
  - `trashed_path`: actual path inside trash
  - `trashed_at`: timestamp in seconds when trashed
  - `filename`: file name

## Commands

### `trash-manager.sh add <file>`
Move to trash and update index. **All deletion operations must use this.**

```bash
# Example
~/.openclaw/scripts/trash-manager.sh add /path/to/unused-file.txt
~/.openclaw/scripts/trash-manager.sh add ~/.openclaw/workspace/tmp/old.log
```

### `trash-manager.sh clean`
Clean files in trash older than 7 days (triggered by cron on Mondays).

```bash
# Dry run (does not actually delete)
~/.openclaw/scripts/trash-manager.sh clean --dry-run

# Actual cleanup
~/.openclaw/scripts/trash-manager.sh clean
```

### `trash-manager.sh list`
List all files in the index.

```bash
~/.openclaw/scripts/trash-manager.sh list
```

### `trash-manager.sh restore <original_path>`
Restore a file from trash.

```bash
~/.openclaw/scripts/trash-manager.sh restore /path/to/file
```

## Restore Flow

If the user changes their mind:
1. Run `trash-manager.sh list` to find the file
2. Run `trash-manager.sh restore <original_path>` to restore
3. The entry is removed from index, file returns to original path

## Other Agents

All agents share the same trash and index. Use `trash-manager.sh add` for all deletions and `trash-manager.sh restore` for all restorations.

**Note**: Trash is shared. File paths are unique, so no cross-agent conflicts. Cleanup is based on `trashed_at` time, regardless of which agent deleted the file.

## Constraints

- Retention: 7 days (based on `trashed_at`, not file mtime)
- Conflicts: same-name files get a numeric prefix
- Irreversible: once auto-cleaned, files are permanently gone

## Recommended Cron Setup

Recommended cron for automatic trash cleanup:

```json
{
  "name": "Weekly Trash Cleanup",
  "schedule": { "kind": "cron", "expr": "0 3 * * 1", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "Please execute the cleanup task:\n\n1. Run /home/node/.openclaw/scripts/trash-manager.sh clean to remove files trashed more than 7 days ago\n2. Check /home/node/.openclaw/logs/trash-clean.log for cleanup results\n3. Reply with \"Trash cleanup done\" listing how many files were removed",
    "timeoutSeconds": 60
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "user:ou_YOUR_OPEN_ID"
  },
  "sessionTarget": "isolated"
}
```

Key points:
- Use `agentTurn` + `sessionTarget: "isolated"` to run in an isolated session without interrupting the main conversation
- Use `announce` delivery mode to push results to Feishu
- Cleanup is based on `trashed_at` in the index, not file mtime

## Related Files

- Script: `~/.openclaw/scripts/trash-manager.sh`
- Index: `~/.openclaw/trash/index.json`
- Cron: Runs clean every Monday 3 AM