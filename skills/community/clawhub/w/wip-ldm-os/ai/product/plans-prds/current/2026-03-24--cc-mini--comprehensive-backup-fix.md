# Plan: Comprehensive Backup Fix + Installer Integration

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Issue:** #119

## Context

Three backup systems running with no coordination. Lesa's script points to a deleted iCloud path (broken tonight). LDM's script only covers ~/.ldm/. Nobody tars to iCloud for offsite. Scripts live in random locations (Lesa's repos, memory-crystal repo, .openclaw/scripts). The installer doesn't handle any of this.

## Current State (broken)

| System | Script | Where it lives | Schedule | Destination | Problem |
|--------|--------|----------------|----------|-------------|---------|
| Lesa's backup | daily-backup.sh | `staff/Lēsa/scripts/` | Midnight (cron -> LDM Dev Tools.app) | Old iCloud path (DELETED) | **BROKEN** |
| LDM backup | ldm-backup.sh | `~/.ldm/bin/` (deployed by crystal init) | 3 AM (LaunchAgent) | `~/.ldm/backups/` | Only covers ~/.ldm/ |
| Verify | verify-backup.sh | `~/.openclaw/scripts/` | 00:30 (cron) | N/A | Checking wrong path |

## The Fix (one script, one place, one command)

### Where scripts live

**`~/.ldm/bin/`** ... runtime scripts. Managed by `ldm install`. Not in staff dirs, not in repos, not in .openclaw.

```
~/.ldm/bin/
  ldm-backup.sh      <- THE backup script (replaces both Lesa's and the old ldm-backup.sh)
  crystal-capture.sh  <- already here
  process-monitor.sh  <- already here
```

Source of truth for the script: `wip-ldm-os-private/scripts/ldm-backup.sh`. `ldm install` deploys it to `~/.ldm/bin/`.

Config for backup: `~/.ldm/config.json` (workspace path) + `~/wipcomputerinc/settings/config.json` (backup section: keep, includeSecrets, icloudBackup path).

### What the unified script backs up

Merge Lesa's comprehensive list with LDM's sqlite3 .backup safety:

| Source | Method | Why |
|--------|--------|-----|
| `~/.ldm/memory/crystal.db` | sqlite3 .backup | Irreplaceable memory |
| `~/.ldm/agents/` | cp -a | Identity, journals, daily logs |
| `~/.ldm/state/` | cp -a | Config, version, registry |
| `~/.ldm/config.json` | cp | Workspace pointer, org |
| `~/.openclaw/memory/main.sqlite` | sqlite3 .backup | OC conversations (21 GB) |
| `~/.openclaw/memory/context-embeddings.sqlite` | sqlite3 .backup | Embeddings |
| `~/.openclaw/workspace/` | tar | Shared context, daily logs |
| `~/.openclaw/openclaw.json` | cp | OC config |
| `~/.openclaw/agents/main/sessions/` | tar | OC session JSONL |
| `~/.claude/CLAUDE.md` | cp | CC instructions |
| `~/.claude/settings.json` | cp | CC settings |
| `~/.claude/projects/` | tar | CC auto-memory + transcripts |
| `~/wipcomputerinc/` | tar (exclude node_modules, .git objects) | Entire workspace: settings, staff, repos (ai/ folders, uncommitted work), _sort, _temp, _transfer, _trash |

NOT backed up: `node_modules/` dirs, `.git/objects/` (reconstructable from remote), extensions (reinstallable), `~/.claude/cache`.

### Backup structure

```
~/.ldm/backups/
  2026-03-24/                    <- date folder
    ldm/                         <- ~/.ldm/ data
      memory/crystal.db
      agents/
      state/
      config.json
    openclaw/                    <- ~/.openclaw/ data
      memory/main.sqlite
      memory/context-embeddings.sqlite
      workspace.tar
      sessions.tar
      openclaw.json
    claude/                      <- ~/.claude/ data
      CLAUDE.md
      settings.json
      projects.tar
    wipcomputerinc.tar           <- entire workspace (excludes node_modules, .git/objects)
```

### iCloud offsite

After local backup, tar the day's folder and copy to iCloud:

```bash
tar -czf "${ICLOUD_BACKUP}/wipcomputerinc-mac-mini-${DATE}.tar.gz" -C ~/.ldm/backups "$DATE"
```

Destination: `~/Library/Mobile Documents/com~apple~CloudDocs/wipcomputerinc-icloud/backups/`

Rotate to keep days (from config.json backup.keep).

### One schedule, one entry point

| What | How | When |
|------|-----|------|
| Backup | `~/.ldm/bin/ldm-backup.sh` | Midnight via cron -> LDM Dev Tools.app |
| Verify | Built into ldm-backup.sh (exit code + log) | End of backup |

Kill the LaunchAgent (`ai.openclaw.ldm-backup`). Kill the separate verify cron. One cron entry, one script, one app.

## Implementation

### Phase 1: Write the unified script

**File:** `wip-ldm-os-private/scripts/ldm-backup.sh`

Merge the two scripts. Use sqlite3 .backup for all databases. Read icloudBackup path from `~/.ldm/config.json` -> workspace -> `settings/config.json`. Tar to iCloud after local backup completes.

### Phase 2: Add to ldm install

**File:** `wip-ldm-os-private/bin/ldm.js`

`ldm install` deploys `scripts/ldm-backup.sh` to `~/.ldm/bin/ldm-backup.sh`. Same pattern as crystal-capture.sh and process-monitor.sh.

### Phase 3: Update LDM Dev Tools.app

**File:** `~/Applications/LDMDevTools.app/Contents/Resources/jobs/backup.sh`

Point to `~/.ldm/bin/ldm-backup.sh` instead of Lesa's script:

```bash
#!/bin/bash
exec /bin/bash "$HOME/.ldm/bin/ldm-backup.sh" 2>&1
```

### Phase 4: Update cron

Replace the three cron entries (backup, verify, ldm-backup LaunchAgent) with one:

```
0 0 * * * open -W ~/Applications/LDMDevTools.app --args backup >> ~/.ldm/logs/cron.log 2>&1
```

Remove:
- `ai.openclaw.ldm-backup` LaunchAgent (3 AM, redundant)
- `com.wipcomputer.daily-backup` LaunchAgent (if exists)
- Verify cron entry (built into the script now)

### Phase 5: Retire old scripts

- `staff/Lēsa/scripts/daily-backup.sh` -> add deprecation notice, point to ldm-backup.sh
- `~/.openclaw/scripts/verify-backup.sh` -> delete (built into unified script)
- Old `~/.ldm/bin/ldm-backup.sh` -> replaced by new version

### Phase 6: Clean up old backup dirs

- `~/wipcomputerinc/_temp/backups/` (166 GB) -> delete after unified backup is proven (keep 1 week)
- `~/wipcomputerinc/staff/cc-mini/documents/backups/` (179 GB) -> delete after unified backup is proven

### Phase 7: Update healthcheck config

**File:** `~/.openclaw/wip-healthcheck/config.json`

Update `backupRoot` to `~/.ldm/backups/`. Update `backupExpectedFiles` to match new structure.

## What gets backed up

Everything in these four locations:

| Location | Method | What's in it |
|----------|--------|-------------|
| `~/.ldm/` | sqlite3 .backup (crystal.db) + cp -a (rest) | Memory, agents, state, config |
| `~/.openclaw/` | sqlite3 .backup (main.sqlite, context-embeddings.sqlite) + tar (workspace, sessions) + cp (config) | OC conversations, embeddings, workspace, config |
| `~/.claude/` | cp (CLAUDE.md, settings.json) + tar (projects/) | CC instructions, auto-memory, transcripts |
| `~/wipcomputerinc/` | tar --exclude node_modules --exclude .git/objects | Entire workspace: settings, staff, repos (ai/ folders, uncommitted work), _sort, _temp, _transfer, _trash |

## Files to modify

### Code (wip-ldm-os-private)
| File | Change |
|------|--------|
| `scripts/ldm-backup.sh` | New unified script (replaces both existing scripts) |
| `bin/ldm.js` | Deploy backup script in `ldm install` |

### Code (wip-ai-devops-toolbox-private)
| File | Change |
|------|--------|
| TECHNICAL.md | Update backup section with new architecture |

### Docs (~/wipcomputerinc/settings/docs/)
| File | Change |
|------|--------|
| `how-backup-works.md` | Rewrite: one script, one schedule, what's backed up, iCloud offsite, restore |
| `system-directories.md` | Update backup row in runtime table |
| `directory-map.md` | Update backups line |

### Config (~/wipcomputerinc/settings/)
| File | Change |
|------|--------|
| `config.json` | Already has backup section. Verify paths correct. |
| `config-dependencies.json` | Add backup script path as a tracked reference |

### Runtime
| File | Change |
|------|--------|
| `~/Applications/LDMDevTools.app/.../backup.sh` | Point to ~/.ldm/bin/ldm-backup.sh |
| `~/.openclaw/wip-healthcheck/config.json` | Update backupRoot + expectedFiles |
| crontab | Remove verify entry, remove duplicate LaunchAgent |
| `~/Library/LaunchAgents/ai.openclaw.ldm-backup.plist` | Remove (replaced by cron -> LDM Dev Tools.app) |
| `~/Library/LaunchAgents/com.wipcomputer.daily-backup.plist` | Remove (replaced) |

### Retire
| File | Change |
|------|--------|
| `staff/Lēsa/scripts/daily-backup.sh` | Deprecation notice: replaced by ~/.ldm/bin/ldm-backup.sh |
| `~/.openclaw/scripts/verify-backup.sh` | Delete (built into unified script) |

## Verification

```bash
# Dry run
~/.ldm/bin/ldm-backup.sh --dry-run

# Real backup
~/.ldm/bin/ldm-backup.sh

# Check local
ls ~/.ldm/backups/2026-03-24/
# ldm/ openclaw/ claude/ wipcomputerinc/

# Check iCloud
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/wipcomputerinc-icloud/backups/
# wipcomputerinc-mac-mini-2026-03-24.tar.gz

# Check size (should be ~25 GB local, ~5 GB compressed tar)
du -sh ~/.ldm/backups/2026-03-24/

# Verify restore
tar -xzf .../wipcomputerinc-mac-mini-2026-03-24.tar.gz -C /tmp/restore-test/
sqlite3 /tmp/restore-test/2026-03-24/ldm/memory/crystal.db "SELECT count(*) FROM chunks;"
```

## Stopgap (tonight)

Before implementing the full plan, fix LDM Dev Tools.app backup.sh to call the existing ldm-backup.sh instead of Lesa's broken script. This at least saves ~/.ldm/ tonight.
