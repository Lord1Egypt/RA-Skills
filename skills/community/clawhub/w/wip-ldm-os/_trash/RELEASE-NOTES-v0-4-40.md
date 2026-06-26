# Release Notes: wip-ldm-os v0.4.40

Fixes #191

## Fix: shared/ and scripts/ now ship in npm package

v0.4.39 added rules, prompts, and scripts but they were excluded from the npm package by the `files` field in package.json. `ldm init` couldn't deploy DEV-RULES.md to OpenClaw because the source files weren't there.

Now `shared/rules/`, `shared/prompts/`, and `scripts/` all ship. `ldm init` deploys:
- `~/.ldm/shared/rules/` (5 rule files)
- `~/.ldm/shared/prompts/` (6 prompt files)
- `~/.claude/rules/` (Claude Code)
- `~/.openclaw/workspace/DEV-RULES.md` (OpenClaw)
