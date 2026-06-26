---
name: rss-sitemap
description: Discover website URLs, feed entries, and latest publications by checking sitemap.xml, sitemaps.xml, atom.xml, and rss.xml before crawling a specific site. Use when Codex needs to find the most recent posts/articles/publications from a named website or domain, search, crawl, scrape, monitor, or enumerate site content, and should prefer the site's own sitemap, Atom feed, or RSS feed over blind link crawling.
metadata: '{"openclaw":{"requires":{"bins":["node"]}}}'
---

# RSS Sitemap

## Overview

Use this skill to bootstrap site discovery from the site's own machine-readable indexes before doing general crawling. For any task that targets a specific website, first look for sitemap, Atom, and RSS resources and use them to find the latest publications or guide the crawl.

## Workflow

1. Normalize the target site to an origin such as `https://example.com`.
2. Run the bundled preprocessor through the OpenClaw `exec` tool when Node.js 18+ is available. `exec` is the shell tool name; do not require a separate `bash` tool:
   ```bash
   node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --site https://example.com --output /tmp/rss-sitemap.json
   ```
3. Probe these root resources first when running manually:
   - `/sitemap.xml`
   - `/sitemaps.xml`
   - `/atom.xml`
   - `/rss.xml`
4. If available, also inspect `/robots.txt` for `Sitemap:` directives and include those sitemap URLs.
5. Fetch only resources that return a successful HTTP response and XML-like content.
6. Parse XML with a real parser when possible. Avoid ad hoc regex parsing except for quick triage.
7. Use discovered URLs or entries as the crawl frontier before falling back to regular page crawling.

## Bundled Tool

Use `scripts/preprocess-rss-sitemap.js` for deterministic pre-crawl discovery. It has no npm dependencies and uses Node's built-in `fetch`, so it requires Node.js 18 or newer for URL fetching.

Common commands:

```bash
node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --site https://example.com
node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --url https://example.com/sitemap.xml --url https://example.com/feed.xml
node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --file ./sitemap.xml --file ./feed.xml
node skills/rss-sitemap/scripts/preprocess-rss-sitemap.js --site https://example.com --max-depth 2 --output /tmp/rss-sitemap.json
```

The script outputs JSON with:

- `resources`: probed XML or robots resources, HTTP status, content type, detected kind, and entry count.
- `entries`: normalized sitemap URLs, RSS items, or Atom entries with source provenance.

For latest-publication requests, sort `entries` by the best available date:

1. RSS `pubDate`
2. Atom `updated`
3. Atom `published`
4. Sitemap `lastmod`

If entries do not include dates, prefer RSS or Atom feed order before sitemap order because feeds usually list newest content first.

If the script fails because the site blocks requests, needs JavaScript, or requires authentication, use the available web scraping/search/browser tools for fetching, then apply the same parsing and crawl strategy.

Required tools:

- OpenClaw `exec` enabled for host script execution.
- Node.js 18+ for remote URL discovery with the bundled script.
- Any available HTTP, scraping, search, or browser tool when Node fetch cannot access the target site.

## Parsing Rules

For sitemaps:

- Treat `<sitemapindex>` as a list of nested sitemaps; recursively fetch each `<loc>`.
- Treat `<urlset>` as crawlable page URLs; extract `<loc>` and keep useful metadata such as `<lastmod>`, `<changefreq>`, and `<priority>` when present.
- De-duplicate URLs after canonicalizing obvious variants such as fragments.

For RSS feeds:

- Extract each `<item>` with `title`, `link`, `guid`, `pubDate`, and `description` when present.
- Prefer `link` as the crawl URL; fall back to `guid` only if it is URL-like.

For Atom feeds:

- Extract each `<entry>` with `title`, `id`, `updated`, `published`, `summary`, and `link`.
- Prefer `<link rel="alternate" href="...">`; otherwise use the first URL-like `href`.

## Crawl Strategy

- Prefer newest or most relevant entries when the user asks for recent content.
- For "latest publications", "recent posts", "new articles", or equivalent requests, use RSS/Atom first and return dated entries in descending order when dates are available.
- Prefer sitemap URLs when the user asks for broad site coverage.
- Keep feed and sitemap provenance with each discovered URL so later summaries can explain where a URL came from.
- If none of the well-known resources exist, state that discovery fell back to normal crawling or search.
- Respect robots, rate limits, authentication boundaries, and user instructions before expanding a crawl.
