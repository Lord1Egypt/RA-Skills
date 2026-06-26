# Release Notes: wip-ldm-os v0.4.10

**Fix re-entrant install lock that blocked every `ldm install` run**

## What changed

- `acquireInstallLock()` now checks if the lock holder is the current process before blocking
- `cmdInstall()` acquires the lock, then calls `cmdInstallCatalog()` which tried to acquire again. Since the PID was alive (itself), the check failed with "Another ldm install is running." Adding `lock.pid === process.pid` makes the lock re-entrant.

## Why

`ldm install` was completely broken since v0.4.9. Every run hit the lock it created itself and refused to continue.

## Issues closed

- Fixes the lock regression introduced in v0.4.9

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@0.4.10
ldm install --dry-run
# Should show system state, not "Another ldm install is running"
```
