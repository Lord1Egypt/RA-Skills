# Release Notes Quality Gate

**Date:** 2026-03-15

## What changed

wip-release now blocks ALL releases (patch, minor, major) if the release notes are bad. Previously, patch releases only warned. Now they block.

The gate checks:
- Notes must be at least 50 characters
- Notes can't look like a changelog entry ("fix: ...", "add: ...", "update: ...")
- Minor/major still require a file (not --notes flag)

If the gate blocks, it tells you exactly how to fix it: write a RELEASE-NOTES file, write a dev update, or use --notes with at least 50 chars of real description.

## Why

Release notes were consistently garbage. One-liner --notes flags like "Fix bug" or "Update docs" sailed through on patch releases. The warnings were ignored by both humans and agents. Every release page on GitHub had thin, useless notes that didn't explain what changed or why.

## Also in this release

- wip-repo-init templates renamed from ai/ to templates/ so they ship with npm install (deploy-public.sh was stripping them)
- SKILL.md restart notice after install (hooks need session restart)
- SPEC.md and TECHNICAL.md updated with all 17 tools and LDM OS links
- Branch guard matcher fix (catches Bash + NotebookEdit)
- Forced Git Worktrees and Branch Guard sections added to SKILL.md
