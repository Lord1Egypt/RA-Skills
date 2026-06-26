# Sonoff Orchestration Playbooks

Use these patterns for multi-device automation.

## Playbook 1: Safe Batch Rollout

1. Define target cohort and blast-radius cap.
2. Validate mode compatibility across cohort.
3. Run canary command on one device.
4. Verify state convergence.
5. Roll out in small batches with checkpoints.
6. Stop immediately on repeated divergence.

## Playbook 2: Mixed Plane Coordination

When cloud and LAN are both active:

- define primary plane and fallback plane
- prevent duplicate writes across planes
- verify state from one authoritative source per step
- log when fallback path is triggered

## Playbook 3: Incident Containment

When states diverge or devices flap:

- freeze further writes
- snapshot affected state across active planes
- classify issue: auth, mode mismatch, transport, or offline device
- apply minimal corrective commands
- verify recovery before resuming automation

## Observability Baseline

Track for each run:
- run id and timestamp
- target count and success rate
- selected control plane
- first failure signature
- rollback or remediation outcome
