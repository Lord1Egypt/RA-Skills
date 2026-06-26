---
name: tob-poc-war-room
description: POC war-room skill for ToB AI delivery. Use when a user needs to diagnose POC status, track pass rate, classify blockers, build a 48-hour closure plan, detect customer silence risk, generate daily POC war-room reports, or decide when a POC is ready to enter contract closing.
priority: critical
source: lining-field-experience
workers: [tech, pm, sales]
created: 2026-06-03
tags: [tob, poc, delivery, war-room, risk-control]
---

# tob-poc-war-room

Use this skill to run a ToB POC like a war room, not a loose project tracker.

The goal is to convert POC facts into:
- current risk level
- blocker ownership
- 48-hour closure plan
- customer communication move
- decision on whether to trigger `poc-to-contract-closer`

Do not output generic project-management templates. Every output must tie back to concrete POC signals.

## Required Inputs

Ask for missing essentials only when they change the decision:
- POC objective and acceptance criteria
- current day or phase
- pass rate or accepted test count
- open issue list with severity, owner, age, and next action
- customer feedback or silence duration
- decision maker / champion status
- procurement path status: unknown / tender / price comparison / single-source / framework agreement / renewal
- competitor or parallel POC signal, if any

If inputs are incomplete, still produce a triage note and list the missing evidence.

## Field Rules

### Pass Rate

- `>=90%`: closeable if no P0 blocker remains and acceptance evidence is concrete.
- `70-89%`: yellow; focus the next 48h on the smallest set of blockers that affect acceptance.
- `<70%`: red; do not talk contract yet unless customer scope changed.
- Unknown pass rate: red-yellow; first action is to force a measurable acceptance baseline.

Use the 93% pass-rate pattern as a reference signal, not a promise.

### Blockers

Classify each issue:
- `P0`: blocks acceptance or executive demo.
- `P1`: affects key user confidence but has workaround.
- `P2`: cosmetic, edge case, or post-POC backlog.

48h rule:
- P0 older than 48h without owner/action is red.
- P1 older than 48h becomes yellow-red if it affects the champion's narrative.
- P2 should not consume war-room attention unless customer names it.

### Customer Silence

- 0-2 days: normal, continue planned follow-up.
- 3 days: proactive touchpoint required.
- 7 days: danger signal; trigger executive/champion path and closing diagnosis.
- Silence after successful demo is not neutral. Treat it as an unowned buying-process risk.

### Procurement Path

ToB POC cannot move cleanly into closing if procurement path is unknown.

Check:
- tender or formal bidding
- price comparison
- single-source justification
- framework agreement call-off
- renewal / expansion
- direct purchase under threshold

If pass rate is high but procurement path is unknown, trigger `poc-to-contract-closer` with a buying-process gap instead of sending a quote.

### Ownership

No output may contain an action without:
- owner
- next step
- deadline
- expected evidence

If owner is unknown, assign a role placeholder such as `Tech owner`, `Sales owner`, or `Customer champion`.

### Trigger To Closing

Trigger `poc-to-contract-closer` when:
- pass rate is `>=90%`, or
- all P0 blockers are closed and customer has accepted the core value, or
- the POC has entered final demo / recap / procurement discussion, or
- customer silence appears after a successful POC and the buying process must be restarted.

Do not trigger closing when the POC is still proving basic feasibility.

### Return From Closing

If `poc-to-contract-closer` finds unresolved P0, pass rate below closeable level, or missing acceptance evidence, return to `tob-poc-war-room` and run a 48-hour issue closure plan. Closing and war-room are a two-way loop, not a one-way handoff.

Terminology:
- `closeable`: enough accepted POC evidence to start closing diagnosis.
- `contract-ready`: closer confirms buyer path, procurement path, closing window, and issue treatment.
- Do not treat closeable as contract-ready.

## Output Format

```markdown
## POC War-Room Triage

### 1. Status
- Phase:
- Risk: Green / Yellow / Red
- Pass rate:
- Main reason:

### 2. Blocker Table
| Issue | Level | Age | Owner | Next action | Deadline | Evidence |

### 3. Next 48 Hours
1.
2.
3.

### 4. Customer Move
- Message objective:
- Recommended message:
- Who sends it:
- When:

### 5. Escalation
- Escalate? yes/no
- Escalation target:
- Reason:

### 6. Closing Trigger
- Trigger `poc-to-contract-closer`? yes/no
- Reason:
- Inputs to pass forward:

### 7. Return Path
- If closer rejects readiness, next war-room action:
```

## Acceptance Example

Input:

```text
POC day 5. 14/15 tests accepted. One SSO issue open for 60h. Customer champion likes results, but procurement not involved. No customer reply for 3 days after demo.
```

Expected reasoning:
- pass rate is green, but SSO age and customer silence create yellow risk.
- next 48h must close SSO or document workaround.
- Sales should restart champion/procurement path.
- trigger `poc-to-contract-closer` with the risk flagged, because the POC is closeable but not contract-ready.

## Boundaries

- Do not invent customer names, project names, exact contract amount, or private data.
- Do not promise conversion probability.
- Do not call a POC successful if acceptance criteria are missing.
- Do not bury a P0 blocker under a positive summary.
