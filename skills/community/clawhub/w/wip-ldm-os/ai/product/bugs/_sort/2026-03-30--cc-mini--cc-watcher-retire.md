# Bug: cc-watcher LaunchAgent broken, needs redesign

**Date:** 2026-03-30
**Filed by:** cc-mini
**Priority:** medium

## Problem

The `com.wipcomputer.cc-watcher` LaunchAgent is broken. It points to the old iCloud path (`~/Documents/wipcomputer--mac-mini-01/staff/Lēsa/repos/cc-watcher/src/index.js`) which doesn't exist after the Mar 24 migration. The node path is also wrong (`/usr/local/bin/node` instead of `/opt/homebrew/bin/node`). launchctl shows exit code 78.

## Current state

```
launchctl list | grep cc-watcher
-	78	com.wipcomputer.cc-watcher
```

No repo at the old path. No repo at the new `~/wipcomputerinc/` path. The code never survived the migration.

## What cc-watcher did

1. Idle-time detection + auto-approving Claude Code permission dialogs (Peekaboo-based screen scanning)
2. Checking lesa-bridge inbox
3. Monitoring Claude Code sessions

## Decision

Parker (Mar 30): cc-watcher should not be fully retired. The agent-to-agent communication channel it provided is still needed, but in a different mode. The Peekaboo screen-scanning approach is fragile (requires screen recording permissions, only works when Terminal is visible). The redesign should be a proper message relay or command channel, not screen automation.

Lesa confirmed the monitoring side is covered by healthcheck. The inbox check is handled by heartbeats. But the cross-agent command channel needs to be rebuilt properly.

## Immediate fix

1. Disable the broken LaunchAgent (it's crashing on every restart)
2. Do NOT delete it. Rename to `.disabled` so we can reference the original when redesigning.

## Future: redesign ticket needed

A new ticket should cover:
- What mode should cc-watcher operate in?
- Message relay between Claude Code and OpenClaw?
- Command channel for agents to trigger actions on each other?
- How does this relate to the existing lesa-bridge MCP tools?

## Files to change (immediate)

| File | Change |
|------|--------|
| `bin/ldm.js` (dead trigger cleanup) | Disable cc-watcher plist on install |
