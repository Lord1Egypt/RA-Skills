---
name: rankforge
description: SEO analysis and optimization via RankForge API — site audits, keyword research, competitor analysis, ranking reports. Use when user needs SEO analysis, keyword research, site audits, backlink checks, or search ranking optimization. Free tier available (100 req/day).
---

# RankForge

AI SEO analysis API by Voss Consulting Group.

## Setup

Set `RANKFORGE_API_KEY` or `RANKFORGE_EMAIL` for auto-signup (free, no credit card).

```bash
curl -X POST https://anton.vosscg.com/v1/keys -H 'Content-Type: application/json' -d '{"email":"you@example.com"}'
```

## Usage

```bash
curl -X POST https://anton.vosscg.com/v1/seo/analyze \
  -H "Authorization: Bearer $RANKFORGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "analysis_type": "full_audit"}'
```

## Capabilities
- `full_audit` — Complete site SEO audit
- `keyword_research` — Keyword discovery and difficulty scoring
- `competitor_analysis` — Compare against competitor domains
- `backlink_check` — Backlink profile analysis

## API Reference
- `POST /v1/seo/analyze` — Run SEO analysis (requires API key)
- `POST /v1/keys` — Get API key (email-only for free tier)
- `GET /v1/health` — Health check
- `GET /v1/openapi.json` — Full OpenAPI spec
