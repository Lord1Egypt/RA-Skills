# Backup Master Plan

**Date:** 2026-03-31 (updated)
**Author:** cc-mini (with Parker)
**Consolidates:** 2026-03-18 unified backup + 2026-03-24 comprehensive fix + 2026-03-27 system fix
**Status:** MOSTLY DONE. Remaining: optional stale backup delete, LDMDevTools.app PID fix (future).

## Status update (Apr 1, evening)

All immediate fixes done:
- OpenClaw backup-verify cron: removed (was creating 23GB duplicate nightly). Done.
- Config updated with full backup section. Done.
- Library doc updated. Done.
- Repo docs created (docs/backup/). Done.
- Scripts deploy on every `ldm install`. Done.
- Dead triggers disabled. Done.
- Parker cleaned 102GB stale backups. Done.
- One backup trigger running (3 AM LaunchAgent). Correct.

Still open:
- Optional: delete `2026-03-30--07-30-04/` (23GB manual test). iCloud copy exists.
- Future: fix LDMDevTools.app PID error for midnight-via-app target.
- Future: Phase 2 incremental backups (rsync --link-dest).

## Status update (Apr 1, morning)

Parker manually cleaned up stale backups on Mar 30-31:
- Deleted `_archive/2026-03-21/` (79GB, pre-migration). Done.
- Deleted `2026-03-31--00-31-00/` (23GB, duplicate from OpenClaw cron). Moved to `_trash-rm-tool/`, then deleted. Done.
- `2026-03-30--07-30-04/` (23GB, manual test run) still exists. Optional delete. iCloud copy exists.

Net disk reclaimed: ~102GB.

## What works (Phase 1, completed Mar 27-30)

These are done and should not be touched:

- **Backup script** (`~/.ldm/bin/ldm-backup.sh`): backs up ~/.ldm/, ~/.openclaw/, ~/.claude/, ~/wipcomputerinc/. SQLite databases use sqlite3 .backup. Everything else uses cp or tar. Excludes node_modules, .git/objects, _temp/_archive, _trash.
- **`ldm backup` command**: --dry-run, --list, --pin, --unpin, --keep N. Working.
- **Pin mechanism**: .pinned marker file. Rotation skips pinned backups. Working.
- **Size guard**: estimates workspace size before tar. Aborts if > 10GB. Fixed for macOS (`du -I` not `--exclude`).
- **iCloud offsite**: tar.gz to `~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputerinc-icloud/backups/`. Tested and working (Mar 30).
- **Config reads from `~/.ldm/config.json`**: workspace path, iCloud backup path, keep days. Working.
- **Dead triggers disabled**: cron entries for LDMDevTools.app commented out. `com.wipcomputer.daily-backup` renamed to .disabled.
- **Hardcoded paths fixed**: backup script reads org name from config, not hardcoded "wipcomputerinc".

## What's broken

### 1. Two triggers still running (46GB per night)

| # | Trigger | Schedule | Status | What it does |
|---|---------|----------|--------|-------------|
| 1 | `ai.openclaw.ldm-backup` LaunchAgent | 3:00 AM | **Running** | Runs `bash ~/.ldm/bin/ldm-backup.sh` directly. No FDA. |
| 2 | OpenClaw `backup-verify` cron (ID: be68c256) | 00:30 | **Running** | Runs a FULL backup, not a verification. Creates duplicate 23GB backup every night. |
| 3 | macOS cron -> LDMDevTools.app | Midnight | Disabled | App can't launch from cron (PID error). |
| 4 | `com.wipcomputer.daily-backup` LaunchAgent | Midnight | Disabled | Old script, old path. Dead. |

### 2. Config doesn't describe the backup system

Current config:
```json
"backup": {
  "keep": 7,
  "includeSecrets": false
}
```

Missing: schedule, trigger method, trigger label, script path, iCloud on/off, iCloud path, max size, FDA method.

### 3. Library doc doesn't match reality

`~/wipcomputerinc/library/documentation/how-backup-works.md` says: "midnight via cron -> LDM Dev Tools.app." Reality: 3 AM via LaunchAgent + 00:30 via OpenClaw cron.

### 4. No repo docs for backup

`wip-ldm-os-private/docs/backup/` doesn't exist. Every other component has docs (bridge, recall, total-recall, skills, universal-installer). Backup doesn't.

### 5. Stale backups eating disk (~23GB reclaimable)

| Backup | Size | Status |
|--------|------|--------|
| ~~`_archive/2026-03-21/`~~ | ~~79GB~~ | Deleted by Parker (Mar 31). |
| `_archive/2026-03-24 - KEEP/` | 28GB | Keep. Last pre-new-system backup. |
| `2026-03-27--00-00-00/` (pinned) | 6.6GB | Keep. Incomplete but small. |
| `2026-03-28--01-00-04/` | 23GB | Keep. |
| `2026-03-29--01-00-05/` | 23GB | Keep. |
| `2026-03-30--01-00-04/` | 23GB | Keep. |
| `2026-03-30--07-30-04/` | 23GB | Manual test run. Optional delete. iCloud copy exists. |
| ~~`2026-03-31--00-31-00/`~~ | ~~23GB~~ | Deleted by Parker (Mar 31). Moved to _trash-rm-tool. |
| `2026-03-31--01-00-05/` | 23GB | Keep. Tonight's real backup. |

## The target architecture

### Three apps

1. **LDMDevTools.app** (macOS): Full Disk Access wrapper. Runs scheduled jobs (backup, branch protect, crystal capture). The FDA "elevator" that gives scripts access to protected files. Already exists but can't launch from cron (PID error).

2. **LDM OS Mac app** (macOS, future): settings UI, agent dashboard, pairing, local MCP server. The desktop equivalent of the iOS app.

3. **LDM OS iOS app** (Lesa App, future): Core partner. Pairing, payments, MCP for mobile AI apps, crystal mirror.

The FDA app (#1) is separate because FDA is a security privilege. Backup runs through it. Everything else runs through #2 and #3.

### ONE backup trigger

**Target:** LDMDevTools.app at midnight via LaunchAgent.

**Current (interim):** `ai.openclaw.ldm-backup` LaunchAgent at 3:00 AM running bash directly (no FDA). This works for everything except potentially iCloud-protected paths. iCloud offsite IS working without FDA (tested Mar 30). So this is acceptable until the app is fixed.

**To reach target:**
1. Fix the PID error when launching LDMDevTools.app from a LaunchAgent
2. Create `ai.ldm.backup` LaunchAgent at midnight pointing to the app
3. Remove `ai.openclaw.ldm-backup` (the 3 AM one)

**Fallback if app can't be fixed:** Add Terminal.app or bash to FDA allowlist in System Preferences. The LaunchAgent runs bash directly and still gets FDA.

### Config describes everything

Target `~/.ldm/config.json` backup section:

```json
"backup": {
  "keep": 7,
  "includeSecrets": false,
  "schedule": "03:00",
  "trigger": "launchagent",
  "triggerLabel": "ai.openclaw.ldm-backup",
  "script": "~/.ldm/bin/ldm-backup.sh",
  "icloudOffsite": true,
  "icloudPath": "~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputerinc-icloud/backups",
  "maxSizeGB": 10,
  "fda": false,
  "fdaTarget": "LDMDevTools.app"
}
```

Note: `schedule` and `triggerLabel` reflect CURRENT state (3 AM, openclaw label). When the app is fixed, these change to `"00:00"` and `"ai.ldm.backup"` and `fda` becomes `true`.

## Steps to execute (in order)

### Immediate (CC does, no releases needed)

1. **Remove OpenClaw backup-verify cron.** `openclaw cron remove be68c256-ca61-4437-b3ca-bcb2591b9bdd`. Stops the duplicate 00:30 backup.

2. **Update config.json backup section.** Add the full config above to `~/.ldm/config.json`.

3. **Tell Parker which backups to delete.** Parker runs rm commands:
   - ~~`rm -rf ~/.ldm/backups/_archive/2026-03-21` (79GB, pre-migration)~~ Done (Mar 31).
   - ~~`rm -rf ~/.ldm/backups/2026-03-31--00-31-00` (23GB, duplicate)~~ Done (Mar 31, via _trash-rm-tool).
   - Optional: `rm -rf ~/.ldm/backups/2026-03-30--07-30-04` (23GB, manual test)

### Repo work (CC does, needs worktree + PR)

4. **Create `docs/backup/` in wip-ldm-os-private.** README.md (user-facing) + TECHNICAL.md (reference). Source of truth for backup documentation.

5. **Update library doc.** `how-backup-works.md` needs to match reality. Update schedule, trigger, config section. Note the FDA status.

6. **Update `ldm doctor`** to verify backup config (LaunchAgent loaded, last backup < 24h, iCloud path accessible).

### Future (separate tickets)

7. **Fix LDMDevTools.app PID error.** Investigate why `open -W` fails from cron/LaunchAgent. Test alternative launch methods. This unblocks the midnight-via-app target.

8. **Phase 2: Incremental backups.** rsync --link-dest. Each backup looks full but only stores changes. Parker's requirement: don't start until Phase 1 is proven reliable. Phase 1 is proven. Phase 2 is next.

9. **Phase 3: Offsite improvements.** FDA investigation for iCloud-protected files. Compression improvements (main.sqlite is 16GB, dominates backup size).

## What gets backed up (reference)

| Source | Method | What's in it |
|--------|--------|-------------|
| `~/.ldm/memory/crystal.db` | sqlite3 .backup | Memory Crystal (82K+ chunks) |
| `~/.ldm/agents/` | cp -a | Identity, journals, daily logs |
| `~/.ldm/state/` | cp -a | Config, version, registry |
| `~/.ldm/config.json` | cp | Workspace pointer, org |
| `~/.openclaw/memory/main.sqlite` | sqlite3 .backup | OC conversations (16GB) |
| `~/.openclaw/memory/context-embeddings.sqlite` | sqlite3 .backup | Embeddings (127MB) |
| `~/.openclaw/workspace/` | tar | Shared context, daily logs |
| `~/.openclaw/agents/main/sessions/` | tar | OC session JSONL |
| `~/.openclaw/openclaw.json` | cp | OC config |
| `~/.claude/CLAUDE.md` | cp | CC instructions |
| `~/.claude/settings.json` | cp | CC settings |
| `~/.claude/projects/` | tar | CC auto-memory + transcripts |
| `~/wipcomputerinc/` | tar (excludes node_modules, .git/objects, _temp/_archive, _trash) | Entire workspace |

**NOT backed up:** node_modules, .git/objects (reconstructable), extensions (reinstallable), ~/.claude/cache.

## Previous docs (superseded)

- `backup/2026-03-18--unified-backup-system.md` ... first plan. Designed the backup structure. Much of this was implemented.
- `plans-prds/current/2026-03-24--cc-mini--comprehensive-backup-fix.md` ... detailed plan. Correct direction (midnight via app). Implementation diverged when app broke.
- `backup/2026-03-27--cc-mini--backup-system-fix.md` ... Phase 1 execution. Fixed 5 of 6 bugs. Missed OpenClaw cron. Didn't update config.
