---
name: iploop-qa-scraper
description: QA web scraping skill using IPLoop proxy infrastructure. Scrapes 66 major sites via SDK v1.5.3 with API extractors, anti-bot bypass, smart fallbacks, and real data extraction. 100% success rate. Use when testing proxy quality, scraping sites through IPLoop, or validating proxy data extraction. Triggers on proxy QA, site scraping, data extraction testing, anti-bot bypass.
---

# IPLoop QA Scraper

Scrape 66 major sites through IPLoop residential proxy + Scrapling anti-bot fingerprinting.

**SDK Version:** v1.8.1 | **Legacy QA Success Rate:** 100% (66/66) | **Install:** `pip install iploop-sdk`

## Strategy: Combo by Default

All sites use Scrapling anti-bot + residential proxy combo. Falls back to plain HTTP if Scrapling fails.

| Tier | Method | Count | Sites |
|------|--------|-------|-------|
| 1 | Public APIs | 12 | YouTube, Stocks, CoinGecko, Spotify, NPM, PyPI, XKCD, ExchangeRate, SpaceX, Pokemon, Weather, RemoteOK |
| 2 | HTTP + Proxy | 28 | Amazon, eBay, TikTok, Target, Airbnb, Cloudflare, Shopify, IMDb, Wikipedia, HackerNews, GitHub, StackOverflow, Steam, Goodreads, Archive.org, CNN, Trustpilot, Craigslist, Newegg, BBC, Medium, DuckDuckGo, Bing, Yahoo News, Fox News, Guardian, Dev.to, Apple, Samsung, Microsoft |
| 3 | Scrapling + Proxy | 26 | Reddit, Twitter, LinkedIn, Instagram, Booking, Walmart, BestBuy, Pinterest, Zillow, Nike, Wayfair, HomeDepot, Costco, Nordstrom, NYTimes, Quora, Twitch, ASOS, IKEA, Coursera, Zappos, Hulu, Walmart Grocery |

## All 67 Site Presets

| # | Site | Method | Status |
|---|------|--------|--------|
| 1 | YouTube | API | ✅ |
| 2 | Reddit | Scrapling | ✅ |
| 3 | Stocks (Yahoo) | API | ✅ |
| 4 | Amazon | Proxy | ✅ |
| 5 | eBay | Proxy | ✅ |
| 6 | Twitter/X | Scrapling | ✅ |
| 7 | LinkedIn | Scrapling | ✅ |
| 8 | TikTok | Proxy | ✅ |
| 9 | Instagram | Scrapling | ✅ |
| 10 | Booking.com | Scrapling | ✅ |
| 11 | Walmart | Scrapling | ✅ |
| 12 | Target | Proxy | ✅ |
| 13 | Airbnb | Proxy | ✅ |
| 14 | BestBuy | Scrapling | ✅ |
| 15 | Cloudflare | Proxy | ✅ |
| 16 | Pinterest | Scrapling | ✅ |
| 17 | Zillow | Scrapling | ✅ |
| 18 | Shopify | Proxy | ✅ |
| 19 | IMDb | Proxy | ✅ |
| 20 | Wikipedia | Proxy | ✅ |
| 21 | HackerNews | Proxy | ✅ |
| 22 | GitHub | Proxy | ✅ |
| 23 | CoinGecko | API | ✅ |
| 24 | Spotify | API | ✅ |
| 25 | StackOverflow | Proxy | ✅ |
| 26 | NPM | API | ✅ |
| 27 | PyPI | API | ✅ |
| 28 | XKCD | API | ✅ |
| 29 | ExchangeRate | API | ✅ |
| 30 | SpaceX | API | ✅ |
| 31 | Pokemon | API | ✅ |
| 32 | Steam | Proxy | ✅ |
| 33 | Goodreads | Proxy | ✅ |
| 34 | Archive.org | Proxy | ✅ |
| 35 | CNN | Proxy | ✅ |
| 36 | Trustpilot | Proxy | ✅ |
| 37 | Weather | API | ✅ |
| 38 | RemoteOK | API | ✅ |
| 39 | Craigslist | Proxy | ✅ |
| 40 | Nike | Scrapling | ✅ |
| 41 | Wayfair | Scrapling | ✅ |
| 42 | HomeDepot | Scrapling | ✅ |
| 43 | Costco | Scrapling | ✅ |
| 44 | Nordstrom | Scrapling | ✅ |
| 45 | Newegg | Proxy | ✅ |
| 46 | BBC | Proxy | ✅ |
| 47 | NYTimes | Scrapling | ✅ |
| 48 | Quora | Scrapling | ✅ |
| 49 | Medium | Proxy | ✅ |
| 50 | DuckDuckGo | Proxy | ✅ |
| 51 | Bing | Proxy | ✅ |
| 52 | Yahoo News | Proxy | ✅ |
| 53 | Fox News | Proxy | ✅ |
| 54 | The Guardian | Proxy | ✅ |
| 55 | Twitch | Scrapling | ✅ |
| 56 | Dev.to | Proxy | ✅ |
| 57 | ASOS | Scrapling | ✅ |
| 58 | IKEA | Scrapling | ✅ |
| 59 | Apple | Proxy | ✅ |
| 60 | Samsung | Proxy | ✅ |
| 61 | Coursera | Scrapling | ✅ |
| 62 | Zappos | Scrapling | ✅ |
| 63 | Target Tech | Proxy | ✅ |
| 64 | Hulu | Scrapling | ✅ |
| 65 | Walmart Grocery | Scrapling | ✅ |
| 66 | Microsoft | Proxy | ✅ |

## Quick Start

```bash
pip install iploop==1.5.3
```

```python
from iploop import IPLoop

client = IPLoop(api_key="YOUR_API_KEY")

# One-liner — auto-detects site, returns structured data
result = client.scrape("https://www.amazon.com/dp/B0BSHF7WHW")
print(result)
# → {"success": True, "data": {"title": "MacBook Pro", "price": "1,873"}, "source": "http_proxy"}
```

## QA Runner

```bash
# Run all 66 presets
python3 scripts/qa_scraper.py --api-key YOUR_KEY --country US

# Run specific site
python3 scripts/qa_scraper.py --site amazon --api-key YOUR_KEY

# Stability test (multiple runs)
python3 scripts/qa_scraper.py --api-key YOUR_KEY --runs 5
```

## Proxy Auth Format

```
http://iploop:APIKEY-country-XX@proxy.iploop.io:8880
```

Parameters: `country-XX`, `city-NAME`, `session-ID`, `sesstype-sticky|rotating`

## Known Limitations

- **Google Search** — 429 rate limits on rapid sequential hits (removed from presets)
- **Indeed** — Cloudflare security check blocks ~50% (removed)
- **AliExpress** — anti-bot catches 60%+ (removed)
- **Etsy/Glassdoor/DataDome** — enterprise anti-bot, needs full browser automation
- **LinkedIn** — has "sign in" prompts but returns full data (handled with >100KB rule)
- **HomeDepot** — category pages blocked by Akamai, homepage works fine

## Version History

| Version | Date | Changes | Success Rate |
|---------|------|---------|-------------|
| v1.5.0 | Feb 19 | Initial 33 presets | 81.8% |
| v1.5.3 | Feb 20 | Amazon DuckDuckGo fallback, residential proxy | 96.6% |
| v2.0 | Mar 10 | 48 presets, Scrapling anti-bot, stability tested 5x | 100% (48/48) |
| v2.5 | Mar 10 | LinkedIn fix, block detection fix | 100% (49/49) |
| v2.8 | Mar 10 | 66 presets, 17 new sites, HomeDepot fix | 100% (66/66) |

## References

- `scripts/qa_scraper.py` — main QA test runner (66 presets)
- `references/site-presets.md` — detailed extractor logic per site
- `references/anti-bot-notes.md` — known blocks and workarounds
