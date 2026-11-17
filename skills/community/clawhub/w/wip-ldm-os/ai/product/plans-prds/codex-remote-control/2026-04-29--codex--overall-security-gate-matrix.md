# Overall Security Codex Gate Matrix

**Date:** 2026-04-29  
**Owner:** Codex Remote Control security stream  
**Status:** Source of truth for current security gates  
**Scope:** Codex Remote Control private alpha, post-hardening dogfood, and public alpha readiness

## Purpose

This file is the current gate matrix for Codex Remote Control security. Use it as the first status check before answering whether the product can be dogfooded, exposed beyond Parker, or treated as public alpha.

Related detail tickets:

- `2026-04-29--codex--relay-auth-security-ticket.md`
- `2026-04-29--codex--public-alpha-relay-abuse-gate.md`
- `2026-04-28--cc-mini--codex-remote-control-live-test-runbook.md`
- `../../bugs/security/2026-04-28--cc-mini--vps-hosted-mcp-audit.md`

## Gate Matrix

| Gate | Current state | Meaning | Required next proof |
|------|---------------|---------|---------------------|
| Gate 1: pre-hardening baseline | Allowed, not complete | Parker and agents can keep inspecting, planning, and doing tightly scoped local validation. This does not authorize secure dogfood or broader users. | Capture the exact baseline evidence: current deployed route behavior, current relay auth behavior, current daemon behavior, current known weaknesses. |
| Postgres token check | Not complete | Hosted MCP auth storage and token handling are not yet proven safe enough to rely on as a hardened production gate. | Prove whether production is using Postgres or JSON fallback; prove raw `ck-...` and device tokens are not leaking through backups or logs; identify any required rotation. |
| Gate 2: post-hardening dogfood | Blocked | Real dogfood through the hosted relay should wait until the relay-auth blockers and storage checks have landed and been verified. | Close the P0 relay-auth blockers: no `ck-` in browser WS URLs, production token fallback removed, hardcoded keys gone, WS Origin allowlist active, E2EE-only relay path verified, route-bound tickets verified. |
| Public alpha | Blocked | Public or semi-public use is blocked until the VPS cannot be used as an anonymous, unlimited, generic encrypted tunnel. | Close the public-alpha abuse gate: passkey identity required, relay-specific grants, protocol envelope allowlist, message and bandwidth caps, socket and session caps, metadata logging, and kill switches. |

## Operational Read

Current posture:

- Private repo planning and implementation work: allowed.
- Pre-hardening baseline inspection: allowed.
- Post-hardening dogfood over the hosted relay: blocked.
- Public alpha: blocked.
- Public release or package release: not implied by this matrix.

## Status Rules

- Do not mark Gate 2 unblocked from source review alone. It needs live route and relay verification.
- Do not mark Public alpha unblocked from token/E2EE work alone. It needs abuse limits and kill switches.
- Do not treat Agent Pay as a blocker for free alpha. Agent Pay is the next authorization/payment layer, but the free alpha still needs identity, quota, scoped grants, and revocation.
- Do not conflate Memory Crystal storage with hosted MCP auth storage. The Postgres token check here is for hosted MCP / Kaleidoscope auth and relay credentials.

## Update Rules

When a gate changes state, update this file in the same PR that provides the evidence or link to the evidence PR. Keep the matrix short and status-focused; detailed work belongs in the related tickets.

