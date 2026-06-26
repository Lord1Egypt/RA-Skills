# Incident runbook (UPI launch)

## Severity model

- **P0**: Broad payment outage or widespread wrong status (high business impact).
- **P1**: Elevated failures/pending backlog with active workarounds.
- **P2**: Isolated issues, no broad impact.

## First 15 minutes

1. Declare incident and assign incident commander.
2. Freeze risky deploys and config changes.
3. Check provider status page and internal alert panels.
4. Confirm blast radius:
   - flows affected (collect/intent/QR/mandate)
   - geographies/channels affected
   - failure mode (timeout, webhook outage, status mismatch)
5. Publish first internal update.

## Containment options

- Enable "degraded mode" messaging in checkout.
- Pause new high-risk flow variants if needed.
- Route users to safer fallback flow when possible.
- Increase reconciliation frequency for pending backlog.

## Customer communication template

`Some UPI transactions are currently delayed due to a payment network/provider issue. Please avoid repeated retries if your status is pending. We are actively reconciling and will update by {{time}}.`

## Technical triage checklist

- [ ] webhook receiver health
- [ ] signature verification failures
- [ ] provider API timeout/error rates
- [ ] queue lag / worker lag
- [ ] pending-to-final conversion trend
- [ ] reconciliation job success

## Resolution checklist

- [ ] root cause identified
- [ ] temporary mitigation removed safely
- [ ] data repaired (status corrections, fulfillment corrections)
- [ ] customer-facing follow-up completed
- [ ] postmortem action items assigned

## Post-incident review fields

- incident start/end time
- impacted flows and counts
- direct customer impact
- root cause
- corrective actions
- prevention actions with owner and due date

