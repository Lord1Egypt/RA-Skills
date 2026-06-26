# Wine Info Search

> **READ-ONLY**: This skill only searches and displays information. It does NOT make purchases, process payments, or modify any accounts.

> Search for wine and alcohol information, ratings, prices, and value comparisons across 16+ major platforms worldwide.

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.6.1-orange.svg)](CHANGELOG)

## ✨ Features

- **Multi-source search** — Wine-Searcher, Vivino (via Firecrawl), Wikipedia API, Open Food Facts
- **110+ bilingual name mapping** — Chinese ↔ English auto-translation (e.g. "拉菲" → "Lafite")
- **Multi-segment replacement** — "拉菲 奥希耶黑鸢" → "Lafite Aussieres Noir"
- **Wine & winery background** — Wikipedia-powered history, region, and appellation info (bilingual)
- **Vintage comparison & recommendations** — Rating-based labels (Outstanding/Very Good/Good/Fair/Poor) with value advice
- **16+ platform price links** — 京东, 天猫, 淘宝, 拼多多, Vivino, Wine-Searcher, Total Wine, etc.
- **Health drinking advice** — Age-group limits, 10 health condition warnings
- **Food pairing** — Staple food & main dish recommendations for 6 wine types
- **Image OCR search** — Identify wines from label photos (pytesseract/easyocr)
- **China-friendly** — Firecrawl proxy bypasses Vivino blockade; Wikipedia API accessible from China

## 📊 Data Sources

| Source | Type | Key Required | Data | Status |
|--------|------|-------------|------|--------|
| Wine-Searcher (WebFetch) | Web + AI parsing | No | Ratings, prices, vintages, tasting notes | Primary |
| Vivino (Firecrawl) | Firecrawl scrape | Yes | Ratings, taste profile, grapes, food pairing | Secondary |
| Wikipedia API | REST API | No | Wine & winery background, history | Tertiary |
| Open Food Facts API | REST API | No | Basic metadata (ABV, grape, image) | Supplementary |
| Vivino API | REST API | No | — | Blocked (403) |

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (uses standard library only for core functionality)

### Install

```bash
git clone https://github.com/Amurtiger01/wine-info-search-skill.git
cd wine-info-search-skill
```

No `pip install` required for core functionality. Optional dependencies (pinned versions):

```bash
# Install all optional OCR dependencies with pinned versions
pip install -r scripts/requirements.txt

# Or install individually (pinned versions recommended):
# pip install pytesseract==0.3.13 Pillow==11.2.1   # Requires Tesseract-OCR on system
# pip install easyocr==1.7.2                        # Deep learning OCR, standalone
```

### Basic Usage

```bash
# Search by brand name (Chinese or English)
python scripts/wine_search.py "拉菲"
python scripts/wine_search.py "Penfolds"

# Search with vintage year
python scripts/wine_search.py "拉菲" 2018

# Search with brand + year + series
python scripts/wine_search.py "奔富" 2020 "Bin 389"

# Search mode: info only / price only / all (default)
python scripts/wine_search.py "拉菲" 2018 --mode info
python scripts/wine_search.py "奔富" --mode price

# Image-based search (wine label photo)
python scripts/wine_search.py --image "/path/to/wine_label.jpg"

# Use Firecrawl for Vivino access
python scripts/wine_search.py "拉菲" --firecrawl-key fc-xxxx
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FIRECRAWL_API_KEY` | No | Firecrawl API key for Vivino access (wine search only). Prefer env var over `--firecrawl-key` to avoid key exposure. Free tier: 500 req/month. Register at [firecrawl.dev](https://firecrawl.dev) |

## 📋 Output Sections

When running in default (`--mode all`) mode, the script outputs:

1. **📋 酒款信息** — Search results, best match details, grape varieties, taste profile, vintage comparison
2. **🏛️ 酒款与酒庄背景** — Wikipedia-sourced wine & winery history
3. **💰 各平台价格与购买链接** — WebFetch price hints + 16 platform search links
4. **Drinking Tips** — Drinking window advice, value recommendations
5. **🏥 健康饮用建议** — Age-group limits, health condition warnings
6. **🍽️ 餐饮搭配建议** — Food pairing recommendations

## 🗺️ Bilingual Name Mapping

The script contains 110+ Chinese ↔ English wine name entries with smart multi-segment replacement:

| Input | Output |
|-------|--------|
| 拉菲 | Lafite |
| 拉菲古堡 | Château Lafite Rothschild |
| 奔富Bin 389 | Penfolds Bin 389 |
| 拉菲 奥希耶黑鸢 | Lafite Aussieres Noir |
| 木桐古堡 | Château Mouton Rothschild |
| 作品一号 | Opus One |

## 🌐 Platform Coverage

**Domestic (China):** 京东 · 天猫 · 淘宝 · 苏宁易购 · 拼多多 · 1919吃喝 · 也买酒 · 酒仙网

**International:** Vivino · Wine.com · Drizly · Total Wine · Wine-Searcher · Wine Spectator · CellarTracker · Decántalo

## 📁 Project Structure

```
wine-info-search/
├── README.md
├── SKILL.md                  # Skill definition (for Claude Code / AI agent integration)
├── scripts/
│   ├── wine_search.py        # Main script (~3500 lines)
│   └── requirements.txt      # Optional dependencies
└── references/
    └── api_reference.md      # Data source API reference & troubleshooting
```

## ⚙️ Advanced Configuration

### Firecrawl Integration

Firecrawl enables Vivino access from China by providing US proxy IPs + JavaScript rendering. **Prefer the environment variable** to avoid exposing the key in shell history or process listings.

```bash
# Recommended: Environment variable
export FIRECRAWL_API_KEY=fc-xxxx     # Linux/macOS
set FIRECRAWL_API_KEY=fc-xxxx        # Windows

# Alternative: Command-line argument (key visible in shell history)
python scripts/wine_search.py "拉菲" --firecrawl-key fc-xxxx
```

**Security**: When a Firecrawl API key is present, `--insecure` is automatically blocked to prevent bearer token interception.

### SSL Note

The script **validates SSL certificates by default** — no automatic fallback to insecure mode. If certificate verification fails, the error includes a suggestion to use `--insecure`. The `--insecure` flag is **blocked** when a Firecrawl API key is present:

```bash
# Only works when no API key is configured
python scripts/wine_search.py "拉菲" --insecure
```

## 🔧 Integration with AI Agents

This project is designed as a **Claude Code Skill**. The `SKILL.md` file provides:
- Trigger conditions for when to invoke the skill
- Detailed workflow for AI agents
- Command reference and common query patterns
- Output format documentation

AI agents can use the script's output directly, or use **WebFetch** to visit the generated URLs for real-time price data.

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Wine-Searcher](https://www.wine-searcher.com) — Primary wine data source
- [Vivino](https://www.vivino.com) — Community wine ratings and reviews
- [Firecrawl](https://firecrawl.dev) — Web scraping proxy for Vivino access
- [Wikipedia](https://www.wikipedia.org) — Wine & winery background information
- [Open Food Facts](https://world.openfoodfacts.org) — Supplementary wine metadata
