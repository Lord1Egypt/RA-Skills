---
name: seomatic-seo-audit
description: Run a complete, zero-cost SEO audit of the connected site through the SEOmatic connector - real Search Console data, technical crawl, on-page issues, and AI-search visibility - ending with a prioritized fix list the agent can stage for approval. Use when the user asks for an SEO audit, "how is my site doing", or a health check.
version: 1.0.0
license: MIT
homepage: https://app.seomatic.ai
metadata:
  paperclip:
    requirements:
      env: []
      binaries: []
      mcp: [seomatic]
  openclaw:
    requires:
      mcp: [seomatic]
  hermes:
    requires_mcp_servers: [seomatic]
mcp:
  servers:
    seomatic:
      url: https://app.seomatic.ai/api/mcp
      transport: streamable-http
      auth: oauth
      setup: 'Add the SEOmatic MCP server (OAuth, or a Bearer smk_ API key from https://app.seomatic.ai/dashboard/settings?tab=ai-agents). Free tier covers every read in this skill.'
tools:
  - gsc_performance
  - gsc_insights
  - site_pages
  - ai_citations
  - task_manage
  - gsc_indexing
  - site_audit
  - run_ai_visibility_scan
---

# SEOmatic SEO audit

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

All reads below are FREE (each tool's description confirms). Never ask the
user for their domain - every tool is already scoped to the connected
workspace.

1. **Baseline**: `gsc_performance` (28d vs prior period) for clicks,
   impressions, CTR, position. Note the trend before judging anything.
2. **Diagnosis layer**: `gsc_insights` - cannibalization, CTR outliers
   (pages under-earning their position), seasonality verdicts, sitemap
   health. These are pre-computed diagnoses; do not recompute from raw.
3. **Index health**: `gsc_indexing` batch-inspect the top pages from step 1.
4. **Technical**: `site_audit` (site-wide crawl: duplicate/missing metas,
   thin content, noindex leaks, broken links). Partial crawls say so -
   report the coverage honestly.
5. **AI search**: `ai_citations` action `scan_results` for the stored scan (free). Only
   offer `run_ai_visibility_scan` (bills credits) if the user wants fresh.
6. **Synthesize**: a ranked list - quick wins first (CTR outliers with
   position <= 10), then structural issues. Quantify with the GSC numbers.
7. **Offer to act**: for each fixable item, name the specific fix and offer
   to stage it via `task_manage` create. Staging needs a paid plan (the
   `agents:act` scope); it costs no credits and never runs anything, and
   the user approves every change. On a free key the staging actions are
   locked and say which plan includes them - describe the fix and pass
   that on.

Honesty rules: report only what the tools returned; a missing data source
returns a connect link - give it to the user rather than improvising.
