# Recipe: Search the Web

## Goal
Run a general-purpose web search with the Tavily Search API and return ranked, relevant results (optionally with a synthesized `answer`) that downstream steps can read, cite, or extract from.

## When to use
- The user asks a factual or open-ended question and you need fresh, ranked web results.
- You need a starting set of candidate URLs before doing deeper `extract` or `crawl`.
- You want a quick synthesized answer plus the sources that support it.
- Do NOT use this when you already have a known URL and only need its full text — use `extract-and-summarize.md` instead. Do NOT use it to traverse an entire site — use `crawl`/`map`.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `query` | Yes | Natural-language search string. Keep it focused; 3–12 keywords works best. |
| `TAVILY_API_KEY` | Yes | Read from environment. Never hardcode. |
| `search_depth` | No | `"basic"` (cheaper/faster) or `"advanced"` (deeper retrieval). Default `"basic"`. |
| `topic` | No | `"general"` (default) or `"news"`. Use `"news"` for current events. |
| `time_range` | No | e.g. `"day"`, `"week"`, `"month"`, `"year"` — pairs well with `topic:"news"`. |
| `max_results` | No | Cap result count (e.g. 5). Lower = cheaper. |
| `include_answer` | No | `true` to get a synthesized `answer` field. |
| `include_domains` / `exclude_domains` | No | Domain allow/deny lists for scoping. |

## Steps
1. **Read the API key** from the environment variable `TAVILY_API_KEY`. If it is missing, stop and report that the key is not configured — do not proceed.
2. **Scope the query.** Trim filler words, add disambiguating keywords, and decide whether the question is time-sensitive. If it is, set `topic:"news"` and an appropriate `time_range`.
3. **Choose depth and limits.** Default to `search_depth:"basic"` and `max_results:5` for cheap exploratory searches; escalate to `"advanced"` only when basic results are thin.
4. **Build the request** to `POST https://api.tavily.com/search` with header `Authorization: Bearer <TAVILY_API_KEY>` and a JSON body containing the parameters above.
5. **Send the request** and capture the response.
6. **Validate the response status.** Handle `401`, `422`, and `429` per Edge cases below before reading the body.
7. **Rank and filter results.** Sort by `score` (0–1) descending. Drop low-score results (e.g. `score < 0.5`) unless coverage is sparse.
8. **Return** the top results and, if requested, the `answer`. Pass URLs forward to extract/citation steps as needed.

## Output format
The Search API returns:
```json
{
  "answer": "Optional synthesized answer string (only if include_answer=true)",
  "results": [
    {
      "title": "Page title",
      "url": "https://example.com/page",
      "content": "Short relevant snippet",
      "score": 0.93,
      "raw_content": "Full page text if include_raw_content=true, else null"
    }
  ]
}
```
Present results to the user as a compact ranked list: `title — url (score)`, optionally with the snippet.

## Example
Request body:
```json
{
  "query": "EU AI Act enforcement timeline 2025",
  "topic": "news",
  "time_range": "month",
  "search_depth": "advanced",
  "max_results": 5,
  "include_answer": true
}
```
Expected handling: read `answer` for a quick summary, then list the 5 `results` sorted by `score`, keeping only those above ~0.5.

## Edge cases
- **401 Unauthorized:** API key invalid or missing. Stop, report the auth problem, do not retry blindly.
- **422 Unprocessable Entity:** Malformed request (bad parameter, empty query). Fix the request body; do NOT retry the identical request — it will fail again.
- **429 Too Many Requests:** Rate/quota limit. Back off exponentially and retry a small number of times; if it persists, report quota exhaustion.
- **Empty `results`:** Broaden the query, remove restrictive `include_domains`, drop `time_range`, or switch `search_depth` to `"advanced"`.
- **All low scores:** Treat findings as weak; tell the user the evidence is thin rather than overstating confidence.

## Production notes
- Prefer `"basic"` depth and a small `max_results` by default; `"advanced"` and large result counts cost more.
- Only request `include_raw_content`/`raw_content` when you actually need full text — it inflates payload and cost.
- Cache results for identical queries within a session to avoid duplicate billed calls.
- Log the query and result count (never the key) for debugging.
- > Verification needed: confirm exact accepted `time_range` values and current pricing tiers with https://docs.tavily.com
