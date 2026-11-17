---
title: "Remote Control needs two-browser cross-thread no-cross-talk regression"
status: open
priority: P1
owner: unassigned
repo: wip-codex-remote-control-private / wip-ldm-os-private
created: 2026-05-11
security_gate: hardening follow-up; daemon thread authority P0 remains closed
---

# Remote Control Two-Browser Cross-Thread No-Cross-Talk Regression

## Problem

The daemon thread authority binding is covered by unit-level and source-shape tests:

- relay injects the ticket-bound `route_thread_id` before forwarding `e2ee.hello`;
- daemon binds the E2EE session to that route;
- daemon dispatch rejects cross-thread attach, send, interrupt, and close.

Those tests satisfy the P0 gate. The remaining regression gap is an end-to-end or cross-repo harness proving two browser clients for the same agent but different threads cannot affect or receive each other's traffic.

## Expected Behavior

Add a focused regression that models or exercises:

1. one daemon for an account;
2. browser A connected to thread A;
3. browser B connected to thread B;
4. same-agent, same-daemon routing;
5. thread A traffic is visible only to thread A clients;
6. thread B traffic is visible only to thread B clients;
7. cross-thread send, stop, close, and attach attempts are rejected.

The harness should prove composition across both layers:

- hosted relay route binding and fanout;
- daemon E2EE authority binding and dispatch rejection.

## Acceptance

- Test covers two browsers with the same agent and different thread ids.
- Test proves no cross-talk in relay fanout.
- Test proves cross-thread commands do not reach the daemon manager or Codex App Server adapter.
- Test runs without production credentials, live PM2, or real user accounts.
- Existing same-thread multi-browser co-presence remains covered.

## Non-Goals

- Do not reopen the daemon thread authority P0.
- Do not require production VPS access.
- Do not weaken E2EE by asking the relay to inspect decrypted command payloads.

