# Resource Hunter 2.1.1

## Summary

This is a presentation-polish release on top of the success-first source-expansion work.

It keeps the expanded runtime intact while making the GitHub / ClawHub first impression clearer and more accurate.

## Highlighted capabilities

- structured torrent support through `animetosho`, `dmhy`, and `torlock`
- structured pan/clue support through `dalipan`
- indexed discovery fallback through `search-index:bing` and `search-index:brave`
- layered retrieval with direct / actionable / clue semantics
- stronger title/year validation and evidence fusion

## Important semantics

### Dalipan
- anonymous search is confirmed
- runtime emits `dalipan://provider/eu-token`
- current Dalipan results are structured clue outputs, not guaranteed final share URLs

### Bing / Brave
- public HTML fallback only
- useful for indexed discovery and recall
- still best-effort fallback providers

## Presentation improvements

- clearer README hero copy
- tighter ClawHub-facing SKILL description
- cleaner release-facing phrasing around current strengths and limits
- validation snapshot updated for the current synchronized state

## Validation

- focused runtime/source regression set: `96 passed, 1 skipped`
- `ruff check skills/resource-hunter`: passed
- GitHub `resource-hunter-ci`: green

## Follow-up

- finish PanSearch content-card link extraction before integration
- revisit Dalipan detail/url completion and transport hardening
- continue one-by-one probing for additional public no-API sources
