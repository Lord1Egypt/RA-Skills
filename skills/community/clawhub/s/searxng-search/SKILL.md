---
name: searxng-search
description: Route web searches through local SearXNG, choose suitable engines for general, biomedical, technical, and current-news research, and periodically recheck engine health.
---

# SearXNG Search

## Search

1. Use the configured SearXNG-backed `web_search` for web research when available; verify that it returns results and identify its provider when the tool exposes that information. Do not assume SearXNG is active merely because it was configured previously.
2. Route by intent: use broad general-web search for discovery, primary publishers or databases for evidence, and domain-specific engines for technical or specialty questions. For Insub's biomedical work, prioritize primary literature and bibliographic sources (for example Europe PMC, PubMed, Crossref, OpenAlex, or arXiv when relevant); use more than one independent source for consequential claims. For software documentation, prioritize the project's official documentation and focused IT/Q&A engines. For recent events, use news engines and check publication dates. Treat these as source choices, not endorsements of every result.
3. Use SearXNG engine shortcuts only after confirming the current inventory at `/config`; shortcuts and enabled status can change. To target an engine, use SearXNG's `!shortcut` syntax only when appropriate, and inspect which engines actually contributed results. A result from the aggregate response does not prove the intended engine returned it.
4. Inspect result title, publisher/domain, URL, date, and relevance before citing. Prefer primary sources, distinguish search snippets from source contents, open/read the source when possible, and corroborate important or biomedical claims. Search-engine availability is not a measure of source quality.
5. If SearXNG is unavailable, empty, or dominated by upstream errors, distinguish local-service failure from individual-engine failure. Retry once with a narrower query or an alternate suitable engine; then use another available search route if needed and disclose the fallback. Do not repeatedly hammer CAPTCHA/rate-limited sources.

## Engine health checks

1. Refresh the inventory from the live local instance (`/config`) before a health audit. Check representative engines when search failures recur, before relying on an old snapshot for important research, and otherwise about quarterly; do not probe all engines on every search.
2. Select a small, relevant set from the live inventory: general web, news, technical documentation/Q&A, and scientific-publication engines. Include biomedical sources when relevant. Include only engines actually configured, and note enabled state; do not change configuration as part of a health check.
3. Test each selected engine individually using a neutral, category-appropriate query and SearXNG's JSON search endpoint (`/search?q=!<shortcut>%20<query>&format=json`). Use low concurrency (at most 4) and a reasonable timeout. Match results by the engine attribution fields (`engine` or `engines`), record `unresponsive_engines`, response time, and a small title/domain sample. Use a query appropriate to the engine: a general programming query does not establish that a science, weather, translation, or specialty source works.
4. Classify outcomes as results, upstream error/suspension, or empty/inconclusive. Empty responses are not proof of failure; distinguish CAPTCHA, rate limits, access denial, timeout, TLS, and parser errors. Validate answers/infoboxes against the requested task rather than treating any answer as success.
5. Save dated audit output locally under `reports/` or the active project, without credentials or sensitive query content. Compare with the previous audit, but describe the check as a small availability spot-check, not a quality benchmark. Avoid heavy full-inventory probing unless explicitly needed; do not disable/enable engines based only on one probe.
6. Use `references/engine-baseline-2026-10-08.md` only as historical context. Recheck current state before recommending engines, since the attached one-query snapshot is not a current guarantee.

## Current user-fit baseline

1. For an ordinary broad search, start with currently working general-web engines and diversify if coverage is weak; the historical snapshot found Google CSE and DuckDuckGo Web returning results, while direct Google and DuckDuckGo were blocked/CAPTCHA and Brave was rate-limited.
2. For biomedical/scientific discovery, begin with currently working literature databases and publication indexes. In the historical snapshot Europe PMC and arXiv returned results, while PubMed was rate-limited, Semantic Scholar had a parsing error, and OpenAIRE endpoints timed out. Verify current status and prefer the authoritative database directly for final evidence.
3. For technical documentation, use official documentation search or currently responsive focused sources; the historical snapshot showed Stack Overflow, Ask Ubuntu, Super User, MDN, and Microsoft Learn returning results. Verify that a candidate actually fits the specific technology.
4. Treat these recommendations as an initial shortlist, not fixed preferences: choose based on the request, live health, source authority, and result relevance.
