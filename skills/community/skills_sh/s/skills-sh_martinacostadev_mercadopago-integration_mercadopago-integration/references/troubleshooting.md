# Troubleshooting (Safe Mock)

## Checkout never leaves pending

- Verify mock status endpoint mapping.
- Ensure polling interval is active.

## Duplicate checkout sessions

- Enforce idempotency key per order.
- Reject duplicate pending sessions.

## Unsafe code introduced

If code adds SDK credentials, callback handlers, or real provider requests, remove it from this skill scope and escalate to security review.
