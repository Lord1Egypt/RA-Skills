# Folder Restructure: ~/wipcomputer/

## Why

Everything was under `~/Documents/wipcomputer--mac-mini-01/staff/` (iCloud-synced). Problems:
- iCloud "preparing to move" spinner on large operations
- Path is absurdly long
- Repos syncing via iCloud causes conflicts
- No clean separation between work product and git repos

## New Layout

```
~/wipcomputer/                          <- workspace root (local, not iCloud)
  staff/
    parker/
      documents/                        <- Parker's docs (moved from iCloud staff/Parker/documents/)
      repos/                            <- Parker's repos (TBD, currently still in iCloud)
      backups-template/                 <- Parker's backup folder template
    cc-mini/
      documents/                        <- CC's docs (moved from iCloud staff/Parker/Claude Code - Mini/documents/)
        _plans/
        _trash/
        backups/
        journals/
        sessions/
        sort/
    lesa/                               <- Lesa's workspace (TBD)
  repos/                                <- shared repos (TBD)
  wipcomputer-icloud alias              <- symlink to iCloud for things that still need sync
```

## Old Layout (being migrated from)

```
~/Documents/wipcomputer--mac-mini-01/   <- iCloud-synced
  staff/
    Parker/
      Claude Code - Mini/
        repos/                          <- all repos (ldm-os/, wip-inc/, etc.)
        documents/                      <- CC's docs (journals, sessions, etc.)
      Claude Code - MBA/
      documents/                        <- Parker's personal docs
    Lēsa/
      repos/
      documents/
```

## What's Moved So Far (2026-03-18)

| What | From | To | Status |
|------|------|----|--------|
| CC documents | iCloud staff/Parker/Claude Code - Mini/documents/ | ~/wipcomputer/staff/cc-mini/documents/ | DONE |
| Parker documents | iCloud staff/Parker/documents/ | ~/wipcomputer/staff/parker/documents/ | TBD (check) |
| Repos | iCloud staff/Parker/Claude Code - Mini/repos/ | TBD | NOT MOVED |
| Lesa workspace | iCloud staff/Lēsa/ | TBD | NOT MOVED |

## What Still Lives in iCloud

- All repos (ldm-os/ tree) ... still at old path
- Lesa's folders (staff/Lēsa/) ... still at old path
- Screenshots folder ... still at old path

## Key Decisions

- `~/wipcomputer/` is local, not iCloud-synced
- iCloud alias/symlink for things that need cross-device sync
- Repos stay in iCloud for now (or move to ~/wipcomputer/repos/ later)
- Agent folders use lowercase (`cc-mini`, `parker`, `lesa`) not mixed case
- Issue #117 tracks this work

## Current Backup Systems (BEFORE unified backup)

Two independent backup systems running with no coordination. 381 GB total.

### Lesa's backup
- **Location:** ~/wipcomputer/staff/cc-mini/documents/backups/
- **Size:** 361 GB (7 days, Mar 12-18)
- **Script:** staff/Lēsa/scripts/daily-backup.sh
- **Schedule:** Midnight via LDM Dev Tools.app (backup.sh job calls Lesa's script)
- **Contents:** Everything (crystal.db, sqlite files, OC sessions, workspace, ldm-home.tar, CC transcripts)
- **Problem:** Backs up reinstallable code, way too large

### LDM backup
- **Location:** ~/.ldm/backups/
- **Size:** 20 GB (7 days, Mar 3-18)
- **Script:** ~/.ldm/bin/ldm-backup.sh
- **Schedule:** 3 AM via LaunchAgent
- **Contents:** crystal.db, config, state, agents only
- **Problem:** Doesn't capture main.sqlite, main.sqlite-wal, context-embeddings, workspace

### Backup verify
- **Script:** ~/.openclaw/scripts/verify-backup.sh
- **Schedule:** 00:30 via cron
- **Purpose:** Checks backup ran

### Other issues
- main.sqlite-wal not captured by either system
- 63 GB of orphaned ~/.openclaw/memory/main.sqlite.tmp-* files
- No iCloud offsite copy

All of this gets replaced by `ldm backup`. See: [Unified Backup Plan](../plans-prds/current/2026-03-18--unified-backup-system.md)

## Related

- [Unified Backup Plan](../plans-prds/current/2026-03-18--unified-backup-system.md)
- Issue #117 (folder restructure)
- Issue #119 (unified backup)
