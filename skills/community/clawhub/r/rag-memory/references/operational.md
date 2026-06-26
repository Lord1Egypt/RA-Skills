# Operational Guide — vector_search

## When to call vector_search

Always prefer `vector_search` over reading full memory files. Specifically:

- Before reading MEMORY.md → call `vector_search` with `scope: memory` first
- Before reading any daily log file → call `vector_search` with `scope: memory`
- Before reading TOOLS.md → call `vector_search` with `scope: docs`
- Before reading any SKILL.md → call `vector_search` with `scope: docs`
- Only fall back to reading the full file if vector_search returns no results above threshold

## Scope selection

| Situation | scope to use |
|---|---|
| Looking for a past incident, config detail, or fact | `memory` |
| Looking for a tool, command, or how-to | `docs` |
| Unsure which | `all` |

## Interpreting scores

- `score >= 0.85` — high confidence, treat as authoritative
- `score 0.70–0.84` — relevant but verify against context
- `score < 0.70` — below threshold, not returned (filtered by plugin)
- No results returned — nothing relevant in memory, or Qdrant unreachable

## top_k guidance

- Routine lookups: `top_k: 3` is enough
- Incident reconstruction (multiple related facts): `top_k: 7`
- Never exceed `top_k: 10`

## If Qdrant is unreachable

1. Try once — do not retry in a loop
2. Fall back to reading the relevant file directly
3. Note in your response that vector search was unavailable
4. Do not attempt to restart Qdrant automatically — alert the user instead
5. Check: `curl $QDRANT_HOST/readyz`

## If results seem stale or wrong

Ask the user: "Results may be outdated — should I run a resync?"

```bash
~/.openclaw/skills/rag-memory/venv/bin/python ~/.openclaw/skills/rag-memory/sync_to_qdrant.py
```

If the question is urgent, fall back to reading the file directly while sync runs.

## Citing results

When using vector_search results in a response, briefly indicate the source:
- `[from MEMORY.md]`, `[from 2026-03-25.md]`, `[from TOOLS.md]` etc.
- Include the date if it came from a daily log — relevance may be time-sensitive
