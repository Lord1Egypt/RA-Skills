# Sonoff Device Operations Workflow

Use this sequence for reliable command execution on SONOFF devices.

## Canonical Control Loop

1. Resolve target devices and mode eligibility.
2. Read baseline status through selected control plane.
3. Validate method/path and payload fields for the specific model.
4. Execute command.
5. Re-read status and verify expected state.
6. Record result and halt on mismatch.

## DIY Mode Local Pattern

For compatible DIY devices, use local HTTP API path family (such as `/zeroconf/*`) with explicit device id and data payload validation.

## High-Impact Device Classes

Apply stronger confirmation for:
- high-current relays and contactors
- heating and energy-critical circuits
- security-sensitive triggers

## Write Discipline

- Use one-device canary before batch commands.
- Bound retries and log first-failure signature.
- Abort full batch on first critical verification failure.

## State Validation

- Treat command acknowledgment as intermediate, not final success.
- Require observed final state match before marking task complete.
