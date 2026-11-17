---
title: "Remote Control tenant boundary must not depend on user-entered display label"
status: done
priority: P0
owner: hosted auth token security K-partner / Cody
repo: wip-ldm-os-private
created: 2026-05-06
security_gate: BLOCKED for non-Parker users
closed: 2026-05-06
---

# Remote Control AgentId Tenant Boundary

## Problem

`agentId` is currently the relay tenant boundary, but registration previously let user-entered labels bleed into tenant identity.

The signup prompt asks what Lēsa should call the user. That value is a display label or passkey label, not a public username and not a security handle. A real user must not be able to choose a label such as `parker-smoke-test`, mint their own `ck` key for that same tenant namespace, and reach Parker's daemon namespace.

This is a critical blocker for non-Parker users.

## Security Review Evidence

Review verdict:

```text
BLOCKED for non-Parker users. PASS PRIVATE ONLY for Parker smoke/co-presence while blockers are fixed.
```

Source pointers from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:464`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:680`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2561`

Observed runtime evidence:

- live PM2 logs showed active `parker-smoke-test` relay traffic.
- label sanitize is shape cleanup only.
- registration used to derive `agentId` from `stored.username`.
- relay maps daemons and web clients by immutable `agentId`.

## Expected Behavior

Remote Control relay tenancy must use immutable account identity, not a user-entered display label.

Required shape:

- account/user id is the authoritative tenant key,
- display names, nicknames, passkey labels, and `identity.handle` are user-facing metadata only,
- duplicate display labels are allowed unless a separate public-username product decision introduces real handles later,
- relay auth routes by account id or durable internal subject, not a mutable or user-selected label,
- no user can claim another user's relay namespace by choosing the same display label.

Future WIP Directory handles are a separate product surface. They are expected to be DNS-like identity names for ownership, routing, Agent Pay, and trust. They need their own model, preferences UI, reservation rules, transfer/recovery policy, and security review. Do not accidentally implement that future namespace by making the signup display label globally unique.

## Acceptance

- Duplicate display label registration does not collide tenants.
- User-entered labels such as `parker-smoke-test` remain display metadata and cannot claim internal tenant namespaces.
- Two accounts can choose the same display label and still receive different immutable tenant IDs.
- Browser relay tickets bind to immutable account id plus thread id.
- Daemon relay registration binds to immutable account id plus device identity.
- Display label changes do not move or expose daemon namespaces.
- A regression proves a second account cannot mint a browser ticket or daemon auth for Parker's namespace by choosing Parker's display label.
- Existing Parker smoke path is migrated without losing paired daemon state.

## Closure Evidence

Implemented in PR #835 with follow-up clarification in PR #856. Released as `@wipcomputer/wip-ldm-os@0.4.85-alpha.7` and deployed to the hosted MCP relay.

Validation after deploy:

- `npm run test:crc-agentid-tenant-boundary` passed.
- `npm run test:crc-pair-login-flow` passed.
- `node --check src/hosted-mcp/server.mjs` passed.
- Parker completed the live Remote Control co-presence smoke after deploy.

## Non-Goals

- Do not redesign display names or profile UI beyond what is required to separate identity from display labels.
- Do not weaken passkey auth.
- Do not make the hosted relay session authority for Codex turns.
