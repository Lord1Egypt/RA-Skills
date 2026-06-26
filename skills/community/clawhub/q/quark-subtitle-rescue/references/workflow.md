# Workflow Reference

## Decision flow

1. Run baseline batch.
2. If success rate >= 70%, run strict remaining retry.
3. If one folder dominates failures, switch to folder-specific script.
4. If mismatch risk appears, pause and validate before uploads.
5. For final long-tail files, run explicit alias queries.

## Success criteria

- Batch-level: successful upload exists for target files.
- Quality-level: spot checks do not show repeated wrong subtitle content.
- Delivery-level: report lists completed and pending folders.

## Recommended cadence

- Large sets: process in batches and add small waits to reduce 429.
- Long-tail: 5–10 files per manual precision pass.
