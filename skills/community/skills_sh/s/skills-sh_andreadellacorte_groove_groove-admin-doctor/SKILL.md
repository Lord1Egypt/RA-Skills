---
name: groove-admin-doctor
description: "Run all groove health checks: config, backends, companions, AGENTS.md."
license: MIT
allowed-tools: Read Write Edit Glob Grep Bash(git:*) Bash(beans:*) Bash(gh:*) Bash(linear:*) Bash(npx:*) Bash(mkdir:*) AskUserQuestion
metadata:
  author: andreadellacorte
---

<!-- groove:managed — do not edit; changes will be overwritten by groove update -->

# groove-admin-doctor

## Outcome

All groove sub-skill health checks are run and a consolidated summary is reported. User knows exactly what is working, what is misconfigured, and what action to take for any failure.

## Acceptance Criteria

- `/groove-utilities-task-doctor` and `/groove-utilities-memory-doctor` are run
- Companion skill presence is checked directly
- Results are shown per sub-skill with pass/fail per check
- Overall status is shown: all healthy, or N issues found
- Each failure includes a specific remediation action

## Output format

```
groove doctor
─────────────────────────────────────
groove
  ✓ git repo: detected
  ✓ groove-version: 0.1.0
  ✓ installed version: 0.1.0
  ✓ up to date

task
  ✓ .groove/index.md present
  ✓ tasks.backend: beans
  ✓ beans installed (v0.x.x)
  ✓ .beans.yml present
  ✓ beans reachable

memory
  ✓ memory path exists (.groove/memory/) [hardcoded]
  ✓ memory dirs exist (.groove/memory/daily/, weekly/, monthly/, git/)

companions
  ✓ find-skills installed
  ✓ agent-browser installed
  ✓ pdf-to-markdown installed

platform symlinks
  ✓ .claude/skills/groove → ../../.agents/skills/groove
  ✗ .cursor/skills/ missing — run: /groove-admin-install

─────────────────────────────────────
1 issue found. Run the suggested commands above to fix.
```

## Constraints

- Run git repo check first, then version check, then `/groove-utilities-task-doctor`, `/groove-utilities-memory-doctor`, companions check in sequence
- Git repo check:
  - Run `git rev-parse --is-inside-work-tree` in the current directory
  - If it succeeds: `✓ git repo: detected`
  - If it fails: `✗ git repo: not a git repository — groove requires a git repo`
- Version check:
  - Read `groove-version:` from `.groove/index.md` (if absent, treat as `0.1.0`)
  - Read `version:` from `skills/groove/SKILL.md`
  - If they differ: `✗ groove-version (<local>) behind installed (<installed>) — run: /groove-admin-update`
- Companions check:
  - Check `ls .agents/skills/find-skills/SKILL.md` — if absent: `✗ find-skills not installed — run: /groove-admin-install`
  - Check `ls .agents/skills/agent-browser/SKILL.md` — if absent: `✗ agent-browser not installed — run: /groove-admin-install`
  - Check `ls .agents/skills/pdf-to-markdown/SKILL.md` — if absent: `✗ pdf-to-markdown not installed — run: /groove-admin-install`
- Platform symlinks check (after companions):
  - For each `groove-*` directory in `.agents/skills/`: check that `.claude/skills/<name>` is a symlink pointing to `../../.agents/skills/<name>`
    - If missing or not a symlink: `✗ .claude/skills/<name> not a symlink — run: /groove-admin-install`
    - If symlink is broken (target doesn't exist): `✗ .claude/skills/<name> broken symlink — run: /groove-admin-install`
  - Check if `.cursor/skills/` directory exists:
    - If absent: `✗ .cursor/skills/ missing — run: /groove-admin-install`
    - If present: check each groove symlink as above
  - All symlinks healthy: `✓ platform symlinks (.claude/, .cursor/)`
- Claude Code native hooks check (after platform symlinks):
  - Check if `.claude/settings.json` exists
  - If it exists: parse JSON and verify groove's hook entries are present (`daily-end-reminder`, `git-activity-buffer`, `block-managed-paths`, `context-reprime`, `version-check`, `session-capture` commands in the `hooks` key)
    - Each missing entry: `✗ .claude/settings.json missing groove hook <name> — run: /groove-admin-claude-hooks`
  - If absent: `ℹ .claude/settings.json not present — run /groove-admin-claude-hooks to install native hooks (optional)`
  - All present: `✓ Claude Code native hooks (daily-end-reminder, git-activity-buffer, block-managed-paths, context-reprime, version-check, session-capture)`
- Cursor native hooks check (after Claude Code hooks):
  - Check if `.cursor/` directory exists
  - If `.cursor/` exists:
    - Check if `.cursor/hooks.json` exists
    - If it exists: parse JSON and verify groove's hook entries are present (`context-reprime`, `daily-end-reminder`, `git-activity-buffer`, `block-managed-paths`, `version-check`, `session-capture` commands in the `hooks` key)
      - Each missing entry: `✗ .cursor/hooks.json missing groove hook <name> — run: /groove-admin-cursor-hooks`
    - If absent: `ℹ .cursor/hooks.json not present — run /groove-admin-cursor-hooks to install native hooks (optional)`
    - All present: `✓ Cursor native hooks (context-reprime, daily-end-reminder, git-activity-buffer, block-managed-paths, version-check, session-capture)`
  - If `.cursor/` absent: skip silently (Cursor not in use)
- Collect all results before printing — do not interleave output with check progress
- Each `✗` item must include a concrete remediation command on the same line
- Exit with a clear "all healthy" message if no issues found
- Do not attempt to auto-fix issues — report only
