---
name: x
description: "Use when the user wants to collect tweets, search Twitter/X, get tweet details, set up site-use, or browse cached posts. Examples: 'set up site-use', 'grab latest tweets', 'search Twitter for AI news', 'get replies to this tweet'"
metadata: { "openclaw": { "emoji": "🌐", "homepage": "https://github.com/WilliamPenrose/site-use", "requires": { "bins": ["site-use"] }, "install": [{ "kind": "node", "package": "site-use", "bins": ["site-use"] }] } }
---

# Twitter/X — site-use skill

## Scope

Only use `site-use` commands listed below.
Do not use puppeteer, chrome-devtools-mcp, or any other browser automation tool directly.

## First-time setup

When the user asks to set up site-use or you get a `BrowserNotRunning` error on first use:

1. Run `site-use browser launch` to start Chrome
2. Tell the user to log in to Twitter in the Chrome window that opened
3. Wait for the user to confirm they've logged in
4. Run `site-use twitter check-login` to verify
5. If logged in, run `site-use twitter feed --count 10 --fields author,text,url` to collect the first batch

The launched Chrome uses an isolated profile — the user's regular browser data is never exposed.

## When to use which command

| Need | Command |
|------|---------|
| Latest timeline | `site-use twitter feed` |
| Search Twitter | `site-use twitter search` |
| Specific tweet + replies | `site-use twitter tweet_detail` |
| Query cached data | `site-use search` |

## Intent Freshness

Determine whether to fetch fresh data or use cache based on the user's intent.

| Freshness | Signal | Example intents | Strategy |
|-----------|--------|-----------------|----------|
| **High** | User explicitly asks for "now/today/latest/trending/breaking" | "what's trending", "latest news on X" | Always `--fetch` |
| **Medium** | No explicit time, but topic is time-sensitive | "any updates on Claude Code", "what happened with the outage" | Prefer `--fetch` |
| **Low** | Retrospective or analysis, references past time | "analyze last week's AI discussions", "what did we collect yesterday" | `--local` or default cache |

**Default:** When freshness is ambiguous, prefer fetch. The cost of missing breaking news outweighs an extra fetch.

## Commands

### twitter feed

Collect tweets from the home timeline. Results are auto-stored in the local knowledge base.

```
site-use twitter feed [options]
  --count <n>          Number of tweets, 1-100 (default: 20)
  --tab <name>         following | for_you (default: for_you)
  --local              Force local cache query (no browser)
  --fetch              Force fetch from browser (skip freshness check)
  --max-age <minutes>  Max cache age before auto-fetching (default: 120)
  --fields <list>      Comma-separated: author,text,url,timestamp,links,mentions,media
  --quiet, -q          Suppress JSON output, show one-line summary only
  --debug              Include diagnostic trace
```

- **`for_you`** — algorithmic feed, personalized recommendations
- **`following`** — chronological, only accounts the user follows

Just run `twitter feed` directly — the framework auto-checks login. If the user isn't logged in, you'll get a `SessionExpired` error with a clear hint.

### twitter search

Search tweets on Twitter. Supports Twitter search operators.

```
site-use twitter search [options]
  --query <text>       Search query (required, supports Twitter operators)
  --tab <name>         top | latest (default: top)
  --count <n>          Number of tweets, 1-100 (default: 20)
  --fields <list>      Comma-separated: author,text,url,timestamp,links,mentions,media
  --quiet, -q          Suppress JSON output, show one-line summary only
  --debug              Include diagnostic trace
```

### twitter tweet_detail

Get a specific tweet and its replies.

```
site-use twitter tweet_detail [options]
  --url <url>          Tweet URL (required)
  --count <n>          Max replies, 1-100 (default: 20)
  --fields <list>      Comma-separated: author,text,url,timestamp,links,mentions,media
  --quiet, -q          Suppress JSON output, show one-line summary only
  --debug              Include diagnostic trace
```

Returns JSON with `items[0]` as the anchor tweet, `items[1..n]` as replies. Each reply has `siteMeta.inReplyTo` for threading. Quoted tweets are nested under `siteMeta.quotedTweet`.

### twitter check-login

```
site-use twitter check-login
```

No options. Returns `{ loggedIn: boolean }`. Reserve for when the user explicitly asks about login status — `twitter feed` auto-checks login already.

### search (local knowledge base)

Query the local knowledge base. Does NOT fetch new data.

```
site-use search [query] [options]

Filters:
  --author <name>         Filter by author (@ prefix optional)
  --start-date <date>     Start date (local time, flexible format)
  --end-date <date>       End date (local time, flexible format)
  --hashtag <tag>         Filter by hashtag
  --mention <handle>      Filter by mentioned handle (@ prefix optional)
  --surface-reason <r>    original | retweet | quote | reply
  --min-likes <n>         Minimum likes
  --min-retweets <n>      Minimum retweets

Output:
  --max-results <n>       Max results (default: 20)
  --fields <list>         Comma-separated: author,text,url,timestamp,links,mentions,media
```

### Browser management

```bash
site-use browser launch     # Launch Chrome (detached)
site-use browser status     # Show connection status
site-use browser close      # Kill Chrome and clean up
```

### Screenshots

```bash
site-use screenshot --site twitter
# Returns: {"screenshot": "~/.site-use/screenshots/twitter.png"}
```

Then use the Read tool to view the image file.

### Stats

```bash
site-use stats              # Show storage statistics
```

## Smart Cache

`twitter feed` has smart caching (default 120 min):

| Flag | Behavior |
|------|----------|
| (none) | Check cache freshness; fetch if stale (> `--max-age`) |
| `--local` | Force local cache only — no browser needed |
| `--fetch` | Force fresh fetch — skip freshness check |
| `--max-age <min>` | Custom staleness threshold (default: 120) |

## Error Recovery

| Error | Action |
|-------|--------|
| **SessionExpired** | Ask the user to log in manually in Chrome, then retry |
| **RateLimited** | Stop ALL twitter commands. Wait 15+ min. Use `search` for cached data meanwhile |
| **BrowserDisconnected** | Run `site-use browser launch`, then retry |
| **BrowserNotRunning** | Run `site-use browser launch` first |
| **ElementNotFound** | Page may still be loading. Wait a few seconds, retry |

### Rate limiting deserves extra care

- Do not retry immediately. Wait for the reset time shown in the error.
- Do not run any twitter commands during cooldown — this can extend the limit.
- Switch to offline work — use `search` to analyze cached data.
- If "account suspended" appears, alert the user — this is a policy issue, not a quota issue.

## Examples

### Daily hot topics briefing (High freshness)

```bash
# 1. Fetch fresh timeline
site-use twitter feed --fetch --count 50 --tab for_you --fields author,text,url

# 2. Filter high-engagement posts from cache
site-use search --start-date "today" --min-likes 100 --fields author,text,url
```

User says "what's hot today" → freshness is high, always fetch first, then filter.

### Breaking news search (High freshness)

```bash
site-use twitter search --query "Claude Code" --count 30 --fields author,text,url
```

Topic is actively unfolding → always fetch. Do NOT rely on cache for breaking events.

### Retrospective analysis (Low freshness)

```bash
# Pure cache query, no browser needed
site-use search "AI agent" --start-date "2026-03-24" --end-date "2026-03-28" --min-likes 50 --fields author,text,url

# Or explicitly local
site-use twitter feed --local --tab for_you --fields author,text,url
```

User asks about past data → use cache. No reason to fetch.

## Time Convention

All timestamps are **local timezone ISO 8601** (e.g. `2026-03-29T10:03:00+08:00`). Date filters (`--start-date`, `--end-date`) accept flexible local formats — `"2026-03-29"`, `"yesterday"`, `"2026-03-29 10:00"` all work.

When the user doesn't specify a time range, default to the last 24 hours.

## Tips

- **Always use `--fields` to control output size.** Output exceeding ~30KB gets truncated to a temp file. Always pass `--fields author,text,url` (or whichever fields needed) to keep output compact.
- **Prefer `search` over re-fetching.** If tweets were collected recently, search the cache instead. Saves time and avoids rate limits.
- **Use `--local` for offline analysis.** When the browser isn't running or you want speed, `--local` reads from cache without touching the browser.
- **Use `--debug` when troubleshooting.** Adds diagnostic trace. On errors, trace is always included regardless of `--debug`.
- **Short search queries are slow.** Full-text search needs 3+ characters. Shorter queries fall back to a full table scan.
- **Combine filters for precision.** `search "AI" --min-likes 500 --start-date "yesterday"` is more useful than a broad search.
