---
name: upi-go-live-checklist
description: Drive a zero-to-first-test-payment UPI onboarding workflow with explicit readiness checks: provider selection, sandbox setup, credentials, webhook validation, test matrix, go-live gates, and incident rollback planning. Use when preparing to launch UPI payments safely.
metadata: {"openclaw":{"homepage":"https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898","emoji":"🚦"}}
---

# UPI Go-Live Checklist

## Purpose

This skill takes a team from **no setup** to **first successful test payment** and then to **go-live readiness**.

It is execution-oriented: checklists, artifacts, and release gates.

## Disclaimer

This skill provides launch-planning and operational guidance only. It does not execute payments, move funds, or replace legal/compliance review. Payment regulations, provider APIs, and operational requirements may change; verify against the latest official PSP, RBI, and NPCI documentation before go-live.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, fraud, chargebacks, penalties, downtime, or other damages arising from use or misuse of this guidance.

Always complete sandbox validation, policy review, and internal approvals before production launch.

## Scope boundaries

- This skill **does not** move money by itself.
- It assumes you have (or will obtain) a PSP/aggregator account and required approvals.
- It coordinates onboarding and launch readiness; use `upi-payment-integration` for deep code patterns and `upi-payment-ux-ops` for messaging/support copy.

## Setup

On first use, read [setup.md](setup.md) and create a local project memory file from [memory-template.md](memory-template.md).

## Source freshness

- Last verified date: 2026-03-19
- Treat this as a launch framework; always re-validate policy/provider details before go-live.

## Source validation checklist

- [ ] Confirm current RBI digital payment authentication direction applicability.
- [ ] Confirm latest recurring mandate/e-mandate rules for your payment categories.
- [ ] Confirm selected provider's current onboarding, settlement, and support SLAs.
- [ ] Confirm incident/escalation contacts are current and tested.
- [ ] Confirm all gate criteria in your org's compliance policy are mapped in `go-live-gates.md`.

## Standard execution workflow

Follow these phases in order:

### Phase 0 - Program setup

Required inputs:

- target launch date
- owner names (engineering, product, ops, finance)
- chosen market and currency assumptions
- provider short-list

Outputs:

- project tracker with owners and due dates
- risk log initialized

### Phase 1 - Provider and account readiness

Checklist:

- [ ] Select provider path (direct bank/PSP/aggregator).
- [ ] Confirm sandbox access is enabled.
- [ ] Confirm production onboarding/KYC requirements.
- [ ] Confirm settlement model and reconciliation report availability.
- [ ] Confirm support and escalation contacts from provider side.

Output:

- signed-off provider decision note

### Phase 2 - Security and configuration baseline

Checklist:

- [ ] Define required env vars and secret ownership.
- [ ] Store credentials in secure secret manager (not chat, not source control).
- [ ] Define webhook endpoint URL(s) for sandbox and prod.
- [ ] Define IP allowlist / auth / signature verification policy.
- [ ] Define data retention policy for payment logs and PII.

Output:

- configuration manifest (`env-name -> secret -> owner -> rotation policy`)

### Phase 3 - Build minimum viable payment flow

Checklist:

- [ ] Create order/payment record model with idempotency anchor.
- [ ] Implement payment initiation endpoint.
- [ ] Implement webhook receiver with signature validation.
- [ ] Implement payment state transitions and transition guardrails.
- [ ] Implement reconciliation job for stale pending transactions.

Output:

- end-to-end sandbox payment flow working in test environment

### Phase 4 - Test matrix and evidence

Run and capture evidence for:

- [ ] successful payment
- [ ] failed payment
- [ ] timeout leading to reconciliation
- [ ] duplicate webhook delivery
- [ ] out-of-order webhook sequence
- [ ] refund (if enabled in scope)
- [ ] mandate create/cancel (if recurring is in scope)

Output:

- test evidence log (screenshots, traces, IDs, expected vs actual)

### Phase 5 - Operational readiness

Checklist:

- [ ] Monitoring dashboards live (success rate, pending aging, webhook failures).
- [ ] Alerts configured (failure spike, pending backlog, reconciliation failures).
- [ ] L1/L2 support runbook approved.
- [ ] Incident communication templates approved.
- [ ] On-call ownership and escalation ladder confirmed.

Output:

- runbook + on-call contact sheet

### Phase 6 - Go-live gate review

Gate must pass all:

- [ ] critical test cases pass
- [ ] no unresolved P0/P1 payment defects
- [ ] rollback procedure tested
- [ ] financial reconciliation dry run accepted by finance
- [ ] compliance sign-off recorded

Output:

- go/no-go decision record

## Agent behavior rules

When user asks for launch help:

1. Determine current phase (0 to 6).
2. Return only missing tasks for that phase.
3. Mark blockers explicitly as `BLOCKER`.
4. Do not suggest go-live if any gate is incomplete.
5. Keep outputs actionable with owner and due date fields.

## Output template

Use this format:

```text
Current phase: <N>

Completed:
- ...

Missing:
- [BLOCKER] <task> | owner: <name/role> | due: <date>
- <task> | owner: <name/role> | due: <date>

Next milestone:
- <milestone and acceptance criteria>
```

## Companion files

- First-use checklist: [setup.md](setup.md)
- Project tracking template: [memory-template.md](memory-template.md)
- Provider comparison and prerequisites: [provider-matrix.md](provider-matrix.md)
- Launch decision criteria: [go-live-gates.md](go-live-gates.md)
- Consolidated release sequence: [launch-playbook.md](launch-playbook.md)
- Incident handling and rollback: [incident-runbook.md](incident-runbook.md)

## Related skills

- `upi-payment-integration` for implementation and technical reliability controls
- `upi-payment-ux-ops` for customer communication and support readiness

