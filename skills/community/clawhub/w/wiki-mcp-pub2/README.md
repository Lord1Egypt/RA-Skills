# Wikipedia MCP

A Model Context Protocol (MCP) server that provides access to Wikipedia via the free REST API. No API key required.

⭐ If you find this useful, please star the repo — it helps others discover it.

## Contributing

Contributions are welcome — new tools especially. See [CONTRIBUTING.md](CONTRIBUTING.md) for the how-to: one file, one tool per PR, smoke tests included.

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search Wikipedia for articles matching a query |
| `summary` | Get a Wikipedia article summary + thumbnail by title |
| `random` | Get a random Wikipedia article summary |
| `simple_summary` | Get the Simple English Wikipedia version of a topic — plain-language explanation |
| `did_you_know` | Get a random "Did You Know" style fact |
| `dino_fact` | Get a dino/prehistory-specific fact (specific species or random) |
| `featured_article` | Get today's Wikipedia Featured Article |
| `picture_of_the_day` | Get Wikimedia Commons' Picture of the Day (today, or a YYYYMMDD date) |
| `media_of_the_day` | Get Wikimedia Commons' Media of the Day — the curated daily video/audio clip (today, or a YYYYMMDD date) |
| `article_extract` | Get a full plain-text extract of an article (longer than `summary`) |
| `article_sections` | Get the table of contents (section headings) for an article — useful for navigating long articles before reading the full body |
| `section_text` | Read one section of an article as plain text — by number, hierarchical number (e.g. `2.1`), or heading name — without pulling the whole article |
| `on_this_day` | Get historical events that happened on today's date |
| `deaths_on_this_day` | Get notable deaths that happened on today's date (companion to `on_this_day`) |
| `births_on_this_day` | Get notable births that happened on today's date (companion to `on_this_day` / `deaths_on_this_day`) |
| `categories` | List Wikipedia categories an article belongs to |
| `links` | List outgoing Wikipedia links from an article (the article's reference network) |
| `backlinks` | List incoming Wikipedia links to an article (what links here / referrer pages — inverse of `links`) |
| `external_links` | List external (off-wiki) links from an article — citations, references, and primary sources the article points to (outbound complement to `links` + `backlinks`) |
| `nearby` | List Wikipedia articles geographically near a location — anchor by article title (e.g. 'Eiffel Tower') or lat/lon, with distances |
| `translations` | List all language versions of an article (langlinks) — discover what languages it exists in |
| `revisions` | Show an article's recent edit history (who edited it, when, edit summaries, size deltas) with diff links |
| `pageviews` | Get daily view counts for an article (popularity, trending, historical interest) |
| `news` | Get current events from Wikipedia's Main Page "In the news" section |
| `top_reads` | Get the most-read articles on Wikipedia for a given date |
| `image` | Get just the lead image (thumbnail + original URLs) for an article, no summary text |
| `media_list` | List all media (images, videos, audio) used in an article — full inventory with type, caption, and thumbnail |
| `media_search` | Search Wikimedia Commons for freely-licensed media by keyword (topic-based discovery — `filetype`: image/video/audio/all) |
| `quote` | Get a random notable quote from a curated list of famous authors |
| `recent_changes` | Live window into Wikipedia right now — most recent edits, with kind filter ('all', 'edit', 'new', 'categorize', 'log') for breaking-news edits, newly published articles, and more |
| `category_members` | List articles filed under a category — taxonomy-based discovery, the reverse of `categories`; each entry has a 1–2 sentence extract + thumbnail |
| `infobox` | Extract an article's structured fact box (infobox) as a field/value table — dates, people, places, statistics; the fastest path to a concrete fact without reading prose |
| `article_quality` | Wikipedia's quality assessments for an article — WikiProject grades (FA, GA, B, C, Start, Stub) + importance ratings; the encyclopedia's own trust signal before relying on an article |
| `related_articles` | Find articles semantically similar to a given article ("what should I read next") — Wikipedia's own MoreLikeThis search ranking, each with short description + thumbnail |
| `contributors` | Who writes and maintains an article — most active recent editors ranked by edit count (up to 500 sampled revisions), with user-page links + anonymous (IP) edit share; the provenance companion to `article_quality` |
| `references` | The sources an article cites — its bibliography: each citation's text plus the off-wiki URLs it points to (DOI, publisher, archive, primary-source links); the verification companion to `external_links` |
| `revision_diff` | Compare two revisions of an article — plain-text unified diff of what a specific edit changed, each side labelled with timestamp, editor, and edit summary |
| `disambiguation` | Resolve a disambiguation page into its candidate articles — title + one-line description, grouped by section; pick the right one, then fetch it |
| `user_contribs` | What a Wikipedia editor has been doing — latest contributions by a username or IP (timestamp, byte delta, edit comment, new-page/minor/current flags), with registration date + total edit count; profile contributors or audit anonymous IPs |
| `citation_needed` | Find statements Wikipedia has flagged as needing a source — pass `article` to extract its tagged claims (with tag dates), or `topic` for articles with unsourced claims on a topic; the verification companion to `references` |
| `talk` | Read an article's talk page — the most recently active editor discussion threads, each with heading, last-activity timestamp, signed-comment count, and an excerpt of the latest comment; automated notices filtered out — the behind-the-scenes companion to `contributors` and `article_quality` |
| `article_flags` | Show the maintenance banners editors placed on an article — {{POV}}, {{Original research}}, {{Unreferenced}}, {{Cleanup}}, {{Disputed}} and more, each with tag date, location (article top or section), and a plain-language meaning; the trust-signal companion to `article_quality`, `citation_needed`, and `talk` |
| `article_protection` | Is this Wikipedia article locked — which actions are restricted (editing, moving/renaming, creating), at what level (semi-protection, extended-confirmed, administrators-only), and when each restriction expires; follows redirects; the lockdown companion to the other trust signals |
| `article_pulse` | Vital signs of an article — creation date + creator, page length, watcher count, most recent edit, and edit velocity over the last 30 days, with a plain-language activity verdict (buzzing / active / quiet / dormant); the liveliness companion to `article_quality`, `contributors`, `revisions`, and `pageviews` |
| `citation_sources` | Which publishers an article's evidence comes from — its references aggregated by source domain into a ranked publisher map with per-domain share, plus archived-copy and DOI-linked scholarly shares and a plain-language verdict (diverse / balanced / top-heavy / lopsided / thin); the diversity companion to `references`, `article_quality`, `article_flags`, and `citation_needed` |
| `article_path` | Find the shortest click-path between two articles — the six-degrees game: searches Wikipedia's link graph for the shortest chain of blue links (1–3 hops, bidirectional and bounded), follows redirects; the discovery companion to `links` and `backlinks` |
| `article_at_date` | Show what an article said on a given date — the time machine: given a title and a YYYY-MM-DD date, returns the lead text of the latest surviving revision at or before that day, with revision ID, timestamp, editor, edit summary, and a permanent link to the exact revision; follows redirects; the history companion to `summary`, `revisions`, and `revision_diff` |

All tools accept an optional `lang` parameter (one of: `en`, `de`, `es`, `fr`, `ja`, `zh`, `pt`, `it`, `ru`, `nl`), except `media_search` — Wikimedia Commons is language-independent, so it takes no `lang` — and `simple_summary`, which always reads Simple English Wikipedia. Note: `quote` accepts the parameter for API consistency but is currently English-only (curated list).

## Setup

This is a standard MCP server — it works with any MCP client (Claude Code, Cursor, Windsurf, etc.).

### Any MCP client

Add to your client's MCP config (e.g. `~/.claude.json`, or Cursor's `mcp.json`):

```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "python3",
      "args": ["/path/to/wikipedia-mcp/src/server.py"]
    }
  }
}
```

Then restart your client (or reload its MCP servers) to pick it up.

### OpenClaw (via mcporter)

Add the same `mcpServers` block to `~/.openclaw/workspace/config/mcporter.json`, then restart the gateway:

```bash
openclaw gateway restart
```

## Usage

```bash
# Search
mcporter call wikipedia search --args '{"query": "velociraptor", "limit": 5}'

# Article summary
mcporter call wikipedia summary --args '{"title": "Tyrannosaurus"}'

# Random article
mcporter call wikipedia random

# Simple English explanation ("explain it simply")
mcporter call wikipedia simple_summary --args '{"title": "Photosynthesis"}'

# Random dino fact
mcporter call wikipedia dino_fact

# Specific species
mcporter call wikipedia dino_fact --args '{"species": "Spinosaurus"}'

# Today's featured article
mcporter call wikipedia featured_article

# Picture of the Day (curated daily image from Wikimedia Commons)
mcporter call wikipedia picture_of_the_day
mcporter call wikipedia picture_of_the_day --args '{"date": "20260901"}'

# Media of the Day (curated daily video/audio clip from Wikimedia Commons)
mcporter call wikipedia media_of_the_day
mcporter call wikipedia media_of_the_day --args '{"date": "20260830"}'

# Full plain-text article extract (vs summary)
mcporter call wikipedia article_extract --args '{"title": "Tyrannosaurus"}'

# Article table of contents — section headings (navigate before reading full body)
mcporter call wikipedia article_sections --args '{"title": "Tyrannosaurus"}'

# Read one section of an article (by number, "2.1", or heading name — 0 = lead/intro)
mcporter call wikipedia section_text --args '{"title": "Tyrannosaurus", "section": "Description"}'
mcporter call wikipedia section_text --args '{"title": "Tyrannosaurus", "section": 3}'

# On this day (historical events for today)
mcporter call wikipedia on_this_day
mcporter call wikipedia on_this_day --args '{"count": 8}'

# Deaths on this day (notable deaths for today — in memoriam content hooks)
mcporter call wikipedia deaths_on_this_day
mcporter call wikipedia deaths_on_this_day --args '{"count": 6}'

# Births on this day (notable births for today — "born on this day" content hooks)
mcporter call wikipedia births_on_this_day
mcporter call wikipedia births_on_this_day --args '{"count": 6}'

# Categories for an article (taxonomy-based discovery)
mcporter call wikipedia categories --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia categories --args '{"title": "Tyrannosaurus", "limit": 10}'

# Outgoing links from an article (graph-style discovery)
mcporter call wikipedia links --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia links --args '{"title": "Tyrannosaurus", "limit": 30}'

# Translations — list all language editions of an article
mcporter call wikipedia translations --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia translations --args '{"title": "Tyrannosaurus", "limit": 10}'

# Revision history — recent edits, editors, summaries, diffs
mcporter call wikipedia revisions --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia revisions --args '{"title": "Tyrannosaurus", "limit": 20}'

# Daily view counts (popularity research, trending topics)
mcporter call wikipedia pageviews --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia pageviews --args '{"title": "Python_(programming_language)", "start": "20250101", "end": "20250107"}'

# Current events from Wikipedia's Main Page (today's "In the news")
mcporter call wikipedia news
mcporter call wikipedia news --args '{"limit": 8}'

# Top reads — most-viewed articles on a given date
mcporter call wikipedia top_reads
mcporter call wikipedia top_reads --args '{"date": "20260101", "limit": 15}'

# Lead image — thumbnail + original URLs for an article (no text)
mcporter call wikipedia image --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia image --args '{"title": "Tyrannosaurus", "lang": "de"}'

# Media inventory — all images/videos/audio in an article (full list, not just lead)
mcporter call wikipedia media_list --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia media_list --args '{"title": "Tyrannosaurus", "limit": 50}'
mcporter call wikipedia media_list --args '{"title": "Berlin", "lang": "de"}'

# Media search — freely-licensed Commons media by keyword (topic-based, not article-based)
mcporter call wikipedia media_search --args '{"query": "aurora borealis"}'
mcporter call wikipedia media_search --args '{"query": "volcano eruption", "filetype": "video", "limit": 5}'

# Related articles — semantically similar articles ("what should I read next")
mcporter call wikipedia related_articles --args '{"title": "Velociraptor"}'
mcporter call wikipedia related_articles --args '{"title": "Velociraptor", "limit": 10}'

# Contributors — who writes and maintains an article
mcporter call wikipedia contributors --args '{"title": "Albert Einstein"}'
mcporter call wikipedia contributors --args '{"title": "Velociraptor", "limit": 5}'

# References — the sources an article cites (its bibliography)
mcporter call wikipedia references --args '{"title": "Albert Einstein"}'
mcporter call wikipedia references --args '{"title": "Velociraptor", "limit": 10}'

# Random notable quote (curated list of famous authors)
mcporter call wikipedia quote
mcporter call wikipedia quote --args '{"lang": "de"}'  # lang accepted, currently English-only

# Non-English Wikipedia
mcporter call wikipedia summary --args '{"title": "Berlin", "lang": "de"}'
```

## Requirements

- Python 3.10+
- `requests>=2.28.0`

## API

Uses Wikipedia's free REST API:
- Search: MediaWiki Action API (`/w/api.php`)
- Summary / Random / Featured / Media-list: REST API v1 (`/api/rest_v1/...`)
- Pageviews / Top reads: Wikimedia cross-wiki metrics API (`https://wikimedia.org/api/rest_v1/metrics/pageviews/...`)
- Related articles: MediaWiki Action API (search generator with `morelike:` scoring)

No API key required. Respects Wikipedia's User-Agent policy.

## Development

Run the smoke tests:

```bash
python3 tests/test_server.py
```

## License

MIT
