# Troubleshooting & Diagnostics Runbook

Use this document to diagnose and resolve integration issues when deploying Tavily.

---

## 1. Common Error Code Resolution

### 401 Unauthorized
- **Cause:** Invalid, missing, or revoked API key.
- **Resolution:** Check your `TAVILY_API_KEY` environment variable. Ensure the key is active in your Tavily Dashboard.

### 403 Forbidden
- **Cause:** Accessing an endpoint or feature not allowed by your plan (e.g., trying to use Crawl on a Free plan).
- **Resolution:** Upgrade your subscription tier or contact enterprise support.

### 429 Too Many Requests
- **Cause:** Exceeded requests per minute (RPM) limits (100 RPM for Dev, 1,000 RPM for Prod).
- **Resolution:** Implement exponential backoff. Parse and respect the `retry-after` header returned in the response.

---

## 2. Diagnostic Runbook

### High Latency on Advanced Search
- **Cause:** Heavy multi-query expansion and scraping of up to 20 sites.
- **Resolution:**
  - Downgrade to `search_depth="basic"` or use `search_depth="fast"` if sub-second latency is required.
  - Disable raw content scraping by setting `include_raw_content=false`.
  - Reduce `max_results` (e.g., to 3 or 5).

### Empty Search Results
- **Cause:** Restrictive search parameters (e.g., using `exact_match=true` on a phrase that doesn't exist verbatim, or combining narrow `include_domains` with a restrictive `time_range`).
- **Resolution:**
  - Set `exact_match=false` and remove domain restrictions as a fallback strategy.
  - Enable `auto_parameters=true` to let Tavily dynamically optimize query parameters.

### Downstream LLM Context Overflow
- **Cause:** Injecting massive amounts of raw Markdown from `include_raw_content=true` directly into the prompt.
- **Resolution:**
  - Use the Extract API with a `query` to trigger **Intent-Based Extraction**.
  - Restrict `chunks_per_source` to 2 or 3 to return short, high-density snippets instead of full-page text.
