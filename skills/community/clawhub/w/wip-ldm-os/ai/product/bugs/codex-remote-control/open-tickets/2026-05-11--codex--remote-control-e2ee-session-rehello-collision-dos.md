---
title: "Remote Control E2EE re-hello can replace an existing session id"
status: open
priority: P2
owner: unassigned
repo: wip-codex-remote-control-private
created: 2026-05-11
security_gate: hardening follow-up; daemon thread authority P0 remains closed
---

# Remote Control E2EE Re-Hello Session Collision DoS

## Problem

During E2EE setup, the browser supplies `msg.session`. If the daemon already has an encrypted session with the same id, `relay-client.ts` currently replaces the old key state for that session id.

That does not appear to be an authority bypass because the relay injects the ticket-bound `route_thread_id` and the daemon binds commands to that route. A cross-thread command still cannot pass authority checks.

The remaining risk is denial of service: a second browser that guesses, reuses, or replays another browser's E2EE session id could replace that session's key slot and break the first browser session.

## Expected Behavior

Harden re-hello handling so one browser cannot cheaply evict another active encrypted session.

Possible fixes:

- reject `e2ee.hello` for an already-active session id unless it comes from the same WebSocket;
- bind the E2EE session id to the WebSocket that established it;
- require a fresh, high-entropy daemon-generated nonce or relay-issued binding as part of the handshake;
- close the old WebSocket explicitly with a structured reason if replacement is intentional.

Pick the smallest fix that preserves reconnect behavior and keeps the relay unable to inspect plaintext commands.

## Acceptance

- A second WebSocket cannot silently replace an active E2EE session id owned by another WebSocket.
- Legitimate reconnect or refresh behavior still works.
- Cross-thread authority remains enforced by the ticket-bound route.
- Regression test covers duplicate `e2ee.hello` for an active session id from a different WebSocket.
- The test distinguishes denial-of-service hardening from authority bypass.

## Non-Goals

- Do not reopen the daemon thread authority P0.
- Do not change public pairing UX.
- Do not add broad WebSocket abuse limits here. Frame size and rate limits remain tracked separately.

