# Bug: Session export plugin writes to old iCloud path, LDM agents folder stale

**Date:** 2026-03-30
**Filed by:** cc-mini
**Priority:** critical

## Problem

Lesa's session exports have been going to the wrong location since the Mar 24 migration. The session-export OpenClaw plugin has a hardcoded `DEFAULT_OUTPUT_DIR` pointing to the old iCloud path. The LDM agents folder stopped receiving sessions on Feb 26 (was a one-time copy, never a live destination).

Three locations, all out of sync:

| Location | Date range | Count | Status |
|----------|-----------|-------|--------|
| `~/.ldm/agents/oc-lesa-mini/memory/sessions/` | Feb 7 - Feb 26 | 663 | Stale since Feb 26. Never updated. |
| `~/wipcomputerinc/team/Lēsa/documents/sessions/` | Feb 7 - Mar 24 | 860 | Stopped at migration day. |
| Old iCloud: `~/Documents/wipcomputer--mac-mini-01/staff/Lēsa/documents/sessions/` | Mar 21 - Mar 30 | 77 | Still being written to (wrong). |

53 sessions from Mar 25-30 only exist in the old iCloud location. They need to be copied.

## Root cause

1. `session-export` plugin at `~/.openclaw/extensions/session-export/dist/index.js` line 7:
   ```javascript
   const DEFAULT_OUTPUT_DIR = join(HOME, "Documents/wipcomputer--mac-mini-01/staff/Lēsa/documents/sessions");
   ```
   Never updated during migration.

2. `openclaw.json` didn't set `outputDir` override, so the plugin used the hardcoded default.

3. LDM agents sessions folder was populated once (Feb 7-26) and never kept in sync. No mechanism exists to write there.

## Immediate fix (done)

Set `outputDir` in `openclaw.json` plugin config:
```json
"session-export": {
  "enabled": true,
  "config": {
    "outputDir": "/Users/lesa/wipcomputerinc/team/Lēsa/documents/sessions"
  }
}
```
Gateway restarted. New sessions now export to the correct team location.

## Still needs doing

1. **Copy missing sessions.** 53 files from Mar 25-30 in the old iCloud location need to be copied to:
   - `~/wipcomputerinc/team/Lēsa/documents/sessions/`
   - `~/.ldm/agents/oc-lesa-mini/memory/sessions/`

2. **Backfill LDM agents folder.** 860 files from team sessions (Feb 7 - Mar 24) need to be copied to `~/.ldm/agents/oc-lesa-mini/memory/sessions/`.

3. **Update plugin to write to both locations.** The session-export plugin should write to:
   - The configured `outputDir` (team documents, human-readable)
   - `~/.ldm/agents/{agentId}/memory/sessions/` (LDM agents folder, agent memory)

4. **Fix the hardcoded default.** Change `DEFAULT_OUTPUT_DIR` in the plugin source to read from LDM config or use a sensible default that doesn't reference old paths.

5. **Add monitoring.** `ldm doctor` should check that session exports are landing in the right place. Flag if the last export is older than 24 hours.

## Files to change

| File | Change |
|------|--------|
| Session-export plugin source | Fix DEFAULT_OUTPUT_DIR, add dual-write to LDM agents |
| `bin/ldm.js` (doctor) | Add session export health check |

## What the memory system should have caught

This is a systemic issue. When the migration happened on Mar 24, every path-dependent component should have been audited. The session-export plugin was missed. The healthcheck plist was missed. The backup script was missed. These are all the same class of bug: path references not updated during migration.

The config-dependencies.json system was designed to track these. It should flag every file that references a path when that path changes. That system exists but wasn't run during the migration.
