---
name: upi-payment-integration
description: Design and implement robust UPI payment integrations (collect, intent, QR, and autopay mandates) with production-grade webhook handling, idempotency, reconciliation, and RBI-aligned authentication/compliance guardrails. Use when building or debugging UPI payment flows, payment status issues, recurring mandates, settlement mismatches, or gateway timeout edge cases.
metadata: {"openclaw":{"homepage":"https://www.npci.org.in/what-we-do/upi/product-overview","emoji":"💸","requires":{"env":["UPI_PROVIDER_KEY_ID","UPI_PROVIDER_KEY_SECRET","UPI_WEBHOOK_SECRET","UPI_MERCHANT_ID"],"bins":["curl","jq"]}}}
---

# UPI Payment Integration

## What this skill does

Use this skill to help users build, review, or troubleshoot UPI integrations that are safe for production.

Covered flows:

- UPI collect requests
- UPI intent payments
- UPI QR payments (static/dynamic)
- UPI autopay / e-mandate recurring payments

## Disclaimer

This skill provides implementation and operational guidance only. It does not execute payments, move funds, or replace legal/compliance review. Payment regulations, provider APIs, limits, and policies may change; always verify against the latest official PSP, RBI, and NPCI documentation before production use.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, fraud, chargebacks, penalties, downtime, or other damages arising from use or misuse of this guidance.

Always validate in sandbox/staging before production and never share secrets or private keys in chat.

## Setup

On first use, read [setup.md](setup.md) and confirm:

- provider and environment (sandbox vs production)
- credentials availability in secret manager
- webhook endpoint and verification strategy
- database/reconciliation ownership

## Source freshness

- Last verified date: 2026-03-19
- Before production changes, re-check provider docs and current RBI/NPCI circulars.

## Source validation checklist

- [ ] Confirm chosen PSP's latest webhook event semantics and retry policy.
- [ ] Confirm latest UPI transaction limits and mandate policy for your use case.
- [ ] Confirm current signature verification/auth requirements from provider docs.
- [ ] Confirm current settlement and reconciliation report fields from provider dashboard.
- [ ] Confirm any newly introduced compliance/legal requirements with your legal/compliance team.

## Core operating principles

1. **Treat payment lifecycle as asynchronous**
   - API response is not final truth.
   - Webhook + reconciliation determine final status.

2. **Make every write idempotent**
   - De-duplicate by event ID / provider payment ID / merchant request ID.
   - Reprocessing the same webhook must be safe.

3. **Persist before processing**
   - Store raw webhook payload and headers first.
   - Process in a retriable job/queue.

4. **Reconcile continuously**
   - Poll or fetch status for `PENDING`, timed-out, or disputed records.
   - Close state gaps between app DB, PSP dashboard, and settlement reports.

5. **Keep compliance explicit**
   - Follow RBI authentication and risk controls.
   - Keep consent and cancellation paths clear for recurring mandates.

## Mandatory implementation checklist

Use this checklist in every implementation/review:

- [ ] Payment state machine exists (`CREATED`, `PENDING`, `SUCCESS`, `FAILED`, `EXPIRED`, `REFUNDED` as applicable).
- [ ] Unique merchant-side request ID/correlation ID is generated and stored.
- [ ] Webhook signature verification is implemented.
- [ ] Raw webhook body is stored before business logic.
- [ ] Duplicate webhook delivery is handled safely.
- [ ] Out-of-order events are handled safely.
- [ ] Retry policy exists for provider/network failures.
- [ ] Reconciliation job exists for stale `PENDING` records.
- [ ] Refund and reversal flows are explicit.
- [ ] Alerting exists for failure spikes and webhook downtime.
- [ ] Mandate create/pause/cancel paths are implemented and visible to users.

## Standard workflow (for the agent)

When user asks for UPI help, do this:

1. **Identify integration mode**
   - Collect vs intent vs QR vs mandate.

2. **Map current architecture**
   - Client request path
   - Backend order/payment records
   - Provider API call
   - Webhook receiver
   - Reconciliation worker

3. **Enforce reliability controls**
   - Idempotency keys
   - Signature validation
   - Event dedupe
   - Retries and dead-letter handling

4. **Validate business correctness**
   - No shipment/service unlock before durable success
   - Correct handling of late success after apparent failure
   - Correct handling of duplicate attempts

5. **Validate compliance and customer UX**
   - Authentication and risk controls
   - Consent and cancellation clarity for mandates
   - Clear customer-visible status and support trace IDs

## Webhook handling rules

- Always verify signature using provider secret.
- Use raw request body for signature validation; do not mutate/parse first.
- Acknowledge quickly (2xx) after durable receipt.
- Process asynchronously.
- Never assume strict event ordering.
- Build handlers as idempotent upserts, not one-time inserts.

## Error handling and reconciliation rules

- On timeout, mark local payment as `PENDING_RECON` (or equivalent), not immediate failure.
- Reconcile by provider payment ID and merchant request ID.
- If provider says success after client saw failure, trust reconciled final state and repair downstream records.
- Log every status transition with source (`api`, `webhook`, `recon`).

## Recurring mandate (Autopay) rules

- Treat mandate creation as a first-class object with lifecycle states.
- Store mandate ID, start/end dates, frequency, max amount, and status.
- Support pause/cancel from product UI and backend admin.
- Send pre-debit reminders where required by provider/framework.
- On recurring debit failures, retry only within allowed policy; avoid silent repeated debits.

## Compliance and policy guardrails

- Follow RBI authentication expectations (minimum two factors, with dynamic factor requirements where applicable).
- Keep evidence logs for user consent and mandate actions.
- Protect personal/payment data with least-privilege access and retention policy.
- Keep customer grievance paths clear (transaction reference IDs, support response playbook).

## Output format

When responding to a user request, return:

1. **Architecture or fix plan**
2. **Concrete code/database changes**
3. **Failure-mode checks**
4. **Test plan (happy path + retries + duplicates + out-of-order events + reconciliation)**

## References

- First-use checklist: [setup.md](setup.md)
- Release workflow: [launch-playbook.md](launch-playbook.md)
- See [reference.md](reference.md) for policy and operational notes.
- See [examples.md](examples.md) for implementation templates and edge-case patterns.
- See [validation-checklist.md](validation-checklist.md) for release readiness checks.
- See [failure-handling.md](failure-handling.md) for incident and recovery patterns.

## Related skills

- `upi-go-live-checklist` for phase tracking and launch gates
- `upi-payment-ux-ops` for customer messaging and support operations

