# Installer: CC Plugin (#8) detection verified end-to-end

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## What

The toolbox SPEC and detect.mjs claim CC Plugin (`.claude-plugin/plugin.json`) is detected as interface #8. The work landed on `cc-mini/docs-cleanup` in March 2026. The canonical SPEC.md just gained the section in PR #715. We have not verified end-to-end that `ldm install` against a real `.claude-plugin/plugin.json` actually emits the right output in 2026-04.

## Why this matters

The whole point of the spec is that an AI reads it, runs `ldm install`, and gets a coherent report. If CC Plugin detection is silently broken (e.g. detector regressed during a refactor, or the install action prints nothing), our docs are lying.

## Verification steps

1. Find a repo that has `.claude-plugin/plugin.json` (one of the official CC plugins works).
2. Run `ldm install --dry-run <path-or-slug>`.
3. Assert: output includes `Claude Code Plugin` in the detected interface list.
4. Assert: install action references `/plugin install` or marketplace registration (whatever the current install path is).
5. If detection fails, file a fix ticket and link from this one.
6. If detection passes, mark this ticket complete and move to `archive/`.

## Acceptance

- A live run against a real CC Plugin repo emits the expected output.
- A test fixture under `examples/cc-plugin/` exists in the toolbox detector and passes CI.

## Why a separate ticket

The codebase changes for CC Plugin already shipped. This ticket is verification-only. It lives in `bugs/installer/` because if verification fails it converts to a real bug.
