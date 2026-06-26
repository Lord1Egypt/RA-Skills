# Dev Update: Skill Publish + Stale Dev Update Fix

**Date:** 2026-03-13
**Author:** CC-Mini

## What changed

### Skill Publish to Website (new feature)
After every `wip-release`, SKILL.md is automatically copied to the website as plain text. Any repo with a SKILL.md auto-publishes when `WIP_WEBSITE_REPO` env var is set. No config file needed.

Name resolves from `package.json` name (strip `@scope/`), then directory name. Optional `.publish-skill.json` overrides.

Result: `wip.computer/install/{name}.txt` always matches the latest release.

### Stale Dev Update Check (bug fix)
The old product docs check used a 3-day date window. This let the same stale dev update file pass across 11 releases in one session (the v0.7.8 to v0.7.19 marathon). Now uses git tags: checks if any `ai/dev-updates/` file was modified since the last release tag. Same pattern as roadmap and readme-first checks.

### Documentation
SKILL.md updated with full Skill Publish section. README updated with tool #7. Pipeline step list updated (14 steps).
