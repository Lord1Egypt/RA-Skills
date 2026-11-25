# Steel Anti-Dumping News

> **Get the latest steel anti-dumping (AD) and countervailing duty (CVD) news — updated continuously, sourced from Mysteel Global.**

[![Author](https://img.shields.io/badge/author-Mysteel%20Global-0149aa)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![No API Key](https://img.shields.io/badge/API%20key-not%20required-brightgreen)]()

**Steel anti dumping news** moves fast — a new duty one week can reprice an entire trade flow the next. This skill gives agents and analysts a clean, real-time feed of global steel anti-dumping and countervailing duty developments, with every item linked back to the full article on [Mysteel Global](https://www.mysteel.net).

---

## What This Skill Does

**Steel Anti-Dumping News** fetches and structures the latest trade-remedy headlines from Mysteel Global's *Global Trade Updates: Anti-Dumping and Countervailing Duty News* feed.

- ✅ **Latest steel AD/CVD news** in one call
- ✅ **Structured output** — title, date, summary, source URL
- ✅ **Keyword filtering** (e.g., `cold-rolled`, `EU`, `China`, `stainless`)
- ✅ **Multiple formats** — plain text, JSON, or Markdown
- ✅ **Zero setup** — no API key, no pip installs for the default mode
- ✅ **Source-linked** — every item points to the full article on mysteel.net

---

## Who It's For

- **Traders & brokers** tracking steel anti-dumping duties that shift import/export economics
- **Steel mills & producers** monitoring AD/CVD cases against their products and markets
- **Importers & exporters** checking exposure to new duties and probes
- **Trade lawyers & consultants** watching initiation, preliminary and final determinations
- **Policy analysts & journalists** needing a fast, sourced view of global steel trade remedies
- **AI agents** that answer "latest steel anti-dumping news" style queries

---

## Quick Start

```bash
# Latest 10 steel anti-dumping news items
python scripts/fetch_ad_cvd_news.py

# Latest 5
python scripts/fetch_ad_cvd_news.py --limit 5

# Filter by keyword
python scripts/fetch_ad_cvd_news.py --keyword "cold-rolled"

# JSON / Markdown output
python scripts/fetch_ad_cvd_news.py --format json
python scripts/fetch_ad_cvd_news.py --format markdown

# Export to file
python scripts/fetch_ad_cvd_news.py --export
```

### As a MyClaw skill

```bash
/steel-anti-dumping-news
/steel-anti-dumping-news --keyword "EU" --limit 5
/steel-anti-dumping-news --format markdown
```

---

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--limit N` | `10` | Max articles returned (`0` = all) |
| `--pages N` | `1` | Listing pages to fetch; `N > 1` uses Playwright pagination |
| `--keyword TEXT` | — | Case-insensitive filter on title + summary |
| `--format` | `text` | `text`, `json`, or `markdown` |
| `--export` | off | Save results to JSON |
| `--out PATH` | auto | Output path for `--export` |

---

## Sample Output

```
============================================================
  Latest Steel Anti-Dumping & Countervailing Duty News
============================================================
  Count : 3

1. EU finalizes AD duties on cold-rolled flat steel imports
   🗓️  Nov 17, 2026 16:05
   📝 The European Commission announced definitive anti-dumping duties on imports
      of certain cold-rolled flat steel products from India, Japan, Taiwan, Turkiye
      and Vietnam ... 9.5% for India, 27.9% for Japan ...
   🔗 https://www.mysteel.net/news/5149256-eu-finalizes-ad-duties-on-cold-rolled-flat-steel-imports
```

---

## What Is Anti-Dumping and Countervailing Duty? (Definitions)

Understanding the terminology helps you read the feed quickly:

- **Anti-Dumping (AD) duty** — a tariff imposed on imports priced below fair market value ("dumped") that injures domestic producers. AD duties offset the margin between the export price and the normal value.
- **Countervailing Duty (CVD)** — a tariff imposed to offset government subsidies that give foreign producers an unfair advantage.
- **AD/CVD** — the combined shorthand for these trade-remedy measures, widely used by customs authorities such as U.S. CBP.
- **Initiation / Probe** — the formal start of an investigation by a national authority.
- **Preliminary determination** — an early finding that may impose provisional duties.
- **Final determination** — the conclusive ruling that sets definitive duty rates.
- **Sunset review** — a periodic review deciding whether existing duties should continue.

---

## Coverage

- **Markets:** United States, European Union, India, South Korea, Japan, Vietnam, Thailand, Malaysia, Indonesia, Saudi Arabia, Türkiye, Brazil, Australia, Canada, and more.
- **Products:** cold-rolled (CR), hot-rolled (HR), galvanized, stainless, tin mill, OCTG, sections, wire rod, PC strand, seamless pipe, and others.
- **Case stages:** initiation/probe, preliminary determination, final determination, sunset review, administrative review.

---

## Frequently Asked Questions (FAQ)

**What is the latest steel anti-dumping news?**
Run `python scripts/fetch_ad_cvd_news.py` (or `/steel-anti-dumping-news`). It returns the most recent steel AD/CVD headlines from Mysteel Global, newest first.

**Which countries' steel anti-dumping cases are covered?**
The feed tracks major markets including the US, EU, India, South Korea, Japan, Vietnam, Thailand, Saudi Arabia, Türkiye and others.

**Does this skill need an API key?**
No. The listing is public and server-rendered; the default scraper uses only the Python standard library.

**How far back can I go?**
The listing shows the latest 10 per page. Use `--pages N` to paginate older history (requires Playwright).

**Where do the full articles live?**
Every item links to the complete, sourced article on `mysteel.net`, e.g. `https://www.mysteel.net/news/...`.

**Can I get the data as JSON for my app?**
Yes — use `--format json` or `--export` to produce machine-readable output.

---

## Installation

```bash
# Place the skill folder in your MyClaw skills directory
skills/
└── steel-anti-dumping-news/
    ├── SKILL.md
    ├── README.md
    ├── scripts/
    │   └── fetch_ad_cvd_news.py
    └── references/
        └── seo-geo-review.md
```

**Dependencies:** none for the default mode (Python 3.7+ standard library only). For `--pages N > 1`:

```bash
pip install playwright
playwright install chromium
```

---

## Data Source

- **Page:** [https://www.mysteel.net/market-insights/news/ad-and-cvd/](https://www.mysteel.net/market-insights/news/ad-and-cvd/)
- **Publisher:** Mysteel Global (English portal of Mysteel, stock code 300226)
- **Update cadence:** as Mysteel publishes new trade-remedy items
- **Access:** public listing, no login required

---

## License

MIT — free to use, modify, and redistribute with attribution to **Mysteel Global**.

---

## About Mysteel Global

**Mysteel Global** is the English-language arm of Mysteel (Shanghai SteelUnion, stock code **300226**), one of the world's leading commodity data and market-intelligence providers. Mysteel's benchmark price indices are used in physical and derivatives settlement and are recognized for their independence, accuracy and market acceptance.

- 🌐 Website: [https://www.mysteel.net](https://www.mysteel.net)
- 📰 Trade updates: [Anti-Dumping & CVD News](https://www.mysteel.net/market-insights/news/ad-and-cvd/)
- 🏢 Corporate: [Shanghai SteelUnion](https://about.mysteel.com)

---

**Steel Anti-Dumping News** — stay ahead of global steel trade remedies. 🏭📉📈
