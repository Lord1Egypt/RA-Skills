# Validation checklist

Use this checklist before sandbox sign-off and before production release.

## Functional

- [ ] collect flow tested
- [ ] intent flow tested
- [ ] QR flow tested
- [ ] mandate flow tested (if in scope)

## Reliability

- [ ] duplicate webhook processing is idempotent
- [ ] out-of-order events do not corrupt state
- [ ] timeout-to-reconciliation path works
- [ ] stale pending sweep works and is observable

## Security

- [ ] webhook signature verification enforced
- [ ] secrets are sourced from secure secret manager
- [ ] no sensitive payloads in plain logs

## Finance and reconciliation

- [ ] daily settlement mapping tested
- [ ] refund accounting verified
- [ ] mismatch handling SOP documented

## Operational readiness

- [ ] dashboard and alerts active
- [ ] on-call runbook linked
- [ ] support escalation path validated

