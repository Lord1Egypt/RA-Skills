# Bug: LaunchAgents are manually placed, not managed by ldm install

**Date:** 2026-03-27
**Filed by:** cc-mini
**Ticket:** #236
**Priority:** High

## Problem

LaunchAgent plists are manually placed in ~/Library/LaunchAgents/. They have:
- Hardcoded paths that break after migration
- Log paths in /tmp/ (cleared on reboot, lose all logs)
- No PATH env var (tools like sqlite3, npm not found)
- No way to update them except manual editing
- Healthcheck still points to old iCloud path

## Current state

| Plist | Status | Issues |
|-------|--------|--------|
| ai.openclaw.ldm-backup.plist | Working | Log to /tmp/, no PATH |
| ai.openclaw.healthcheck.plist | Running | Points to OLD iCloud path for script |
| ai.openclaw.gateway.plist | Working | OpenClaw gateway |
| com.wipcomputer.daily-backup.plist.disabled | Dead | Disabled Mar 27 |
| com.wipcomputer.cc-watcher.plist | Unknown | Needs audit |

## Fix

### Source
/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/shared/launchagents/*.plist

### Deployment
ldm install reads shared/launchagents/, deploys to ~/Library/LaunchAgents/, runs launchctl unload/load.

### Code changes
/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/bin/ldm.js (cmdInit): add LaunchAgent deployment section after rules/templates/docs deployment.

### What to test
1. ldm install deploys plist to ~/Library/LaunchAgents/
2. launchctl list | grep ai.openclaw shows agents loaded
3. Backup runs at 3am, log appears at ~/.ldm/logs/backup.log
4. ldm doctor checks LaunchAgent health
