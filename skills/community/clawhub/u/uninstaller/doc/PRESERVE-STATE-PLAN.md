# Plan: Selective Preservation of ~/.openclaw for Reinstall Inheritance

## Context

**Previous approach (reverted):** backup create → move/copy to ~/.openclaw-backup-* → install detects backup → restore.  
**New approach:** Don't delete ~/.openclaw during uninstall when user intends to reinstall. State stays in place; reinstall inherits it automatically.

## Principle

- **Inheritance over restore:** If ~/.openclaw is preserved, reinstall needs no restore step.
- **Simpler flow:** No backup archive, no restore CLI, no install.sh detection logic.
- **User choice:** Add `--preserve-state` to uninstall for "I'm reinstalling soon" scenarios.

## Current Uninstall Flow (uninstall-oneshot.sh)

1. (optional) Backup: `openclaw backup create` or manual cp → ~/.openclaw-backup-YYYYMMDD-HHMMSS
2. Stop gateway
3. **Delete** ~/.openclaw (rm -rf)
4. Remove CLI, macOS app, etc.

## Proposed Change

### New flag: `--preserve-state`

| Flag | Backup | Delete state dir |
|------|--------|------------------|
| (default) | Yes | Yes |
| `--no-backup` | No | Yes |
| `--preserve-state` | No | **No** |

**When `--preserve-state`:**
- Skip backup (no point — we're not deleting)
- Skip deletion of ~/.openclaw
- Still: stop gateway, remove CLI, remove macOS app
- Result: ~/.openclaw remains. Reinstall uses it as-is.

### Implementation (openclaw-uninstall)

**File:** `scripts/uninstall-oneshot.sh`

1. Add `PRESERVE_STATE=false` and `--preserve-state` arg.
2. When `PRESERVE_STATE=true`:
   - Skip backup block (lines 71–99)
   - Skip state dir deletion (lines 144–147)
   - Log: "State preserved at $STATE_DIR for reinstall inheritance"
3. Update `schedule-uninstall.sh` to pass through `--preserve-state`.
4. Update AGENTS.md with new flag.

### Install Script (openclaw)

**No change needed.** Install script installs the binary; it does not touch ~/.openclaw. When the new binary runs, it uses existing ~/.openclaw if present. No restore flow required.

### Documentation

- Add `--preserve-state` to uninstall usage docs.
- Document: "Use when reinstalling: uninstall preserves state, reinstall inherits it."

## Checklist

- [ ] openclaw-uninstall: Add `--preserve-state` to uninstall-oneshot.sh
- [ ] openclaw-uninstall: Update schedule-uninstall.sh to pass flag
- [ ] openclaw-uninstall: Update AGENTS.md
- [ ] openclaw-uninstall: Add test for `--preserve-state` (state dir exists after run)
- [ ] docs: Add preserve-state usage to uninstall docs

## Reverted (already done)

- ~~backup restore CLI~~
- ~~backup-restore.ts infra~~
- ~~install.sh backup detection/restore flow~~
- ~~docs/install/backup-restore-during-install.md~~
