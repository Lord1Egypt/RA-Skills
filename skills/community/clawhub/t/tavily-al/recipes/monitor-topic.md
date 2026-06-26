# Recipe: Monitor a Topic

## Goal
Track recent developments on a topic over time by repeatedly running freshness-scoped Tavily news searches and reporting only genuinely new, relevant items.

## When to use
- The user wants ongoing or periodic updates ("what's new on X this week").
- Recency is the priority; current events, releases, incidents.
- Do NOT use for static/background questions — use `search-the-web.md` or `build-research-brief.md`.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `topic_query` | Yes | The subject/keywords to monitor. |
| `TAVILY_API_KEY` | Yes | From environment. Never hardcode. |
| `time_range` | Yes | Freshness window: `"day"`, `"week"`, `"month"`. |
| `seen_urls` | No | Set of URLs already reported, to suppress duplicates. |
| `max_results` | No | Items per run (default 5–10). |

## Steps
1. **Read `TAVILY_API_KEY`** from environment; abort if missing.
2. **Build a news search:** `POST https://api.tavily.com/search` with `topic:"news"`, the given `time_range`, `search_depth:"advanced"`, and `max_results`.
3. **Validate status** (`401`/`422`/`429`).
4. **Filter for freshness and relevance:** keep results within the window, rank by `score`, drop off-topic items.
5. **Deduplicate** against `seen_urls`; report only items not seen before.
6. **Summarize each new item** in one line, grounded in its `content`/`raw_content`, with its source URL.
7. **Update `seen_urls`** with the newly reported URLs for the next run.
8. **Return** a dated digest of new items (or "no new developments" if empty).

## Output format
```
Update for "<topic_query>" — window: <time_range> — <date>
- <one-line summary> — https://example.com/new1 (score 0.91)
- <one-line summary> — https://example.com/new2 (score 0.88)

(or: No new developments in this window.)
```

## Example
`topic_query:"OpenAI model releases"`, `time_range:"week"`. Run weekly: search news, drop URLs already in `seen_urls`, summarize the rest, and persist new URLs.

## Edge cases
- **All results already seen:** Report "no new developments"; do not re-summarize old items.
- **Empty results:** Widen `time_range` once; if still empty, report no activity.
- **Spammy/low-score items:** Filter by `score` threshold to avoid noise.
- **429 on a scheduled run:** Back off and retry; if it fails, skip this cycle and note the gap.

## Production notes
- Persist `seen_urls` between runs (e.g. small store keyed by topic) — without it you will re-report duplicates.
- Match `time_range` to cadence (daily run -> `"day"`, weekly -> `"week"`) to avoid both gaps and overlap.
- Keep `max_results` modest to control recurring cost.
- > Verification needed: confirm the full list of supported `time_range` values for `topic:"news"` with https://docs.tavily.com
