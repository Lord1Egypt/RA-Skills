---
name: tavily
description: Web search and content extraction using Tavily Search/Extract/Research APIs (Bearer auth). Use when you need web results (general/news/finance), date/topic/domain filtering, source citations, or want Tavily instead of built-in web_search/Firecrawl. Requires TAVILY_API_KEY.
version: 1.0.0
compatibility: Requires env var TAVILY_API_KEY
requires_env: [TAVILY_API_KEY]
primary_credential: TAVILY_API_KEY
outbound_hosts: ["api.tavily.com"]
metadata:
  hermes:
    tags: [Web, Search, Tavily, Research, API, Citations]
    requires_env: [TAVILY_API_KEY]
    outbound_hosts: ["api.tavily.com"]
  openclaw:
    requires:
      env: ["TAVILY_API_KEY"]
---

# Tavily (Web Search / Extract / Research)

## Prereqs

- Ensure `TAVILY_API_KEY` is set in the Hermes environment (commonly `~/.hermes/.env`).
- Do not hardcode or paste API keys into chat logs. See `references/bp-api-key-management.md`.

## Security Notes

- The bundled CLI (`scripts/tavily.py`) reads only `TAVILY_API_KEY` from the environment and only sends requests to `https://api.tavily.com`.
- Prefer `search` then `extract` over `include_raw_content` on `search` to keep outputs small and reduce accidental data exposure.

## Quick Reference

Use the terminal tool to run the bundled CLI script (prints JSON).
`SKILL_DIR` is the directory containing this `SKILL.md` file.

```bash
# Search (general)
python3 SKILL_DIR/scripts/tavily.py search --query "latest OpenAI API changes" --max-results 5

# Search (news) with recency filter
python3 SKILL_DIR/scripts/tavily.py search --query "latest OpenAI API changes" --topic news --time-range week --max-results 5

# High-precision search (more cost/latency)
python3 SKILL_DIR/scripts/tavily.py search --query "OpenAI API rate limits March 2026" --search-depth advanced --chunks-per-source 3 --max-results 5

# Search + answer (still cite URLs from results)
python3 SKILL_DIR/scripts/tavily.py search --query "What is X?" --include-answer basic --max-results 5

# Extract (targeted chunks; prefer this over include_raw_content on search)
python3 SKILL_DIR/scripts/tavily.py extract --url "https://example.com" --query "pricing" --chunks-per-source 3 --format markdown

# Research (creates task + polls until complete)
python3 SKILL_DIR/scripts/tavily.py research --input "Summarize the EU AI Act enforcement timeline. Provide numbered citations." --model auto --citation-format numbered --max-wait-seconds 180
```

Use returned `results[].url` fields as citations/sources in your final answer.

## No-Script Option (curl)

Use Tavily directly via curl (same endpoints, no bundled script):

```bash
curl -s "https://api.tavily.com/search" \
  -H "Authorization: Bearer <TAVILY_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"query":"latest OpenAI API changes","topic":"news","time_range":"week","max_results":5}'

curl -s "https://api.tavily.com/extract" \
  -H "Authorization: Bearer <TAVILY_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"urls":"https://example.com","query":"pricing","chunks_per_source":3,"extract_depth":"basic","format":"markdown"}'
```

## Procedure

1. Turn the user request into a focused search query (keep it short, ideally under ~400 chars). Split multi-part questions into 2-4 sub-queries.
2. Choose `topic`:
   - `general` for most searches
   - `news` for current events (prefer also setting `time_range` or date range)
   - `finance` for market/finance content
3. Choose `search_depth`:
   - Start with `basic` (1 credit) unless you need higher precision.
   - Use `advanced` (2 credits) for high-precision queries; use `chunks_per_source` to control snippet volume.
4. Keep `max_results` small (default 5) and filter by `score` + domain trust.
5. For primary text, run `extract` on 1-3 top URLs:
   - Provide an `extract --query ... --chunks-per-source N` to avoid dumping full pages into context.
6. For synthesis across multiple subtopics with citations, run `research` and poll until `status=completed`.

## Pitfalls

- `include_raw_content` on `search` can explode output size; prefer the two-step flow: `search` then `extract`.
- `auto_parameters` can silently pick `search_depth=advanced` (2 credits). Set `--search-depth` explicitly when you care about cost.
- `exact_match` is restrictive; wrap the phrase in quotes inside `--query` and expect fewer results.
- `country` boosting is only available for `topic=general`.
- On failures, keep the `request_id` from responses for support/debugging.

## Verification

- Check credits/limits: `python3 SKILL_DIR/scripts/tavily.py usage`
- Add `--include-usage` on `search`/`extract` if you want per-request usage info.

## References

- `references/search.md`
- `references/extract.md`
- `references/research.md`
- `references/research-get.md`
- `references/bp-search.md`
- `references/bp-extract.md`
- `references/bp-research.md`
- `references/bp-api-key-management.md`
- `references/usage.md`
