---
title: "Remote Control pair and relink need audit, rotation, and stale-key invalidation"
status: done
priority: P1
owner: hosted auth token security K-partner / Cody
repo: wip-ldm-os-private / wip-codex-remote-control-private
created: 2026-05-05
---

# Remote Control Pair and Relink Audit

## Problem

Pair-complete is browser-authenticated and code-bound, which is good. But pair or relink can replace the registered daemon public key for an agent.

That replacement needs a durable policy before non-Parker dogfood.

The current alpha path is protected by bearer auth, not fresh presence. A stolen `ck-` token could pair a new daemon, replace the registered E2EE key, and kick the prior daemon for that handle.

CC security review classed re-pair without fresh presence as `HIGH`: fix before adding any non-Parker user.

## Security Review Evidence

Review finding:

```text
P1: pair/relink is acceptable for Parker-only but needs a durable audit and replacement policy.
```

Risks:

- A relink could replace the daemon public key without enough operator visibility.
- Stale browser assumptions could survive after key rotation.
- The product needs a clear story for legitimate device replacement versus suspicious daemon replacement.
- Reusable `ck-` token authority is too broad for daemon replacement.

Additional source pointers from review:

- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/pair.html:87`
- `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2700`

Hosted auth review gate:

- Pair/relink remains acceptable for Parker-only smoke.
- Non-Parker users require fresh presence or short-lived pair-only token before daemon replacement.

Additional CC security review evidence:

- `handleCodexPairComplete` overwrites the current registered daemon public key for `identity.agentId` with no already-paired check, no fresh passkey assertion, and no visible confirmation.
- Source pointer:
  - `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2700-2738`
- Re-pair is re-key. Treat it like rotating a root credential.

## Expected Behavior

Pair and relink have explicit, observable semantics:

- pair code has a short lifetime,
- pair or relink requires fresh presence, such as a WebAuthn assertion, or a short-lived pair-only token,
- pair completion logs operator-visible metadata,
- replacing a daemon key invalidates the old key's assumptions,
- stale browser sessions cannot continue as if the old daemon key is still valid,
- relink is visible to the user or operator,
- relink is recovery, not routine deploy behavior.

## Acceptance

- Pair complete records safe audit metadata: agent identity, daemon key fingerprint, timestamp, route, and replacement status.
- Pair or relink requires fresh WebAuthn presence or a short-lived pair-only token.
- A reusable `ck-` token alone cannot replace a registered daemon key.
- Repeating `pair-complete` with a paired user's `apiKey` rejects unless a fresh passkey assertion is present.
- Relink records old and new daemon key fingerprints where safe.
- Replacing a daemon pubkey invalidates stale browser E2EE assumptions.
- Stale browser keys or sessions cannot keep working silently after relink.
- Pair code reuse fails.
- Pair code expiry is tested.
- The UI or CLI gives a clear message when relink replaced an existing daemon key.

## Resolution

Implemented on 2026-05-11.

Pair and relink now use a short-lived pair-presence token minted only after successful WebAuthn register or auth verification. The pair page passes that token to `pair-complete`; a reusable `ck-` bearer token alone is no longer enough to complete daemon public-key pairing.

Daemon public-key registration now records safe audit metadata in `codex_daemon_e2ee_key_audit`:

- immutable tenant id,
- source,
- old daemon public-key fingerprint,
- new daemon public-key fingerprint,
- replacement status,
- registration timestamp.

When the registered daemon public key changes, the relay closes existing browser Remote Control sockets for that tenant and clears E2EE session routes. Stale browser sessions cannot silently continue under the old daemon key assumptions. Pair status and pair UI also surface whether the operation replaced an existing daemon key.

Follow-up hardening on 2026-05-12 closed the daemon reconnect composition gap between E2EE key persistence and fresh-presence relink. Authenticated `daemon.identity` reconnect can now self-heal only when no daemon key is registered, or re-register the same key idempotently. If a key is already registered and reconnect presents a different public key, the relay rejects it with `daemon key change requires fresh pair`. Key replacement must use the fresh-presence pair-complete path so stale browser sessions are invalidated and audit metadata is recorded under the relink policy.

A second 2026-05-12 follow-up moved daemon online replacement behind accepted `daemon.identity`. A new authenticated daemon socket no longer evicts the currently online daemon before its identity frame passes reconnect policy. If a daemon is already online, a duplicate reconnect is closed with `daemon already online`; if a daemon sends routed frames before identity acceptance, it is closed with `daemon identity required`. This prevents a reusable `ck-` token from repeatedly kicking the legitimate daemon before failing the key policy.

Regression coverage:

```bash
npm run test:crc-pair-relink-audit-and-rotation
```

## Non-Goals

- Do not require relink after normal hosted deploys.
- Do not expose private keys.
- Do not weaken passkey authentication.
