# Shelly Troubleshooting and Recovery

Use this guide to resolve common Shelly failures.

## Symptom: Device Not Reachable Locally

Checks:
- Confirm IP reachability in target network segment.
- Confirm device and client are in expected VLAN/routing scope.
- Confirm selected transport (HTTP/WS/MQTT) is actually enabled.

Recovery:
- Fall back to cloud mode if remote control is allowed.
- Re-validate local routing and control-plane decision.

## Symptom: RPC Method Fails

Checks:
- Method name matches supported component capability.
- Required params are present and type-valid.
- Target component id exists on this device model.

Recovery:
- Re-read status and component layout.
- Retry with minimal valid params and canary scope.

## Symptom: State Does Not Match Expected After Write

Checks:
- Distinguish command acknowledgment from final state notification.
- Verify if concurrent automation rewrote target state.
- Confirm read-after-write delay is sufficient for apply latency.

Recovery:
- Poll state with bounded backoff.
- Temporarily disable conflicting automation path.
- Re-run command with explicit verification gate.

## Symptom: Cloud and Local State Disagree

Checks:
- Ensure both references map to same physical device identity.
- Check for stale cloud sync windows.
- Validate precedence policy between local and cloud writes.

Recovery:
- Treat local state as source for immediate control decisions when reachable.
- Reconcile identity mapping and refresh cloud context before next write.

## Symptom: Batch Rollout Produces Partial Failures

Checks:
- Cohort has mixed capabilities not handled in one payload pattern.
- Retry policy too aggressive, amplifying transient faults.
- Missing fail-fast rules after first critical mismatch.

Recovery:
- Split cohort by capability profile.
- Reduce batch size and apply canary-first rollout.
- Add hard stop and rollback checkpoints per batch.
