# Sitemap Selection Reference

Use this reference when the user names a content class but the site exposes multiple sitemaps.

## Common Sitemap Hints

- `docs`, `documentation`, `manual`, `developer`, `api`: documentation content
- `kb`, `knowledge-base`, `help`, `support`, `hc`, `articles`: support and help-center content
- `blog`, `post`, `posts`, `news`, `insights`: blog or news content
- `academy`, `learn`, `education`, `courses`, `tutorials`, `guides`: educational content
- `changelog`, `release`, `updates`: release notes

## Scoped URL Inputs

When the user prompt includes a scoped URL like `https://example.com/docs`:

1. Run `discover_sitemaps.py` with the provided URL.
2. Read `scope_hint_substring` from discovery output.
3. Use that value as default `--include-substring` in `scrape_sitemap.py` unless the user asks for a broader or narrower scope.
4. If the hint conflicts with the chosen sitemap samples, ask the user which scope to prioritize.

## How To Decide

1. Prefer the sitemap name when it clearly matches the user request.
2. If the name is ambiguous, inspect `sample_urls` from `discover_sitemaps.py`.
3. If a sitemap mixes multiple sections, scrape with `--include-substring` and `--exclude-substring`.
4. If two sitemaps both fit, show both to the user and ask which one they want.

## Output Layout

`scrape_sitemap.py` writes:

- `manifest.json`: inventory of saved files, skipped URLs, and errors
- `pages/.../*.md`: one Markdown file per page

Each Markdown file contains:

- Page title
- Source URL
- Scraped timestamp
- Optional description
- Extracted body text

## When To Warn

- The page content is mostly empty or navigation-heavy.
- The site is heavily client-rendered and the saved Markdown lacks the visible article body.
- The chosen sitemap contains account, cart, or other non-public URLs.
- The target host is local or private-network scoped (`localhost`, RFC1918/private IPs, `.local`, `.internal`).
