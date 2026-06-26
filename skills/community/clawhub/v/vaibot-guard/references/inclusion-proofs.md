# Inclusion Proofs (Merkle)

VAIBot Guard can generate Merkle inclusion proofs for individual events.

## Stored data

Per session (under `VAIBOT_GUARD_LOG_DIR`):

- `<session>.jsonl` — raw events (source of truth)
- `<session>.leaves.jsonl` — leaf hashes in chronological order (one per event)
- `<session>.checkpoints.jsonl` — periodic checkpoint receipts containing Merkle roots

`leafHash = sha256("leaf:" + eventHash)`

## Proof generation

Endpoint: `POST /api/proof`

Request:
```json
{ "sessionId": "...", "index": 0, "checkpointSeq": 1 }
```

- `index` is 0-based event index.
- `checkpointSeq` selects which checkpoint root to prove inclusion against.

Response:
```json
{
  "ok": true,
  "sessionId": "...",
  "index": 0,
  "count": 50,
  "leaf": "<leafHash>",
  "siblings": ["<hash>", "<hash>", "..."],
  "root": "<computedRoot>",
  "checkpoint": { "seq": 1, "root": "...", "count": 50 }
}
```

The verifier recomputes the root by hashing `leaf` with each sibling hash along the path.

## Performance note

Current implementation recomputes the proof from stored leaves (O(n) time, O(n) memory for the selected checkpoint window). This is acceptable for MVP and can be optimized later by storing per-level hashes per checkpoint window.
