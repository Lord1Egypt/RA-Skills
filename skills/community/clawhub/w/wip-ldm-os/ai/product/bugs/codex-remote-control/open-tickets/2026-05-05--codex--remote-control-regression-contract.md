---
title: "Remote Control co-presence must have a durable regression contract"
status: open
priority: P0
owner: Cody
repo: wip-codex-remote-control-private / wip-ldm-os-private / openai-codex-private
created: 2026-05-05
---

# Remote Control Regression Contract

## Problem

Remote Control co-presence now works. That creates a new risk: future changes to the daemon, hosted relay, browser UI, or patched Codex path could silently degrade the product back into handoff, single-browser mode, stale-thread attach, or a parallel runner.

We need one durable contract that says what must stay green.

## Contract

The following flow is the minimum Remote Control v1 product contract:

1. Start a fresh patched Codex TUI:

   ```text
   codex-wip
   ```

2. In Codex, say:

   ```text
   start remote control
   ```

3. The MCP tool returns the current live session URL.
4. Browser A opens the URL and attaches to the current thread.
5. Browser B opens the same URL and attaches to the current thread.
6. Browser A sends a message. Browser B and the TUI receive it.
7. Browser B sends a message. Browser A and the TUI receive it.
8. The TUI sends a message. Browser A and Browser B receive it.
9. Closing Browser A leaves Browser B connected.
10. Refreshing Browser B reattaches to the thread.
11. Refreshing Browser B hydrates the existing transcript.
12. Browser Stop interrupts the shared live App Server turn.
13. Hosted MCP reload does not require `codex-daemon link`.

## Security Regression Rows

These rows must stay green before any non-Parker user is added:

- [ ] PM2 reload of `mcp-server` preserves daemon E2EE registration. User does not have to re-pair.
- [ ] Repeat `/api/codex-relay/pair-complete` with a paired user's `apiKey` rejects without a fresh passkey assertion.
- [ ] `/api/codex-relay/pair-status/<pairing_id>` without the daemon-bound poll token returns `401`, not the `apiKey`.
- [ ] Browser ticket for thread A cannot `session.attach`, `session.send`, `session.close`, or `session.interrupt` thread B.
- [ ] After E2EE ready, browser plaintext protocol messages are ignored or rejected.
- [ ] Relay WebSocket frame and byte floods are rate-limited or disconnected.

## Current Status

Green from live dogfood:

- `start remote control` returns the current session URL.
- Browser A attaches.
- Browser B attaches.
- Browser A to TUI works.
- Browser B to TUI works.
- TUI to both browsers works.
- Closing one browser leaves the other alive.
- Refreshing a browser can reattach.

Still open:

- Refresh hydration must render existing thread history.
- Stop must interrupt shared state and update all peers.
- Hosted MCP reload must not require relink.
- Browser transcript rendering still needs UI fidelity work.
- Non-Parker users are blocked until the security rows above are green.

## Acceptance

- This contract is referenced by every Remote Control release, deploy, or significant refactor.
- The contract is added to the Remote Control dogfood checklist.
- Each green item has either an automated test, a manual smoke step, or an explicitly tracked test gap.
- The security rows above become automated tests when their fixes land, not just manual smoke steps.
- New changes that touch `codex-daemon`, hosted relay, Remote Control browser UI, or patched Codex App Server cite this contract in their validation notes.

## Non-Goals

- Do not implement the tests in this ticket.
- Do not solve refresh hydration here.
- Do not solve Stop here.
- Do not change the patched Codex install path here.
