---
name: upi-payment-ux-ops
description: Design UPI payment user experience and operations playbooks: consent wording, payment status messaging, retries, support workflows, refunds, and dispute communication. Use when creating product copy, UX flows, support SOPs, or incident communication for UPI payments and mandates.
metadata: {"openclaw":{"homepage":"https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898","emoji":"🧾"}}
---

# UPI Payment UX and Ops

## What this skill does

Use this skill to create user-facing and ops-facing assets for UPI journeys:

- Payment UI copy and screen flows
- Retry and failure handling UX
- Mandate consent and cancellation wording
- Support macros and triage playbooks
- Refund/dispute communication templates
- Incident and downtime customer messaging

## Disclaimer

This skill provides messaging and operations guidance only. It does not execute payments, move funds, or replace legal/compliance review. Payment regulations, provider APIs, limits, and policy expectations may change; verify against the latest official PSP, RBI, and NPCI documentation before production use.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, fraud, chargebacks, penalties, downtime, customer harm, or other damages arising from use or misuse of this guidance.

Always validate copy and workflows in sandbox/staging and approved policy review before production rollout.

## Scope

This skill is for **product, design, CX, and operations**.
For deep integration code and webhook architecture, use `upi-payment-integration`.

## Setup

On first use, read [setup.md](setup.md) and confirm:

- brand voice and policy constraints
- support SLA windows and escalation ownership
- payment state taxonomy used by engineering
- reference ID fields available to support

## Source freshness

- Last verified date: 2026-03-19
- Before launch messaging, re-check provider behavior and current RBI/NPCI circular context.

## Source validation checklist

- [ ] Confirm current pending/failure semantics from your PSP to avoid misleading copy.
- [ ] Confirm latest mandate consent and cancellation expectations for your flow.
- [ ] Confirm current refund and reversal timelines from provider and partner banks.
- [ ] Confirm grievance/escalation wording with legal/compliance and support operations.
- [ ] Confirm status labels shown in product match backend truth sources.

## UX principles

1. **State clarity over jargon**
   - Prefer "Payment pending with bank" over ambiguous "processing".

2. **Actionable next step**
   - Every failure/pending state must tell users what to do next.

3. **Trust through transparency**
   - Show reference IDs (UTR/provider ref/order ID) and expected timelines.

4. **No dark patterns**
   - Mandate creation/cancellation should be explicit and reversible.

5. **Calm, concise tone**
   - No blame language. No internal system jargon in user copy.

## Mandatory UX checklist

- [ ] Each payment state has user copy + CTA.
- [ ] Pending state includes expected wait time and refresh behavior.
- [ ] Failure state distinguishes retryable vs non-retryable outcomes.
- [ ] Success state includes reference ID and receipt/share options.
- [ ] Customer gets clear refund timeline and status visibility.
- [ ] Mandate screens show amount/frequency/next debit/cancel path clearly.
- [ ] Support can locate transaction using any one user-provided identifier.
- [ ] Incident mode communication templates are pre-approved.

## Standard user-state copy framework

For each state, define:

- **Title** (plain language)
- **Body** (what happened)
- **Confidence** (is money debited, likely debited, or not debited)
- **CTA** (what user should do now)
- **Escalation trigger** (when user should contact support)

## Required flows

### 1) Payment initiation

- Confirm payee + amount before submit.
- Set expectation: app switch to UPI app may happen.
- Keep session-safe return behavior if user abandons app switch.

### 2) Pending payment flow

- Display "Pending with bank/PSP" style status.
- Do not double-charge by encouraging blind retries.
- Offer "Check status" and "Try again" only with clear guidance.

### 3) Failed payment flow

- If likely no debit: show immediate retry CTA.
- If debit uncertain: route to status check first.
- If debit happened but order not confirmed: communicate auto-reconciliation window.

### 4) Success flow

- Show amount, timestamp, payee, and transaction reference.
- Provide receipt/share and support path.

### 5) Mandate (Autopay) flow

- Explicitly show:
  - debit frequency
  - max amount
  - start date and end date (if any)
  - pause/cancel path
- Send pre-debit reminder where applicable.

### 6) Refund/dispute flow

- Show "refund initiated" vs "refund completed" as separate states.
- Provide expected SLA windows and "last checked" timestamp.
- Route to human support when SLA breaches.

## Ops playbook rules

- Triage in this order:
  1. confirm transaction identity
  2. check final provider/bank status
  3. check internal order fulfillment state
  4. apply resolution template

- Never ask user to retry without confirming current debit certainty.
- Escalate unresolved pending items after defined SLA threshold.
- Keep a standard reason-code taxonomy for analytics and product feedback.

## Compliance and customer protection guardrails

- Keep consent records for mandate creation/changes/cancellation.
- Avoid misleading status language that implies final success before confirmation.
- Use clear grievance and escalation channels.
- Align authentication/transaction communication with RBI expectations.

## Output format

When helping the user, return:

1. Screen/message copy (by state)
2. Support macro templates
3. Escalation matrix (L1/L2/L3)
4. Metrics to monitor (failure reasons, pending aging, refund SLA adherence)

## References

- First-use checklist: [setup.md](setup.md)
- Release operations: [launch-playbook.md](launch-playbook.md)
- See [reference.md](reference.md) for message taxonomy and SLA patterns.
- See [examples.md](examples.md) for reusable UX copy and support scripts.
- See [validation-checklist.md](validation-checklist.md) for launch quality checks.

## Related skills

- `upi-payment-integration` for backend/payment architecture and reliability
- `upi-go-live-checklist` for launch planning, blockers, and go/no-go decisions

