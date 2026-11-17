---
title: "Remote Control cross-thread interrupt should not leak session existence"
status: open
priority: P2
owner: unassigned
repo: wip-codex-remote-control-private
created: 2026-05-11
security_gate: hardening follow-up; daemon thread authority P0 remains closed
---

# Remote Control Cross-Thread Interrupt Error Parity

## Problem

The daemon thread authority binding blocks cross-thread commands for an E2EE browser session. However, `session.interrupt` can still return different errors depending on whether the requested session id resolves locally:

- known but unauthorized session: `unauthorized thread for this remote control session`;
- unknown session: `no active turn`.

A browser with a valid ticket for thread A could use this difference as a small oracle to distinguish whether thread B is attached in the daemon.

This is not an authority bypass. The attacker still needs a valid ticket and a target session id, and the cross-thread interrupt does not reach Codex App Server. It is a side-channel cleanup.

## Expected Behavior

For authority-bearing E2EE sessions, `session.interrupt` should not reveal whether the requested session id exists outside the bound thread.

If the requested session is missing or unauthorized, return the same generic error shape.

## Acceptance

- `session.interrupt` for a different known thread returns the same generic rejection as an unknown or missing session under an authority-bound E2EE session.
- The generic response does not reveal whether the target thread exists or is attached.
- Normal same-thread interrupt behavior remains unchanged.
- Loopback or legacy non-authority dispatch remains unchanged unless the implementation explicitly chooses to normalize it too.
- Regression test covers known-cross-thread and unknown-thread interrupt parity.

## Non-Goals

- Do not reopen the daemon thread authority P0.
- Do not change relay ticket semantics.
- Do not broaden this into WebSocket rate limiting or frame abuse limits.

