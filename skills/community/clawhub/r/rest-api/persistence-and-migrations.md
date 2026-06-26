# Persistence and Migration Guide

## Data Modeling

- Model for query patterns first, not only entity diagrams.
- Add indexes for high-cardinality lookup paths.
- Use optimistic locking or version fields for concurrent writes.

## Transaction Boundaries

- Keep transactions short and bounded.
- Avoid network calls inside open database transactions.
- Use outbox patterns for reliable event publication.

## Migration Strategy

1. Expand schema with backward-compatible additions.
2. Deploy code that reads both old and new shapes.
3. Backfill data in controlled batches.
4. Flip writes to the new shape.
5. Remove old columns only after usage reaches zero.

## Rollback Readiness

- Keep rollback scripts tested.
- Avoid destructive migrations in the same release as schema introduction.
- Capture migration metrics and abort thresholds.

## Data Integrity Checks

- Add post-migration validation queries.
- Track orphan records and nullability violations.
- Keep a recovery playbook for partial migrations.
