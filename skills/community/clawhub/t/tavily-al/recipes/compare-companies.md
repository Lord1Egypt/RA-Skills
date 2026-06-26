# Recipe: Compare Companies

## Goal
Produce a side-by-side, cited comparison of two or more companies across defined dimensions (e.g. products, funding, headcount, recent news), grounded in Tavily search and extract results.

## When to use
- The user wants a structured comparison ("X vs Y") rather than a single answer.
- You need per-company, per-dimension facts each backed by a source.
- Do NOT use for a single company profile (use `build-research-brief.md`).

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `companies` | Yes | Two or more company names. |
| `dimensions` | Yes | Comparison axes (e.g. products, funding, employees, latest news). |
| `TAVILY_API_KEY` | Yes | From environment. Never hardcode. |
| `freshness` | No | For news/financials, use `topic:"news"` + `time_range`. |

## Steps
1. **Read `TAVILY_API_KEY`** from environment; abort if missing.
2. **Generate per-company, per-dimension queries** (e.g. "<Company A> total funding 2025"). Use `prompts/query-planning.md`.
3. **Search each query** via `POST https://api.tavily.com/search` (`search_depth:"advanced"`, small `max_results`). Validate status.
4. **Prefer authoritative sources** per company (official site, filings, reputable press); rank by `score`.
5. **Extract** full text for the strongest source per cell when snippets are insufficient.
6. **Evaluate sources** (`prompts/source-evaluation.md`); avoid relying on a single source for a contested figure.
7. **Fill the comparison matrix:** one cell per (company × dimension), each with a value and a `[n]` citation. Mark unknowns as "Not found".
8. **Hallucination-check** every cell against its source.
9. **Return** the matrix plus a numbered sources list.

## Output format
```
Comparison: <Company A> vs <Company B>

| Dimension | Company A | Company B |
|-----------|-----------|-----------|
| Products  | ... [1]   | ... [4]   |
| Funding   | ... [2]   | ... [5]   |
| Headcount | Not found | ... [6]   |
| Latest news | ... [3] | ... [7]   |

Sources:
[1] Title — https://...
...
```

## Example
`companies:["Anthropic","Mistral AI"]`, `dimensions:["flagship model","funding","HQ"]`. Run 6 targeted searches, extract the best source per cell, fill the matrix with citations, mark any missing value as "Not found".

## Edge cases
- **Asymmetric data** (one company well-covered, the other not): use "Not found" rather than guessing or borrowing the other's figures.
- **Stale figures:** funding/headcount age quickly — prefer recent sources and note the date.
- **Conflicting numbers:** cite the most authoritative source and note the discrepancy.
- **429:** Back off; gather what you can and flag incomplete cells.

## Production notes
- One focused query per cell beats one broad query; it keeps citations precise.
- Date-stamp volatile metrics (funding, valuation, employee count).
- Do not normalize/convert figures silently; keep them as the source states unless conversion is explicit and cited.
- > Verification needed: confirm reliable source patterns for financial data with https://docs.tavily.com
