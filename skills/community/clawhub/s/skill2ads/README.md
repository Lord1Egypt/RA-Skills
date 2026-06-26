# website-to-ads

**OpenClaw Skill** — Scrape any business website and generate 5 Meta-ready ad variants that match the brand's voice.

## What It Does

1. **Scrapes** the website using [Apify's Website Content Crawler](https://apify.com/apify/website-content-crawler) (homepage + about + products, up to 3 pages)
2. **Analyzes** the brand — extracts voice, tone, audience, products, USPs, geographic focus
3. **Generates** 5 ad variants with Meta-compatible targeting and scheduling, written in the brand's authentic voice
4. **Gates export** to Meta behind optional Civic identity verification

Every business has a website. This skill turns it into a creative brief.

## Quick Start

```bash
# Install
openclaw skills install website-to-ads

# Configure
export APIFY_TOKEN=your_token
export OPENAI_API_KEY=your_key
export CIVIC_AUTH_ENABLED=true          # optional
export CIVIC_CLIENT_ID=your_client_id   # preferred when CIVIC auth is enabled
export CIVIC_ACCESS_TOKEN=your_civic_access_token  # optional for CLI demos (skips prompt)
# export CIVIC_GATEWAY_KEY=your_key      # optional fallback
```

Then ask your agent:

> "Generate ads for https://sarahsbakery.com"

If you need help retrieving `CIVIC_ACCESS_TOKEN` in a Next.js app, use the example in `examples/civic-nextjs-token-route.ts`.
Never commit real credentials or access tokens to source control.

## Manual Testing

```bash
cd website-to-ads
npm install
cp .env.example .env   # fill in your keys
npx tsx src/index.ts https://example.com
```

## Tools Provided

| Tool | Description |
|------|-------------|
| `scrape_website` | Scrape a URL → cleaned text content |
| `generate_ads` | Brand analysis + ad generation from text |
| `website_to_ads` | End-to-end: URL → brand profile → numbered ads + optional Civic-gated Meta export |

## Output Format

Each ad includes:

- **intent** — strategic angle (awareness, conversion, retargeting, etc.)
- **hook** — scroll-stopping headline
- **body** — ad copy matching the brand's voice
- **cta** — call to action
- **visual_direction** — creative guidance
- **why_it_works** — strategic rationale
- **targeting** — Meta-compatible: geo, age, gender, platforms
- **adset_schedule** — daypart schedule optimized for Stories/Reels

## Tech Stack

- [Apify](https://apify.com) — website scraping (sponsor)
- [Civic](https://www.civic.com) — optional identity verification before Meta export
- [OpenAI](https://openai.com) — brand analysis + ad copywriting
- [OpenClaw](https://openclaw.ai) — agent skill framework

## License

MIT
