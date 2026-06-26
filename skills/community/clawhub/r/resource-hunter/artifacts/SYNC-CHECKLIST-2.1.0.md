# Sync Checklist for 2.1.0

## Must-sync runtime files
- `src/resource_hunter/_version.py`
- `src/resource_hunter/adapters.py`
- `src/resource_hunter/common.py`
- `src/resource_hunter/core.py`
- `src/resource_hunter/engine.py`
- `src/resource_hunter/intent.py`
- `src/resource_hunter/precision_core.py`
- `src/resource_hunter/ranking.py`
- `src/resource_hunter/rendering.py`
- `src/resource_hunter/retrieval_layers.py`
- `_meta.json`
- `pyproject.toml`

## Must-sync tests
- `tests/test_source_expansion.py`
- any already-modified existing regression files that belong to the same release wave

## Must-sync release/docs files
- `README.md`
- `SKILL.md`
- `STATUS.md`
- `NEXT_ACTION.md`
- `references/sources.md`
- `references/architecture.md`
- `references/usage.md`
- `artifacts/RELEASE-NOTES-2.1.0.md`
- `artifacts/live-tests/README.md`

## Evidence files worth keeping
- `artifacts/live-tests/next-batch/probe-summary.md`
- `artifacts/live-tests/the-merry-widow-1952.json`
- selected probe scripts/raw captures only if you want research traceability in the sync

## Final gate snapshot
- targeted pytest regression set: passed
- broader runtime/source regression set: `96 passed, 1 skipped`
- `ruff check skills/resource-hunter`: passed

## Important release caveats
- `dalipan` is currently token-only clue output, not guaranteed final share URL output
- `search-index:bing` and `search-index:brave` are best-effort indexed-discovery fallback providers
- `PanSearch` is not yet integrated
