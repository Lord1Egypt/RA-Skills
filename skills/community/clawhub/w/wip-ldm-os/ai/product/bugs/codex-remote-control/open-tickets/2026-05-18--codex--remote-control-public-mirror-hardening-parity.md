---
title: "Remote Control public mirror must reflect hosted relay hardening"
status: open
priority: P1
owner: Merge/Deploy K
repo: wip-ldm-os-private -> wip-ldm-os
created: 2026-05-18
source_review: 2026-05-18 security triage of private Remote Control architecture
master_plan_item: 38
---

# Remote Control Public Mirror Must Reflect Hosted Relay Hardening

## Problem

The 2026-05-18 security triage found a trust/audit mismatch:

- The private hosted relay appears to have the right hardening shape:
  - no hardcoded production API keys;
  - WebSocket URL token fallback off by default;
  - pair-status one-time poll token;
  - fresh passkey presence for pairing;
  - route-bound short-lived WS tickets;
  - origin allowlist;
  - daemon key replacement protection.
- Safe live probes rejected the public default keys.
- But the public `wip-ldm-os` relay source snapshot that was inspected looked older and still showed the previous weak pair-status/default-key shape.

That mismatch is itself a trust problem. External reviewers use the public mirror to decide whether Remote Control is inspectable and whether the live relay matches the open source artifact.

## Risk

P1 launch trust and auditability risk.

This is not necessarily a live production vulnerability if the deployed relay is already hardened. It is still unacceptable for broader launch because public source inspection can reasonably conclude that the relay is weaker than the live service.

## Fix shape

Use the standard private-to-public path only. Do not edit the public mirror directly.

- Identify the private commit that contains the deployed hosted relay hardening.
- Identify the public `wip-ldm-os` commit that should mirror it.
- Run the private-to-public sync path when appropriate.
- Verify the public mirror contains the hardened relay source.
- Add a release/deploy checklist item so hosted relay security releases record:
  - private source SHA;
  - deployed SHA or manifest hash;
  - public mirror SHA when public sync is expected;
  - whether alpha/beta/stable policy intentionally skipped public sync.

## Acceptance

- Public `wip-ldm-os/src/hosted-mcp/server.mjs` reflects the hardened relay behavior for the Remote Control paths listed above, or a documented release-track policy explains why the public mirror intentionally lags.
- Public docs in `wip-codex-remote-control` point to a public relay source that matches the security claims in `TECHNICAL.md`.
- A read-only parity check exists or is documented:

```text
private source commit -> deployed relay -> public mirror commit
```

- No direct public repo edit is used to repair the mismatch.
- The ticket records whether the mismatch was stale public mirror, stale live deploy, or reviewer snapshot drift.

## Non-goals

- Do not move hosted relay runtime code into `wip-codex-remote-control-private`.
- Do not duplicate hosted relay code between repos.
- Do not make public mirrors into working surfaces.
- Do not run a hosted deploy unless the release/deploy owner explicitly assigns it.
