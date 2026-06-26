# Required mode semantics

`VAIBOT_PROVE_MODE=required` applies to **both**:

- **Per-event receipts** (precheck + finalize)
- **Checkpoint root anchoring** (Merkle checkpoints)

Meaning:
- `/v1/decide/exec` will **fail-closed** if it cannot successfully call VAIBot `/api/prove` for the precheck receipt (including missing `VAIBOT_API_URL`/`VAIBOT_API_KEY` or API outage).
- `/v1/finalize` will return an error if it cannot successfully call `/api/prove` for the finalize receipt.
- Checkpoint flush (`/v1/flush` and background flush) will also **fail-closed** if checkpoint anchoring cannot be completed.

This provides true "no proof, no action" behavior for execution when connectivity/auth are required.
