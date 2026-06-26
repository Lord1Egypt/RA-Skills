# Installer: unregister stale MCP entries on deploy (Phase 3b)

## What changed

When an extension's current source does not expose an MCP interface, `installFromPath` now removes any stale `~/.claude.json` entry whose args path resolves under this extension's LDM or OpenClaw directory.

- New helper: `lib/deploy.mjs::unregisterStaleMCP(toolName)`.
- Branches: if `interfaces.mcp` is present the existing registration path runs; if it is absent the new unregister path runs.
- Matching is keyed on the resolved args path, not on `source.repo` (which is unreliable; see the buildSourceInfo fix landing separately).
- Clean via `claude mcp remove ... --scope user` first, fallback to direct `~/.claude.json` edit if the CLI command fails.
- Also attempts `openclaw mcp unset ...` (non-fatal if OpenClaw is not present).

## Why

Phase 3b of the 1password MCP bug plan. The prior failure mode:

1. v1 of extension X ships with `mcp-server.mjs` at root. Install registers it in `~/.claude.json`.
2. v2 of extension X renames the file (or drops it entirely, or moves it to `src/`). Install deploys v2. The `~/.claude.json` entry is still there, still pointing at the v1 path, which has been rotated into `_trash/`. `claude mcp list` shows a red ✗.

No code path removed the stale entry. This change closes that gap.

## Matching scope

Strictly limited to entries whose `args[0]` points under `LDM_EXTENSIONS/<toolName>/` or `OC_EXTENSIONS/<toolName>/`. Anything else (user-added entries, entries pointing at external tools) is not touched. Safe by default.

## Verification

- `node --check lib/deploy.mjs` passes.
- Dry-run: prints "would unregister stale ..." without touching `.claude.json`.
- Manual test: take an extension that has an MCP, edit its source to drop the MCP file, re-run `ldm install <extension>`, watch for the `MCP: unregistered stale ...` line, and confirm `claude mcp list` no longer shows the entry.

## Tracking

Closes Phase 3b of:
`ai/product/bugs/1password/2026-04-21--cc-mini--mcp-server-missing-from-install.md`

Phase 3c (`ldm doctor` MCP path check) lands in a separate PR.

## Non-goal

Does not fix `buildSourceInfo` capturing the parent repo's remote when extraction lands inside `~/.ldm/tmp`. That is a separate bug that affects registry `source.repo` values but does not affect Phase 3b since Phase 3b is path-based, not source-based.
