---
title: "Remote Control E2EE persistence needs restart regression test"
status: done
priority: P1
owner: Cody
repo: wip-ldm-os-private / wip-codex-remote-control-private
created: 2026-05-11
security_gate: test-hardening follow-up; P0 product behavior remains closed
---

# Remote Control E2EE Persistence Restart Regression Test

## Problem

The P0 E2EE key persistence bug is fixed and passed live dogfood, but the automated test coverage does not yet exercise a real relay restart or PM2-equivalent reload.

Current coverage verifies the code shape and models the persisted-key behavior. It does not boot the hosted relay, register a daemon key, drop or restart in-memory relay state, then verify `/api/codex-relay/bootstrap/<threadId>` still reports E2EE availability without requiring `codex-daemon link`.

This is not evidence that the product fix is broken. It is a regression-test gap around behavior that has already passed live validation.

## Background

The closed P0 ticket is:

```text
ai/product/bugs/codex-remote-control/2026-05-05--codex--remote-control-e2ee-key-persistence.md
```

That ticket accepted two durability paths:

- persist the daemon E2EE public key server-side;
- make the daemon re-register its existing E2EE public key on authenticated relay reconnect.

Both shipped and passed dogfood. The remaining gap is that the test suite should fail if either the persisted-key load path or reconnect registration path regresses.

## Expected Behavior

Add an automated regression that proves:

1. a daemon E2EE public key is registered for an authenticated tenant;
2. hosted relay in-memory key state can be lost or the relay can restart;
3. persisted key load restores `e2ee_available: true`, or daemon reconnect self-heals it with `daemon.identity`;
4. `/api/codex-relay/bootstrap/<threadId>` returns the daemon public key without running `codex-daemon link`;
5. the test fails if key persistence, boot load, or reconnect registration is removed.

## Suggested Test Shape

Prefer a focused harness over a brittle production PM2 dependency.

Possible approaches:

- Extract the Codex relay E2EE pubkey registry into a small testable module and unit-test restart semantics directly.
- Add a hosted-relay integration harness that starts the server with a temporary Postgres or test DB, registers a key, restarts the process, then calls bootstrap.
- Add a narrower in-process harness that clears `codexDaemonPubkeys`, reloads persisted rows, and asserts bootstrap returns `e2ee_available: true`.

The test should cover both persistence and reconnect self-healing if practical:

- persisted-row restore path: key exists in DB before process startup;
- reconnect path: key is missing from memory and DB, authenticated daemon sends `daemon.identity`, then bootstrap succeeds.

## Acceptance

- New test is runnable from `npm test` or a named script in `wip-ldm-os-private`.
- Test fails if `await loadCodexDaemonPubkeysFromDb()` is removed or no longer runs before bootstrap.
- Test fails if `daemon.identity` reconnect registration is removed or ignored.
- Test verifies bootstrap output, not only source strings.
- Test does not require a real PM2 process or live production deploy.
- P0 E2EE key persistence ticket stays closed unless live relink behavior regresses.

## Closure Evidence

Implemented on 2026-05-11.

The hosted relay E2EE pubkey registry was extracted to `src/hosted-mcp/codex-relay-e2ee-registry.mjs` so restart behavior can be tested without production PM2 or live Postgres.

Regression coverage now lives in:

```bash
npm run test:crc-e2ee-key-persistence
```

The test proves:

- pair completion registers and persists a daemon E2EE public key;
- a fresh registry instance restores the key from persisted rows after in-memory state is lost;
- bootstrap payload returns `e2ee_available: true` and the daemon public key after restore;
- an empty registry can self-heal when an authenticated daemon sends `daemon.identity`;
- the reconnect-registered key survives the next simulated restart;
- the server still loads persisted keys before `handleCodexBootstrap`;
- the server still handles `daemon.identity` reconnect registration.

Validation passed:

- `npm run test:crc-e2ee-key-persistence`
- `npm run test:crc-e2ee-session-route`
- `npm run test:crc-pair-status-poll-token`
- `npm run test:crc-pair-login-flow`
- `node --check src/hosted-mcp/server.mjs`
- `node --check src/hosted-mcp/codex-relay-e2ee-registry.mjs`

## Non-Goals

- Do not reopen the P0 product bug.
- Do not change the live relay protocol unless the test exposes a real regression.
- Do not require production PM2 access in normal CI.
- Do not add broad Remote Control security scope to this ticket.
