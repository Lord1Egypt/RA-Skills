---
title: "Remote Control daemon commands must be bound to the ticket thread"
status: done
priority: P0
owner: Cody
repo: wip-codex-remote-control-private
created: 2026-05-05
security_gate: LIVE BLOCKED for broad dogfood
---

# Remote Control Daemon Thread Authority Binding

## Problem

The hosted relay routes browser sockets by `agentId:threadId`, but after E2EE decrypt the daemon dispatches `session.send`, `session.interrupt`, and `session.close` by whatever `sessionId` is inside the encrypted payload.

A browser connected for thread A could potentially attach to, send to, interrupt, or close thread B if it knows the session id and the daemon has that session attached.

This violates the product contract from the generated Remote Control URL: this URL controls only the Codex session named in the URL.

This blocks broad dogfood. Parker-only co-presence can continue with stop-on-first-failure.

## Security Review Evidence

Verdict:

```text
PASS PRIVATE ONLY. LIVE BLOCKED for broad dogfood until fixed.
```

Source pointers from review:

- `repos/ldm-os/apps/wip-codex-remote-control-private/src/dispatch.ts:24`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/dispatch.ts:51`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/dispatch.ts:118`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/relay-client.ts:175`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/relay-client.ts:140`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/codex-manager.ts:267`
- `repos/ldm-os/apps/wip-codex-remote-control-private/src/mcp.ts:90`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2771`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:3052`

Additional review finding:

- Relay ticket is bound to `(agentId, threadId)`, but after WebSocket open the relay forwards encrypted frames to the daemon without passing an authoritative route scope.
- `session.attach` trusts `req.threadId`.
- `codex-manager` accepts any UUID-shaped thread by asking App Server to resume it.
- Hosted auth review confirmed the same boundary: encrypted frames dispatch directly after relay forwarding, and dispatch resolves arbitrary session refs.

## Expected Behavior

Each E2EE browser session is bound to the ticket/thread at handshake.

After binding:

- `session.send` is accepted only for the bound thread.
- `session.attach` is accepted only for the bound URL/ticket thread.
- `session.interrupt` is accepted only for the bound thread.
- `session.close` is accepted only for the bound thread.
- Stop interrupts only the bound thread's active App Server turn.
- Browser A on thread A cannot affect thread B for the same agent.
- A malformed or cross-thread command is rejected, logged with metadata only, and never forwarded to App Server.

## Likely Implementation

- Store the allowed thread/session id on the daemon-side E2EE session after bootstrap or attach.
- Have the relay wrap or sign route scope so the daemon can enforce the URL ticket's bound thread after decrypting.
- Validate every decrypted command against that binding before dispatch.
- Treat missing binding as fail-closed.
- Include `sessionId`, bound thread id, and command type in safe structured logs, without secrets or plaintext prompt content.

## Acceptance

- Browser ticket for thread A can send to thread A.
- Browser ticket for thread A cannot `session.attach` thread B.
- Browser ticket for thread A cannot send to thread B.
- Browser ticket for thread A cannot interrupt thread B.
- Browser ticket for thread A cannot close thread B.
- Stop only interrupts the active turn for the bound thread.
- Cross-thread Stop is rejected.
- Two browsers on the same thread still work.
- Two browsers on the same agent but different threads cannot send, stop, close, or receive each other's frames.
- Regression test covers cross-thread command rejection.

## Closure

Closed on 2026-05-11 after:

- `wip-codex-remote-control-private` PR #68 and PR #69 shipped daemon-side E2EE session thread binding;
- `wip-ldm-os-private` PR #881 shipped relay-side route injection and validation;
- hosted deploy verification passed with healthy `/health`;
- Parker live smoke passed with browser to TUI and TUI to browser markers;
- behavior was documented in `wip-codex-remote-control-private/TECHNICAL.md`.

## Non-Goals

- Do not change relay fanout semantics for same-thread peers.
- Do not make the hosted relay the session authority.
- Do not weaken E2EE or inspect plaintext commands on the relay.
