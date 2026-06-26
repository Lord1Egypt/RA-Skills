# Maintenance Patterns

Use this file when adding freshness checks and refresh workflows.

## Goal

Avoid expensive full rebuilds when only a small part of the workspace changed.

## Recommended maintenance layers

1. **Status**
   - Report document and chunk counts.
   - Surface metadata needed for quick health checks.

2. **Fingerprinting**
   - Track corpus-level fingerprints.
   - Optionally track file-level signatures for selective refresh.

3. **Action planning**
   - Decide between:
     - `no-op`
     - `file-selective-reindex`
     - `selective-reembed`
     - `full-rebuild`

4. **Selective refresh**
   - Reindex only changed files when the changed set is small enough.
   - Re-embed only new or changed chunks when possible.

5. **Smoke tests**
   - Query a core concept expected to hit the target corpus.
   - Verify corpus filtering.
   - Verify one denied access path.

## Good defaults

- fingerprints based on path + size + mtime
- compact JSON output for automation
- fallback to full rebuild only when selective paths become too messy

## Operational guidance

Prefer status-first maintenance:
1. inspect status
2. compute changed corpora / files
3. choose the lightest reliable action
4. run smoke tests

## Known failure classes to guard against

- stale embeddings after selective reindex
- indexing private directories because exclude globs were incomplete
- wrapper and policy config drifting apart
- overlapping corpora causing noisy duplicate recall
