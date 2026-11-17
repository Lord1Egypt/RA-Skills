---
title: "Remote Control Codex fork currently allows only one active TUI control socket"
status: open
priority: P1
owner: Cody
repo: openai-codex-private
created: 2026-05-05
---

# Remote Control Single Global Socket Limitation

## Problem

The current patched `codex-wip` exposes one global App Server control socket:

```text
~/.codex/app-server-control/app-server-control.sock
```

That was enough to prove one visible TUI plus one browser, but it prevents multiple `codex-wip` TUI sessions from running with Remote Control enabled at the same time.

Observed behavior:

```text
codex-wip
Error: failed to start embedded app server
```

Investigation showed:

- another `codex-wip` process was still alive,
- it owned the global control socket,
- the second TUI failed because it could not bind the same path.

The generic error message is also poor.

## Current Product Decision

Do not block the one-session dogfood on this.

For the current smoke, one visible `codex-wip` TUI is enough.

For product-ready Remote Control, multiple Codex sessions must work.

## Expected Behavior

Eventually Parker should be able to run multiple Codex TUI sessions, and each Remote Control URL should target the correct one.

Two acceptable designs:

1. Per-session socket:

```text
~/.codex/app-server-control/<threadId>.sock
```

2. One broker socket:

```text
~/.codex/app-server-control/app-server-control.sock
```

with explicit routing by thread id to loaded sessions.

For v1, per-session sockets are probably simpler and match the product model: one URL controls one session.

## Immediate Fix

Improve the error message before broader dogfood:

```text
Another Codex TUI already owns the Remote Control App Server socket.
Close that TUI or use a different control socket path.
```

Do not leave users with only:

```text
Error: failed to start embedded app server
```

## Acceptance

Short-term:

- Starting a second `codex-wip` while one already owns the socket produces a clear actionable error.
- The error names the socket path or explains the one-active-TUI limitation.
- The first TUI remains unaffected.

Product-ready:

- Two visible `codex-wip` sessions can run.
- Each can start Remote Control.
- Each printed URL controls only its own thread.
- Browser input to session A never lands in session B.
- Stop for session A never interrupts session B.

## Non-Goals

- Do not redesign browser UI here.
- Do not solve multi-browser fanout here.
- Do not put WIP relay or passkey code into the upstream Codex patch.

