---
name: trinity-evolution
description: Use this skill when auditing or operating the Trinity/OpenClaw self-evolution loop: checking version status, preflight health, capability validation gates, direction radar output, failure-repair fallback, and user-facing progress reports. It helps verify that OpenClaw capability changes are source-backed, externally judged, practical, and not self-referential.
---

# Trinity Evolution

Use this skill to operate and audit the OpenClaw self-evolution loop.

## Core Workflow

1. Check the local system status command before making readiness claims.
2. Run the operational preflight before publishing or reporting a release baseline.
3. Confirm there are no pending holdouts, repair failures, or unverified current repairs.
4. Treat external validation and explicit validation as promotion gates.
5. Reject self-referential proof, internal metrics alone, auto-scored results alone, social-only signals, and stale repair status.
6. Summarize user-facing impact in plain language: what OpenClaw improved, why it matters, and how the user should use it.

## Evidence Rules

Only claim a capability improvement when the current repair has:

- At least two independent external PASS results.
- Zero external FAIL results for the current repair.
- At least one explicit positive validation.
- Zero pending current-repair holdouts.
- A source-backed or artifact-backed rationale.

If any required evidence is missing, state that the evidence is insufficient and do not claim improvement.

## v16.0 Baseline

v16.0 means the loop can:

- Discover candidate OpenClaw capabilities from source-backed direction radar.
- Materialize a candidate into repair and holdout records.
- Ask OpenClaw to answer holdouts.
- Judge outputs with an external or configured OpenClaw judge.
- Promote only after repair-level gates pass.
- Preserve failed repairs and create conservative replacement repairs without fabricating success.
- Produce a user-facing daily progress report.

## User-Facing Reporting

Reports should describe OpenClaw's practical capability changes, not internal Trinity mechanics.

Use plain language:

- What OpenClaw can now do better.
- Why that matters to the user.
- How the user should use the new behavior.
- What evidence supports the claim.

## Safety And Publishing Notes

Do not include sensitive local data, private operational records, messaging service configuration, machine-specific paths, or generated private state in public artifacts.
