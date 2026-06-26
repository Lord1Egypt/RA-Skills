---
name: urlmitra-link-manager
description: Manage branded redirects, audit traffic analytics, and execute semantic link queries using URLMitra.
metadata:
  openclaw:
    requires:
      env:
        - URLMITRA_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: URLMITRA_API_KEY
---

# URLMitra Link Manager Skill

This skill extends your OpenClaw agent, enabling it to manage branded redirects, audit links for broken destinations, analyze click attribution metrics, and semantically search workspace resources using standard URLMitra endpoints.

## Objectives
1. **Shorten & Brand Links:** Turn long, ugly URLs into memorable shortlinks under the standard redirect domain (e.g., `mitr.to/roadmap` or `mitr.to/product-tour`).
2. **Audit Redirect Health:** Autonomously monitor links for broken redirects or `404` errors to protect traffic.
3. **Analyze click performance:** Pull workspace click and conversion stats to report ROI metrics.
4. **Semantic Resource Search:** Query the workspace's internal embeddings database conceptually using natural language.

## Required Environment Variables
- `URLMITRA_API_KEY`: Your workspace API credential. Secure this key via your developer settings dashboard in URLMitra.

## Execution Rules & Tooling
Always use standard `curl` calls and `jq` parsing to communicate with URLMitra's APIs.

### 1. Create a Branded Shortlink
To create a branded link, send a POST request with destination URL and alias parameters.
*   **Command:**
    ```bash
    curl -s -X POST \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $URLMITRA_API_KEY" \
      -d '{"url": "{url}", "alias": "{slug}"}' \
      https://api.urlmitra.com/api/v1/links
    ```

### 2. Live Redirect Health Diagnostics
Validate target destinations in real-time. If an alias is provided, check its target. If no alias is provided, sweep all active workspace redirects.
*   **Command (Whole Workspace Sweep):**
    ```bash
    curl -s -H "X-API-Key: $URLMITRA_API_KEY" \
      https://api.urlmitra.com/api/v1/health/summary
    ```
*   **Command (Specific Link Verification):**
    1. Resolve the alias to its core document context first:
       ```bash
       curl -s -H "X-API-Key: $URLMITRA_API_KEY" \
         https://api.urlmitra.com/api/v1/links/{alias}
       ```
    2. Extract the `"id"` property from the resulting JSON, and POST to trigger the manual checker:
       ```bash
       curl -s -X POST \
         -H "X-API-Key: $URLMITRA_API_KEY" \
         https://api.urlmitra.com/api/v1/health/check/{linkId}
       ```

### 3. Semantic Resource Retrieval
Use backend Gemini vectors to search the workspace conceptually.
*   **Command:**
    ```bash
    curl -s -X POST \
      -H "Content-Type: application/json" \
      -H "X-API-Key: $URLMITRA_API_KEY" \
      -d '{"query": "{searchTerm}"}' \
      https://api.urlmitra.com/api/v1/mitra/search
    ```

## Trigger Intents
- "Shorten this URL using URLMitra"
- "Trigger a redirect health check on our links"
- "Audit our marketing campaigns for broken targets"
- "Find the onboarding documentation semantically in our workspace"
- "Report this week's click conversions and ROI"
