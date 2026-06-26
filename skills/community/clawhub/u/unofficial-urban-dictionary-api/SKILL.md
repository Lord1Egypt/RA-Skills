---
name: unofficial-urban-dictionary-api
description: Query the Unofficial Urban Dictionary API for slang definitions. Use when asked to define slang/phrases, fetch random Urban Dictionary entries, browse by letter/new, or get entries by author/date. Supports endpoints /api/search, /api/random, /api/browse, /api/author, and /api/date.
---

Use this skill to fetch Urban Dictionary-style definitions from:

- Base URL: `https://unofficialurbandictionaryapi.com/api`

## Fast path

Prefer running the bundled helper script for deterministic output:

- `python3 scripts/ud_api.py search --term "yeet" --limit 3`
- `python3 scripts/ud_api.py random --limit 1`
- `python3 scripts/ud_api.py browse --character a --limit 5`
- `python3 scripts/ud_api.py author --term "some_author" --limit 5`
- `python3 scripts/ud_api.py date --term "2024-01-01" --limit 5`

If script execution is unavailable, use direct HTTP GET calls to the same endpoints.

## Endpoint mapping

- `search` -> `/search`
- `random` -> `/random`
- `browse` -> `/browse`
- `author` -> `/author`
- `date` -> `/date`

## Common query params

- `term`: word/phrase/author/date (depends on endpoint)
- `limit`: integer > 0
- `strict`: `true|false` (search)
- `matchCase`: `true|false` (search)
- `page`: integer >= 1
- `multiPage`: `min,max` page range string
- `character`: browse target (example: `a`, `new`, `*`)

## Output behavior

When reporting results to users:

1. Show top entries only (default 3–5 unless asked for more).
2. Include:
   - term/word
   - short definition
   - example (if present)
   - thumbs up/down (if present)
   - permalink (if present)
3. If no entries found, say so clearly and suggest a broader query (disable strict, remove matchCase, etc.).
4. Content can be NSFW/offensive; reflect results neutrally without adding extra slurs or escalation.

## Troubleshooting

- Empty result: retry with `strict=false` and lower constraints.
- Bad response: retry once, then report API/network failure.
- Very long entries: truncate cleanly and offer full dump on request.
