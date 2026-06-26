# `/api/prove` idempotency strategy (VAIBot Guard)

VAIBot Guard relies on VAIBot `/api/prove` `idempotencyKey` to make anchoring safe across retries, outages, and replay.

## Principles

- Keys MUST be deterministic and stable across retries.
- Keys SHOULD be unique per logical proof event.
- Keys SHOULD NOT depend on volatile timestamps.

## Keys used by VAIBot Guard

### Per-run receipts

- Precheck receipt: `idempotencyKey = <runId>:precheck`
- Finalize receipt: `idempotencyKey = <runId>:finalize`

Rationale:
- `runId` is generated once per precheck and persisted locally.
- Precheck and finalize are distinct proof events.

### Checkpoint roots

- Checkpoint proof: `idempotencyKey = <sessionId>:checkpoint:<seq>`

Rationale:
- `seq` is monotonically increasing per session.
- Replay flush can safely retry without duplicating proofs.

## Notes

- VAIBot `/api/prove` uses `idempotencyKey` as `requestId` in queue mode.
- VAIBot leaves/merkle batching do **not** include `metadata`.
