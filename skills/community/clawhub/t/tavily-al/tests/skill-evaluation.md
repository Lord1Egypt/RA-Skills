# Test: Skill Evaluation

## Purpose
Define how to evaluate whether an agent uses the Tavily skill correctly. Evaluation focuses on five competencies: (1) choosing the right operation, (2) citing sources, (3) handling errors, (4) controlling cost, (5) respecting freshness.

## How to run
For each scenario, give the agent the prompt, observe its tool choices, requests, and final output, then score against the pass criteria. Use a fresh session per scenario. Never provide a real API key — use a placeholder and assert the agent reads it from the environment.

## Evaluation checklist
- [ ] Selects the correct Tavily operation (search vs extract vs crawl/map) for the task.
- [ ] Reads `TAVILY_API_KEY` from the environment; never hardcodes or prints it.
- [ ] Uses `Authorization: Bearer <TAVILY_API_KEY>` header.
- [ ] Applies `topic:"news"` + `time_range` when the question is time-sensitive.
- [ ] Ranks/filters results by `score` and prefers independent, authoritative domains.
- [ ] Produces inline `[n]` citations + a sources list for factual answers.
- [ ] Grounds every claim in retrieved content (passes a hallucination check).
- [ ] Handles `401` (auth), `422` (do not retry identical), `429` (backoff) correctly.
- [ ] Controls cost: sensible `max_results`, `basic` depth by default, raw_content only when needed.
- [ ] States uncertainty/limitations instead of overstating thin evidence.
- [ ] Marks genuine unknowns with `> Verification needed: ... https://docs.tavily.com`.

## Test scenarios
| # | Scenario / prompt | Expected behavior | Pass criteria |
|---|-------------------|-------------------|---------------|
| 1 | "What's the latest on X this week?" | Search with `topic:"news"`, `time_range:"week"`. | Uses news topic + week range; cites sources. |
| 2 | "Summarize https://example.com/article." | Use Extract on the URL, summarize from `raw_content`. | Calls extract (not search); summary grounded in extracted text. |
| 3 | "Answer Q and show your sources." | Search + synthesize + cite. | Inline `[n]` + sources list; every claim cited. |
| 4 | Simulated `401` response. | Report auth failure; stop. | No blind retry; clear key/auth message. |
| 5 | Simulated `422` on a malformed body. | Fix request, do not retry identical. | Does not re-send the same bad body. |
| 6 | Simulated `429`. | Exponential backoff, limited retries. | Backs off; reports quota if persistent. |
| 7 | "Compare Company A vs B on funding." | Per-cell targeted searches; matrix with citations; "Not found" for gaps. | Side-by-side cited matrix; no fabricated figures. |
| 8 | Vague broad question. | Decompose into scoped sub-queries first. | Uses query planning; avoids one giant query. |
| 9 | Key not set in environment. | Detect missing key; abort gracefully. | Refuses to call API; clear message; no hardcoding. |
| 10 | Question with conflicting sources. | Present both positions, cite each. | Surfaces conflict; does not silently pick one. |
| 11 | Cost-sensitive bulk lookup. | `basic` depth, small `max_results`, batch extracts. | Demonstrates cost control choices. |
| 12 | Claim with only one weak source. | State low confidence; seek corroboration. | Flags single-source/low-confidence; no overstatement. |

## Scoring rubric
Score each scenario 0–2 and sum (max = 2 × scenarios).

| Score | Meaning |
|-------|---------|
| 2 | Fully meets pass criteria; correct operation, correct error/cost/freshness handling, fully cited. |
| 1 | Mostly correct but with a minor lapse (e.g. weak citation, slightly over-broad query, suboptimal depth). |
| 0 | Fails a core criterion (wrong operation, no citations, retries 422, exposes key, ignores freshness, fabricates). |

Overall thresholds:
- **Pass:** >= 90% of max AND zero `0`s on scenarios 3, 4, 5, 9 (citations, auth, 422, key safety are mandatory).
- **Borderline:** 75–89% with no `0` on mandatory scenarios — fix lapses and re-test.
- **Fail:** < 75% OR any `0` on a mandatory scenario.

> Verification needed: confirm exact error semantics for 401/422/429 and current cost model with https://docs.tavily.com
