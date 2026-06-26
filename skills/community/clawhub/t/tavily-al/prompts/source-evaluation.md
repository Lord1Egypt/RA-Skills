# Prompt: Source Evaluation

## Purpose
Judge the reliability of each Tavily result before trusting it. The model weighs the relevance `score`, domain authority, recency, and corroboration across independent sources, and decides which results to keep, deprioritize, or drop.

## Reusable prompt template
```
Evaluate the reliability of these search results for the claim/topic below.

Topic or claim:
{{claim_or_topic}}

Results (from Tavily):
{{results_json}}   # array of {title, url, content, score, raw_content}

Today's date: {{today}}

For each result, output JSON:
{
  "url": "<url>",
  "relevance_score": <0-1 from Tavily>,
  "domain_authority": "high | medium | low",   # official/primary > established media > unknown blog
  "recency": "fresh | dated | unknown",
  "independent": true|false,                    # distinct domain/owner vs other kept sources
  "verdict": "keep | deprioritize | drop",
  "reason": "<short justification>"
}

Then output:
{
  "kept": ["<url>", ...],
  "corroboration": "strong | weak | single-source",
  "notes": "<conflicts, gaps, or caveats>"
}

Rules:
- Drop results with very low relevance_score unless coverage is otherwise empty.
- Treat a single source as weak; require independent corroboration for contested claims.
- Down-weight dated sources for time-sensitive claims.
- Prefer primary/official sources over aggregators for facts and figures.
```

## Variables
| Variable | Description |
|----------|-------------|
| `{{claim_or_topic}}` | The claim or topic the sources are meant to support. |
| `{{results_json}}` | The Tavily `results` array to evaluate. |
| `{{today}}` | Current date, for recency judgments. |

## Example use
Pass the `results` from a search about a company's funding total. The model should mark the official press release / filing as `high` authority, a random blog as `low`, and report `corroboration: strong` only if two independent reputable sources agree.

## Bad example
```
"This one has the highest score, so it must be true."
verdict: keep (single source, low-authority blog, no corroboration)
```
Treats `score` as truth, ignores domain authority, recency, and independence.

## Good example
```json
{
  "kept": ["https://sec.gov/filing/...", "https://reuters.com/article/..."],
  "corroboration": "strong",
  "notes": "Filing (primary, high authority) corroborated by Reuters (independent). A personal blog with score 0.62 dropped: low authority, no corroboration."
}
```

> Verification needed: Tavily `score` reflects relevance, not factual accuracy — confirm its exact meaning with https://docs.tavily.com
