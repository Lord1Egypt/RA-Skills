---
name: weekend-scout
description: >
  Weekend Scout discovers next-weekend outdoor events, festivals, fairs, and
  road-trip ideas near the user's city and nearby cities. It builds home-city
  picks and road-trip options, formats the digest, sends it to Telegram. This 
  skill bootstraps the matching platform runtime from the current bundle.
author: Dmitry Nikolaenya
version: 1.0.0
tags:
  - events
  - travel
  - telegram
  - multi-platform
  - python
---
# Weekend Scout

Use this repo-root skill as the stable bundle entrypoint. Weekend Scout scouts
next-weekend outdoor events near the configured city, ranks local picks and
road trips, and relies on run-scoped session caching plus a persistent SQLite
cache managed through the CLI.

Do not treat this root file as the full scouting workflow. Its job is limited
to bootstrapping the Python runtime from this bundle and dispatching to the
matching bundled runtime `SKILL.md`.

## Bootstrap

1. Resolve `bundle_root`.
   Prefer `{baseDir}` when the host provides it. Otherwise resolve the
   directory containing this `SKILL.md`.
2. Resolve a Python command by trying `python`, then `python3`.
   If neither exists, stop and report that Python 3.10+ is required.
3. Read the bundle package version from `pyproject.toml`.
4. Check the installed `weekend-scout` package version with the chosen
   interpreter via `importlib.metadata`.
5. If the package is missing or the version differs from the bundle version,
   run:
   `"<python_cmd>" "{bundle_root}/install/install_skill.py" --with-pip --runtime-only`
6. If bootstrap fails because of an externally managed environment, stop and
   show the exact retry command with `--break-system-packages`. Do **not**
   auto-retry with that flag.
7. If bootstrap succeeds, or the installed version already matches the bundle,
   continue in the same invocation.

## Dispatch

1. Identify the host only when it is explicit from the active environment,
   active skill path, or tool/runtime surface.
   Treat the active workspace-installed bundle case as OpenClaw only when the
   current session clearly is OpenClaw. Otherwise use Claude Code or Codex
   only when that host is equally explicit.
2. Use exactly one bundled runtime file:

| Platform | Canonical runtime skill |
|----------|-------------------------|
| OpenClaw | `.openclaw/skills/weekend-scout/SKILL.md` |
| Codex | `.agents/skills/weekend-scout/SKILL.md` |
| Claude Code | `.claude/skills/weekend-scout/SKILL.md` |

3. Before dispatching, confirm that the chosen nested `SKILL.md` exists.
4. Follow the chosen nested runtime skill and its adjacent `references/`
   directory exactly as shipped.
5. If the host is not clear, stop and list the available bundled runtime paths
   instead of guessing.

## Guardrails

- Keep this root skill as the permanent bundle entrypoint. Do **not**
  self-replace it, overwrite the installed workspace bundle, or promote a
  shared/global skill copy as the primary path.
- Keep later invocations cheap: if the installed package version already
  matches the bundle version, skip installation and dispatch immediately.
- Use only `python -m weekend_scout ...` CLI commands for config, discovery,
  cache, digest preparation, formatting, and delivery.
- Do **not** manually edit cache files, transport payloads, YAML config, or
  SQLite data as a substitute for the CLI workflow.
- Treat the chosen nested runtime `SKILL.md` plus its bundled references as
  the sole authority for scout workflow, command order, payload shape, and
  failure handling.

## Failure Handling

- If the bootstrap command fails, surface the exact command you ran plus the
  installer's own guidance. Do **not** invent an alternative recovery flow.
- If the chosen nested runtime file is missing, report the exact missing path
  and stop.
- Do **not** send the user to README-style manual setup as the primary path.
