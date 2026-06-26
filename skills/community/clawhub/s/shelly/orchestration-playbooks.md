# Shelly Orchestration Playbooks

Use these patterns for multi-device workflows.

## Playbook 1: Safe Batch Rollout

1. Define target cohort and blast-radius cap.
2. Validate method compatibility across cohort.
3. Run canary command on one device.
4. Verify state convergence and latency.
5. Roll out in small batches with checkpoints.
6. Stop immediately on repeated divergence.

## Playbook 2: Event-Driven Coordination

For sensor-triggered control logic:

- define trigger conditions and debounce logic
- map each trigger to explicit action and rollback action
- prevent duplicate execution with run ids
- verify post-action state before re-arming trigger

## Playbook 3: Incident Containment

When states diverge or devices flap:

- freeze further writes
- snapshot affected device state
- classify issue: transport, auth, model mismatch, or offline device
- apply minimal corrective commands
- verify recovery before resuming automations

## Observability Baseline

Track for each run:
- run id and timestamp
- target count and success rate
- channel and method used
- first failure signature
- rollback or remediation outcome
