---
name: steel-anti-dumping-news
description: "Steel anti dumping news — get the latest steel anti-dumping (AD) and countervailing duty (CVD) news from Mysteel Global's Global Trade Updates. Covers AD/CVD duties, investigations, probes, sunset reviews and final determinations across the US, EU, India, South Korea, Vietnam, Thailand, Japan, MENA and more. Returns article titles, dates, summaries and source links. Keyword: steel anti dumping news."
user-invokable: true
argument-hint: "[--limit N] [--keyword TEXT] [--format text|json|markdown] [--export]"
license: MIT
metadata:
  author: Mysteel Global
  version: "1.0.0"
  category: trade-news
---

# Steel Anti-Dumping News

> **The fastest way to track steel anti-dumping (AD) and countervailing duty (CVD) news worldwide.**
> Powered by [Mysteel Global](https://www.mysteel.net) — the English-language portal of Mysteel, the world's leading commodity market intelligence provider.

This skill pulls the latest **steel anti dumping news** from Mysteel Global's continuously updated *Global Trade Updates: Anti-Dumping and Countervailing Duty News* feed at:
`https://www.mysteel.net/market-insights/news/ad-and-cvd/`

It is designed for traders, steel mills, importers/exporters, trade lawyers, policy analysts and journalists who need a concise, real-time view of global steel trade remedies.

---

## When To Use This Skill

Use this skill whenever the user asks about:

- "latest steel anti-dumping news" / "steel AD news"
- "countervailing duty news for steel"
- new AD/CVD **investigations**, **probes**, **preliminary** or **final determinations**
- anti-dumping **duties on Chinese steel**, Indian steel, EU steel, US steel, etc.
- **sunset reviews** or **administrative reviews** of steel duties
- trade remedy developments by country (US DOC, EU Commission, India DGTR, Korea MOTIE, etc.)

---

## Quick Start

```bash
# Latest 10 steel anti-dumping news items (default)
python scripts/fetch_ad_cvd_news.py

# Latest 5 items
python scripts/fetch_ad_cvd_news.py --limit 5

# Only items mentioning "cold-rolled"
python scripts/fetch_ad_cvd_news.py --keyword "cold-rolled"

# Machine-readable JSON
python scripts/fetch_ad_cvd_news.py --format json

# Markdown (ideal for briefs / newsletters / AI answers)
python scripts/fetch_ad_cvd_news.py --format markdown

# Save to a JSON file
python scripts/fetch_ad_cvd_news.py --export
```

---

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--limit N` | `10` | Max number of articles to return (`0` = all) |
| `--pages N` | `1` | Listing pages to fetch. `N > 1` paginates via Playwright (optional) |
| `--keyword TEXT` | — | Keep only articles whose title/summary contains `TEXT` (case-insensitive) |
| `--format` | `text` | Output format: `text`, `json` or `markdown` |
| `--export` | off | Save results to a JSON file |
| `--out PATH` | auto | Output path when using `--export` |

---

## How It Works

1. Fetches the **server-side rendered** listing page from Mysteel Global.
2. Parses the article list (`<li class="d-flex align-center m-list-item">` blocks) to extract:
   - **title** (from the `title` attribute and `.m-title` element)
   - **summary** (from `.description`)
   - **date** (from `.date`)
   - **URL** (absolute link to the full article on mysteel.net)
3. Applies keyword filtering and limit.
4. Renders the result as text, JSON or Markdown.

**Default mode needs no third-party packages** — it uses only the Python standard library (`urllib`, `re`, `json`, `argparse`). Multi-page history (`--pages N > 1`) optionally uses Playwright to drive the on-page pagination.

> **Why HTML and not an API?** Mysteel's news listing is rendered on the server with real `<a href>` links and semantic `<p>` tags, so the latest articles are reliably available in the raw HTML. This keeps the skill dependency-free and fast.

---

## Output Example (text)

```
============================================================
  Latest Steel Anti-Dumping & Countervailing Duty News
============================================================
  Source : https://www.mysteel.net/market-insights/news/ad-and-cvd/
  Fetched: 2026-11-20 07:51 UTC
  Count  : 3
------------------------------------------------------------
1. EU finalizes AD duties on cold-rolled flat steel imports
   🗓️  Nov 17, 2026 16:05
   📝 The European Commission announced definitive anti-dumping duties on imports of
      certain cold-rolled flat steel products from India, Japan, Taiwan, Turkiye and
      Vietnam ... duties set at 9.5% for India, 27.9% for Japan ...
   🔗 https://www.mysteel.net/news/5149256-eu-finalizes-ad-duties-on-cold-rolled-flat-steel-imports
```

## Output Example (JSON)

```json
{
  "fetchedAt": "2026-11-20 07:51 UTC",
  "source": "https://www.mysteel.net/market-insights/news/ad-and-cvd/",
  "count": 1,
  "articles": [
    {
      "title": "EU finalizes AD duties on cold-rolled flat steel imports",
      "url": "https://www.mysteel.net/news/5149256-eu-finalizes-ad-duties-on-cold-rolled-flat-steel-imports",
      "summary": "The European Commission announced definitive anti-dumping duties ...",
      "date": "Nov 17, 2026 16:05"
    }
  ]
}
```

---

## Coverage

The feed tracks steel trade remedies across major markets and case types:

- **Markets:** United States, European Union, India, South Korea, Japan, Vietnam, Thailand, Malaysia, Indonesia, Saudi Arabia, Türkiye, Brazil, Australia, Canada and more.
- **Products:** cold-rolled (CR), hot-rolled (HR), galvanized/galv, stainless, tin mill, OCTG, sections, wire rod, PC strand, seamless pipe and others.
- **Case stages:** initiation/probe, preliminary determination, final determination, sunset review and administrative review.

Every item links back to the **original, fully sourced article on `mysteel.net`** for deeper reading.

---

## Notes & Limitations

- Returns the **latest batch** available in the listing (10 per page by default). Use `--pages N` for older history.
- Summaries are truncated in `text` mode (220 chars) — use `json` or `markdown` for the full text.
- No login or API key required to read the public listing.
- Please be considerate with request frequency; results change as Mysteel publishes new items.

---

## Related Mysteel Skills

- **Latest steel conferences** — webinars, conferences and site tours from Mysteel Global.
- For pricing and index data, see Mysteel Global's market insights at [mysteel.net](https://www.mysteel.net).

---

**Maintained by Mysteel Global.** Data © Mysteel. For commercial licensing or full-text access, visit [https://www.mysteel.net](https://www.mysteel.net).
