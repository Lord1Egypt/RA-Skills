# Merkle Roots + Replay (Design notes)

## Goal

- Log all guard events locally in chronological order.
- Maintain an incremental Merkle accumulator over event hashes.
- Periodically create a **checkpoint** containing the current Merkle root.
- Anchor checkpoints to VAIBot `/api/prove`.
- If offline or `/prove` fails, checkpoints remain pending and are replayed later in order.

## State files (per sessionId)

All files live under `VAIBOT_GUARD_LOG_DIR` (default: `${VAIBOT_WORKSPACE}/.vaibot-guard`).

- `<session>.jsonl` — append-only event log (source of truth)
- `<session>.merkle.json` — accumulator state (count, frontier hashes)
- `<session>.checkpoints.jsonl` — checkpoint receipts (root + range)
- `<session>.replay.json` — replay cursor + queue pointers

## Incremental Merkle accumulator (frontier)

- Each event line has a `hash` (sha256 of canonical JSON of the event + prevHash).
- Leaf hash is `sha256("leaf:" + eventHash)`.
- Checkpoint chaining hash (`checkpoint.hash`) is also SHA-256 over a domain-separated canonical payload.
- Maintain an array `frontier[level]` where each entry is the subtree hash for `2^level` leaves.
- On append, "carry" merges like binary addition.

Checkpoint root is computed by folding frontier highest→lowest into a single hash.

## Replay

- Every checkpoint gets an `idempotencyKey` like: `<session>:checkpoint:<seq>`
- On success: persist `lastAnchoredCheckpointSeq`.
- On failure: keep pending; next attempt replays in increasing sequence.
