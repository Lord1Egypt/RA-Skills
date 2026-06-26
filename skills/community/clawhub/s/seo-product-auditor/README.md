# 🔍 SEO Product Auditor — OpenClaw Skill

Scan your entire Shopify or WooCommerce store, score every product listing against
10 SEO criteria, and fix the worst offenders — all from a WhatsApp or Telegram message.

Companion to the Shopify Product Uploader skill. Run the audit to find what's broken,
then push the fixes without touching your browser.

## What it does

- **Full store audit** — scans all products, scores each one out of 100 across 10 criteria, identifies your top issues in seconds
- **Single product audit** — detailed breakdown of every criterion with specific suggestions
- **Auto-fix** — rewrites titles, descriptions, tags, SEO meta title, and meta description in UK English and pushes them directly to Shopify
- **Bulk fix** — fix your worst 10, 20, or all weak listings in one command
- **Targeted scans** — "find products with no SEO meta" · "find products with missing images" · "find products with US spellings"
- **Re-audit** — rescore updated products to confirm improvement
- **CSV export** — download all scores for reporting or client handoff

## Example usage

```
You:  audit my store
Bot:  📊 84 products scanned · avg score 58/100
      🔴 22 products scoring Poor · biggest issue: 61 missing meta descriptions
      Bottom 10: "Scarf" (12/100), "Blue pot" (18/100)...
      Reply "fix top 10" to start

You:  fix top 10
Bot:  ✏️ 10 products ready · avg score projected 58→74/100
      Apply all? YES / review each first

You:  yes
Bot:  ✅ 10 products updated · store avg now 74/100
```

## Scoring criteria

| Criterion | Max |
|-----------|-----|
| Title length (40–70 chars) | 15 |
| Keyword in title | 10 |
| Description length (150–300 words) | 15 |
| Keyword in description | 10 |
| Tags (5–10) | 10 |
| Images (3+) | 15 |
| SEO meta title | 10 |
| SEO meta description | 10 |
| Image alt text | 5 |
| UK English check | flag |

## Setup

Reuses credentials from the Shopify Product Uploader if already installed.
Otherwise: add `read_products`, `write_products`, `read_content`, `write_content` scopes
to your Shopify custom app. Full guide in `CONFIG.md`.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full skill — 6 workflows, scoring rubric, fix logic, UK English rules |
| `EXAMPLES.md` | 8 real examples covering audit, fix, bulk fix, targeted scan, export |
| `CONFIG.md` | Setup guide, API scopes, scoring explained, troubleshooting |

## Platforms

- Shopify (all plans) — full support including SEO metafields
- WooCommerce — full audit support · meta updates require Yoast SEO plugin

## Works best with

- **Shopify Product Uploader** — upload new products with good SEO from day one
- **Order & Returns Manager** — complete e-commerce operations suite

## Notes

- Nothing is pushed without your explicit confirmation
- All generated content is in UK English (colour, grey, aluminium, etc.)
- Audit results stored in memory — ask follow-up questions without re-scanning
- Large stores (500+ products) take 8–10 minutes to scan fully
