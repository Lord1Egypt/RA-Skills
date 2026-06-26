# RSS-Brew Retry / Finalize Architecture

This file describes the current Phase 1 / Phase 2 retry-protection architecture that was added before and during app-ification.

## Scope
This is the current runtime behavior implemented in the legacy pipeline and exercised through the app CLI wrapper.

## Phase 1 protections

### Per-run manifest
Each run writes:
```text
run-records/YYYY-MM-DD/<run_id>.json
```
Tracking fields include:
- `status`
- `new_articles`
- `deep_set_count`
- `delivery_status`
- run metadata and timestamps

### Committed-only winner selection
Only committed runs are eligible to become the day winner.

### Same-day zero-new guardrail
If an earlier same-day committed run has `new_articles > 0`, a later `new_articles = 0` retry must not overwrite the winner digest.

### Delivery state split
Pipeline status and delivery status are tracked separately.

---

## Phase 2 protections

### Staging per run
Each run stages outputs under:
```text
.staging/<run_id>/
```

### Explicit finalize states
The manifest supports state transitions such as:
- `running`
- `staged`
- `finalize_in_progress`
- `committed`
- `failed`

### Per-day finalize lock
Finalize/publish is guarded with a same-day lock file.

### Versioned publish
Committed outputs are written under:
```text
daily/YYYY-MM-DD/<run_id>/
```

### CURRENT pointer
The day winner is exposed through:
```text
daily/YYYY-MM-DD/CURRENT
daily/YYYY-MM-DD/CURRENT.json
run-records/YYYY-MM-DD/CURRENT.json
```

### Delayed top-level promotion
Top-level outputs are promoted from the winner at finalize time rather than being treated as pre-finalize truth.

---

## Known compatibility detail
Legacy committed manifests from before Phase 2 may not have `published_path`.

The system must remain backward-compatible with those manifests when selecting a winner.

---

## Current phase interpretation
The retry/finalize architecture is now in place, but it is not the same thing as full recovery orchestration.

Still deferred:
- stale lock recovery
- finalize resume
- broader delivery redesign
- stronger automated regression coverage for all retry paths
