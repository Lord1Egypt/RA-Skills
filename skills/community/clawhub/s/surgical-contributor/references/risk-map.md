# Risk Map

Use this file while choosing a target bug and during self-review.

## High-Leverage Areas

1. Navigation and state consistency
- Selection state after filtering, sorting, or folder switches
- Current index validity after deletes/moves/refreshes
- Cursor focus and active-pane mismatches

2. Batch actions and drag/drop correctness
- Partial-application failures in mixed-validity selections
- Ordering assumptions in drop handlers
- Duplicate or skipped item mutations

3. Delete and undo/redo integrity
- Missing inverse operations
- Undo stack corruption after chained actions
- Redo invalidation edge cases

4. Cache, prefetch, and invalidation behavior
- Stale previews/thumbnails after edits or metadata updates
- Orphaned cache entries after rename/move/delete
- Incorrect cache key assumptions across platforms

5. Startup and configuration resilience
- Invalid config defaults or migration regressions
- Missing dependency fallbacks (platform-specific)
- Slow-start fallbacks that break first interaction

6. Inter-layer boundary contracts
- Message/payload schema drift
- Missed property or attribute change notifications
- Type coercion and serialization mismatches across layers

7. Platform path and filesystem edge cases
- Windows path normalization and separator drift
- Case sensitivity assumptions
- Unicode and long-path handling

## Quick Triage Heuristics

- Prefer bugs reproducible in less than five steps.
- Prefer defects that affect hot paths (culling, navigation, editing, batching).
- Prefer fixes with local invariants over broad design changes.
- Prefer adding one focused test over touching many loosely related tests.

## Behavior Drift Watchlist

Before finalizing, verify:

- Selection remains stable across operation boundaries.
- Undo/redo semantics stay intuitive and lossless.
- Cache updates reflect source-of-truth changes.
- UI views/components receive updated state exactly once per transition.
- Platform-specific behavior remains consistent with existing conventions.
