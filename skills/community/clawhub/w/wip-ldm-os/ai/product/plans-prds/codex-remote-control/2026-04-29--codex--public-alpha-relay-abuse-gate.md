# Codex Remote Control Public Alpha Relay Abuse Gate

**Date:** 2026-04-29  
**Reporter:** Codex  
**Status:** Open  
**Priority:** P0 before broad public alpha, P1 for Agent Pay integration  
**Scope:** `src/hosted-mcp/server.mjs`, Codex relay routes, Kaleidoscope passkey auth, future Agent Pay gate

## Summary

Codex Remote Control should be useful now. The product should not wait for full Agent Pay before Parker can dogfood it or before a small number of users can try it. OpenAI or another company may eventually ship an official version; this project is both a tool we need today and a proof of concept for WIP's identity, permission, and payment architecture.

The immediate security goal is therefore not "build the final enterprise remote-control platform." The immediate goal is narrower:

> The free public alpha must not let `wip.computer` become an anonymous, unlimited, generic encrypted tunnel.

The earlier relay-auth ticket covers token hijack, E2EE, hardcoded keys, and storage weaknesses. This ticket covers the adjacent abuse boundary: even a legitimate user, or a newly created fake user, should not be able to treat the VPS as free relay infrastructure for non-Codex traffic.

## Product Position

This alpha can be free. Free does not mean anonymous or unlimited.

The desired shape:

- A user signs in with passkey.
- The user pairs a Codex daemon.
- The relay mints short-lived, scoped tickets.
- The relay forwards only Codex Remote Control protocol envelopes.
- The relay meters messages, bytes, sockets, and session lifetimes.
- WIP can revoke abuse quickly.
- Agent Pay later attaches to the same meter as an approval and payment layer.

Agent Pay is important, but it should not block the current release. It becomes the next layer: "Do you want to use Codex Remote Control today? It costs one cent from the starter wallet." The existing `/demo` already demonstrates the pattern: passkey approval, simulated wallet balance, a small per-action cost, and a receipt-style UI.

## Demo Pattern To Reuse Later

The current Kaleidoscope demo already has the bones of the future Agent Pay gate:

- WebAuthn passkey registration and auth verification in `src/hosted-mcp/server.mjs`.
- Agent authorization challenges through `/demo/api/agent-auth`, `/approve`, and `/demo/api/agent-auth/status`.
- Simulated wallet accounting with `INITIAL_BALANCE_CENTS = 500` and `IMAGE_COST_CENTS = 1`.
- Per-action balance deduction after a successful generated action.
- UI copy that makes the cost and remaining balance visible to the user.

For Codex Remote Control, the same idea should eventually become:

- starter wallet credit for each user
- one-cent daily/session/use approval
- passkey confirmation for paid grant
- spending record tied to relay quota
- revocation and receipts

But the free alpha should first implement the same underlying control plane without requiring payment:

- identity
- quota
- scoped grant
- audit metadata
- revocation

## Threat Model

### A1: VPS as arbitrary message bus

An attacker creates a passkey account, pairs a fake daemon, opens a fake web client, and uses the relay to shuttle encrypted payloads unrelated to Codex.

Risk:

- WIP pays bandwidth and compute for non-product traffic.
- `wip.computer` becomes a covert transport domain.
- Security vendors may classify the domain or IP as suspicious.
- Abuse reports arrive before the product is mature enough to respond.

### A2: VPS as low-bandwidth command channel

An attacker uses E2EE frames as opaque command-and-control traffic. The relay cannot inspect payloads by design.

Risk:

- E2EE privacy becomes indistinguishable from arbitrary opaque tunneling unless the server enforces outer envelope, rate, and lifetime.
- WIP has no safe way to prove the relay is only product-scoped.

### A3: Resource exhaustion by "free" users

Legitimate signups or bots consume many sockets, reconnect rapidly, leave sessions open, or push large messages.

Risk:

- Node and nginx resources are consumed cheaply.
- Real users see degraded remote-control sessions.
- Logs and storage grow without useful product value.

### A4: Token sharing and account resale

Users share relay tokens or automate account creation to sell or outsource relay capacity.

Risk:

- A free alpha becomes a commodity relay.
- Abuse is hard to tie back to a real human decision.

## Non-Goals

- Do not block the alpha on full Agent Pay.
- Do not weaken remote Codex into a toy. The phone should be able to drive Codex with the same effective permissions as the local session once the user is authenticated and paired.
- Do not inspect decrypted prompts or Codex output on the VPS.
- Do not add generic content moderation of remote-control payloads.
- Do not build a full billing system before the proof of concept needs it.

## Required Free-Alpha Gate

### P0: Passkey account required for relay use

Relay-capable use must be tied to a passkey account or an agent token approved by a passkey account.

Acceptance:

- Anonymous clients cannot open daemon or web relay sockets.
- Anonymous clients cannot mint WebSocket tickets.
- Pairing and relay use resolve to a stable account or handle in logs.

### P0: Relay-specific grants

Codex Remote Control should use a scoped relay grant instead of treating a broad `ck-...` token as permanent relay authority.

Acceptance:

- Grant records identify product: `codex_remote_control`.
- Grant records identify scope: daemon pairing, web ticket mint, or both.
- Grants have explicit creation time, last-used time, and revocation state.
- A revoked grant cannot mint tickets or connect sockets.

### P0: Protocol envelope allowlist

The relay should accept only the outer protocol shapes required for Codex Remote Control.

Allowed outer message types:

- `e2ee.hello`
- `e2ee.ready`
- `e2ee.error`
- `e2ee.frame`
- optional `ping` / `pong`

Rejected:

- binary streams
- arbitrary JSON message types
- `connect`
- `fetch`
- `proxy`
- `upload`
- `download`
- raw byte-forwarding verbs

Acceptance:

- Unknown outer message types close the socket with a non-sensitive close reason.
- Binary frames are rejected unless explicitly introduced by a future protocol version.
- The relay never adds generic forwarding routes.

### P0: Message and bandwidth caps

The relay must meter outer-envelope traffic even when it cannot inspect encrypted content.

Initial suggested limits for free alpha:

- max frame size: 256 KB
- max messages per minute per socket: 120
- max bytes per minute per account: conservative default, configurable by env
- max bytes per day per account: conservative default, configurable by env
- max failed WS upgrades per IP per minute: low default

Acceptance:

- Oversized frames are rejected.
- Repeated high-rate frames trigger 429-style close behavior.
- Limits are applied before expensive processing.
- Limits are visible in metadata logs.

### P0: Socket and session caps

The relay should make tunnel-like use inconvenient and bounded.

Initial suggested limits for free alpha:

- max daemon sockets per account: 1 active daemon
- max browser sockets per account: 3 active browser sockets
- max relay sessions per account per day: configurable
- idle timeout: 5 minutes without useful traffic
- max socket lifetime: 2 hours
- reconnect throttle per account and IP

Acceptance:

- New daemon connection replaces or rejects the old daemon according to explicit policy.
- Excess browser sockets are rejected or the oldest is closed.
- Idle sockets close automatically.
- Long-lived sockets close and require a fresh ticket.

### P0: Ticket-bound routing only

Browser WebSocket connections must be bound to account, daemon, and thread/session.

Acceptance:

- A ticket cannot be reused.
- A ticket cannot be used for another account.
- A ticket cannot be used for another thread or session.
- A ticket cannot outlive its TTL.
- A web socket without a valid ticket is rejected in production.

### P0: Abuse metadata logging

The relay needs enough metadata to detect and respond to abuse without logging prompts or outputs.

Log fields:

- timestamp
- account or handle
- route
- IP hash or truncated IP
- user agent hash
- daemon or web side
- ticket minted
- ticket consumed
- bytes in/out
- message count
- close reason
- limit hit

Never log:

- full API keys
- full tickets
- prompts
- command output
- decrypted payloads
- E2EE private keys

Acceptance:

- A single account's relay usage can be summarized by day.
- Abuse can be traced to account, token/grant, IP family, and route.
- Logs remain useful even though content is E2EE.

### P0: Kill switches

WIP needs operational escape hatches before public alpha.

Required switches:

- disable Codex relay globally
- disable relay for one account
- revoke one relay grant
- block one IP or subnet
- disable ticket minting while allowing existing sockets to drain
- emergency close all active relay sockets

Acceptance:

- Each switch can be applied without code changes.
- Each switch is visible in logs.
- Disabled users receive a clear non-sensitive error.

## Agent Pay Integration Later

Agent Pay should attach to this same gate once ready.

Future paid flow:

1. User signs in with passkey.
2. User gets starter wallet credit.
3. User requests Codex Remote Control use.
4. The UI shows the cost, such as `$0.01` for a day or session.
5. User approves with passkey or Face ID.
6. Server creates a relay grant and deducts from the wallet.
7. Relay quotas and kill switches still apply.

Important: Agent Pay is not the abuse gate by itself. Payment reduces abuse, but the relay still needs protocol, quota, socket, and revocation controls.

## Validation Plan

### Static checks

```bash
rg 'connect|proxy|tunnel|upload|download|raw' src/hosted-mcp/server.mjs
rg 'codex-relay' src/hosted-mcp/server.mjs
rg 'ck-[A-Za-z0-9_-]{6,}' src/hosted-mcp
```

### Unit tests

Add hosted relay tests for:

- anonymous ticket mint rejection
- revoked grant rejection
- unknown outer message rejection
- oversized frame rejection
- per-account socket cap
- ticket single-use behavior
- ticket wrong-thread rejection
- idle timeout
- max lifetime timeout

### Staging abuse tests

Use two custom clients and verify:

- They cannot pass arbitrary message types through the relay.
- They cannot keep unlimited sockets open.
- They cannot send large opaque frames.
- They cannot exceed daily byte/message quotas.
- They cannot reuse a ticket.
- They cannot use a ticket for another thread.
- Kill switch closes active sockets.

## Done Definition

The free public alpha is acceptable when:

- Relay use requires passkey-backed identity or approved agent identity.
- Relay authority is scoped to Codex Remote Control.
- Outer protocol is allowlisted.
- Message size, bandwidth, socket, session, idle, and reconnect caps exist.
- Tickets are short-lived, single-use, and route-bound.
- Metadata logging can diagnose abuse without payload inspection.
- WIP has per-account, per-grant, per-IP, route-level, and global kill switches.
- Agent Pay is documented as the next layer, not a blocker for free alpha.

