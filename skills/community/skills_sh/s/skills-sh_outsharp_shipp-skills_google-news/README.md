# Google News Skill

Teaches AI agents how to fetch and parse news from [Google News](https://news.google.com) — a free news aggregator that surfaces headlines from thousands of publishers worldwide via public RSS 2.0 feeds.

## What This Skill Provides

The `SKILL.md` file gives your agent full context on:

- **RSS Feed Endpoints** — Top stories, topic-based feeds, and keyword/search feeds
- **Multi-Region Support** — 11 validated locales (US, UK, India, Australia, Canada, Germany, France, Japan, Brazil, Mexico, Israel) with the `hl`, `gl`, and `ceid` query parameters
- **Topic IDs** — Pre-mapped IDs for World, Business, Technology, Entertainment, Sports, Science, Health, and Nation
- **Search Modifiers** — AND, OR, exclusion, exact phrase, time filters (`when:7d`), date ranges (`after:`, `before:`), and site-scoped queries (`site:`)
- **Response Parsing** — Full RSS 2.0 XML schema documentation including how to extract related/clustered articles from the HTML `<description>` field
- **Redirect Resolution** — How to follow Google News redirect URLs to reach the actual publisher page
- **Rate Limits & Error Handling** — Community-observed polling guidelines and HTTP status code reference

## When to Use This Skill

Use the Google News skill when your agent needs to:

- Fetch the latest top headlines for any supported country or language
- Browse news by topic (World, Business, Technology, Sports, Science, Health, Entertainment)
- Search for articles by keyword, phrase, date range, or source domain
- Aggregate news from multiple regions into a single view
- Monitor a topic or search query over time with polling
- Extract clustered/related articles from a single news story
- Resolve Google News redirect URLs to the original publisher links

## Getting Started

### 1. No Setup Required

All Google News RSS feeds are **fully public** — no API key, authentication, or account is needed. Your agent can start fetching headlines immediately.

### 2. Choose Your Feed

| Feed Type | URL Pattern | Example |
|-----------|-------------|---------|
| **Top Stories** | `https://news.google.com/rss?hl={hl}&gl={gl}&ceid={gl}:{lang}` | [US Top Stories](https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en) |
| **Topic** | `https://news.google.com/rss/topics/{TOPIC_ID}?hl=...&gl=...&ceid=...` | Technology, Business, Sports, etc. |
| **Search** | `https://news.google.com/rss/search?q={query}&hl=...&gl=...&ceid=...` | `q=artificial+intelligence+when:7d` |

### 3. Parse the Response

Feeds return standard RSS 2.0 XML. Use any RSS parser — `feedparser` (Python), `xml2js` (Node.js), `xmllint` (CLI), or even `grep` for quick extraction.

## Key Concepts

| Concept | Description |
|---|---|
| **RSS 2.0** | The XML syndication format used by all Google News feeds |
| **`hl` parameter** | Interface language / locale code (e.g., `en-US`, `de`, `ja`) |
| **`gl` parameter** | Country code for geographic targeting (ISO 3166-1 alpha-2, e.g., `US`, `GB`, `DE`) |
| **`ceid` parameter** | Compound locale key in the format `{country}:{language}` (e.g., `US:en`, `DE:de`) |
| **Topic ID** | Base64-encoded protocol buffer string that identifies a news section (e.g., Technology, Sports) |
| **Article Cluster** | A group of related articles from different publishers covering the same story, found in the `<description>` HTML |
| **Redirect URL** | Google News article links (`/rss/articles/...`) redirect (302) to the actual publisher page |
| **Search Modifiers** | Query operators like `when:7d`, `site:`, `after:`, `before:`, `OR`, and `-` for exclusion |

## Feed Endpoints at a Glance

| Endpoint | Path | Purpose |
|---|---|---|
| **Top Stories** | `/rss` | Current headlines for a region |
| **Topic Feed** | `/rss/topics/{TOPIC_ID}` | Articles for a specific news category |
| **Search Feed** | `/rss/search?q={query}` | Articles matching a keyword or phrase |

## Validated Regions

| Region | Parameters |
|---|---|
| 🇺🇸 United States | `hl=en-US&gl=US&ceid=US:en` |
| 🇬🇧 United Kingdom | `hl=en-GB&gl=GB&ceid=GB:en` |
| 🇮🇳 India | `hl=en-IN&gl=IN&ceid=IN:en` |
| 🇦🇺 Australia | `hl=en-AU&gl=AU&ceid=AU:en` |
| 🇨🇦 Canada | `hl=en-CA&gl=CA&ceid=CA:en` |
| 🇩🇪 Germany | `hl=de&gl=DE&ceid=DE:de` |
| 🇫🇷 France | `hl=fr&gl=FR&ceid=FR:fr` |
| 🇯🇵 Japan | `hl=ja&gl=JP&ceid=JP:ja` |
| 🇧🇷 Brazil | `hl=pt-BR&gl=BR&ceid=BR:pt-419` |
| 🇲🇽 Mexico | `hl=es-419&gl=MX&ceid=MX:es-419` |
| 🇮🇱 Israel | `hl=en-IL&gl=IL&ceid=IL:en` |

## Tips

- **Zero setup** — no keys, no auth, no account. Just fetch the URL.
- **Use `feedparser` in Python** — it handles RSS parsing, date normalization, and encoding automatically.
- **Combine search modifiers** for precision — `q=Tesla+site:reuters.com+when:30d`.
- **Topic IDs are locale-specific** — an English topic ID may not work with `hl=de`. Inspect the Google News page in that locale to find the correct ID.
- **Parse `<description>` for related articles** — each story clusters multiple sources as an HTML `<ol>` list.
- **Split `<title>` on ` - `** (from the right) to separate the headline from the publisher name.
- **Resolve redirects lazily** — only follow the Google redirect URL when you need the final publisher link.
- **Respect rate limits** — poll no more frequently than once per 60 seconds per feed.
- **Set a descriptive User-Agent** — e.g., `MyNewsBot/1.0 (contact@example.com)`.

## Resources

| Resource | URL |
|---|---|
| Google News | [news.google.com](https://news.google.com) |
| US Top Stories RSS | [news.google.com/rss?hl=en-US&gl=US&ceid=US:en](https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en) |
| RSS 2.0 Specification | [www.rssboard.org/rss-specification](https://www.rssboard.org/rss-specification) |
| feedparser (Python) | [feedparser.readthedocs.io](https://feedparser.readthedocs.io/) |
| xml2js (Node.js) | [github.com/Leonidas-from-XIV/node-xml2js](https://github.com/Leonidas-from-XIV/node-xml2js) |