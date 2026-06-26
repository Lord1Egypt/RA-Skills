# Write Rules

## Source of truth

Daily memory is the source of truth:
- `memory/YYYY-MM-DD.md`

Indexes and derived files are caches:
- `memory-index/by-date.json`
- `memory-modules/`
- `memory-entities/`

## Write flow

For a high-value interaction:
1. Append or update the relevant daily memory entry.
2. Maintain a short `Preview` only for quick glance; do not force the whole day into 3 sentences.
3. Add or update `Topic Summaries` when the day spans multiple recurring topics.
4. Update `memory-index/by-date.json`.
5. If the topic is likely to recur, create or update the matching module file.
6. If a stable object is central, create or update the entity file.
7. If the interaction reveals reusable execution facts, update `critical-facts/`.
8. If the result is a standing rule, promote it to `MEMORY.md` or a project file.

## Do not over-index

Do not create modules for one-off phrases.
Do not create entities for throwaway nouns.
Do not mirror every daily note into every index.

## Status fields

Prefer these fields for high-value entries:
- importance: low | medium | high | critical
- confidence: confirmed | likely | uncertain
- status: active | superseded | resolved | archived
- loop_status: open | closed
- next_action
- owner
