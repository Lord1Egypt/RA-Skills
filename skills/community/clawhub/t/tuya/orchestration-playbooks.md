# Tuya Orchestration Playbooks

Use these patterns for multi-device operations and automations.

## Playbook 1: Safe Fleet Rollout

1. Define target cohort and blast-radius limit.
2. Validate capability schema consistency across cohort.
3. Execute canary on one device.
4. Verify state convergence.
5. Roll out in small batches.
6. Stop immediately on drift or repeated errors.

## Playbook 2: Scene-Like State Coordination

When coordinating multiple devices (lights, plugs, sensors):

- Define desired end state per device.
- Sort execution order by dependency.
- Write idempotent steps so re-run does not corrupt state.
- After each phase, verify aggregate state before next phase.

## Playbook 3: Incident Containment

If devices diverge from expected state:

- Freeze further writes.
- Snapshot current status of affected devices.
- Classify issue: auth, permission, schema, offline, or device-side failure.
- Apply minimal corrective command set.
- Re-verify before resuming automation.

## Observability Baseline

Track for each run:
- run id and timestamp
- target device count
- success/failure per device
- first error signature
- rollback or remediation action

## Rollback Pattern

- Keep a pre-change status snapshot.
- For reversible states, build explicit revert commands.
- Roll back only verified failed subset unless user requests full revert.

## Practical Limits

- Avoid uncontrolled parallel writes on first rollout.
- Avoid mixed-region operations in one execution plan.
- Avoid blind retries when signature or permission errors are present.
