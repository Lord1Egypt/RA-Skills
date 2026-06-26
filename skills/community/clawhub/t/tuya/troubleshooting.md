# Tuya Troubleshooting and Recovery

Use this guide to resolve the most common Tuya integration failures.

## Symptom: Authentication Fails Immediately

Checks:
- Confirm Access ID and Access Secret are from the active project.
- Confirm endpoint region matches project data center.
- Confirm request timestamp is current.

Recovery:
- Rebuild token request and signature inputs from scratch.
- Retry once with fresh timestamp and nonce.

## Symptom: Signature Errors on Some Requests Only

Checks:
- Signed URL path/query exactly match sent request.
- Body hash matches exact payload bytes.
- Header ordering for signed headers is stable.

Recovery:
- Log canonical string and recompute signature.
- Normalize payload serialization before hashing.

## Symptom: Device Visible but Command Fails

Checks:
- Endpoint uses correct command path for cloud API version.
- Device supports requested function code.
- Value type and range match function schema.
- User/device binding and permissions are valid.

Recovery:
- Re-read function schema and status.
- Test minimal command on single device.

## Symptom: Command Accepted but State Does Not Change

Checks:
- Device online state before and after write.
- Delay required for asynchronous device apply.
- Conflicting automation overwriting desired state.

Recovery:
- Poll status with bounded backoff.
- Disable conflicting automation temporarily.
- Re-run command with verified target value.

## Symptom: Intermittent Fleet Failures

Checks:
- Batch size too large for stable convergence.
- Mixed device capabilities in one rollout plan.
- Unhandled partial success logic.

Recovery:
- Reduce batch size and apply canary-first rollout.
- Split fleet by product capability profile.
- Add per-device verification and fail-fast stop conditions.
