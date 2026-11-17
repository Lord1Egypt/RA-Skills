---
title: "Remote Control pair-status must require daemon-bound poll token before returning apiKey"
status: done
priority: P0
owner: hosted auth token security K-partner / Cody
repo: wip-ldm-os-private / wip-codex-remote-control-private
created: 2026-05-06
security_gate: CLEARED for this finding; non-Parker users remain blocked by later gates
---

# Remote Control Pair Status Poll Token

## Problem

`/api/codex-relay/pair-status/<pairing_id>` can return the daemon `apiKey` without authenticating the polling daemon. Pairing IDs are random UUIDs, so remote brute force is impractical, but the pairing id can appear in daemon memory, local logs, stdout, or process capture.

Anyone who obtains the pairing id during the pair window can poll pair-status and retrieve the `apiKey`.

This is a high-severity credential exposure path and blocks non-Parker users.

## Security Review Evidence

Finding:

```text
H2. /api/codex-relay/pair-status/<pairing_id> returns the apiKey unauthenticated.
```

Source pointer from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2686-2698`

Threat model:

- Not a remote attacker guessing the UUID.
- A local attacker, log scrape, or process capture that sees the pairing id can escalate to `apiKey` theft.

## Expected Behavior

Pair status has a daemon-bound poll token:

- `pair-init` mints a one-time pair-poll token bound to the `pairing_id`.
- The daemon stores that token only for the active pair flow.
- The daemon includes `Authorization: Bearer <pair-poll-token>` on pair-status calls.
- pair-status without the poll token returns `401`.
- pair-status with the wrong poll token returns `401`.
- token is consumed on the first `status: completed` response that returns the daemon credential.
- token expires with the pairing code.

## Acceptance

- `/api/codex-relay/pair-status/<pairing_id>` without poll token returns `401`.
- Wrong poll token returns `401`.
- Correct poll token returns pending status before completion.
- Correct poll token returns completed status and `apiKey` once.
- Reusing the same poll token after completed status fails.
- Expired pair-poll token fails.
- `codex-daemon link` still pairs successfully.
- Regression test covers unauthorized pair-status cannot retrieve `apiKey`.

## Closure Evidence

Closed on 2026-05-06.

Implemented in two coordinated slices:

- Daemon PR: `wip-codex-remote-control-private#56`
- Daemon release: `wip-codex-remote-control@0.0.2-alpha.15`
- Hosted relay PR: `wip-ldm-os-private#860`
- Hosted release: `@wipcomputer/wip-ldm-os@0.4.85-alpha.8`
- Hosted deploy manifest: `2026-05-07T01-48-16Z.json`

Validation:

- PASS: `npm run test:crc-pair-status-poll-token`
- PASS: `npm run test:crc-pair-login-flow`
- PASS: `npm run test:crc-agentid-tenant-boundary`
- PASS: `npm run test:crc-e2ee-session-route`
- PASS: `node --check src/hosted-mcp/server.mjs`
- PASS: daemon `npm test`
- PASS: daemon `npm run typecheck`
- PASS: daemon `npm run test:pair-status-poll-token`
- PASS: hosted `/health` returned healthy Postgres state after deploy
- PASS: deploy manifest verified `23 ok, 0 mismatched`
- PASS: live server source contains `pair_poll_token`, `invalid_pair_poll_token`, and `pair_poll_token_expired`
- PASS: Parker completed live `codex-daemon link` after deploy and Remote Control reconnected

Observed caveat:

- A first browser-to-TUI send after reconnect showed `error: no active turn to steer`, then subsequent browser and TUI turns worked. That is a separate early attach send-state bug, not this pair-status credential exposure path.

## Non-Goals

- Do not change the visible pair URL format unless required.
- Do not weaken passkey or pair confirmation flow.
- Do not solve re-pair fresh-presence in this ticket.
