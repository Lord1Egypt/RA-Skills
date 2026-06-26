---
name: x-analytics-cli
description: >
  X (Twitter) analytics and data retrieval via x-analytics-cli.
  Use when the user wants to search tweets, count tweet volumes, look up user profiles, get tweet details,
  or pull a user's timeline from X (formerly Twitter).
  Triggers: "X analytics", "Twitter analytics", "tweet search", "tweet lookup", "tweet counts",
  "X user profile", "Twitter user", "tweet timeline", "X API", "Twitter API",
  "search tweets", "tweet volume", "trending tweets", "X data", "Twitter data".
---

# X Analytics CLI Skill

You have access to `x-analytics-cli`, a read-only CLI for the X API v2. Use it to search recent tweets, count tweet volumes over time, look up users and tweets by ID, and retrieve the authenticated user's timeline. All requests use OAuth 1.0a signing.

## Quick start

```bash
# Check if the CLI is available
x-analytics-cli --help

# Get the authenticated user's profile
x-analytics-cli me

# Search recent tweets
x-analytics-cli search "OpenAI"
```

If the CLI is not installed, install it:

```bash
npm install -g x-analytics-cli
```

## Authentication

The CLI requires four OAuth 1.0a credentials: API Key, API Secret, Access Token, and Access Token Secret. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variables: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`
3. Auto-detected file: `~/.config/x-analytics-cli/credentials.json`

The credentials JSON file must contain these four fields:

```json
{
  "api_key": "...",
  "api_secret": "...",
  "access_token": "...",
  "access_token_secret": "..."
}
```

API access tiers affect which commands are available:
- **Free tier** -- authenticated user lookup (`me`)
- **Basic or higher** -- tweet lookup (`tweet`, `tweets`), user lookup (`user`), search (`search`), tweet counts (`tweet-counts`), timelines (`timeline`)

Before running any command, verify credentials are configured by running `x-analytics-cli me`. If it fails with a credentials error, ask the user to set up authentication.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping). The only valid format values are `json` (default) and `compact`.

Errors are written to stderr as JSON with an `error` field and a non-zero exit code, e.g. `{"error": "Unauthorized - Invalid or expired token"}`.

The response shape follows the X API v2 convention: `data` (primary results), `includes` (expanded objects), and `meta` (pagination info). Not all fields are present in every response.

## Commands reference

### User lookup

#### me

Get the authenticated user's profile.

```bash
x-analytics-cli me
x-analytics-cli me --user-fields public_metrics,description,created_at
x-analytics-cli me --expansions pinned_tweet_id --tweet-fields created_at,public_metrics
```

Options:
- `--user-fields <fields>` -- user fields to include
- `--expansions <expansions>` -- expansions to include
- `--tweet-fields <fields>` -- tweet fields to include (useful with expansions)

#### user

Get a user by username or numeric ID. Accepts usernames with or without the leading `@`. Numeric IDs are auto-detected and routed to the ID-based endpoint.

```bash
x-analytics-cli user elonmusk
x-analytics-cli user @elonmusk
x-analytics-cli user 44196397
x-analytics-cli user elonmusk --user-fields public_metrics,description,created_at
x-analytics-cli user elonmusk --expansions pinned_tweet_id --tweet-fields text
```

Options:
- `--user-fields <fields>` -- user fields to include
- `--expansions <expansions>` -- expansions to include
- `--tweet-fields <fields>` -- tweet fields to include (useful with expansions)

### Tweet lookup

#### tweet

Get a single tweet by ID.

```bash
x-analytics-cli tweet 1234567890
x-analytics-cli tweet 1234567890 --tweet-fields public_metrics,created_at,author_id
x-analytics-cli tweet 1234567890 --expansions author_id --user-fields username,name
```

Options:
- `--tweet-fields <fields>` -- tweet fields to include
- `--expansions <expansions>` -- expansions to include
- `--user-fields <fields>` -- user fields to include
- `--media-fields <fields>` -- media fields to include
- `--place-fields <fields>` -- place fields to include
- `--poll-fields <fields>` -- poll fields to include

#### tweets

Get multiple tweets by IDs (comma-separated).

```bash
x-analytics-cli tweets 1234567890,9876543210
x-analytics-cli tweets 1234567890,9876543210 --tweet-fields public_metrics,created_at
x-analytics-cli tweets 1234567890,9876543210 --expansions author_id --user-fields username,name
```

Options:
- `--tweet-fields <fields>` -- tweet fields to include
- `--expansions <expansions>` -- expansions to include
- `--user-fields <fields>` -- user fields to include
- `--media-fields <fields>` -- media fields to include
- `--place-fields <fields>` -- place fields to include
- `--poll-fields <fields>` -- poll fields to include

### Search

#### search

Search recent tweets (last 7 days). Requires Basic API access or higher.

```bash
x-analytics-cli search "from:elonmusk"
x-analytics-cli search "OpenAI" --max-results 50 --sort-order relevancy
x-analytics-cli search "#AI" --start-time 2026-03-10T00:00:00Z --end-time 2026-03-17T00:00:00Z
x-analytics-cli search "lang:en bitcoin" --tweet-fields public_metrics,created_at,author_id --expansions author_id --user-fields username
```

Options:
- `--max-results <n>` -- max results, 10-100
- `--start-time <time>` -- ISO 8601 start time
- `--end-time <time>` -- ISO 8601 end time
- `--sort-order <order>` -- `recency` or `relevancy`
- `--next-token <token>` -- pagination token from `meta.next_token` in the response
- `--tweet-fields <fields>` -- tweet fields to include
- `--expansions <expansions>` -- expansions to include
- `--user-fields <fields>` -- user fields to include
- `--media-fields <fields>` -- media fields to include
- `--place-fields <fields>` -- place fields to include
- `--poll-fields <fields>` -- poll fields to include

Supports the full X API v2 search query syntax: `from:`, `to:`, `is:retweet`, `has:media`, `lang:`, hashtags, mentions, boolean operators (`OR`, `-`), and more.

#### tweet-counts

Get tweet counts for a search query over time (last 7 days). Requires Basic API access or higher.

```bash
x-analytics-cli tweet-counts "OpenAI"
x-analytics-cli tweet-counts "#AI" --granularity hour
x-analytics-cli tweet-counts "from:elonmusk" --granularity day --start-time 2026-03-01T00:00:00Z
x-analytics-cli tweet-counts "bitcoin OR ethereum" --granularity minute --start-time 2026-03-18T00:00:00Z --end-time 2026-03-18T01:00:00Z
```

Options:
- `--granularity <g>` -- `minute`, `hour`, or `day` (default: `day`)
- `--start-time <time>` -- ISO 8601 start time
- `--end-time <time>` -- ISO 8601 end time
- `--next-token <token>` -- pagination token from `meta.next_token` in the response

Returns an array of time-bucketed counts in `data`, plus `meta.total_tweet_count` for the total across all buckets.

### Timeline

#### timeline

Get tweets posted by the authenticated user. Internally calls `/users/me` first to resolve the user ID, then fetches the timeline.

```bash
x-analytics-cli timeline
x-analytics-cli timeline --max-results 50
x-analytics-cli timeline --exclude retweets,replies
x-analytics-cli timeline --tweet-fields public_metrics,created_at --start-time 2026-03-01T00:00:00Z
x-analytics-cli timeline --max-results 20 --expansions author_id --user-fields username
```

Options:
- `--max-results <n>` -- max results, 1-100
- `--start-time <time>` -- ISO 8601 start time
- `--end-time <time>` -- ISO 8601 end time
- `--exclude <types>` -- exclude types: `retweets`, `replies` (comma-separated)
- `--next-token <token>` -- pagination token from `meta.next_token` in the response
- `--tweet-fields <fields>` -- tweet fields to include
- `--expansions <expansions>` -- expansions to include
- `--user-fields <fields>` -- user fields to include
- `--media-fields <fields>` -- media fields to include
- `--place-fields <fields>` -- place fields to include
- `--poll-fields <fields>` -- poll fields to include

### Common field values

#### tweet-fields

`attachments`, `author_id`, `context_annotations`, `conversation_id`, `created_at`, `edit_controls`, `edit_history_tweet_ids`, `entities`, `geo`, `id`, `in_reply_to_user_id`, `lang`, `public_metrics`, `possibly_sensitive`, `referenced_tweets`, `reply_settings`, `source`, `text`, `withheld`

The `public_metrics` object contains: `retweet_count`, `reply_count`, `like_count`, `quote_count`, `bookmark_count`, `impression_count`.

#### user-fields

`created_at`, `description`, `entities`, `id`, `location`, `most_recent_tweet_id`, `name`, `pinned_tweet_id`, `profile_image_url`, `protected`, `public_metrics`, `url`, `username`, `verified`, `verified_type`, `withheld`

The `public_metrics` object contains: `followers_count`, `following_count`, `tweet_count`, `listed_count`.

#### media-fields

`duration_ms`, `height`, `media_key`, `preview_image_url`, `public_metrics`, `type`, `url`, `width`, `alt_text`, `variants`

#### expansions (for tweets)

`author_id`, `referenced_tweets.id`, `in_reply_to_user_id`, `attachments.media_keys`, `attachments.poll_ids`, `geo.place_id`, `entities.mentions.username`, `referenced_tweets.id.author_id`, `edit_history_tweet_ids`

#### expansions (for users)

`pinned_tweet_id`

### Pagination

The `search`, `tweet-counts`, and `timeline` commands support pagination via `--next-token`. When a response includes `meta.next_token`, pass that value to the next call to fetch the next page. The `me`, `user`, `tweet`, and `tweets` commands do not paginate.

## Workflow guidance

### When the user asks about a user's profile or stats

1. Run `x-analytics-cli user <username> --user-fields public_metrics,description,created_at` to get their profile and metrics
2. Present follower counts, tweet count, and account creation date

### When the user asks to search for tweets on a topic

1. Run `x-analytics-cli search "<query>" --max-results 50 --tweet-fields public_metrics,created_at,author_id --expansions author_id --user-fields username`
2. Adjust `--sort-order relevancy` if the user wants the most relevant results rather than the most recent
3. Use `--next-token` to paginate through more results if needed

### When the user asks about tweet volume or trends

1. Run `x-analytics-cli tweet-counts "<query>" --granularity hour` to see volume over time
2. Use `--granularity minute` for fine-grained analysis or `--granularity day` for a broader view
3. Narrow with `--start-time` and `--end-time` for a specific window
4. Compare multiple queries by running `tweet-counts` for each term

### When the user asks about a specific tweet

1. Run `x-analytics-cli tweet <id> --tweet-fields public_metrics,created_at,author_id --expansions author_id --user-fields username` to get the tweet with engagement metrics and author info
2. For multiple tweets, use `x-analytics-cli tweets <id1>,<id2>` with the same fields

### When the user asks about their own tweets

1. Run `x-analytics-cli timeline --max-results 50 --tweet-fields public_metrics,created_at` to get recent tweets with engagement
2. Use `--exclude retweets,replies` to focus on original tweets only
3. Use `--start-time` and `--end-time` to narrow to a specific date range

### When the user asks for a comprehensive analysis

1. Start with `x-analytics-cli me --user-fields public_metrics` to get the user's own stats
2. Use `timeline` with `--tweet-fields public_metrics` to analyze engagement on their tweets
3. Use `search "from:<username>"` for a broader view of their recent output
4. Use `tweet-counts "from:<username>" --granularity day` to see their posting frequency

## Error handling

- **"No credentials found"** -- ask the user to set up authentication via credentials file, environment variables, or `--credentials` flag
- **"Unauthorized"** -- the access token is invalid or expired; ask the user to regenerate tokens in the X Developer Portal
- **"Forbidden" / 403** -- the API access tier may not support the endpoint (e.g., search requires Basic tier)
- **Empty data** -- the query returned no results; check the search query syntax, date range, or whether the user/tweet exists
- **Rate limit errors** -- the X API has per-endpoint rate limits; wait and retry, or reduce request frequency

## API documentation references

- [x-analytics-cli documentation](https://github.com/Bin-Huang/x-analytics-cli)
- [X API v2 overview](https://docs.x.com/x-api)
- [Tweet Lookup](https://docs.x.com/x-api/posts/lookup)
- [User Lookup](https://docs.x.com/x-api/users/lookup)
- [Recent Search](https://docs.x.com/x-api/posts/search)
- [Tweet Counts](https://docs.x.com/x-api/posts/counts)
- [Timelines](https://docs.x.com/x-api/posts/timelines)
- [X API v2 fields and expansions](https://docs.x.com/x-api/fields)
- [Search query syntax](https://docs.x.com/x-api/posts/search/integrate/build-a-query)
