---
title: "Remote Control daemon duplicate-connection takeover should be throttled and visible"
status: done
priority: P1
owner: VPS security coder / Cody
repo: wip-ldm-os-private
created: 2026-05-06
---

# Remote Control Daemon Takeover Throttling

## Problem

A new daemon WebSocket connection with the same `ck` currently replaces the previous daemon connection. That is useful for normal daemon restarts, but a stolen `ck` can repeatedly reconnect and keep the legitimate daemon offline.

Combined with re-pair weaknesses, this creates a takeover loop: attacker rebinds the daemon public key, then keeps the daemon socket.

## Security Review Evidence

Finding:

```text
M2. Daemon takeover via duplicate ck- connection is allowed silently.
```

Source pointer from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2972`

## Expected Behavior

Duplicate daemon connection replacement remains possible for legitimate restarts, but it is throttled and visible:

- allow occasional replacement,
- rate-limit repeated replacements,
- log replacement metadata safely,
- expose current daemon connection metadata where useful,
- detect suspicious replacement loops.

## Acceptance

- One normal daemon restart can replace the prior connection.
- Rapid repeated daemon replacements are rate-limited or rejected.
- Replacement logs include safe metadata: agent id or account id, old connection age, new connection source metadata where safe, timestamp.
- Pair/status or diagnostics can expose active daemon connection age or last replacement time.
- Regression covers repeated replacement throttling.

## Closure

Closed on 2026-05-12 after:

- `wip-ldm-os-private` PR #895 shipped daemon online activation only after accepted `daemon.identity`;
- `@wipcomputer/wip-ldm-os@0.4.85-alpha.19` deployed the hosted relay change;
- hosted deploy verification passed with healthy `/health`;
- duplicate daemon reconnect while a daemon is already online closes with `4004` and `daemon already online`;
- daemon frames before identity acceptance close with `1008` and `daemon identity required`;
- behavior was documented in `wip-codex-remote-control-private/TECHNICAL.md` under the pair and relink fresh presence section.

## Non-Goals

- Do not prevent legitimate daemon restart.
- Do not print `ck` tokens or daemon secrets in logs.
- Do not solve pair/relink fresh presence here.
