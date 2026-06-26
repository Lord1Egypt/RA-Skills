# Metadata indexing (VAIBot Guard)

VAIBot Guard sends `metadata` alongside `/api/prove` requests. Metadata is **not required for cryptographic verification**, but is useful for UX, triage, and audit workflows.

## Recommended metadata keys (default)

- `schema` (string)
  - e.g. `vaibot-guard/receipt@0.1`, `vaibot-guard/checkpoint@0.1`
- `kind` (string)
  - e.g. `exec`, `merkle.checkpoint`
- `runId` (string, optional)
- `sessionId` (string, optional)

## Optional metadata keys (useful later)

- `policyVersion`
- `risk` (e.g. `low|high`)
- `checkpointSeq`

## Where metadata should be stored

- For queued proofs, metadata should be persisted in DB alongside the job/proof record so operators can filter/search.
- It should NOT be hashed into Merkle leaves in v1 (keep verification stable).

## Current VAIBot backend status

- `/api/prove` currently accepts `metadata` but does not persist it directly.
- Queue path now stores metadata inside `verification_jobs.leaf_payload.metadata`.

Future backend work:
- Add a dedicated column/JSONB field for metadata on the proofs/jobs table (or materialize key fields for indexing).
