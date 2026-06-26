# Sonoff Troubleshooting and Recovery

Use this guide to resolve common SONOFF and eWeLink failures.

## Symptom: LAN Command Fails

Checks:
- Device model and firmware support LAN control mode.
- Device and controller share reachable LAN path.
- Selected endpoint and path match device mode.

Recovery:
- Confirm mode eligibility and control-plane selection.
- Fall back to cloud mode only if policy allows.

## Symptom: DIY Mode API Returns Errors

Checks:
- Device is in DIY-capable state.
- Request path and payload fields are valid for model API version.
- Device id and data object are formatted correctly.

Recovery:
- Re-read service metadata and baseline status.
- Retry with minimal validated payload on one device.

## Symptom: Cloud and LAN State Disagree

Checks:
- Cloud id and LAN id map to same physical device.
- Cloud sync lag vs immediate LAN state observations.
- Duplicate writes from mixed-plane automation.

Recovery:
- Use local observed state as operational truth when on LAN.
- Reconcile identity mapping before new writes.

## Symptom: iHost API Control Inconsistent

Checks:
- Bridge token is fresh and valid.
- REST and SSE channels point to same iHost instance.
- Device sync between iHost and account is current.

Recovery:
- Refresh token and replay read-only checks.
- Re-sync devices and retry with canary scope.

## Symptom: Batch Rollout Produces Partial Failures

Checks:
- Cohort has mixed mode support not handled in one payload pattern.
- Retry policy too aggressive, amplifying transient faults.
- Missing fail-fast rules after first critical mismatch.

Recovery:
- Split cohort by capability and control mode.
- Reduce batch size and apply canary-first rollout.
- Add hard stop and rollback checkpoints per batch.
