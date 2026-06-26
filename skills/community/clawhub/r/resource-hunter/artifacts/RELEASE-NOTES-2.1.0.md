# Resource Hunter 2.1.0

## Summary

This release prepares `skills/resource-hunter` for sync after a success-first source-expansion wave focused on real public no-API retrieval.

## Added / integrated

### Structured torrent sources
- `animetosho`
- `dmhy`
- `torlock`

### Structured pan / clue source
- `dalipan`

### Indexed discovery fallback
- `search-index:bing`
- `search-index:brave`

## Retrieval changes

- layered retrieval is now explicit in runtime metadata
- query planning, source-aware budgets, validation, and evidence fusion are active
- indexed discovery fallback is part of the search flow when direct retrieval is weak
- wrong-year same-title results are downgraded more aggressively

## Important semantics and limits

### Dalipan
- anonymous search is confirmed through the public search API
- runtime currently emits `dalipan://provider/eu-token` placeholders
- these are structured clue records, not guaranteed final share URLs
- anonymous `detail/url` completion is still not fully open in current runtime behavior

### Bing / Brave
- public HTML search fallback only
- best-effort discovery providers
- subject to layout drift, throttling, and regional variation

### Torlock
- detail-page fetches are now isolated so a single broken detail page does not fail the whole source batch

## Validation

- `95 passed, 1 skipped`
- `ruff` all green

## Known follow-up items

- finish PanSearch content-card link extraction before integration
- revisit Dalipan detail/url completion and transport hardening
- continue one-by-one probing for additional public no-API sources
