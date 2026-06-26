# Reference: Common errors

Each failure mode, its shape/cause, and the agent's correct reaction. `SKILL.md` section 14 is authoritative; this elaborates.

Core principle: **distinguish "fix-don't-retry" (your request is wrong: 401, 422) from "retry-with-backoff" (transient: 429, 5xx, timeout). Never retry in an infinite loop. Never print the API key in any error path.**

> Verification needed: confirm exact status codes and error body shapes with https://docs.tavily.com

---

## 401 Unauthorized — invalid or missing key

- **Shape:** HTTP 401 with an authentication error message.
- **Cause:** `TAVILY_API_KEY` is missing, malformed, revoked, or wrong.
- **Reaction:** **Do not retry.** Stop and report that `TAVILY_API_KEY` is missing/invalid and must be set in the host environment. **Never echo the key.** This is a configuration problem, not a transient one.

## 422 Unprocessable Entity — validation error

- **Shape:** HTTP 422 with a body indicating which field/value is invalid.
- **Cause:** A bad parameter — e.g. `max_results` out of the 0-20 range, invalid `search_depth`/`topic`/`time_range` value, missing `query`, malformed `urls`.
- **Reaction:** **Fix the request, then retry.** Read the error body, correct the offending field, and resend the corrected payload. Do **not** resend the same invalid payload.

## 429 Too Many Requests — rate limit or out of credits

- **Shape:** HTTP 429, possibly with rate-limit headers or an "out of credits" message.
- **Cause:** Too many requests too quickly, or the account has exhausted its credits.
- **Reaction:**
  - If **rate limited:** retry with **exponential backoff + jitter** (e.g. ~1s, 2s, 4s) for a small, capped number of attempts. Reduce load (switch to `basic`, lower `max_results`).
  - If **out of credits:** **stop retrying** and report it; optionally check `/usage`. Backoff will not help.

## 5xx — server error

- **Shape:** HTTP 500/502/503/504.
- **Cause:** Transient server-side problem.
- **Reaction:** Retry with **exponential backoff**, a few attempts max. If it persists, report the failure and proceed with whatever results you already have. Include `request_id` if available.

## Timeout / network error

- **Shape:** No response within the client timeout, or a connection error.
- **Cause:** Network or latency issue.
- **Reaction:** Retry with **exponential backoff**, capped attempts. On continued failure, report and degrade gracefully (answer from what you have, or say you could not retrieve).

## Empty results (not an error)

- **Shape:** HTTP 200 with `results: []` (and possibly no `answer`).
- **Cause:** Query too narrow/misspelled, over-filtered domains, or too tight a `time_range`.
- **Reaction:** **Refine the query** (SKILL.md section 13): rephrase/keywords, widen `time_range`, switch `topic`, relax domain filters, or raise `search_depth`. Try ~2-3 refinements. If still empty, tell the user nothing was found — **do not fabricate** an answer.

## `failed_results` (extract / crawl)

- **Shape:** A `failed_results` array listing URLs that could not be fetched, alongside successful `results`.
- **Cause:** Page blocked, paywalled, removed, or unparseable.
- **Reaction:** Retry those specific URLs once (e.g. `extract_depth: "advanced"`); if still failing, skip and report them. Continue with the URLs that succeeded.

---

## Reaction summary

| Condition | Retry? | How |
|---|---|---|
| 401 | No | Report missing/invalid key; stop. Never print key. |
| 422 | Yes, after fixing | Correct the bad field, resend once. |
| 429 rate limit | Yes | Exponential backoff + jitter, capped; reduce load. |
| 429 out of credits | No | Report; stop. |
| 5xx | Yes | Exponential backoff, capped; then degrade. |
| Timeout / network | Yes | Exponential backoff, capped; then degrade. |
| Empty results | N/A | Refine query 2-3x; else report none found. |
| `failed_results` | Per-URL once | Retry advanced, else skip + report. |
