# Release Notes: wip-ldm-os v0.4.54

Harness-aware installer. Skills deploy to every AI on your system in one pass.

## What changed

- ldm install now detects all installed AI harnesses before deploying (Claude Code, OpenClaw, Codex, Cursor, Claude macOS)
- Skills (SKILL.md + references/) deploy to EVERY detected harness in one pass
- Permanent copy saved to ~/.ldm/extensions/<name>/ so subsequent installs don't lose files when tmp clones are cleaned up
- ldm init shows which harnesses are detected
- New extensions default to enabled=true (install means it works)
- Harness config cached in ~/.ldm/config.json

## Why

v0.4.50-v0.4.53 tried to fix skill deployment with patches: CC deploy target, enabled gate removal, OC fallback. Each fix revealed another bug because the installer wasn't harness-aware. It hardcoded paths instead of detecting what's installed and deploying to all targets. This release replaces all the patches with one proper fix.

## Issues closed

- #212

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm install
ls ~/.claude/skills/         # should have 13+ skill directories
ls ~/.openclaw/skills/       # should match
cat ~/.ldm/config.json       # should show harnesses field
```
