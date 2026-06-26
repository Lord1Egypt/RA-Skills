# Release Notes: wip-ldm-os v0.4.50

Skills now deploy to Claude Code. CC can discover LDM OS skills automatically.

## What changed

- ldm install now deploys SKILL.md and references/ to ~/.claude/skills/ (CC standard discovery path)
- Previously only deployed to ~/.openclaw/skills/ (OC only). CC never saw our skills.
- CC users no longer need to paste the wip.computer URL to get skill instructions. CC discovers them automatically after ldm install.

## Why

The Universal Installer badge says "Claude Code Skill" on every repo. But installSkill() only deployed to ~/.openclaw/skills/. CC was getting our MCP servers, hooks, and rules... but not our skill instructions. The one interface that tells the AI HOW to use everything else was missing from CC.

## Issues closed

- #212

## How to verify

```bash
ldm install
ls ~/.claude/skills/              # should now have skill directories
ls ~/.claude/skills/wip-ldm-os/   # should have SKILL.md + references/
```
