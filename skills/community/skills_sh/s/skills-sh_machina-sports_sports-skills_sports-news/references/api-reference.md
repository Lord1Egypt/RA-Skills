# Sports News — API Reference

## Commands

### fetch_feed
Fetch an RSS/Atom feed by URL and return feed metadata plus recent entries.
- `url` (str, required): Full RSS/Atom feed URL

Returns feed title, last updated timestamp, and `entries[]` with title, link, published date, summary, and source.

### fetch_items
Fetch news items from Google News or an RSS feed.
- `google_news` (bool, optional): Set to `True` to use Google News search
- `query` (str, optional, **required when `google_news=True`**): Search query string
- `url` (str, optional): RSS/Atom feed URL (mutually exclusive with `google_news`)
- `limit` (int, optional): Max items to return
- `after` (str, optional): Filter items after this date (YYYY-MM-DD)
- `before` (str, optional): Filter items before this date (YYYY-MM-DD)
- `sort_by_date` (bool, optional): Sort results by date descending (newest first)

Returns `items[]` with title, link, published date, summary, and source.

**Important constraints:**
- `google_news=True` requires a `query` — without it, Google News has nothing to search.
- `url` and `google_news` are mutually exclusive — use one or the other, not both.
- Always use `sort_by_date=True` for recency queries to show newest articles first.

## Curated RSS Feed URLs

See `references/rss-feeds.md` for the full list of curated RSS feed URLs (BBC Sport, ESPN, The Athletic, Sky Sports, etc.).

## Date Handling

Derive dates from the system prompt's `currentDate`:
- **"this week"**: `after = today - 7 days`
- **"recent" or "latest"**: `after = today - 3 days`
- **Specific date range**: use as-is

Never hardcode dates — always derive from `currentDate`.
