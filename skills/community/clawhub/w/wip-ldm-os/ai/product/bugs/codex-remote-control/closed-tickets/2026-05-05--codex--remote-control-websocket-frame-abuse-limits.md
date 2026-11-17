---
title: "Remote Control WebSocket frames need abuse limits after ticket attach"
status: done
priority: P1
owner: VPS security coder / CODI partner
repo: wip-ldm-os-private / wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control WebSocket Frame Abuse Limits

## Problem

HTTP mint, validate, and status endpoints are rate-limited, but once a browser has a valid ticket the relay forwards every browser WebSocket frame to the daemon.

That established WebSocket path is now the main tunnel-abuse surface.

## Security Review Evidence

Review finding:

```text
P1: HTTP rate limits do not cover established WebSocket frame abuse.
```

Additional source pointers from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:3052`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2595`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:381`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/nginx/codex-relay.conf:81`

The relay should not become a generic high-throughput encrypted tunnel to a user's Mac.

## Expected Behavior

Both hosted relay and daemon enforce reasonable limits for established browser connections:

- max frame size,
- max messages per time window,
- max bytes per time window,
- max browser sockets per `(agentId, threadId)`,
- idle connection TTL,
- per-agent kill switch,
- per-ticket message rate,
- max malformed frames per connection,
- max pending bytes or queued frames,
- disconnect behavior when limits are exceeded,
- metadata-only logging for violations.

Limits should be strict enough for public-alpha safety and adjustable as real usage becomes clearer.

## Acceptance

- Oversized browser frames are rejected or disconnected.
- Message floods are rate-limited or disconnected.
- Byte floods are rate-limited or disconnected.
- Too many browser sockets for one `(agentId, threadId)` are rejected or disconnected.
- Idle connections are closed.
- Per-agent kill switch can stop new attach and active forwarding during an incident.
- Long nginx WebSocket timeouts do not allow unbounded idle or flood behavior at the app layer.
- Malformed frame floods are rate-limited or disconnected.
- Legitimate Remote Control message streaming still works.
- Multi-browser fanout still works.
- Browser-specific E2EE session frames still route only to the owning browser socket.
- Thread-routed daemon frames still fan out to same-thread browser peers.
- Logs include connection id, agent id, thread id where available, and reason, but no decrypted prompt contents or secrets.

## Implementation PR

2026-05-12 Cody implementation slice:

- adds hosted relay browser WebSocket abuse limits for established Remote Control connections;
- enforces max frame bytes, message rate, byte rate, max malformed frames, max pending daemon bytes, idle TTL, per-thread browser socket cap, and operator kill switch;
- keeps logs metadata-only: reason, tenant id, thread id, and generated connection id;
- preserves daemon-to-browser streaming and same-thread multi-browser fanout;
- adds `npm run test:crc-websocket-abuse-limits` plus deploy inventory coverage for the new hosted relay module.

This ticket should move to `done` only after PR merge, hosted deploy verification, and Parker live co-presence smoke.

## Closure

Closed on 2026-05-12 after:

- `wip-ldm-os-private` PR #908 merged;
- `@wipcomputer/wip-ldm-os@0.4.85-alpha.23` published on the alpha dist-tag;
- hosted MCP deploy completed and reloaded PM2;
- `/health` returned healthy with Postgres;
- deploy manifest verified `25 ok, 0 mismatched`, including `codex-relay-ws-abuse-limits.mjs`;
- Parker live smoke passed after deploy.

## Non-Goals

- Do not block normal Codex streaming output.
- Do not add plaintext inspection to the hosted relay.
- Do not solve daemon key persistence here.
