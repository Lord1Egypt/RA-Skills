# Example 08 — Error Recovery

Handle 401 / 422 / 429 and empty results gracefully: detect, react (fix vs retry vs refine), and communicate clearly to the user. Includes before/after.

## User request

> "Find recent benchmarks comparing the newest open-weight LLMs."

## Agent reasoning summary

- Network-facing calls fail in predictable ways; I should branch on the HTTP status and on empty results.
- 401 = auth/config problem (cannot retry blindly), 422 = bad request I should fix, 429 = rate limit I should back off and retry, empty results = refine the query.
- I will communicate the cause and the action taken without leaking the API key.

## Tavily operation to use

Use the **search** endpoint, wrapped in error handling that inspects the response status and body.
Why: the task is a normal search, but the value of this example is the recovery logic layered around any Tavily call (search, extract, crawl, or map).

## Request shape

Initial call:

```json
{
  "query": "recent open-weight LLM benchmark comparison",
  "topic": "news",
  "time_range": "month",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 10
}
```

## Response handling — error matrix

| Symptom | Likely cause | Correct reaction |
|---|---|---|
| HTTP 401 | Missing/invalid `TAVILY_API_KEY` or wrong `Authorization` header | Do NOT retry. Check the key is set in the environment; ask the user/operator to fix config. Never print the key. |
| HTTP 422 | Validation error — bad/unknown parameter or malformed value (e.g., invalid `time_range`, empty `query`) | Read the error body, fix the offending field, and re-issue once. |
| HTTP 429 | Rate limit exceeded | Back off and retry with exponential delay + jitter (e.g., 1s, 2s, 4s), up to a small max; then inform the user if still failing. |
| 200 but `results: []` | Query too narrow/odd, or filters too strict | Refine: relax `time_range`, broaden/rephrase `query`, drop restrictive `include_domains`, then retry. |

Detection notes:
- Inspect the HTTP status first; then parse the JSON body for an error message.
- Treat a 200 with empty `results` as a soft failure, not success.
- Cap total retries to avoid loops; each retry should change something (fix, backoff, or refine).

## Before / after

### Before (fragile)

```json
{ "query": "", "time_range": "last_week" }
```

Outcome: server returns **422** (empty `query`, and `time_range` value is not a recognized enum). The naive agent surfaces a raw stack trace or, worse, hallucinates an answer with no data.

### After (resilient)

1. Catch 422, read body: "query must not be empty; time_range must be one of day/week/month".
2. Fix both fields and retry:

```json
{
  "query": "recent open-weight LLM benchmark comparison",
  "topic": "news",
  "time_range": "month",
  "search_depth": "advanced",
  "include_answer": true,
  "max_results": 10
}
```

3. If that returns `results: []`, refine by dropping `time_range` and broadening the query, then retry once.
4. If 429 occurs at any point, back off (1s → 2s → 4s) and retry.
5. If 401 occurs, stop and report a configuration problem (do not retry, do not expose the key).

## Citation behavior

- On success after recovery, cite normally (ranked, deduped sources with `[n]` -> URL).
- On unrecoverable failure, give NO fabricated citations — state plainly that no sources were retrieved.

## Final answer pattern

Success after recovery:

```
Here are recent open-weight LLM benchmark comparisons I found:
- [summary claim] [1]
- [summary claim] [2]

Sources:
[1] ... — https://...
[2] ... — https://...
```

Graceful failure (e.g., 401 unrecoverable):

```
I couldn't complete the search because the Tavily request was rejected
(authentication error, HTTP 401). This usually means the API key is
missing or invalid. Please verify the TAVILY_API_KEY configuration and
I'll try again. I have not guessed an answer, since I retrieved no sources.
```

Rate-limited and still failing:

```
Tavily is rate-limiting requests right now (HTTP 429). I retried with
backoff but still couldn't get through. Please try again shortly.
```

## Common failure mode

Treating every error the same way — e.g., retrying a 401 in a tight loop (which will never succeed and may lock the key), retrying a 422 unchanged (same error forever), or presenting a confident answer when `results` was empty. Also: echoing the API key or full headers in an error message.

## Improved version

- Branch on status: fix (422), back off and retry (429), stop and report (401), refine and retry (empty results).
- Always change something between retries and cap the retry count.
- Never expose secrets in logs or user-facing messages.
- On unrecoverable failure, say so honestly and provide zero fabricated sources.

> Verification needed: confirm the exact set of error status codes and the canonical `time_range` enum values at https://docs.tavily.com
