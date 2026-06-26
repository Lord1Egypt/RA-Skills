---
name: openclaw-workspace-doctor
description: Use when the user wants to inspect, repair, package, or troubleshoot an OpenClaw workspace doctor setup, especially for stale bootstrap state, missing daily memory notes, or codex-cli launch hazards in OpenClaw config.
---

# OpenClaw Workspace Doctor

## Overview

This skill runs the OpenClaw workspace doctor, applies safe workspace-local fixes, and handles the companion fixer for the external `codex-cli` backend config. Use it when the user asks to diagnose workspace startup drift, package the doctor tool, or repair the known `--full-auto` non-interactive stall risk.

## When To Use It

- The user asks to run or extend the workspace doctor tool.
- The workspace has stale bootstrap/onboarding behavior.
- Daily `memory/YYYY-MM-DD.md` notes are missing or inconsistent.
- OpenClaw is hanging because `codex-cli` launches with `--full-auto`.
- The user wants the doctor packaged as a repo or a Codex skill.

## Workflow

1. Run the doctor first:
   `python3 scripts/workspace_doctor.py`

2. If the problem is workspace-local, apply safe fixes:
   `python3 scripts/workspace_doctor.py --fix`

3. If the remaining problem is the external OpenClaw config, inspect or patch it with the companion fixer:
   `python3 scripts/fix_openclaw_codex_config.py --check`
   `python3 scripts/fix_openclaw_codex_config.py`

4. If the environment blocks writing `~/.openclaw/openclaw.json`, do not pretend the live fix happened. Report the sandbox restriction clearly and, if useful, use:
   `python3 scripts/fix_openclaw_codex_config.py --stdout`

5. For repo packaging tasks, update:
   - `README.md`
   - `pyproject.toml`
   - `setup.py`
   - `tests/`
   - `.github/workflows/ci.yml`

6. Validate before closing:
   - `python3 -m unittest discover -s tests`
   - `python3 scripts/workspace_doctor.py`
   - `python3 scripts/workspace_doctor.py --json`
   - `python3 /Users/xutao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/openclaw-workspace-doctor`

## Repo Commands

- Run doctor:
  `python3 scripts/workspace_doctor.py`
- Run doctor with fixes:
  `python3 scripts/workspace_doctor.py --fix`
- Emit JSON:
  `python3 scripts/workspace_doctor.py --json`
- Check external config:
  `python3 scripts/fix_openclaw_codex_config.py --check`
- Patch external config:
  `python3 scripts/fix_openclaw_codex_config.py`
- Print patched config without writing:
  `python3 scripts/fix_openclaw_codex_config.py --stdout`

## References

- Read [references/commands.md](references/commands.md) for the command map and fix boundaries.
- Read [references/repo-layout.md](references/repo-layout.md) when you need the repo structure and what each area is for.

## Scripts

- `scripts/run_doctor.py` runs the packaged CLI.
- `scripts/fix_openclaw_config.py` runs the external config fixer.
- Prefer these wrappers or the repo-root scripts instead of retyping logic.
