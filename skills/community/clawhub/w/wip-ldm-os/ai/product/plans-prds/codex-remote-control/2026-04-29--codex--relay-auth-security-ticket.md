# Codex Remote Control Relay Auth Security Ticket

**Date:** 2026-04-29  
**Reporter:** Codex  
**Status:** Open  
**Priority:** P0 for dogfood, P1 for storage hardening  
**Scope:** `src/hosted-mcp/server.mjs`, `src/hosted-mcp/app/codex-remote-control/`, `wip-codex-remote-control-private`

## Summary

Codex Remote Control has the right local daemon direction: E2EE-capable daemons reject plaintext relay traffic, and the daemon-side gate tests pass. The remaining high-risk holes are in the hosted relay and browser app contract.

The current phone page still opens the relay WebSocket with a long-lived `ck-` bearer in the URL and sends plaintext `session.*` messages. The hosted relay has newer `/bootstrap` and `/ws-ticket` support, but the shipped browser page does not consume it yet. The server also still accepts `?token=ck-...` WebSocket fallback for compatibility.

This is not Memory Crystal. The JSON fallback issue below belongs to hosted MCP / Kaleidoscope auth and relay credentials. It affects control credentials such as `ck-...` API keys, not Memory Crystal's memory store directly. It could indirectly expose memory actions only if another API behind the same token grants memory capabilities.

## Product Boundary

Codex Remote Control is a control plane:

- A browser or phone page sends instructions to a local Codex daemon.
- The relay at `wip.computer` forwards between the phone and daemon.
- The local daemon can start, attach, send, interrupt, close, and list Codex sessions.

Because this controls a local coding agent, bearer-token leakage or relay hijack is not just account risk. It can become local machine control within whatever Codex sandbox and approval mode the local session is running.

## Current Evidence

- Local daemon E2EE and plaintext rejection exist in `wip-codex-remote-control-private/src/relay-client.ts`.
- Local daemon gate tests passed on 2026-04-29 after allowing the loopback WebSocket test server: `20 passed, 0 failed`.
- Hosted relay exposes `/api/codex-relay/bootstrap/:threadId` and `/api/codex-relay/ws-ticket` in `src/hosted-mcp/server.mjs`.
- Hosted relay still accepts browser WebSocket auth through `?token=ck-...` in `src/hosted-mcp/server.mjs`.
- Phone app still opens `/api/codex-relay/web/<threadId>?token=<ck>` in `src/hosted-mcp/app/codex-remote-control/index.html`.
- Phone app currently sends plaintext `session.start`, `session.send`, and `session.interrupt` messages.
- The hosted server still has hardcoded default `ck-...` keys in source.
- Hosted auth silently falls back from Prisma to JSON files and writes plaintext token backups.

## Threat Model

### A1: Malicious browser page or extension

Goal: drive the user's Codex daemon from a web context.

Path today:

1. Obtain or reuse a `ck-...` token from `sessionStorage`, URL logs, browser extension access, DevTools, proxy logs, or historical nginx logs.
2. Open `/api/codex-relay/web/<threadId>?token=<ck>`.
3. Send `session.*` messages.

Required fixes:

- No long-lived bearer token in WebSocket URLs.
- WebSocket Origin allowlist.
- Short-lived single-use ticket for browser WebSocket upgrade.
- E2EE-only relay payloads.

### A2: Stolen `ck-...` bearer

Goal: impersonate a paired user or daemon.

Path today:

- Use the token against `/bootstrap`, `/ws-ticket`, or WS fallback.
- If hardcoded defaults ever worked in production, use those known keys directly.

Required fixes:

- Remove hardcoded default keys from source.
- Rotate every currently known or historically logged `ck-...` key.
- Reject historically known default keys even if present in a backup file.
- Hash API keys at rest and compare by keyed hash.
- Add rate limits and audit logs for token validation and ticket minting.

### A3: Relay subscription to other threads

Goal: read output from other active remote-control threads for the same agent.

Path today:

- Daemon-to-web messages are forwarded to all web sockets whose key starts with `agentId:`, not only the matching `agentId:threadId`.
- E2EE reduces this if both sides are using encrypted frames, but the current phone app is plaintext.

Required fixes:

- Route daemon responses by session or thread, not all sockets for the agent.
- If the daemon cannot know the target thread from the encrypted envelope, define an outer non-sensitive routing envelope that does not leak prompt or output content.
- Add tests proving one thread's events are not visible to another thread's browser socket.

### A4: Data store downgrade

Goal: keep auth running from weaker storage or steal plaintext credentials.

Path today:

- If Prisma cannot connect, hosted MCP logs that it is using JSON files and continues.
- API keys are written to a plaintext JSON backup even when Prisma is active.

Required fixes:

- Production must fail closed when Prisma is unavailable.
- JSON fallback must require an explicit dev-only env flag.
- Token backups must be removed, encrypted with strict retention, or replaced by non-sensitive metadata.

## Required Fixes

### P0: Browser must use the secure relay contract

Implement the phone app flow:

1. Read `wip_api_key` from session storage only long enough to call authenticated HTTPS endpoints.
2. Call `GET /api/codex-relay/bootstrap/:threadId`.
3. Require `e2ee_available === true` for production.
4. Generate browser ephemeral ECDH keypair.
5. Call `POST /api/codex-relay/ws-ticket` with `thread_id`.
6. Open WebSocket with a short-lived single-use ticket, not `ck-...`.
7. Send `e2ee.hello`.
8. Send all `session.*` messages only inside `e2ee.frame`.

Acceptance:

- DevTools WS URL never contains `ck-`.
- Browser sends no plaintext `session.*` frames over the relay.
- Daemon receives and decrypts `e2ee.frame`.
- If bootstrap says E2EE is unavailable in production, the UI refuses remote control.

### P0: Remove production `?token=ck-...` WebSocket fallback

The server can keep a dev-only fallback if explicitly gated, but production must reject browser WebSocket upgrades that use long-lived `ck-` tokens in the query string.

Acceptance:

- `GET /api/codex-relay/web/:threadId?token=ck-anything` returns 401 in production.
- Existing `/ws-ticket` flow still works.
- Tests cover both production and dev-mode behavior.

### P0: Route daemon responses to the matching browser session

The daemon side currently broadcasts each daemon frame to every web client for the same agent. That must narrow to the intended thread or session.

Acceptance:

- Two browser sockets for the same agent but different threads do not receive each other's daemon events.
- Test proves cross-thread message isolation.
- Routing metadata does not include prompt text, command output, or agent response text.

### P0: Remove hardcoded API keys and rotate exposed keys

Delete source-level `ck-...` defaults. Move dev fixtures to local-only config or test-only setup.

Acceptance:

- `rg 'ck-[A-Za-z0-9_-]{6,}' src/hosted-mcp` returns no production key constants.
- Previously hardcoded keys are rejected by `/bootstrap`, `/ws-ticket`, and WS upgrade.
- Production keys are rotated after log audit.

### P0: WebSocket Origin allowlist

Add an env-driven allowlist for browser WebSocket upgrades.

Acceptance:

- Allowed production origins can connect.
- Disallowed origins are rejected before ticket or token validation.
- Raw non-browser clients are still governed by ticket and bearer semantics. Origin is a browser defense, not the only defense.

### P1: Production auth storage must fail closed

Hosted MCP must not silently continue from JSON token files in production.

Acceptance:

- With Prisma unavailable in production mode, token minting and validation fail with 5xx.
- JSON fallback only works with an explicit dev-mode flag.
- Production startup logs make the active storage mode unambiguous.
- Plaintext API-key JSON backup is removed or replaced with a non-sensitive alternative.

### P1: Hash control credentials at rest

Do not store raw `ApiKey.key` or `Device.token` values.

Acceptance:

- Postgres stores keyed hashes plus display metadata such as prefix or last four.
- Runtime auth compares presented tokens by keyed hash.
- Migration rotates or reissues existing plaintext keys.
- Backups and logs contain no raw `ck-...` or `dk-...` values.

### P1: Rate limits and audit logs

Add basic abuse controls around authority-minting and validation endpoints.

Acceptance:

- Rate limits cover `/webauthn/*`, `/api/codex-relay/pair-init`, `/pair-status`, `/pair-complete`, `/bootstrap`, `/ws-ticket`, and WS upgrade failures.
- Logs record non-sensitive markers: route, agent id when known, result, rate-limit hit, ticket mint, ticket consume.
- Logs never include full API keys, tickets, prompts, command output, or decrypted payloads.

## Validation Plan

1. Run static checks:

   ```bash
   rg 'ck-[A-Za-z0-9_-]{6,}' src/hosted-mcp
   rg '\\?token=|token=' src/hosted-mcp/app src/hosted-mcp/server.mjs
   rg 'session\\.' src/hosted-mcp/app/codex-remote-control src/hosted-mcp/server.mjs
   ```

2. Run daemon package gates:

   ```bash
   cd repos/ldm-os/apps/wip-codex-remote-control-private
   npm test
   ```

3. Add hosted relay unit tests for:

   - ticket mint and consume
   - token fallback rejection in production
   - Origin allowlist
   - cross-thread isolation
   - Prisma fail-closed behavior

4. Live staging checks:

   - Confirm `/api/codex-relay/bootstrap/:threadId` returns JSON, not homepage HTML.
   - Confirm `/api/codex-relay/ws-ticket` mints a 60-second single-use ticket.
   - Confirm WebSocket URL contains ticket only, never `ck-`.
   - Confirm nginx and PM2 logs redact ticket query strings.
   - Confirm a stale or reused ticket is rejected.

5. Historical log audit before dogfood:

   - Search nginx access and error logs for `ck-`, `?token=`, `key=`.
   - Search PM2 logs for token-shaped strings.
   - Rotate any key that appears in any log.

## Done Definition

Dogfood can resume when:

- Browser relay traffic is E2EE-only.
- Browser WS auth uses short-lived single-use tickets, not long-lived `ck-` query params.
- Production rejects token fallback.
- Hardcoded default keys are gone and rotated.
- WebSocket Origin allowlist is active.
- One user's thread cannot receive another thread's events.
- Hosted auth fails closed when Prisma is unavailable.
- Logs and persistent stores do not expose raw control credentials.

