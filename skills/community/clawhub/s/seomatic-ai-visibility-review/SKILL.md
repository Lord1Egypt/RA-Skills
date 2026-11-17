---
name: seomatic-ai-visibility-review
description: Review how the connected brand shows up inside AI answers (ChatGPT, Claude, Perplexity, Gemini, Grok, AI Overviews) using SEOmatic's stored scans, tune the tracked prompts, and only then consider a fresh scan. Use for "are we visible in AI search", GEO reviews, or managing tracked prompts.
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
  - ai_citations
  - visibility_manage
  - run_ai_visibility_scan
---

# AI-visibility review

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

1. **Read the stored scan**: `ai_citations` action `scan_results` (FREE - stored scan): per-engine visibility, the
   prompts where the brand was MISSED and who won instead, competitors,
   and the sources engines cite.
2. **Check the tracked prompts**: `visibility_manage` list: the tracked prompts, the plan allowance, and
   cadence. Check the prompts still match the business (stale prompts =
   wasted scan spend).
3. **Tune the prompts**: add missing money questions with `visibility_manage` add (the
   buyer's words, not keywords - "best invoicing software for freelancers").
   Remove or deactivate stale ones (deactivate keeps history). Plan-capped:
   relay the upgrade path on a limit refusal.
4. **Set the cadence**: weekly is the default. Set daily ONLY if the user explicitly
   asks AND you have told them it multiplies scan spend ~7x; it is also
   plan-gated.
5. **Run a fresh scan only on request**: `run_ai_visibility_scan` bills AI credits (one
   assistant-triggered scan per hour). Run it ONLY when the user asks for
   fresh numbers after you have named the cost; it returns a scanId and
   results land in a few minutes, then re-read with `ai_citations` action
   `scan_results`.
6. **Report**: visibility by engine, the top missed prompts with who won them,
   and 2-3 content/citation moves. Cited-source gaps are link-target
   ideas, not guaranteed placements - say "worth pitching", never promise.
