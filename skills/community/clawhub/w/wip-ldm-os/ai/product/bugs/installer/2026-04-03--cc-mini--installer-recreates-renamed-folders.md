# Bug: Installer recreates folders that were renamed

**Date:** 2026-04-03
**Reporter:** Parker + CC Mini
**Component:** ldm install

## Description

`ldm install` deploys docs to `~/wipcomputerinc/settings/docs/`. But on March 28, `settings/` was renamed to `library/` and `docs/` to `documentation/`. The installer doesn't know about the rename and recreates `settings/docs/` on every run.

Same issue with `team/lesa-mini/`. Lēsa's real folder is `team/Lēsa/` (unicode). The installer scaffolds `team/lesa-mini/` from the agent name in `~/.ldm/config.json` without checking that the real folder uses a different name.

## Two instances

1. **settings/ ghost folder**: Renamed to `library/` on Mar 28. Installer recreated `settings/` on Apr 1. Two copies of the same docs drifting apart. Parker moved `settings/` to `_trash/`.

2. **team/lesa-mini/ duplicate**: Real folder is `team/Lēsa/`. Installer created `team/lesa-mini/` on Mar 31 from config.json agent name. Empty duplicate.

## Root cause

The installer hardcodes deployment paths without checking if the target was renamed. It should either:
1. Read the actual folder names and deploy there
2. Have a config option for custom folder paths
3. Check for existing folders with similar names before creating new ones

## Fix needed

1. Update installer to deploy docs to `library/documentation/` not `settings/docs/`
2. Update installer to respect unicode folder names or add a folder mapping in config.json
3. Update all references in CLAUDE.md and rules files from `settings/docs/` to `library/documentation/`
4. Update all references from `settings/config.json` to `~/.ldm/config.json`

## Wrong path references found

- `~/.claude/CLAUDE.md` line 10: `~/wipcomputerinc/settings/config.json` should be `~/.ldm/config.json`
- `~/.claude/rules/git-conventions.md` lines 17, 21: `settings/config.json` should be `~/.ldm/config.json`
- `~/.claude/rules/writing-style.md` line 3: `settings/config.json` should be `~/.ldm/config.json`
- `~/.claude/rules/security.md` line 5: `settings/config.json` should be `~/.ldm/config.json`
- Multiple references to `settings/docs/` in rules should be `library/documentation/` or removed
