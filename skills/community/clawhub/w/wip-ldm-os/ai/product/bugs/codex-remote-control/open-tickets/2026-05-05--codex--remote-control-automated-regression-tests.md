---
title: "Remote Control co-presence needs automated regression tests"
status: open
priority: P0
owner: Cody
repo: wip-codex-remote-control-private / wip-ldm-os-private / openai-codex-private
created: 2026-05-05
---

# Remote Control Automated Regression Tests

## Problem

Manual dogfood proved the core co-presence product. Manual proof is not enough now. We need automated tests around the pieces that can regress independently.

The goal is not to automate every browser click immediately. The goal is to protect the contract in layers so a daemon, relay, browser, or Codex fork change cannot silently break co-presence.

## Required Test Layers

### Daemon App Server Tests

Repo: `wip-codex-remote-control-private`

Cover:

- active TUI App Server socket discovery,
- attach to current `CODEX_THREAD_ID`,
- App Server `initialize`,
- `thread/resume`,
- `thread/read` or `thread/turns/list` for hydration,
- browser prompt maps to `turn/start`,
- Stop maps to `turn/interrupt`,
- daemon does not fall back to `@openai/codex-sdk` parallel runner for live Remote Control.

### Hosted Relay Tests

Repo: `wip-ldm-os-private`

Cover:

- `agentId:threadId -> Set<web sockets>` fanout,
- two browser peers stay connected,
- daemon thread-routed frames broadcast to every browser peer,
- browser-specific E2EE session frames route only to the owning browser,
- closing one browser removes only that socket,
- relay does not become session authority.

### E2EE Reload Tests

Repos: `wip-ldm-os-private`, `wip-codex-remote-control-private`

Cover:

- daemon E2EE public key is durable or automatically re-registered after hosted reload,
- browser bootstrap succeeds after hosted reload without `codex-daemon link`,
- first-time missing-key error remains clear,
- relink remains available as recovery but not routine operation.

### Browser Transcript Tests

Repo: `wip-ldm-os-private`

Cover:

- render hydrated `session.history`,
- render live `session.event`,
- avoid duplicate messages during hydration/live handoff,
- render user messages and Codex assistant messages as chat bubbles,
- keep status diagnostics lightweight and inline,
- show model, effort, cwd, session title, and UUID metadata.

### Codex Fork Tests

Repo: `openai-codex-private`

Cover:

- TUI-owned App Server control socket starts when requested,
- external WebSocket client can initialize over the Unix socket,
- external client can resume the live thread,
- multiple subscribers receive the same live thread events,
- connection ID collision cannot recur,
- the TUI remains authoritative and local.

## Acceptance

- Each layer has a test file or explicit test-gap note linked from the implementation PR.
- CI or local validation can run the daemon and relay tests without manual browser interaction.
- The browser smoke can remain manual initially, but the protocol-level history/live handoff gets automated.
- A failing test points to the correct layer: daemon, relay, browser, E2EE, or Codex fork.
- The manual Remote Control smoke checklist remains as final dogfood until full end-to-end browser automation exists.

## Non-Goals

- Do not block refresh hydration on full end-to-end browser automation.
- Do not require upstream OpenAI CI to run WIP-specific relay tests.
- Do not put WIP relay, auth, or `ai/**` content into an upstream `openai/codex` PR.
