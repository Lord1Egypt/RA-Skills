# Release Notes: wip-ldm-os v0.4.51

Skills now deploy regardless of enabled state. All skill instructions visible to all AIs.

## What changed

- Skills (SKILL.md) deploy to ~/.claude/skills/ and ~/.openclaw/skills/ even when the extension is disabled
- Previously, disabled extensions skipped skill deployment. CC and OC never saw the instructions for most tools.
- Skills are instruction files, not running code. There's no reason to gate them on enabled state.

## Why

After installing v0.4.50, ~/.claude/skills/ was still empty. All extensions were enabled=false in the registry (from the Mar 17 install-everything-enable-disable system). The enable gate made sense for MCP servers and hooks (running code) but not for skills (static markdown files).

## Issues closed

- #212 (fully resolved: skills now deploy to CC for all extensions)

## How to verify

```bash
ldm install
ls ~/.claude/skills/         # should have skill directories for all extensions
ls ~/.openclaw/skills/       # should match
```
