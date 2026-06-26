---
name: xfetch
description: Use xfetch CLI to fetch X/Twitter data - tweets, user profiles, search results, timelines, lists, DMs, and notifications. Use this skill whenever you need to retrieve any data from X/Twitter, whether the user asks to "get tweets", "look up a Twitter user", "search X for...", "check my timeline", "fetch bookmarks", "read DMs", or any variation involving X/Twitter data retrieval. Also use when the user pastes a tweet URL and wants its content, or asks to export Twitter data to CSV/JSON/SQLite.
---

# xfetch - X/Twitter CLI Data Fetcher

xfetch is a cookie-based X/Twitter scraper CLI. It requires no API keys - just browser cookies for authentication. It's installed globally as `xfetch` (or can be run via `npx @lxgic/xfetch` / `bunx @lxgic/xfetch`).

## Prerequisites

Authentication must be set up first. Check with:

```bash
xfetch auth check
```

If not authenticated, extract cookies from the user's browser:

```bash
xfetch auth extract --browser chrome          # or firefox, safari, arc, brave
xfetch auth extract --browser chrome --profile "Profile 1"  # specific profile
```

Or set tokens directly:

```bash
xfetch auth set --auth-token <token> --ct0 <token>
```

## Command Reference

### Single Tweet

Accepts a tweet URL or numeric ID:

```bash
xfetch tweet https://x.com/user/status/123456789
xfetch tweet 123456789
```

Also works with X Article URLs (`/article/ID`).

### User Profile

```bash
xfetch user @handle        # by handle (@ is optional)
xfetch user 12345678       # by numeric ID
```

### User Tweets

```bash
xfetch tweets @handle                     # latest 20 tweets
xfetch tweets @handle -n 50              # 50 per page
xfetch tweets @handle --replies           # include replies
xfetch tweets @handle --all              # all pages (paginated)
xfetch tweets @handle --max-pages 5      # limit to 5 pages
```

### Thread / Conversation

```bash
xfetch thread <url-or-id>    # full conversation thread
```

### Search

```bash
xfetch search "query"                          # top results
xfetch search "query" --type latest            # latest tweets
xfetch search "query" --type people            # user results
xfetch search "query" --type photos            # photo tweets
xfetch search "query" --type videos            # video tweets
xfetch search "from:handle since:2024-01-01"   # advanced operators
xfetch search "query" -n 100 --all             # all pages
```

Search types: `top` (default), `latest`, `people`, `photos`, `videos`.

### Timelines

```bash
xfetch home                    # algorithmic home timeline
xfetch home --following        # chronological (following only)
xfetch bookmarks               # your bookmarks
xfetch likes @handle           # user's liked tweets
```

### Followers / Following

```bash
xfetch followers @handle -n 100
xfetch following @handle -n 100
```

### Lists

```bash
xfetch lists @handle                        # user's lists
xfetch list <list-id-or-url>                # list details
xfetch list-members <list-id-or-url>        # list members
xfetch list-tweets <list-id-or-url> -n 50   # list timeline
```

### Direct Messages

```bash
xfetch dms                                  # inbox overview
xfetch dms inbox                            # same as above
xfetch dms conversation <conversation_id>   # messages in a conversation
xfetch dms <conversation_id>                # shortcut for above
```

### Notifications

```bash
xfetch notifications                  # all notifications
xfetch mentions                       # mentions only
xfetch verified-notifications         # from verified accounts
```

### Auth Management

```bash
xfetch auth check                             # show auth status
xfetch auth extract --browser chrome          # extract cookies
xfetch auth set --auth-token <t> --ct0 <t>    # set tokens manually
xfetch auth clear                             # clear saved auth
xfetch auth browsers                          # list available browsers + profiles
```

### Query ID Management

```bash
xfetch query-ids --refresh    # fetch latest query IDs from X frontend
xfetch query-ids --list       # show cached query IDs
```

## Pagination Options

All list-like commands (`tweets`, `search`, `followers`, `following`, `likes`, `bookmarks`, `home`, `notifications`, `mentions`, `list-members`, `list-tweets`, `dms inbox`, `dms conversation`) support these pagination options:

| Flag | Description |
|------|-------------|
| `-n, --count <N>` | Results per page (default: 20) |
| `--all` | Fetch all available pages |
| `--max-pages <N>` | Maximum number of pages to fetch |
| `--cursor <cursor>` | Resume from a specific cursor |
| `--resume <file>` | Save/restore cursor state to a file |
| `--delay <ms>` | Delay between page requests (default: 1000ms) |

## Output Formats

Control output with `--format`:

```bash
xfetch tweets @handle --format json      # pretty-printed JSON (default)
xfetch tweets @handle --format jsonl     # newline-delimited JSON (streaming)
xfetch tweets @handle --format csv       # CSV with headers
xfetch tweets @handle --format sqlite --db tweets.db   # SQLite database
```

Additional output flags:
- `--json` — shorthand for `--format json`
- `--plain` — disable pretty printing

Pipe to files with shell redirection:
```bash
xfetch tweets @handle -n 100 --format csv > tweets.csv
xfetch search "AI" --all --format jsonl > results.jsonl
```

## Global Options

These can be passed to any command:

| Flag | Description |
|------|-------------|
| `--auth-token <token>` | Override auth_token cookie |
| `--ct0 <token>` | Override ct0 cookie |
| `--cookie-source <src>` | Cookie source browser |
| `--chrome-profile <name>` | Chrome profile name |
| `--proxy <url>` | Proxy URL (`http://user:pass@host:port`) |
| `--proxy-file <path>` | File with proxy URLs for rotation |
| `--timeout <ms>` | Request timeout (default: 30000) |
| `--delay <ms>` | Delay between requests (default: 500) |
| `--no-color` | Disable colored output |

## Tips for Effective Use

- When fetching large datasets, prefer `--format jsonl` for streaming output (avoids buffering entire result set in memory).
- Use `--max-pages` instead of `--all` when you only need a sample — it's faster and avoids rate limits.
- If a request fails with a 404 or query ID error, try `xfetch query-ids --refresh` to update cached query IDs — X periodically rotates these.
- Pipe JSON output through `jq` for filtering: `xfetch tweets @handle | jq '.[].text'`
- For SQLite output, always specify `--db`: `xfetch tweets @handle --format sqlite --db data.db`
- Rate limits are handled internally with jitter, but high-volume scraping benefits from `--delay 2000` or higher.
