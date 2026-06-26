# Soul Memory v3.6.2

## Fixes

1. Restore `_build_index()` implementation
   - memory index now actually builds real segments again
   - `cache/index.json` includes `built_at` and category metadata

2. Preserve v3.6.1 injection pipeline improvements
   - pure JSON CLI output
   - prefer last real user message
   - typed memory focus grouping
   - distilled summaries
   - audit logging

## Result

Heartbeat / CLI / plugin memory search no longer depends on an empty index.

## Version

- Core: v3.6.2
- Skill metadata: v3.6.2
