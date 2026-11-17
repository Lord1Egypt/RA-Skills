---
title: "Remote Control co-presence needs scoped security review lanes"
status: open
priority: P0
owner: K-partner / VPS security coder / CODI partner
repo: wip-ldm-os-private / wip-codex-remote-control-private / openai-codex-private
created: 2026-05-05
---

# Remote Control Security Review Lanes

## Problem

Remote Control now lets a browser or phone drive a live local Codex TUI session through:

```text
browser or phone -> hosted relay -> local daemon -> TUI-owned Codex App Server socket -> live Codex session
```

That is the right product shape, but it must be reviewed as a security boundary, not just a UX feature.

The review must stay scoped to the working primitive. Do not spend this pass on UI polish.

## Review Lanes

### Remote Control Security K-partner

Review the product trust boundary:

- browser to relay to daemon to App Server,
- local TUI remains session authority,
- hosted relay is transport and login surface only,
- browser attach is scoped to the intended thread,
- multi-browser fanout does not create cross-thread leakage,
- Stop cannot interrupt the wrong thread or wrong user session,
- stale URLs and refreshed tabs cannot attach outside authorization.

### Hosted Auth Token Security K-partner

Review auth and identity:

- passkey login session boundary,
- pair URL and code lifetime,
- daemon identity binding,
- `parker-smoke-test` isolation from real users,
- browser session tokens,
- daemon relay tokens,
- thread URL authorization,
- whether relink or re-pair can be abused to replace a daemon identity.

### VPS Security Coder

Review hosted relay and deployment posture:

- PM2 reload behavior,
- in-memory versus durable daemon key registry,
- Postgres persistence for daemon public keys,
- rate limits on pair, bootstrap, and websocket attach,
- websocket fanout resource limits,
- denial-of-service risks from many tabs or stale sockets,
- log redaction for tokens, pair codes, public keys, and thread IDs where needed.

### VPS Security CODI Partner

Review abuse paths and operational controls:

- hosted relay tunnel-abuse risk,
- whether relay can be used as a generic encrypted tunnel,
- daemon reconnect behavior after relay reload,
- monitoring for suspicious attach or pair attempts,
- incident response if a daemon key or relay token is compromised,
- safe defaults for public-alpha dogfood.

## Acceptance

- Each lane returns a short finding list with severity: `BLOCKER`, `P0`, `P1`, or `INFO`.
- Each accepted finding becomes a linked bug ticket.
- The review explicitly states whether broader dogfood can continue.
- The review explicitly states whether any hosted deploy must be blocked.
- No review claims UI polish is a security blocker unless it affects auth, attach, pairing, thread identity, Stop, or E2EE trust.

## Non-Goals

- Do not review color, spacing, footer removal, or raw JSON rendering here unless it creates a security ambiguity.
- Do not redesign the Remote Control architecture in this ticket.
- Do not require upstream OpenAI changes before reviewing WIP's relay, daemon, and browser boundaries.
