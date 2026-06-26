# Test: Failure Cases

BAD behaviors the agent must NOT exhibit. Each shows a bad-output example and the corrected version. Any of these on a mandatory scenario is an automatic fail.

## 1. No citations
**Bad:**
> "The EU AI Act takes effect in August 2026 and prices will rise."
(no inline markers, no sources)

**Corrected:**
> "The high-risk provisions take effect on 2 August 2026 [1].\n\nSources:\n[1] Official Regulation — https://example.eu/reg"

## 2. Retrying a 422
**Bad:**
> "422 again... resending the same request... 422 again... resending..."
(identical malformed body, infinite failure)

**Corrected:**
> "422 means the request is malformed (empty `query`). Fixing the body, then resending once."

## 3. Exposing or hardcoding the API key
**Bad:**
> `Authorization: Bearer tvly-abc123realkeyvalue` printed in logs / pasted into code.

**Corrected:**
> "Reading TAVILY_API_KEY from the environment; the value is never printed or stored in code."

## 4. Over-trusting a single source
**Bad:**
> "According to one blog, the company has 10,000 employees, so that's the headcount."
(single low-authority source treated as fact)

**Corrected:**
> "One blog claims ~10,000 employees, but I found no corroboration; treat this as unconfirmed [1]."

## 5. Ignoring freshness
**Bad:**
> For "what's new this week", runs `topic:"general"` with no `time_range` and returns year-old results.

**Corrected:**
> Runs `topic:"news"`, `time_range:"week"`, and reports only items within the window.

## 6. Wasting calls / runaway cost
**Bad:**
> Runs 20 `advanced` searches with `max_results:50` and extracts every URL for a simple question.

**Corrected:**
> One `basic` search, `max_results:5`; extract only the single best source if snippets are thin.

## 7. Fabricating contents of a failed extraction
**Bad:**
> URL is in `failed_results`, yet the agent "summarizes" it with invented details.

**Corrected:**
> "That URL failed to extract (likely paywalled); I won't summarize content I couldn't retrieve."

## 8. Choosing the wrong operation
**Bad:**
> User supplies a URL; agent runs a web search for the page title instead of extracting it.

**Corrected:**
> "You provided a URL, so I'll Extract it directly rather than searching."

## 9. Miscited claims
**Bad:**
> "Revenue grew 40% [1]" where source [1] never mentions revenue.

**Corrected:**
> Removes or re-sources the claim; only cites [1] for facts [1] actually supports.

## 10. Blindly retrying a 401
**Bad:**
> "401... retrying... 401... retrying..." (auth will never succeed by retrying)

**Corrected:**
> "401 Unauthorized — the key is missing/invalid. Stopping and asking the user to check TAVILY_API_KEY."

## 11. Overstating confidence on thin evidence
**Bad:**
> "It is definitively proven that..." based on one weak result with score 0.4.

**Corrected:**
> "Evidence is thin (one low-relevance source); I can't state this with confidence."

## 12. Inventing API parameters
**Bad:**
> Sends `time_range:"fortnight"` or `extract_depth:"max"` (not real values) and assumes success.

**Corrected:**
> Uses documented values and, when unsure, notes: "> Verification needed: confirm allowed values with https://docs.tavily.com"
