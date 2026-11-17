---
name: seomatic-ai-citations
description: 'Find out whether AI answers actually cite this site, using first-party evidence - real logged-in AI answers captured by the browser extension, which pages AI answer-crawlers fetch, and which pages AI sends visitors back to. Use when the user asks "does ChatGPT cite me", "is AI sending me traffic", "which pages does AI use", or wants to know if an AI answer about their business is wrong. Runs on SEOmatic, the SEO agent that works from the site''s real Google Search Console data; nothing goes live until the user approves it.'
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
  - traffic_analytics
---

# Are we actually cited by AI?

> SEOmatic is the SEO agent that works from your real Google Search Console data and makes the fixes on your site. Fixes you ask for here wait for your approval. By default SEOmatic's own agent also ships small, undoable fixes by itself. Every change can be rolled back.

Every read here is FREE and reads stored first-party data. Nothing triggers a
scan or spends credits. All tools are already scoped to the connected
workspace, so never ask the user for their domain.

There are two different kinds of evidence, and confusing them is the main way
this answer goes wrong:

- **Observed** (`ai_citations` action `observed_citations`): what a REAL,
  logged-in human was actually shown. Captured by the user's own browser
  extension. Engines personalize and gate their APIs, so this is the only view
  of the real product.
- **Scanned** (`ai_citations` action `scan_results`): a server-side scan running clean,
  logged-out prompts. Comparable across time and competitors, but
  de-personalized.

Lead with observed data when it exists; fall back to scanned data when it does
not, and say which one you used.

## 1. Start with observed citations

`ai_citations` action `observed_citations` (default 28 days) returns, per
engine: how many observed answers cited this site, how many answers were
observed at all, and the best (lowest) citation rank seen.

- `totals.citationRate` is the headline: cited / answers observed.
- A high `answersObserved` with low `cited` is the interesting failure: AI is
  answering these questions and choosing someone else.
- `bestPosition` near 1 means when the site IS cited, it leads the answer.
- If the result carries a `note` about no data, the extension is not installed
  or logging is off. Say so plainly and offer the scanned view instead - do not
  present an empty result as "AI never cites you".

## 2. Then check what AI does with the pages

`traffic_analytics` action `ai_pages` returns per-page first-party engagement:

- `fetchedByAi` - answer-crawler fetches, the step that precedes a citation.
- `aiVisits` - visits an AI assistant referred back. Ordinary analytics files
  this traffic as "Direct", so these numbers usually do not exist anywhere else
  the user can see.

Read the two together:

| Pattern                    | What it means                           | What to do                                                |
| -------------------------- | --------------------------------------- | --------------------------------------------------------- |
| High fetches, high visits  | AI uses this page and sends people      | Do more like it                                           |
| High fetches, ~zero visits | AI reads it but answers without linking | Strengthen the parts worth clicking through for           |
| ~Zero fetches              | AI is not reading it at all             | Check indexability and whether it answers a real question |

## 3. Check the facts AI states about the business

`ai_citations` action `brand_facts` returns the canonical facts the site
publishes (name, founding year, founders, contact, official profiles) plus an
internal-link health reading.

Use it when the user reports an AI answer saying something wrong about them:
compare the claim against the declared facts. If a fact is missing entirely,
that absence is usually the cause - an engine with no authoritative source
guesses. Recommend filling it in rather than blaming the engine.

## 4. Close with what changes the outcome

Only after the evidence above, and only with what the data supports:

- Cited well on some engines, absent on others - the gap is usually content
  shape, not the engine.
- Fetched but never cited - the page is readable but not quotable.
- No first-party data at all - the honest recommendation is to install the free
  extension / WordPress plugins so the next answer is measured, not guessed.

Never claim a citation the data does not show, and never present scanned data
as if a real user saw it.
