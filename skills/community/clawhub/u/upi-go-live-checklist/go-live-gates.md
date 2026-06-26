# Go-live gates

This file defines hard gates before enabling production traffic.

## Gate 1 - Functional correctness

- [ ] Successful payments confirmed in both app DB and provider dashboard.
- [ ] Failure and timeout paths handled without false success.
- [ ] Duplicate webhook deliveries do not create duplicate fulfillment.
- [ ] Reconciliation closes stale pending transactions.

## Gate 2 - Financial integrity

- [ ] Finance sign-off on daily reconciliation process.
- [ ] Settlement report mapping to internal ledger is validated.
- [ ] Refund accounting path is validated.

## Gate 3 - Security and compliance

- [ ] Signature verification enforced on webhook endpoint.
- [ ] Secrets are in secure store with rotation policy.
- [ ] Access controls and audit logging enabled.
- [ ] Required compliance/legal review complete.

## Gate 4 - Operational readiness

- [ ] Dashboard and alerts configured.
- [ ] On-call and escalation matrix approved.
- [ ] L1/L2 support playbooks trained.
- [ ] Incident communications template approved.

## Gate 5 - Rollback readiness

- [ ] Feature flag or controlled rollout mechanism in place.
- [ ] Rollback steps tested in non-prod.
- [ ] "Stop new attempts" emergency switch documented.

## Final decision

Go-live allowed only if **all gates pass** with dated evidence and approver names.

