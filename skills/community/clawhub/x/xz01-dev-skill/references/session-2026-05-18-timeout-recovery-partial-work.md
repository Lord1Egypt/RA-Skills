# Session 2026-05-18 — Timeout Recovery During xz01 Detail-Page Work

## Context

During an all-detail-page mixed-sidebar repair, a development worker timed out after several minutes. A later inspection showed that the worker had already modified all active detail templates and CSS, cleared runtime, and left the live site in a partially completed but useful state.

## Durable Lesson

For xz01 Hermes-native dev/test delegation, a timeout is not proof that the worker did nothing and not proof that the task passed. Treat it as an interrupted handoff and inspect the authorized workdir before deciding the next step.

## Recovery Pattern

1. Inspect only authorized writable locations, such as `/www/wwwroot/www.900az.com/public/themes/default/**`, `/www/wwwroot/www.900az.com/runtime/`, `/www/wwwroot/www.900az.com/test-artifacts/...`, and `/root/.hermes/workspace/xz01-artifacts/...`.
2. Check modified timestamps and changed files for the task scope.
3. Read representative changed templates/CSS to determine whether the intended implementation landed.
4. If useful partial work exists, continue with a smaller follow-up task or independent test instead of re-sending the full original request.
5. If no useful work exists, re-dispatch a narrower task with stricter scope and fewer deliverables.
6. Never mark a timed-out worker as PASS without independent validation.
7. Do not write timeout diagnostics, temporary scripts, or recovery reports under `/root/.openclaw`; use `/tmp` or `/root/.hermes/workspace/...`.

## Why This Matters

This pattern prevents two common failures:

- losing valid partial implementation work by blindly rerunning the whole task;
- accepting a timed-out task without evidence.

It also keeps the xz01 stability rule intact: split long tasks into smaller units rather than increasing max-turns or letting a single worker run indefinitely.
