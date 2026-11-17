---
name: whydoesmysitesuck
description: Grade any website 0-100 across categories like SEO, security, performance, accessibility, content, email auth and AI/LLM readiness, using the free whydoesmysitesuck.com API. Use when the user asks "why is my site bad/slow", "audit this website", "check my site's SEO/security", "how good is example.com", "score this domain", "compare these two sites", or wants an objective quality baseline for a URL before or after making changes.
license: MIT
metadata:
  author: Marcin Dudek
  homepage: https://whydoesmysitesuck.com
  api_docs: https://whydoesmysitesuck.com/api
  openapi: https://whydoesmysitesuck.com/openapi.json
---

# whydoesmysitesuck.com — website quality scores

Returns a 0-100 score, a letter grade and a per-category breakdown for any domain,
from a 368-point audit. Free, read-only, one HTTP call.

Use it to answer "is this site any good, and where is it weak?" — and to get a
**before/after** number when you change someone's site.

## Get a key (once)

Free and self-service. Either send the user to https://whydoesmysitesuck.com/api,
or register directly — **ask the user for their email first, and use theirs, not
an invented one**; the key is emailed to that address.

```bash
curl -s -X POST https://whydoesmysitesuck.com/api/partner/register \
  -H "Content-Type: application/json" \
  -d '{"label": "My project", "email": "user@example.com"}'
# -> {"api_key": "wdmss_..."}
```

Store it as `WDMSS_API_KEY`. It is shown once in the response and emailed as a copy.

## Score a domain

```bash
curl -s -H "X-API-Key: $WDMSS_API_KEY" \
  https://whydoesmysitesuck.com/api/public/domain/example.com
```

Pass a **bare domain** — `example.com`, not `https://example.com/pricing`.

```json
{
  "domain": "example.com",
  "score": 72,
  "grade": "C",
  "scanned_at": "2026-07-28 09:24:11",
  "categories": [{"category": "Security", "score": 95}],
  "report_url": "https://whydoesmysitesuck.com/scan/AbC123"
}
```

## Handle these three responses

| Status | Meaning | What to do |
|---|---|---|
| `202` | Never scanned before — a scan just started | Wait ~30s, call the same URL again. Usually ready on the second try. |
| `429` | Out of free budget (3 new scans/min, 60 requests/min) | Honour `Retry-After` (60s). Don't hammer. |
| `422` | The last scan of this domain failed | The site is unreachable or blocking crawlers. Report that; don't retry in a loop. |

A `"stale": true` result is still valid — it's an older scan being refreshed in
the background. Use it, and poll again later if you need fresher data.

## Reading the result

- **score / grade** — the headline. A/B is healthy, C is mediocre, D/F needs work.
- **categories** — where to look. Sort ascending and the worst two or three are
  the real story; quoting every category back at the user is noise. Expect about
  11 entries: the full audit spans 22 categories, but only the ones the automated
  scan can score are returned. Don't treat a missing category as a zero.
- **report_url** — the human-readable report with the specific failing checks.
  **Always give the user this link.** The API returns scores, not the individual
  findings — the report is where they see what to actually fix.

Good: *"execlave.com scores 68 (D). Weakest: Legal & Privacy 31, Accessibility 44.
Full breakdown: <report_url>"*

Bad: dumping every category score as a table.

## Rules

- **Don't scrape** `/scan/<id>` pages to dodge the API. The API is free, faster
  and stable; the HTML is not a contract.
- **Only audit domains the user owns or has a reason to check.** It performs a
  real crawl of a live site.
- **Don't invent scores.** If the call fails, say so — a made-up number here is
  worse than no answer.
- Re-scans are capped at one per domain per 30 days by default; a fresh score
  right after a fix may still show the old value until the refresh completes.

## When something else fits better

- Need Core Web Vitals / Lighthouse field data → use a performance tool; this is
  a breadth audit, not a lab profiler.
- Need the *list of failing checks* programmatically → not exposed; use
  `report_url`, or the emailed full report from the site itself.
