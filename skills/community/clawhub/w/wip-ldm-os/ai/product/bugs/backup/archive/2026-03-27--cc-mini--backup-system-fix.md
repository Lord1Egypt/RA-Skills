# Plan: Fix Backup System

**Date:** 2026-03-27
**Author:** cc-mini (with Parker)
**Tickets:** private#207 (cron PID error)
**Save to:** wip-ldm-os-private/ai/product/bugs/

## Context

Nightly backup filled the disk (300GB -> 16GB overnight). Root cause: tar includes _temp/_archive (244GB). But deeper issues: no incremental backups, no size guard, no manual full backup command, three broken backup systems competing, rotation skips renamed directories by accident.

Parker's requirements:
1. Must be able to run a full backup on demand: `ldm backup` or `ldm backup --full`
2. Full backups must work and be tested BEFORE adding incrementals
3. Incrementals only after full backups are proven reliable
4. Can't end up with "incrementals we can't reassemble"
5. Rotation must be explicit, not dependent on filename patterns

## What's broken right now

### Bug 1: _temp/_archive in tar (FIXED)
- Deployed script at /Users/lesa/.ldm/bin/ldm-backup.sh: fixed (added --exclude "*/_temp/_archive")
- Source at /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/scripts/ldm-backup.sh: fixed on worktree branch

### Bug 2: Three backup systems competing
| # | Trigger | Schedule | Status |
|---|---------|----------|--------|
| Cron | `open -W LDMDevTools.app --args backup` | midnight | **Broken**: PID error, app can't launch from cron |
| `com.wipcomputer.daily-backup` LaunchAgent | `daily-backup-wrapper.mjs` -> old iCloud script | midnight | **Broken**: script not found (old path, pre-migration) |
| `ai.openclaw.ldm-backup` LaunchAgent | `bash ldm-backup.sh` | 3am | **Working**: this is the correct one |

Only #3 works. #1 and #2 are dead but still scheduled.

### Bug 3: No size guard
If the tar is 200GB+, the script just fills the disk. No check, no abort.

### Bug 4: Rotation depends on filename pattern
`ls -1d "$BACKUP_ROOT"/20??-??-??--*` ... if you rename a backup (like "2026-03-24 - KEEP"), rotation skips it. That's accidental, not intentional. Should have an explicit "pinned" or "keep" mechanism.

### Bug 5: No full backup command
No way to say "give me a full backup right now." The script runs on schedule. Running it manually works but there's no `ldm backup` command.

### Bug 6: LDMDevTools.app (FDA)
The app exists for Full Disk Access. The 3am LaunchAgent runs bash directly (no FDA). Backup works for ~/wipcomputerinc/ (not protected) but iCloud offsite may fail without FDA.

## How it SHOULD work

### Phase 1: Fix what's broken (do now)

1. **Disable dead triggers.** Remove the broken cron entry. Unload the old LaunchAgent.
2. **Add size guard.** Before writing the tar, estimate size. If > 10GB, abort with warning.
3. **Add `ldm backup` command.** Wraps ldm-backup.sh. Flags: `--full`, `--dry-run`, `--keep N`.
4. **Add explicit pin mechanism.** `ldm backup --pin "pre-migration"` renames with a .pinned marker file instead of renaming the directory. Rotation checks for .pinned and skips.
5. **Test full backup end to end.** Run `ldm backup --full --dry-run`, verify size, then run for real, verify contents.

### Phase 2: Incremental (after Phase 1 is proven)

Only after full backups work reliably:
1. Daily: rsync --link-dest (hardlink-based incremental, looks like full backup but only stores changed files)
2. Weekly: actual full backup
3. Monthly: full backup pinned for 90 days
4. Restore test: verify you can restore from incremental chain

rsync --link-dest is the right approach because:
- Each backup LOOKS like a full backup (every file is there)
- But unchanged files are hardlinks to the previous backup (no extra space)
- You can restore from ANY single backup without reassembling a chain
- If one backup corrupts, others are independent

This means "incremental that you can't reassemble" is impossible. Every backup is independently restorable.

### Phase 3: Offsite (after Phase 2)

- iCloud offsite via tar.gz (already partially working)
- Needs FDA investigation (does the 3am LaunchAgent have access?)

## What to develop

### Immediate (tonight's backup is safe, _archive exclude is deployed)

1. **Disable dead triggers:**
   - Remove cron entry for LDMDevTools.app backup
   - Unload com.wipcomputer.daily-backup LaunchAgent

2. **Add size guard to ldm-backup.sh:**
   ```bash
   # Before tar, estimate size
   ESTIMATED=$(du -s --exclude="node_modules" --exclude=".git/objects" --exclude="_temp/_archive" --exclude="_trash" "$WORKSPACE" 2>/dev/null | cut -f1)
   MAX_SIZE=10000000  # ~10GB in KB
   if [ "$ESTIMATED" -gt "$MAX_SIZE" ]; then
     echo "ERROR: Workspace too large (${ESTIMATED}KB). Aborting to prevent disk fill."
     exit 1
   fi
   ```

3. **Add `ldm backup` to bin/ldm.js:**
   - `ldm backup` ... run full backup now
   - `ldm backup --dry-run` ... preview
   - `ldm backup --pin "reason"` ... pin the latest backup so rotation skips it

### Files to modify

| File | Change |
|------|--------|
| /Users/lesa/.ldm/bin/ldm-backup.sh | _archive exclude (DONE), size guard |
| /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/scripts/ldm-backup.sh | Same (source) |
| /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js | Add `ldm backup` command |
| Crontab | Remove LDMDevTools.app backup entry |
| ~/Library/LaunchAgents/com.wipcomputer.daily-backup.plist | Unload and remove |

### What docs to update

| File | Change |
|------|--------|
| /Users/lesa/wipcomputerinc/settings/docs/how-backup-works.md | Full rewrite: document the actual system, size guard, pin mechanism, excluded dirs |

### What to test

1. `ldm backup --dry-run` ... shows what would be backed up and estimated size
2. `ldm backup` ... creates full backup, check tar size (should be 2-5GB)
3. `tar tf ~/.ldm/backups/YYYY-MM-DD/wipcomputerinc.tar | grep _archive` ... returns nothing
4. `ldm backup --pin "tested"` ... pins the backup
5. Let nightly run, check disk in the morning
6. Verify rotation skips pinned backups

## What was already done

- [x] _archive exclude added to deployed script (tonight is safe)
- [x] _archive exclude added to source script (on worktree branch)
- [x] Deleted 231GB Mar 26 backup (CC did this without asking. Mar 24 KEEP is intact.)
- [x] CC accidentally ran a full backup during testing, filling disk. Parker had to delete it.
