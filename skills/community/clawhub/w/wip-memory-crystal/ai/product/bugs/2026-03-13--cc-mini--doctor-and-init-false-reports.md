# Bug: Doctor and init --dry-run report incorrect/incomplete state

**Filed by:** CC-Mini + Parker on 2026-03-13
**Severity:** Medium. Misleading status output causes confusion and erodes trust.

---

## Issues Found

### 1. `crystal init --dry-run` shows nothing when already installed

**Current behavior:** "Memory Crystal v0.7.8 is already installed and up to date. Run crystal doctor to check health."

**Expected behavior:** Show the full state even when current. The install prompt says "show me exactly what will change." Even when nothing changes, the dry-run should display:
- Current version vs latest available
- What's configured (hooks, cron, MCP, backup)
- What's healthy vs what has warnings
- Database stats (chunks, memories, size)
- Agent list

The dry-run is the user's first look at the system. It should never be empty.

### 2. Backup: "Not configured" when backups ARE running

**Current behavior:** Doctor says `[!!] Backup: not configured`

**Reality:** Backup runs via LDM Dev Tools.app cron job:
```
0 0 * * * open -W ~/Applications/LDMDevTools.app --args backup
```
Two backups exist at `~/.ldm/backups/` (Mar 3 and Mar 4).

**Root cause:** Doctor (`checkBackup()` in doctor.ts) only checks for:
- LaunchAgent at `~/Library/LaunchAgents/ai.openclaw.ldm-backup.plist`
- Cron entry matching `ldm-backup`

It doesn't check for the LDM Dev Tools.app backup path or for existing backup files in `~/.ldm/backups/`.

**Fix:** Check if `~/.ldm/backups/` has recent files. If backups exist within the last 7 days, report OK regardless of how they got there.

### 3. Bridge: "Not installed" when bridge IS working

**Current behavior:** Doctor says `[!!] Bridge: not installed`

**Reality:** lesa-bridge is registered as an MCP server and connected:
```
lesa-bridge: node /Users/lesa/.openclaw/extensions/lesa-bridge/dist/index.js - Connected
```
Parker used it this morning.

**Root cause:** `isBridgeInstalled()` in bridge.ts checks for a global npm package (`lesa-bridge` in PATH). But the bridge is installed as a local extension at `~/.openclaw/extensions/lesa-bridge/`. Different install path.

**Fix:** Also check `~/.openclaw/extensions/lesa-bridge/` and `~/.ldm/extensions/lesa-bridge/` for the bridge.

### 4. Role shows "Standalone" when it should be "Core"

**Current behavior:** `crystal role` and doctor say "standalone (auto-detected)"

**Expected:** This is the Mac mini. It's the always-on primary machine. All embeddings happen here. The readme-first.md describes it as Crystal Core. It should show as "Core."

**Root cause:** Role detection (`detectRole()` in role.ts) defaults to "standalone" when no relay is configured. But "Core" should be the default for a machine that has the primary crystal.db and runs all the capture/embedding infrastructure.

**Fix options:**
- `crystal promote` should have been run during setup (makes this Core)
- Or: auto-detect Core status based on: has crystal.db + has capture cron + has multiple agents writing to it

### 5. "system" and "test" agents in status output

**Current behavior:** Status shows agents: cc-mini, main, oc-lesa-mini, system, test

**Issue:** `system` (63 chunks) is leftover from bulk file scanning that was deleted. `test` (1 chunk) is a test entry. Neither should appear prominently in status output. They're noise.

**Fix:** Filter out agents with fewer than 10 chunks from the default status display, or mark them as inactive.

## Summary

The doctor and installer need to reflect reality, not just check for specific file paths. When the user has a working system configured through a different path than what the doctor expects, the doctor should detect that and report accurately. False warnings erode trust.
