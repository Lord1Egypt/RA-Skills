# Release Notes: wip-ldm-os v0.4.11

**Fix install lock so `ldm install` actually updates extensions**

## What changed

- v0.4.10 fixed the re-entrant lock (cmdInstall calling cmdInstallCatalog within the same process)
- But `ldm install` also spawns child `ldm install <ext>` processes via execSync for each extension update
- Each child has a different PID, found the parent's lock, and blocked
- Fix: set `LDM_INSTALL_LOCK_PID` env var when acquiring the lock. execSync inherits env vars, so children skip lock acquisition entirely.
- Also moved the scaffolded RELEASE-NOTES-v0-4-10.md to _trash/

## Why

`ldm install` appeared to complete ("Updated 12/12") but no extensions were actually updated. The child processes all hit the lock and silently failed.

## Issues closed

- #95: Fix install lock for child processes
- #92: Fix re-entrant install lock

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@0.4.11
ldm install
# All 12 extensions should update without "Another ldm install is running" warnings
```
