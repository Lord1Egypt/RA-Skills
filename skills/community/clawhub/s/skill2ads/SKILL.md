---
name: website-to-ads
description: Scrape any business website and generate 5 Meta-ready ad variants matching the brand's voice. Use when the user wants to create ads, generate ad copy, or turn a website URL into marketing creatives. Optionally requires Civic verification before exporting selected ads to Meta.
---

# Website to Ads

## Quick Start

Ask the agent:
> "Generate ads for https://example.com"

## Tools

- **scrape_website** — Scrape a URL into cleaned text
- **generate_ads** — Analyze brand + generate ad variants from text
- **website_to_ads** — End-to-end: URL → brand profile → numbered ads

## Requirements

Set these environment variables before use:

```bash
export APIFY_TOKEN=your_apify_token
export OPENAI_API_KEY=your_openai_key
export CIVIC_AUTH_ENABLED=false
export CIVIC_CLIENT_ID=your_civic_client_id
export CIVIC_ACCESS_TOKEN=your_civic_access_token
```

## Output

Each ad includes: hook, body, CTA, visual direction, Meta-compatible targeting, and daypart scheduling.

Meta export behavior:
- Anyone can generate and review ads.
- If `CIVIC_AUTH_ENABLED=true`, exporting selected ads to Meta requires a valid Civic token.
- For CLI demos, set `CIVIC_ACCESS_TOKEN` to skip token prompts.
- Never commit real API keys or Civic access tokens to the repository.
