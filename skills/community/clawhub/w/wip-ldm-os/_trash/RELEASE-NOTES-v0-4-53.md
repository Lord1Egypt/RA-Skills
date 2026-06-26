# Release Notes: wip-ldm-os v0.4.53

Skills now deploy to CC even when source repo is gone. Extensions default to enabled on install.

## What changed

- installSkill() falls back to the already-deployed OC copy when the original source path (tmp clone) no longer exists
- Previously, ~/.claude/skills/ stayed empty because the installer looked for SKILL.md in cleaned-up tmp paths
- New extensions now default to enabled=true instead of enabled=false
- Same fallback for references/ directory

## Why

v0.4.50-52 added CC skill deployment but ~/.claude/skills/ stayed empty after install. Root cause: ldm install clones repos to ~/.ldm/tmp/, installs, then cleans up tmp. The skill deploy code tried to read from the deleted tmp path. Now it falls back to the existing OC copy.

## Issues closed

- #212 (third and final fix: CC skills actually populate now)

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install
ls ~/.claude/skills/    # should have 13+ skill directories
```
