# Shelly Device Operations Workflow

Use this sequence for reliable command execution on Shelly devices.

## Local RPC Pattern

Use `/rpc` with method + params payloads and request ids for traceability.

## Canonical Control Loop

1. Resolve target devices and component ids.
2. Read baseline status and reachability.
3. Validate supported methods and parameter constraints.
4. Build command payload.
5. Execute command through chosen transport.
6. Re-read status and verify expected state.
7. Record result and halt on mismatch.

## High-Impact Device Classes

Apply stronger confirmation for:
- high-current relays and contactors
- heating and energy-intensive circuits
- security-triggering automations

## Write Discipline

- Use one-device canary before batch commands.
- Bound retries and log first-failure signature.
- Abort full batch on first critical verification failure.

## State Validation

- Treat command acknowledgment as intermediate, not final success.
- Require observed final state match before marking task complete.
