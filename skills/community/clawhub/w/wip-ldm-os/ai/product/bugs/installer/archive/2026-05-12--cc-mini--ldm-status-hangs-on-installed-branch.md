---
title: "ldm status can hang indefinitely on installed-branch dogfood"
status: fixed
priority: P1
owner: Installer Cody
repo: wip-ldm-os-private
created: 2026-05-12
---

# `ldm status` can hang indefinitely on installed-branch dogfood

## Problem

The install prompt shipped in alpha.20 (`wip.computer/install/wip-ldm-os.txt`) routes the installed branch through `ldm status` as the first command. On 2026-05-12, a clean dogfood with Codex (gpt-5.5) caused `ldm status` to produce no output for >30 seconds. The process (pid 16606) had to be killed manually.

The install prompt has no completion path when `ldm status` does not return: the documented next steps depend on its output (the version-diff table, the per-component "what's new" summary). The dogfood agent began drifting toward substituting `ldm install --dry-run` output, which would have hidden the bug and silently changed the contract of the installed branch. Parker stopped that drift; the dogfood ended without a clean result.

## Repro

- Machine: mac-mini-01
- LDM OS: 37 extensions installed, alpha track
- `ldm --version`: `0.4.85-alpha.19` (bug is independent of the alpha.20 prompt-policy release)
- Command: `ldm status`
- Behavior: process runs >30s with no output; `pgrep -fl "ldm status"` shows it alive; background `pgrep -fl "node.*ldm"` shows 32+ extension mcp-server processes alive
- Resolution: manual `kill 16606`

## Root cause hypothesis

`ldm status` iterates over all installed extensions and queries each against npm for an update check (and presumably pings or spawns each MCP server to verify connectivity). With 37 extensions, any single stuck network call, npm rate limit, slow MCP probe, or hung extension `mcp-server.mjs` blocks the entire status output. There is no per-extension timeout, no progress output, no isolation.

The high number of `node` processes from various extensions visible in `pgrep` suggests `ldm status` may be invoking each extension's `mcp-server.mjs` for a liveness probe; if one of those probes does not return, status waits.

## Expected behavior

`ldm status` must never hang indefinitely. Specifically:

- Each per-extension check has a bounded timeout. Suggest 5s per network probe, 10s total per extension.
- Progress output: one line per extension printed before its check starts, so the user sees motion.
- Per-extension isolation: a single stuck check is reported as `[timeout]` in its row and the rest of the table completes.
- Total wall-clock bound under 60s for a 37-extension install in steady state, with an option for `--fast` (skip update checks, report installed versions only) if helpful.

## Why this is P1

The install prompt that just shipped in alpha.20 makes `ldm status` load-bearing on the installed branch. Until this is fixed, every clean install-flow dogfood is blocked on the same hang, and the dogfood pattern is the canonical way new users will land on LDM OS. The install spec cannot route around this because the doc commits to `ldm status` as the canonical check (and substituting `ldm install --dry-run` would change the contract).

## Acceptance

- `ldm status` returns within 60s on a 37-extension install in steady state.
- A single stuck per-extension probe reports `[timeout]` and does not block the rest of the table.
- Progress output: one line written per extension before its check starts.
- The install prompt's installed-branch dogfood completes end-to-end without manual intervention on mac-mini-01.
- Regression test: simulate or inject a hung extension probe; assert `ldm status` still returns within the wall-clock bound and prints the stuck row as `[timeout]`.

## Fix

Implemented in PR for the next alpha:

- `ldm status` now prints installed-state output before network update checks.
- npm update checks use bounded per-check timeouts and a total status budget.
- Slow checks are reported in an "Update checks skipped" section instead of blocking the command.
- Regression coverage simulates hung npm probes and asserts status exits quickly with a `[timeout]` row.

## Recommendation

Cut as alpha after fix. Dogfood validation requires an installable artifact. Next alpha is `0.4.85-alpha.21` or later.

## Related

- `wip.computer/install/wip-ldm-os.txt` ... the install spec depending on this command.
- Install-prompt-policy alpha shipped 2026-05-12: PRs `wip-ldm-os-private` #899, #901; `wip-websites-private` #44.
- Companion ticket filed same day: install-prompt regression eval.
- Dogfood transcript that exposed this: Codex (gpt-5.5) session 2026-05-12, hung pid 16606 killed manually.
