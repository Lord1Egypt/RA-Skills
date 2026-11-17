# Durable checkpoint writeback

## Transaction

1. Confirm permitted persistence and material change. Keep private project data out of distributable code.
2. Resolve/read the canonical ledger. Retain its durable ID and storage revision. A new local filename is not a reason to create a second ledger.
3. Prepare the intended delta against that revision; preserve unrelated/user edits. Use stable entry IDs and reuse them on retry.
4. Apply corrections and dependent-claim invalidation. Preserve exact values, exclusions and provenance. Check invariants manually or with `ledger_guard.py` for v2 JSON.
5. Review privacy; write through the owner skill's supported route using the observed revision guard when available. Never bypass a failed guard with an unguarded overwrite.
6. Inspect every receipt and durable identity. An authoritative success establishes `written`. Read back for material exactness, uncertainty, concurrency or required publication gates; avoid redundant reads solely to announce persistence.
7. After a conflict, read the changed canonical content and semantically merge the delta. Reconcile overlapping edits; never replay a stale snapshot blindly. Without a storage concurrency guard, use fresh read/merge and do not call it atomic.

## Receipt states and retries

| State | Evidence |
| --- | --- |
| prepared | Assembled only, including a scratch copy |
| written | Supported durable write succeeded; retain returned identity/version |
| verified | Persisted content subsequently checked for stated scope |
| failed | Definitive failure observed |
| unavailable | No permitted persistent writing capability |
| unknown | Timeout/interruption without definitive outcome |

For `unknown`, inspect target/new version before retrying. Use provider idempotency only if supported. A local operation ID aids comparison but does not make an API idempotent. Compare stable IDs and intended delta to prevent duplicates. Do not silently convert unknown to success/failure.

Avoid endless ledger writes to store their own final revision. Keep returned receipts in session state or a later real milestone. `base_revision` means the revision the write read, never an invented future version.

## Privacy, forgetting and retention

Remove credentials, authentication cookies, private keys, signed/credential-bearing URLs, raw command history and irrelevant sensitive details. Pattern checks supplement semantic review. Store safe source references instead of secrets; minimize identifiers in errors.

On authorized forgetting, remove the content from owned current and derived records, not merely mark its text superseded. If useful/permitted, keep only an opaque entry ID, deletion time and scope as a content-free suppression marker. Never retain the deleted value, a revealing title or guessable hash. This prevents resurrection from older checkpoints. Verify supported deletions and state limits for native Memory/source history/backups that cannot be controlled here. Do not delete unrelated original artifacts without authorization.

Expire temporary state from active retrieval; retain useful decisions/outcomes unless deletion requested. Expiry does not prove a real-world activity completed.

## Handoff and fallback

Use one canonical checkpoint across continuity skills. Separate last verified and pending operations. After context loss re-open evidence when a current change affects the next action. Never repeat an external mutation solely because a summary lacks a receipt.

Without persistence, provide a useful compact checkpoint as `prepared`/`unavailable` and continue feasible work. Claim no future cross-chat availability. Writing a ledger is not updating native Memory.
