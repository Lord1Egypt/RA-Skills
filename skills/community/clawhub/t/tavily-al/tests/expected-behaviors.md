# Test: Expected Behaviors

Concrete GOOD behaviors the agent must exhibit. Each has a short example of correct output. Use these as positive assertions during evaluation.

## 1. Chooses the right operation
Picks search for discovery, extract for known URLs, crawl/map for site traversal.
> "You gave a specific URL, so I'll Extract its full text rather than search." → calls `POST /extract` with that URL.

## 2. Reads the key from the environment
Never hardcodes or prints `TAVILY_API_KEY`.
> "Reading TAVILY_API_KEY from the environment and sending it as `Authorization: Bearer <key>` (value not shown)."

## 3. Applies freshness scoping when needed
Uses `topic:"news"` + `time_range` for time-sensitive questions.
> Request: `{ "query": "...", "topic": "news", "time_range": "week" }` for "what happened this week".

## 4. Ranks and filters by score
Sorts `results` by `score` (0–1), drops weak ones.
> "Keeping the 3 results with score > 0.7; dropping two below 0.5 as low relevance."

## 5. Prefers independent, authoritative sources
Corroborates contested facts across distinct domains.
> "Funding figure confirmed by the SEC filing [1] and Reuters [2] (independent sources)."

## 6. Produces inline citations + a sources list
Every factual claim carries `[n]`; a numbered list follows.
> "The product ships in March 2026 [1] at $999 [2].\n\nSources:\n[1] ... — https://...\n[2] ... — https://..."

## 7. Grounds all claims (passes hallucination check)
No facts beyond retrieved content; unknowns are stated.
> "The sources don't specify a release date, so I can't confirm one."

## 8. Handles 401 correctly
Reports an auth problem and stops; no blind retry.
> "Received 401 Unauthorized — the API key is missing or invalid. Please check TAVILY_API_KEY."

## 9. Handles 422 correctly
Fixes the malformed request; does not resend the identical body.
> "422 indicates a malformed request; the `urls` field was empty. Correcting it and resending once."

## 10. Handles 429 correctly
Exponential backoff with limited retries; reports quota if persistent.
> "429 rate limited — backing off (1s, 2s, 4s). Still limited after 3 tries; likely quota exhausted."

## 11. Controls cost by default
`basic` depth, modest `max_results`, raw_content only when needed, batched extracts.
> "Using search_depth='basic', max_results=5; will only fetch raw_content for the top source if snippets are insufficient."

## 12. States uncertainty honestly
Flags thin or single-source evidence rather than overstating.
> "Only one low-authority source mentions this, so treat it as unconfirmed."

## 13. Reports extraction failures
Surfaces `failed_results`; never fabricates contents of failed URLs.
> "1 of 3 URLs failed to extract (likely paywalled); summarizing the other 2 and noting the gap."

## 14. Decomposes complex questions
Uses query planning to split multi-part questions into scoped queries.
> "This has two parts (battery, price); I'll run one scoped query for each."

## 15. Marks genuine uncertainty about the API
Uses the verification convention for unconfirmed details.
> "> Verification needed: confirm allowed `time_range` values with https://docs.tavily.com"
