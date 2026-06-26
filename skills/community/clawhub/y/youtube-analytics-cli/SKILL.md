---
name: youtube-analytics-cli
description: >
  YouTube channel statistics, video data, and analytics reporting via youtube-analytics-cli.
  Use when the user wants to check YouTube channel stats, video performance, run analytics reports
  with dimensions and filters, or manage analytics groups.
  Triggers: "YouTube Analytics", "YouTube", "channel stats", "video views", "subscribers",
  "watch time", "YouTube report", "estimated minutes watched", "YouTube groups".
---

# YouTube Analytics CLI Skill

You have access to `youtube-analytics-cli`, a read-only CLI for the YouTube Data API v3 and YouTube Analytics API v2. Use it to fetch channel and video details, run analytics reports, and manage analytics groups.

## Quick start

```bash
# Check if the CLI is available
youtube-analytics-cli --help

# Get a channel's public data (API key sufficient)
youtube-analytics-cli channels UCxxxxxxxxxxxxxx

# Get your own channel (OAuth required)
youtube-analytics-cli channels
```

If the CLI is not installed, install it:

```bash
npm install -g youtube-analytics-cli
```

## Authentication

The CLI supports two authentication methods:

| Method | Use case | Commands |
|--------|----------|----------|
| **API key** | Public data (channels, videos) | `channels <id>`, `videos` |
| **OAuth 2.0** | Private data + analytics | All commands (required for `report`, `groups`, `group-items`, `channels` without ID) |

Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. `YOUTUBE_API_KEY`, `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` env vars
3. `~/.config/youtube-analytics-cli/credentials.json` (auto-detected)

The credentials JSON file supports these fields:

```json
{
  "api_key": "YOUR_API_KEY",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

The file must contain at least `api_key` or `client_id`. OAuth commands require all three OAuth fields (`client_id`, `client_secret`, `refresh_token`).

**Important:** Service accounts do NOT work with YouTube APIs. You must use OAuth 2.0 with a refresh token. Required scopes:
- `https://www.googleapis.com/auth/youtube.readonly`
- `https://www.googleapis.com/auth/yt-analytics.readonly`
- `https://www.googleapis.com/auth/yt-analytics-monetary.readonly` (for revenue metrics -- note: revenue metrics may only be available for content owner reports, not standard channel reports)

Before running analytics commands, verify OAuth credentials by running `youtube-analytics-cli channels` (no ID). If it fails, ask the user to set up OAuth 2.0 credentials.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON.

Global options:
- `--format <format>` -- `json` (default, pretty-printed) or `compact` (single-line)
- `--credentials <path>` -- path to credentials JSON file

Errors are written to stderr as JSON with an `error` field and a non-zero exit code.

## Commands reference

### channels

Get channel details. Omit the channel ID to get the authenticated user's own channel (requires OAuth).

```bash
# Get a specific channel by ID (API key sufficient)
youtube-analytics-cli channels UCxxxxxxxxxxxxxx

# Get your own channel (OAuth required)
youtube-analytics-cli channels

# Request specific parts
youtube-analytics-cli channels UCxxxxxxxxxxxxxx --part snippet,statistics,brandingSettings
```

Options:
- `--part <parts>` -- parts to include (default: `snippet,statistics,contentDetails`)

When no channel ID is provided, the command uses `mine=true` which requires OAuth authentication.

### videos

Get video details by IDs. Accepts one or more comma-separated video IDs.

```bash
# Single video
youtube-analytics-cli videos dQw4w9WgXcQ

# Multiple videos
youtube-analytics-cli videos dQw4w9WgXcQ,jNQXAC9IVRw

# Request specific parts
youtube-analytics-cli videos dQw4w9WgXcQ --part snippet,statistics,contentDetails
```

Options:
- `--part <parts>` -- parts to include (default: `snippet,statistics,contentDetails`)

### report

Run a YouTube Analytics report. Requires OAuth.

```bash
youtube-analytics-cli report \
  --metrics <metrics> \
  --start-date <YYYY-MM-DD> \
  --end-date <YYYY-MM-DD> \
  [--dimensions <dims>] \
  [--filters <filters>] \
  [--sort <sort>] \
  [--max-results <n>] \
  [--ids <ids>] \
  [--currency <code>]
```

Required options:
- `--metrics <metrics>` -- metrics to retrieve (e.g. `views,likes,subscribersGained`)
- `--start-date <date>` -- start date in YYYY-MM-DD format
- `--end-date <date>` -- end date in YYYY-MM-DD format

Optional options:
- `--dimensions <dims>` -- dimensions (e.g. `day`, `video`, `country`)
- `--filters <filters>` -- filters (e.g. `video==VIDEO_ID;country==US`)
- `--sort <sort>` -- sort order (e.g. `-views` for descending)
- `--max-results <n>` -- max rows to return
- `--ids <ids>` -- channel or content owner (default: `channel==MINE`)
- `--currency <code>` -- currency code (e.g. `USD`)

#### Report examples

**Daily views and engagement for the last 30 days:**
```bash
youtube-analytics-cli report \
  --metrics views,likes,subscribersGained \
  --start-date 2026-02-17 \
  --end-date 2026-03-19 \
  --dimensions day
```

**Top videos by views:**
```bash
youtube-analytics-cli report \
  --metrics views,estimatedMinutesWatched,averageViewDuration \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions video \
  --sort -views \
  --max-results 10
```

**Country breakdown:**
```bash
youtube-analytics-cli report \
  --metrics views,likes,estimatedMinutesWatched \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions country \
  --sort -views \
  --max-results 20
```

**Country breakdown for a specific video:**
```bash
youtube-analytics-cli report \
  --metrics views,likes \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions country \
  --filters video==dQw4w9WgXcQ
```

**Traffic source breakdown:**
```bash
youtube-analytics-cli report \
  --metrics views,estimatedMinutesWatched \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions insightTrafficSourceType \
  --sort -views
```

**Device type breakdown:**
```bash
youtube-analytics-cli report \
  --metrics views,estimatedMinutesWatched \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions deviceType \
  --sort -views
```

**Subscriber changes by day:**
```bash
youtube-analytics-cli report \
  --metrics subscribersGained,subscribersLost \
  --start-date 2026-02-17 \
  --end-date 2026-03-19 \
  --dimensions day
```

**Revenue report (content owner reports only -- may not work with `channel==MINE`):**
```bash
youtube-analytics-cli report \
  --metrics estimatedRevenue,estimatedAdRevenue,grossRevenue \
  --start-date 2026-01-01 \
  --end-date 2026-03-19 \
  --dimensions day \
  --currency USD
```

### groups

List YouTube Analytics groups. Requires OAuth. Supports pagination via `--next-page-token`.

```bash
# List all your groups
youtube-analytics-cli groups

# Get a specific group by ID
youtube-analytics-cli groups --id GROUP_ID

# Paginate through results
youtube-analytics-cli groups --next-page-token TOKEN
```

Options:
- `--id <id>` -- group ID(s) to retrieve (comma-separated)
- `--next-page-token <token>` -- pagination token

When no `--id` is provided, the command uses `mine=true` to list the authenticated user's groups.

### group-items

List items in a YouTube Analytics group. Requires OAuth. Supports pagination via `--next-page-token`.

```bash
# List items in a group
youtube-analytics-cli group-items GROUP_ID

# Paginate through results
youtube-analytics-cli group-items GROUP_ID --next-page-token TOKEN
```

Options:
- `--next-page-token <token>` -- pagination token

## Common YouTube Analytics dimensions

**Time:** `day`, `month`

**Content:** `video`, `playlist`, `channel` (content owner reports only)

**Geography:** `country`, `province`, `continent` (filter-only), `subContinent` (filter-only)

**Traffic source:** `insightTrafficSourceType`, `insightTrafficSourceDetail`

**Device:** `deviceType`, `operatingSystem`

**Playback:** `liveOrOnDemand`, `subscribedStatus`, `youtubeProduct`

**Demographics:** `ageGroup`, `gender`

**Sharing:** `sharingService`

**Annotations (deprecated since 2019):** `annotationType`, `annotationId`

**Cards:** `cardType`, `cardId`

**End screens:** `endScreenElementType`, `endScreenElementId`

## Common YouTube Analytics metrics

**Views and engagement:** `views`, `likes`, `dislikes`, `comments`, `shares`

**Watch time:** `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`

**Subscribers:** `subscribersGained`, `subscribersLost`

**Revenue (monetized channels):** `estimatedRevenue`, `estimatedAdRevenue`, `grossRevenue`, `estimatedRedPartnerRevenue`, `monetizedPlaybacks`, `adImpressions`, `cpm`

**Cards:** `cardImpressions`, `cardClicks`, `cardClickRate`

**Annotations (deprecated -- historical data only, annotations removed from YouTube in 2019):** `annotationImpressions`, `annotationClicks`, `annotationClickThroughRate`, `annotationClosableImpressions`, `annotationCloseRate`

**End screens:** `endScreenElementImpressions`, `endScreenElementClicks`, `endScreenElementClickRate`

## Workflow guidance

### Quick channel overview

1. Run `youtube-analytics-cli channels` to get your channel's current stats
2. Run a report with `--dimensions day` and key metrics (`views,likes,subscribersGained,estimatedMinutesWatched`) for the last 30 days
3. Run a per-video breakdown to find top-performing content

### Deep video analysis

1. Start broad: per-video views and watch time for the period
2. Drill down: pick a specific video and break down by `country`, `insightTrafficSourceType`, or `deviceType`
3. Use `--filters video==VIDEO_ID` to isolate a single video
4. Compare date ranges by running the same report for different periods

### Audience analysis

1. Run a report with `--dimensions country` to see geographic distribution
2. Use `--dimensions ageGroup,gender` for demographics
3. Use `--dimensions subscribedStatus` to compare subscriber vs non-subscriber engagement

### Content strategy

1. Get per-video stats with `--dimensions video --sort -views --max-results 20`
2. Check traffic sources with `--dimensions insightTrafficSourceType`
3. Compare `estimatedMinutesWatched` across videos to identify engaging content
4. Track `subscribersGained` to see which content drives subscriptions

## Error handling

- **OAuth credentials required** -- the command needs `client_id`, `client_secret`, and `refresh_token`. API key alone is not sufficient for analytics commands.
- **Token refresh failed** -- the refresh token may be expired or revoked. The user needs to re-authorize and obtain a new refresh token.
- **No credentials found** -- provide credentials via `--credentials`, environment variables, or `~/.config/youtube-analytics-cli/credentials.json`.
- **HTTP 403 Forbidden** -- the OAuth scopes may be insufficient, or the YouTube Analytics API may not be enabled in the Google Cloud project.
- **Empty results** -- check date range, metrics/dimensions compatibility, and whether the channel has data for the requested period.

## API documentation references

- [youtube-analytics-cli documentation](https://github.com/Bin-Huang/youtube-analytics-cli)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube Analytics API v2](https://developers.google.com/youtube/analytics)
- [YouTube Analytics reports](https://developers.google.com/youtube/analytics/reference/reports/query)
- [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)
- [YouTube Analytics metrics](https://developers.google.com/youtube/analytics/metrics)
- [YouTube Analytics groups](https://developers.google.com/youtube/analytics/reference/groups/list)
- [YouTube Analytics group items](https://developers.google.com/youtube/analytics/reference/groupItems/list)
