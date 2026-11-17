---
title: "Remote Control co-presence requires a clean patched Codex install path"
status: open
priority: P1
owner: Cody
repo: openai-codex-private
created: 2026-05-05
---

# Remote Control Patched Codex Install Path

## Problem

Remote Control co-presence currently depends on WIP's patched Codex build:

```text
codex-wip
```

The normal stock `codex` binary is untouched. That is correct for dogfood safety, but the product needs a clear install and runtime story before broader use.

The current user-facing state can be confusing:

- `codex-wip` reports version `0.0.0`.
- It can show an update-required warning inherited from upstream metadata.
- Normal `codex` remains stock and will not have the App Server control socket patches.
- Remote Control may appear installed while true co-presence only works from `codex-wip`.

The terminal installer dry-run also under-reports the product shape.

Observed on 2026-05-05:

```text
ldm install --alpha --dry-run wip-codex-remote-control

Installing wip-codex-remote-control@alpha from npm...
+ Installed from npm

Installing: wip-codex-remote-control (dry run)
Detected 2 interface(s): cli, module

2 interface(s): cli, module
CLI: codex-daemon, codex-daemon-mcp
Module: "./dist/index.js"

Dry run complete. No changes made.
```

That output is technically incomplete for the product Parker is dogfooding. It does not tell the user that Remote Control also depends on:

- Codex MCP registration,
- Codex skill installation,
- daemon pairing,
- daemon runtime state,
- patched `codex-wip` for true co-presence.

It also prints `Installed from npm` during a dry run, which can read as though the dry run changed the machine even when it later says no changes were made.

## Current Green Baseline

With `codex-wip` and `wip-codex-remote-control@0.0.2-alpha.11`, one visible TUI plus one browser works:

- correct current session URL,
- browser to TUI,
- TUI to browser,
- same thread id,
- App Server backend path.

## Expected Behavior

For dogfood:

- docs and install output must say that co-presence requires `codex-wip`,
- the stock `codex` binary remains untouched,
- `codex-wip` should be easy to identify in the TUI banner,
- Remote Control failure copy should point users to the patched Codex requirement when the App Server socket is missing.

For public/upstream path:

- upstreamable Codex patch must be split from WIP daemon/auth/UI,
- no `ai/**` files in any upstream-intended branch,
- the public issue should present the working product demo and ask for intended App Server direction before a PR.

## Acceptance

- `codex-wip` install path is documented in Remote Control technical docs or install notes.
- User-facing error for missing App Server socket says the session must be running in patched Codex for now.
- `start remote control` from stock `codex` fails clearly if the required active thread env/socket is missing.
- `start remote control` from `codex-wip` works.
- The normal `codex` binary remains untouched during alpha dogfood.
- Upstream-intended Codex branch contains only code/tests/docs suitable for `openai/codex`, no WIP private planning files.
- `ldm install --alpha --dry-run wip-codex-remote-control` tells the truth about all relevant surfaces: CLI, module, MCP, skill, daemon runtime, and patched-Codex requirement.
- Dry-run copy distinguishes package fetch/cache work from actual install mutations.

## Non-Goals

- Do not replace stock `codex` automatically.
- Do not publish a stable/latest Remote Control package before this is clear.
- Do not put WIP relay, passkey, Kaleidoscope, or daemon code in the upstream Codex patch.
