# Scrape Tool — Detailed Guide

## Tool: `scrape`

Scrapes a URL and returns its content. Handles proxy rotation, CAPTCHAs, and anti-bot measures automatically.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | — | **Required.** Target URL |
| `render` | boolean | false | Enable JS rendering via headless browser |
| `countryCode` | string | — | Two-letter country code for geo-targeting |
| `premium` | boolean | false | Use premium residential proxies |
| `ultraPremium` | boolean | false | Advanced bypass mechanisms (incompatible with `premium`) |
| `deviceType` | enum | — | `"mobile"` or `"desktop"` |
| `outputFormat` | enum | `"markdown"` | `"text"`, `"markdown"`, `"html"`, `"csv"`, or `"json"` |
| `autoparse` | boolean | false | Auto-parse JSON on supported sites; set `true` for csv/json output |

## When to Use Each Parameter

### `render: true`
- Page is a JavaScript SPA (React, Vue, Angular, Next.js client-rendered)
- Initial scrape returns empty or skeleton HTML
- Content loads dynamically via API calls rendered in-browser
- **Cost**: Significantly more expensive than standard scrape

### `premium: true`
- Standard request returns 403/429
- Site has known anti-bot protection (Cloudflare, Akamai, PerimeterX)
- **Cost**: Significantly more expensive than standard; even more with render

### `ultraPremium: true`
- Premium still gets blocked
- Hardest-to-scrape sites
- **Cost**: Most expensive option; combining with render multiplies cost further
- **Restriction**: Cannot use with custom headers

### `countryCode`
- Content varies by region (pricing, availability, regulations)
- Site serves different content per locale
- **Cost**: More expensive than standard

### `deviceType`
- Site serves different layouts for mobile vs desktop
- Need mobile-specific content or responsive version

### `outputFormat`
- `"markdown"` (default) — best for reading content, preserves structure
- `"text"` — plain text, no formatting
- `"html"` — raw HTML when you need to parse DOM structure
- `"csv"` / `"json"` — use with `autoparse: true` on supported sites

### `autoparse: true`
- Scraping a supported site (Amazon, Google, etc.) where ScraperAPI can auto-extract structured data
- Must be `true` when using `csv` or `json` output format

## Escalation Strategy

Always start minimal and escalate only as needed:

1. Call `scrape` with just `url` (cheapest).
2. If response is empty or minimal content: add `render: true` (significantly more expensive).
3. If the page shows a consent/interstitial:
   - Retry with `deviceType: "desktop"`
   - Then try `deviceType: "mobile"` if needed
4. If geo issues / repeated errors: retry with `countryCode` matching the target market (e.g., `us`, `gb`).
5. If 403/429 or blocking persists: add `premium: true` (more expensive still).
6. If still blocked: switch to `ultraPremium: true` (most expensive).
   - **NEVER** combine `premium` and `ultraPremium`.

## Error Patterns

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| Empty response | JS-rendered content | Add `render: true` |
| HTTP 403 | Anti-bot protection | Add `premium: true` or `ultraPremium: true` |
| HTTP 429 | Rate limiting | Add `premium: true`; ScraperAPI retries internally |
| Timeout | Slow target site | ScraperAPI handles retries; if persistent, site may be down |
| Partial content | Page too large (>50MB) | Scrape specific subpages instead of root |

## Tips

- Scrape specific documentation pages rather than root URLs — you get focused content and save credits.
- For large sites, combine with `google_search` to find the exact page first, then `scrape` it.
- The `markdown` output format preserves headings, links, and lists — ideal for reading documentation.
