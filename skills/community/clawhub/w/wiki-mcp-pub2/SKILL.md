---
name: wikipedia
version: 1.1.14
description: Access Wikipedia via MCP — search articles, get summaries, random facts, dinosaur facts, today's featured article, today's historical events, article categories, outgoing links, view counts, current news, and most-read articles. Multi-language support (10 wikis). Great for research, content hooks, and general knowledge lookups.
---

# Wikipedia MCP

Access Wikipedia via Model Context Protocol (MCP). No API key required.

## Tools

| Tool | Description |
|------|-------------|
| `search` | Search Wikipedia for articles |
| `summary` | Get article summary + image by title |
| `random` | Random Wikipedia article |
| `simple_summary` | Simple English Wikipedia version of a topic — plain-language explanation |
| `did_you_know` | Random "Did You Know" fact |
| `dino_fact` | Dinosaur/prehistory fact (specific species or random) |
| `featured_article` | Today's Wikipedia Featured Article |
| `picture_of_the_day` | Wikimedia Commons' Picture of the Day — curated daily image (default today UTC, optional YYYYMMDD date) |
| `media_of_the_day` | Wikimedia Commons' Media of the Day — curated daily video/audio clip (default today UTC, optional YYYYMMDD date) |
| `article_extract` | Full plain-text article extract by title (longer than `summary`) |
| `article_sections` | Table of contents (section headings) for an article — navigate before reading the full body |
| `section_text` | Read one section of an article as plain text — by number, hierarchical number (e.g. `2.1`), or heading name (0 = lead/intro) |
| `on_this_day` | Historical events that happened on today's date |
| `deaths_on_this_day` | Notable deaths that happened on today's date — companion to `on_this_day` (events) |
| `births_on_this_day` | Notable births that happened on today's date — companion to `on_this_day` (events) and `deaths_on_this_day` (deaths) |
| `categories` | List Wikipedia categories an article belongs to |
| `links` | List outgoing Wikipedia links from an article (graph-style discovery) |
| `backlinks` | List incoming Wikipedia links to an article — what links here (inverse of `links`) |
| `external_links` | List external (off-wiki) links from an article — citations, references, primary sources |
| `nearby` | Articles geographically near a location — anchor by article title or lat/lon, distances included |
| `translations` | All language versions of an article (langlinks) — discover what languages it exists in |
| `revisions` | Recent edit history of an article — who edited it, when, edit summaries, byte-size deltas, diff links |
| `pageviews` | Daily view counts for an article (popularity research, trending topics) |
| `news` | Current events from Wikipedia's Main Page "In the news" section |
| `top_reads` | Most-read articles on Wikipedia for a given date (trending discovery) |
| `image` | Lead image for an article — thumbnail + original URLs, no summary text |
| `media_list` | All media (images, videos, audio) in an article — full inventory with type, caption, and thumbnail |
| `media_search` | Search Wikimedia Commons for freely-licensed media by keyword — topic-based discovery (`filetype`: image/video/audio/all) |
| `quote` | Random notable quote from a curated list of famous authors |
| `recent_changes` | Most recent changes to Wikipedia articles (live feed) — filter by 'all', 'edit', 'new', 'categorize', or 'log' |
| `category_members` | Articles filed under a category (reverse of `categories`) — taxonomy-based discovery, each entry with a 1–2 sentence extract + thumbnail |
| `infobox` | An article's structured fact box as a field/value table — dates, people, places, statistics; the fastest path to a concrete fact |
| `article_quality` | Wikipedia's quality assessments (WikiProject grades FA/GA/B/C/Start/Stub + importance) — the trust signal to check before relying on an article |
| `related_articles` | Articles semantically similar to a given article ("what should I read next") — Wikipedia's own MoreLikeThis ranking, each with short description + thumbnail |
| `contributors` | Who writes and maintains an article — most active recent editors ranked by edit count, with user-page links + anonymous (IP) edit share; the provenance companion to `article_quality` |
| `references` | The sources an article cites — its bibliography: each citation's text plus the off-wiki URLs it points to (DOI, publisher, archive, primary-source links); the verification companion to `external_links` |
| `revision_diff` | Compare two revisions of an article — plain-text unified diff of what a specific edit changed, each side labelled with timestamp, editor, and edit summary |
| `disambiguation` | Resolve a disambiguation page into its candidate articles — title + one-line description, grouped by section; pick the right one, then fetch it |
| `user_contribs` | What a Wikipedia editor has been doing — latest contributions by a username or IP (timestamp, byte delta, edit comment, new-page/minor/current flags), with registration date + total edit count; profile contributors or audit anonymous IPs |
| `citation_needed` | Find statements Wikipedia has flagged as needing a source — pass `article` to extract its tagged claims (with tag dates), or `topic` for articles with unsourced claims on a topic; the verification companion to `references` |
| `talk` | Read an article's talk page — the most recently active editor discussion threads, each with heading, last-activity timestamp, signed-comment count, and an excerpt of the latest comment; automated notices filtered out — the behind-the-scenes companion to `contributors` and `article_quality` |
| `article_flags` | Show the maintenance banners editors placed on an article — POV, Original research, Unreferenced, Cleanup, Disputed and more, each with tag date, location, and a plain-language meaning; the trust-signal companion to `article_quality`, `citation_needed`, and `talk` |
| `article_protection` | Is this Wikipedia article locked — which actions are restricted (editing, moving/renaming, creating), at what level (semi-protection, extended-confirmed, administrators-only), and when each restriction expires; follows redirects; the lockdown companion to the other trust signals |
| `article_pulse` | Vital signs of an article — creation date + creator, page length, watcher count, most recent edit, and edit velocity over the last 30 days, with a plain-language activity verdict (buzzing / active / quiet / dormant); the liveliness companion to `article_quality`, `contributors`, `revisions`, and `pageviews` |
| `citation_sources` | Which publishers an article's evidence comes from — its references aggregated by source domain into a ranked publisher map with per-domain share, plus archived-copy and DOI-linked scholarly shares and a plain-language verdict (diverse / balanced / top-heavy / lopsided / thin); the diversity companion to `references`, `article_quality`, `article_flags`, and `citation_needed` |
| `article_path` | Find the shortest click-path between two articles — the six-degrees game: searches Wikipedia's link graph for the shortest chain of blue links (1–3 hops, bidirectional and bounded), follows redirects; the discovery companion to `links` and `backlinks` |
| `article_at_date` | Show what an article said on a given date — the time machine: given a title and a YYYY-MM-DD date, returns the lead text of the latest surviving revision at or before that day, with revision ID, timestamp, editor, edit summary, and a permanent link to the exact revision; follows redirects; the history companion to `summary`, `revisions`, and `revision_diff` |

All tools accept an optional `lang` parameter (default `en`; supported: `en`, `de`, `es`, `fr`, `ja`, `zh`, `pt`, `it`, `ru`, `nl`), except `media_search` — Wikimedia Commons is language-independent, so it takes no `lang`. Note: `quote` accepts the parameter for API consistency but is currently English-only (curated list).

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

(Requires Python 3.10+ and `requests>=2.28.0`)

### 2. Find your install path

The MCP server lives at `<install-dir>/src/server.py`.

```bash
ls ~/.openclaw/workspace/skills/wikipedia/src/server.py
```

### 3. Add to mcporter

Add to `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "python3",
      "args": ["<path-to>/src/server.py"]
    }
  }
}
```

Replace `<path-to>` with the actual install location from step 2.

### 4. Test

```bash
mcporter call wikipedia search --args '{"query": "velociraptor", "limit": 5}'
```

## Usage Examples

```
mcporter call wikipedia search --args '{"query": "velociraptor", "limit": 5}'
mcporter call wikipedia summary --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia dino_fact --args '{"species": "Spinosaurus"}'
mcporter call wikipedia dino_fact
mcporter call wikipedia did_you_know
mcporter call wikipedia featured_article
mcporter call wikipedia picture_of_the_day
mcporter call wikipedia picture_of_the_day --args '{"date": "20260901"}'
mcporter call wikipedia media_of_the_day
mcporter call wikipedia media_of_the_day --args '{"date": "20260830"}'
mcporter call wikipedia article_extract --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia article_sections --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia section_text --args '{"title": "Tyrannosaurus", "section": "Description"}'
mcporter call wikipedia section_text --args '{"title": "Tyrannosaurus", "section": 3}'
mcporter call wikipedia on_this_day
mcporter call wikipedia on_this_day --args '{"count": 8}'
mcporter call wikipedia deaths_on_this_day
mcporter call wikipedia deaths_on_this_day --args '{"count": 6}'
mcporter call wikipedia births_on_this_day
mcporter call wikipedia births_on_this_day --args '{"count": 6}'
mcporter call wikipedia categories --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia categories --args '{"title": "Tyrannosaurus", "limit": 10}'
mcporter call wikipedia links --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia links --args '{"title": "Tyrannosaurus", "limit": 30}'
mcporter call wikipedia backlinks --args '{"title": "Velociraptor"}'
mcporter call wikipedia backlinks --args '{"title": "Velociraptor", "limit": 30}'
mcporter call wikipedia nearby --args '{"title": "Eiffel Tower"}'
mcporter call wikipedia nearby --args '{"lat": 40.7484, "lon": -73.9857, "radius": 2000}'
mcporter call wikipedia translations --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia translations --args '{"title": "Tyrannosaurus", "limit": 10}'
mcporter call wikipedia revisions --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia revisions --args '{"title": "Tyrannosaurus", "limit": 20}'
mcporter call wikipedia revision_diff --args '{"title": "Python_(programming_language)", "rev_from": 1374673264, "rev_to": 1374673393}'
mcporter call wikipedia pageviews --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia pageviews --args '{"title": "Python_(programming_language)", "start": "20250101", "end": "20250107"}'
mcporter call wikipedia news
mcporter call wikipedia news --args '{"limit": 8}'
mcporter call wikipedia top_reads
mcporter call wikipedia top_reads --args '{"date": "20260101", "limit": 15}'
mcporter call wikipedia image --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia media_list --args '{"title": "Tyrannosaurus"}'
mcporter call wikipedia media_list --args '{"title": "Tyrannosaurus", "limit": 50}'
mcporter call wikipedia media_search --args '{"query": "aurora borealis"}'
mcporter call wikipedia media_search --args '{"query": "volcano eruption", "filetype": "video", "limit": 5}'
mcporter call wikipedia related_articles --args '{"title": "Velociraptor"}'
mcporter call wikipedia related_articles --args '{"title": "Velociraptor", "limit": 10}'
mcporter call wikipedia contributors --args '{"title": "Albert Einstein"}'
mcporter call wikipedia references --args '{"title": "Albert Einstein"}'
mcporter call wikipedia references --args '{"title": "Velociraptor", "limit": 10}'
mcporter call wikipedia quote
mcporter call wikipedia infobox --args '{"title": "Albert Einstein"}'
mcporter call wikipedia simple_summary --args '{"title": "Photosynthesis"}'
mcporter call wikipedia summary --args '{"title": "Berlin", "lang": "de"}'
```

## Data Source

Uses Wikipedia's free public REST API — no API key required.

- Search: MediaWiki Action API
- External links: MediaWiki Action API (`prop=extlinks`)
- Infobox: MediaWiki Action API (`action=parse` + `prop=wikitext`), with local wikitext parsing (no new dependencies)
- References: MediaWiki Action API (`action=parse` + `prop=text`), extracting the rendered `<ol class="references">` citation list (no new dependencies)
- Summary / Random / Featured / Picture of the Day: REST API v1 (`/api/rest_v1/...`)
- Media of the Day: MediaWiki Action API on Commons (date-stamped `Template:Motd/YYYY-MM-DD` + `imageinfo` metadata)
- Related articles: MediaWiki Action API (search generator with `morelike:` scoring)

## Notes

- User-Agent is `wikipedia-mcp/1.1.24` per Wikipedia API etiquette
- All responses include links back to the source article
- `dino_fact` falls back to a random species if the requested one isn't found (instead of erroring)
- `featured_article` returns today's curated Featured Article — great for daily content hooks
- `picture_of_the_day` returns Wikimedia Commons' Picture of the Day from Wikipedia's featured feed — the visual counterpart to `featured_article`. Accepts an optional `date` (YYYYMMDD, default today UTC) to browse past pictures. Returns the embedded thumbnail preview, file name, photographer/artist, license, description, and links to the full-size image + Commons file page. `image`/`media_list` cover article-specific media; this covers the editorially curated daily pick.
- `media_of_the_day` returns Wikimedia Commons' Media of the Day — the curated daily video or audio clip, the motion-and-sound counterpart to `picture_of_the_day`. Accepts an optional `date` (YYYYMMDD, default today UTC) to browse past picks; some dates have no Media of the Day and return a clear message. Returns the media kind, duration, a preview thumbnail (video) or listen link (audio), file name, artist, license, description, and links to the direct file + Commons file page.
- `article_extract` returns the full plain-text article (vs `summary`'s short extract + thumbnail) — use when you need more than a summary
- `article_sections` returns the article's table of contents — section number, heading text, and nesting level — so callers can navigate long articles (50KB+ body) by picking the section they want before committing to `article_extract`. Pairs with `summary` (lead), `article_sections` (structure), `article_extract` (full body).
- `section_text` reads a single article section as plain text — the follow-up to `article_sections`: pass a 1-based section number (0 = lead/intro), a hierarchical number like `2.1`, or a heading name (case-insensitive, with close-match suggestions on typos). Strips inline CSS, citation markers, and edit links while keeping paragraph structure; the link at the bottom deep-links to the section. Use it instead of `article_extract` when you only need one part of a long article.
- `on_this_day` returns historical events for today's UTC date from Wikipedia's "On This Day" feed — pairs with featured_article for daily "today in history" content hooks
- `deaths_on_this_day` returns notable deaths for today's UTC date — the deaths-only companion to `on_this_day`. Pairs with `on_this_day` (events) and `featured_article` (today's long-form) for a full "today in Wikipedia" daily digest. Useful for "in memoriam" content hooks and obituary-style social posts.
- `births_on_this_day` returns notable births for today's UTC date — the births companion to `on_this_day` (events) and `deaths_on_this_day` (deaths), completing the "today in Wikipedia" trio. Useful for "born on this day" content hooks and birthday round-ups.
- `categories` returns Wikipedia categories for an article (hidden/maintenance categories filtered) — useful for taxonomy-based discovery beyond text search
- `links` returns the article's outgoing Wikipedia links (main namespace only) — graph-style discovery showing which genera, people, and concepts an article references
- `backlinks` returns the article's incoming Wikipedia links (what links here) — the inverse of `links`. Shows which other articles reference this one (cultural mentions, scientific citations, comparative anatomy pages, etc.). Same main-namespace filtering.
- `nearby` returns Wikipedia articles geographically near a location, with distances — location-based discovery. Anchor by article title (e.g. 'Eiffel Tower', uses that article's coordinates so no geocoding service is needed) or by explicit lat/lon. Radius in meters (default 1000, max 10000), main-namespace only. Useful for travel research and "what's notable around here" questions.
- `translations` returns all language editions of an article (langlinks) — the other-language titles that Wikipedia knows about. Complements the one-way `lang` parameter used by other tools: every tool can query a single language, but only `translations` reveals the article's full language coverage so callers can pick a target language to fetch next. Useful for translation research (full coverage vs. stub languages), cross-language content sourcing, and language-coverage analysis.
- `pageviews` returns daily view counts for an article over a date range (default last 7 days) — popularity research, trending topics, historical interest spikes. Uses Wikimedia's pageviews REST API.
- `news` returns today's editorially-curated current events from Wikipedia's Main Page "In the news" block — pairs with featured_article (today's long-form) and on_this_day (historical) for a full "today in Wikipedia" content hook
- `top_reads` returns the most-viewed articles on Wikipedia for a given date (default yesterday UTC) — answers "what is everyone reading right now" while `pageviews` answers "how is this specific article trending". Filters out Main_Page, Special:Search, Portal:Current_events, etc. so the result is real articles only.
- `image` returns the article's lead image as URLs (300px thumbnail + full-size original) without summary prose — useful for embedding the image elsewhere (cards, slide decks, Telegram hero images). `summary` embeds the thumbnail inline; `image` exposes both URLs separately.
- `media_list` returns every media item (images, videos, audio) the article uses — not just the lead thumbnail. Each entry has file title, type, caption, and thumbnail URL; lead media is marked with 🏆 so callers can skip it when they already have it via `image`. Uses Wikipedia's REST `/page/media-list` endpoint (structured JSON, no HTML parsing). Pairs with `image` (lead only) — use `image` for the headline thumbnail, `media_list` for the full inventory (gallery generation, fact-checking, slide decks, audits).
- `media_search` is the topic-based counterpart to `image`/`media_list`: full-text search across Wikimedia Commons' File: namespace by keyword, so you can find freely-licensed media for a topic with no article yet (blog posts, slide decks, README hero images). Each result has file title, media type + dimensions, 320px thumbnail and full-size URLs, license short name, artist, description snippet, and a Commons file-page link. `filetype` filters to `image` (default: photos + diagrams/SVGs), `video`, `audio`, or `all`; limit clamps to 50. Uses the read-only Commons action API (generator=search) — GET-only, no new dependencies. Language-independent, so no `lang` parameter.
- `infobox` returns the article's structured fact box as a markdown field/value table — the fastest path to a concrete fact ("who founded X?", "population of Y?") without reading prose. Parses raw wikitext from the read-only parse API locally (balanced-brace template extraction, no new dependencies): wikilinks flatten to plain text, citations/HTML are stripped, nested templates collapse to their values, birth/death-date templates render as `YYYY-M-D`. Fields capped at 50, values at 400 chars. Reports clearly when an article has no infobox. Pairs with `summary` (prose gist) and `article_extract` (full text) — use `infobox` for facts, the others for narrative.
- `article_quality` returns Wikipedia's quality assessments for an article — the WikiProject grades (FA/FL featured, A, GA good, B, C, Start, Stub) plus importance ratings, with an overall class (best grade assigned) and per-project table. The encyclopedia's own trust signal: check it before relying on an article (GA/FA passed formal review; a Stub is a skeleton). Read-only pageassessments action API, no new dependencies. Note: assessment is only enabled on some language editions (en works; e.g. de reports no data).
- `related_articles` returns articles Wikipedia's own search engine judges most similar to a given title (MoreLikeThis scoring over article text and link structure) — the "what should I read next" discovery tool. Unlike `links` (raw outgoing links on the page) or `categories` (shared topic buckets), this is a similarity ranking: given "Velociraptor", expect dromaeosaurids, feathered dinosaurs, and "Deinonychus". Each entry shows the short description and a thumbnail; the source article itself is excluded. Read-only action API search generator, no new dependencies.
- `contributors` answers "who writes this article" — the most active recent editors. It tallies up to 500 recent revisions (read-only action API, GET only, no new dependencies) into a ranked table: top named editors by edit count with their share of sampled edits and user-page links, plus the anonymous (IP) edit share, and the sampled date span. A provenance companion to `article_quality` (the grade earned) and `revisions` (the raw log): a page tended by veteran caretakers reads differently from one mostly touched by drive-by IP edits, and the top names are who to credit — or to check for conflicts of interest. Follows redirects; limit clamps to 20.
- `references` answers "what does this article cite" — the article's bibliography. It reads the rendered reference list from the read-only parse API (GET only, no new dependencies): each citation's cleaned text plus the off-wiki URLs it points to (DOI, publisher, archive, primary-source links), with internal wikipedia.org/wikimedia.org links filtered out. Backlink markers (^ a b c / ↑) are stripped and long citations truncated at 420 chars. The verification companion to `external_links` (which dumps every off-wiki link on the page, including templates): `references` returns only the sources actually cited — the bibliography you'd hand to a fact-checker. Pairs with `article_quality` (trust signal) and `contributors` (who wrote it) for a full "can I rely on this article?" audit. Reports clearly when an article has no reference list. Follows redirects; limit clamps to 50.
- `revision_diff` answers "what did this edit actually change" — give it two revision IDs (from `revisions`) and it returns a plain-text unified diff of the article's wikitext between them, each side labelled with timestamp, editor, and edit summary, plus a link to the on-wiki side-by-side view. Fetches both revisions in one read-only action API call and diffs locally with stdlib difflib (no new dependencies); `limit` clamps diff lines (default 100, max 500). The edit-auditing companion to `revisions` (the log): review edits before trusting a new paragraph, audit what a breaking-news change removed, spot stealth rewrites.
- `disambiguation` answers "which article did you mean" — given an ambiguous title like 'Mercury' or 'Apple', it verifies the disambiguation marker via pageprops and returns the page's own option list (article title + one-line description), grouped by section (e.g. Companies, Film and television), main-namespace links only. Reports clearly when the title is a regular article (use `summary` instead) or doesn't exist. The disambiguation companion to `search`: call this when `search`/`summary` land on an ambiguous page, pick the right candidate, then fetch it with `summary` or `article_extract`; `limit` clamps options (default 30, max 100).
- `user_contribs` answers "what has this editor been doing" — the reverse angle of `contributors` (which profiles an *article's* editors): given a username or IP address, it shows their latest edits across the encyclopedia via the read-only `list=usercontribs` action API. Each entry shows the page link, timestamp, byte-size delta, edit comment, diff link, and flags for new pages, minor edits, and edits still current. The header reports the account's registration date and lifetime edit count (or states plainly when the name has no registered account — an IP can still have contributions). Use it to profile a top contributor surfaced by `contributors`, audit an anonymous IP's activity, or spot single-purpose accounts whose edits are confined to one topic (a conflict-of-interest tell). `namespace` scopes the search (default 0 = articles); limit clamps to 50.
- `simple_summary` answers "explain it simply" — it fetches the same topic from Simple English Wikipedia (simple.wikipedia.org), where articles are rewritten in short sentences with common words, and renders it in the same title + summary + thumbnail + read-more shape as `summary`. The accessibility companion to `summary`/`article_extract`: reach for it for kids, ESL readers, or a quick low-jargon intuition of a dense topic, then graduate to `summary` for the full article. Reports clearly when no Simple English article exists for the topic. No `lang` parameter — Simple English is its own wiki.
- `citation_needed` answers "which claims lack a source" — the flip side of `references` (which lists what an article cites): it finds statements Wikipedia editors have flagged with {{citation needed}} tags. Two angles: pass `article` to scan that article's wikitext via the read-only parse API and extract each tagged sentence with its tag date (wiki markup stripped, section headers and reference tags removed), or pass `topic` (or neither) to run a read-only `insource:"citation needed"` search returning tagged articles with the flagged claim's snippet. Use it to find sourcing work as an editor, or to spot the shakiest claims in a topic you're researching. Reports clearly when an article has no tags or doesn't exist; `article` takes precedence when both are given; limit clamps to 25. Tag-name matching is English-Wikipedia-centric (`lang` accepted for API consistency).
- `talk` answers "what are editors discussing" — the behind-the-scenes view of an article. It reads the article's Talk: page wikitext via the read-only action API (GET only, no new dependencies), splits it into discussion threads, and returns the most recently active ones: each thread's heading, last-activity timestamp, signed-comment count, and an excerpt of the latest comment (wiki markup stripped, closed-thread banners removed). Automated maintenance notices (redirect/deletion discussions) are filtered out; unsigned template-only pages report clearly. Use it to find controversies, open questions, and editorial disputes — the discussion companion to `contributors` (who edits) and `article_quality` (how the article is graded) for a full "can I rely on this article?" audit. Follows talk-page redirects; limit clamps to 15. Talk-page conventions are English-centric (`lang` accepted for API consistency).
- `article_flags` answers "what do editors think is wrong with this article" — the warning labels. It reads the article's wikitext via the read-only parse API (GET only, no new dependencies) and matches maintenance-banner templates against a curated English list (POV, Original research, Unreferenced, More citations needed, Cleanup, Disputed, Fringe theories, Notability, Conflict of interest, Outdated, and ~40 more, including section-scoped variants like `{{POV section}}`). Each flag shows its tag date, its location (article top or section heading), and a plain-language meaning; the `{{Multiple issues}}` wrapper is unpacked into its individual flags, and non-editorial templates (infoboxes, citation formats, date styles) never leak in. Reports clearly when an article carries no flags. The trust-signal companion to `article_quality` (the grade), `citation_needed` (unsourced claims), and `talk` (editor discussion) for a full "can I rely on this article?" audit. Banner names are English-Wikipedia-centric (`lang` accepted for API consistency); limit clamps to 25.
- `citation_sources` answers "where does this article's evidence come from" — the diversity lens on the bibliography. It reads the article's rendered reference list via the read-only parse API (GET only, no new dependencies), groups every off-wiki link by registrable domain (so `news.bbc.co.uk` and `www.bbc.co.uk` both count as `bbc.co.uk`, via a hand-curated multi-level-suffix list — no public-suffix dependency), and returns a ranked publisher table with each domain's citation count and share of linked references, capped by a plain-language verdict: diverse / balanced / top-heavy / lopsided / thin. Also reports the share of citations with a Wayback Machine / archive.org copy (link-rot insurance) and the share pointing at DOI-linked scholarly works. The companion to `references` (which lists the full bibliography) for the "can I rely on this article?" audit, alongside `article_quality` (the grade), `article_flags` (editorial warnings), and `citation_needed` (unsourced claims). Follows redirects; limit clamps to 30 domains. Reports clearly when an article has no references or none link off-wiki.
- `article_path` answers "how do these two articles connect" — the six-degrees game. Given `start` and `target` titles, it searches Wikipedia's link graph for the shortest chain of blue links between them (e.g. Banana → Africa → Anatolia → Trojan War), using only read-only action API GETs (no new dependencies): 1 hop checks a direct link, 2 hops intersects the start's outgoing links with the pages linking to the target (every middle found is a real start → middle → target path), and 3 hops expands a bounded sample of the start's links (max 25 pages, 500 links each) looking for one landing on a page that links to the target. Follows redirects (so "USA" → "United States" is 0 hops) and reports exactly what was scanned. The discovery companion to `links` (raw outgoing links) and `backlinks` (every page linking in): play six-degrees, trace how topics connect, or find the surprising middle article bridging two distant subjects. `max_hops` clamps to 1–3 (default 2); reports clearly when no path is found within the budget.
- `article_at_date` answers "what did this article say on that date" — the time machine. Given a title and a YYYY-MM-DD date, it finds the latest surviving revision at or before the end of that day via the read-only action API (`rvstart` + `rvdir=older`), then reads that revision's clean lead text through TextExtracts (no infobox/navbox noise), returning it with the revision ID, timestamp, editor, edit summary, and a permanent link to the exact revision. Reports clearly when the article didn't exist yet (naming its first surviving revision), when the title doesn't exist, or when the date isn't YYYY-MM-DD. Follows redirects. The history companion to `summary` (the article as it reads now), `revisions` (the raw edit log), and `revision_diff` (what changed between two revisions): see what an article claimed before an event, or how a lead evolved.
- Multi-language: pass `lang` to any tool to query de/es/fr/ja/zh/pt/it/ru/nl Wikipedia

## ClawHub

This skill is published on ClawHub as **Wikipedia** under the canonical slug `wikipedia` (1.6k+ downloads, 40 installs as of Aug 20 2026).

Do **NOT** publish to slug `wikipedia-mcp` — that is the abandoned duplicate skill (140 DL, 0 installs, lowercase "wikipedia" display name).

GitHub source: https://github.com/evanfoglia/wikipedia-mcp