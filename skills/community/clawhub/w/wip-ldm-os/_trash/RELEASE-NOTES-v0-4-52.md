# Release Notes: wip-ldm-os v0.4.52

Extensions that are already running now get updated. No more stale versions stuck behind the enabled flag.

## What changed

- MCP servers and hooks that are already deployed now update even if enabled=false in registry
- Previously, extensions installed before the enable/disable system got stuck: they were running but the registry said enabled=false, so ldm install skipped their updates
- Grok (v1.0.2 -> v1.0.3), branch-guard, and other extensions should now update correctly

## Why

ldm status showed updates available for grok, branch-guard, tavily since v0.4.41. But ldm install skipped them because enabled=false. These extensions were installed before the enable/disable system existed. They're running (MCP connected, hooks active) but the registry didn't know that.

## Issues closed

- #212

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install
ldm status   # grok, branch-guard should show current versions
```
