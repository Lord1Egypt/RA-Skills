---
name: reddit-ads-cli
description: >
  Reddit Ads data analysis and reporting via reddit-ads-cli.
  Use when the user wants to check Reddit ad performance, list campaigns/ad groups/ads,
  explore subreddit and interest targeting, track conversion pixels, or generate reports.
  Triggers: "Reddit Ads", "Reddit ad performance", "Reddit campaign stats",
  "Reddit ad spend", "Reddit report", "Reddit pixel", "Reddit audience",
  "Reddit subreddit targeting", "Reddit interest targeting", "Reddit creatives",
  "Reddit ad account", "Reddit ad groups".
---

# Reddit Ads CLI Skill

You have access to `reddit-ads-cli`, a read-only CLI for the Reddit Ads API (v3). Use it to query ad accounts, list campaigns and ads, generate performance reports, inspect creatives, manage custom audiences, track conversion pixels, and explore targeting options (subreddits, interests, geos).

## Quick start

```bash
# Check if the CLI is available
reddit-ads-cli --help

# List accessible ad accounts
reddit-ads-cli accounts

# List campaigns for an account
reddit-ads-cli campaigns t2_abc123
```

If the CLI is not installed, install it:

```bash
npm install -g reddit-ads-cli
```

## Authentication

The CLI requires a Reddit **OAuth access token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `REDDIT_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/reddit-ads-cli/credentials.json`

The credentials file format:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "username": "your_reddit_username"
}
```

Only `access_token` is required. The `username` field is used to build the User-Agent string (`cli:reddit-ads-cli:v<version> (by /u/<username>)`). Reddit rate-limits requests without a proper User-Agent.

When using environment variables:
- `REDDIT_ADS_ACCESS_TOKEN` -- required
- `REDDIT_ADS_CLIENT_ID` -- optional
- `REDDIT_ADS_CLIENT_SECRET` -- optional
- `REDDIT_ADS_USERNAME` -- optional, for User-Agent

Before running any command, verify credentials are configured by running `reddit-ads-cli accounts`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Ad Account (t2_XXXXX)
 +-- Campaign
 |    +-- Ad Group
 |         +-- Ad
 +-- Creative
 +-- Custom Audience
 +-- Pixel
      +-- Pixel Events
```

Ad account IDs use the `t2_` prefix (e.g., `t2_abc123`).

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

## Commands reference

### Account discovery

```bash
# List all ad accounts accessible by the authenticated user
reddit-ads-cli accounts

# Get details of a specific ad account
reddit-ads-cli account t2_abc123
```

### Campaign hierarchy

```bash
# List campaigns (optionally filter by status)
reddit-ads-cli campaigns t2_abc123
reddit-ads-cli campaigns t2_abc123 --status ACTIVE

# List ad groups (optionally filter by campaign or status)
reddit-ads-cli adgroups t2_abc123
reddit-ads-cli adgroups t2_abc123 --campaign-id campaign_abc
reddit-ads-cli adgroups t2_abc123 --status PAUSED

# List ads (optionally filter by ad group, campaign, or status)
reddit-ads-cli ads t2_abc123
reddit-ads-cli ads t2_abc123 --ad-group-id adgroup_abc
reddit-ads-cli ads t2_abc123 --campaign-id campaign_abc
reddit-ads-cli ads t2_abc123 --status ACTIVE
```

#### campaigns options

- `--status <status>` -- filter by status (ACTIVE, PAUSED, etc.)

#### adgroups options

- `--campaign-id <id>` -- filter by campaign ID
- `--status <status>` -- filter by status (ACTIVE, PAUSED, etc.)

#### ads options

- `--ad-group-id <id>` -- filter by ad group ID
- `--campaign-id <id>` -- filter by campaign ID
- `--status <status>` -- filter by status (ACTIVE, PAUSED, etc.)

### Performance reports

The `report` command generates performance reports via a POST request. Both `--start-date` and `--end-date` are required.

```bash
# Campaign-level report (default level)
reddit-ads-cli report t2_abc123 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --metrics impressions,clicks,spend,ecpm,ctr

# Ad group level with timezone
reddit-ads-cli report t2_abc123 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --level AD_GROUP \
  --metrics impressions,clicks,spend \
  --campaign-id campaign_abc \
  --timezone America/New_York

# Account-level report
reddit-ads-cli report t2_abc123 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --level ACCOUNT

# Ad-level report filtered to a specific ad group
reddit-ads-cli report t2_abc123 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --level AD \
  --ad-group-id adgroup_abc
```

#### report options

- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--level <level>` -- report level: ACCOUNT, CAMPAIGN, AD_GROUP, AD (default: CAMPAIGN)
- `--metrics <metrics>` -- comma-separated metrics (default: `impressions,clicks,spend`). Other metrics shown in examples: `ecpm`, `ctr`. The CLI passes metric names directly to the Reddit Ads API without validation. Refer to the [Reddit Ads API docs](https://ads-api.reddit.com/docs/v3) for all available metrics.
- `--campaign-id <id>` -- filter by campaign ID
- `--ad-group-id <id>` -- filter by ad group ID
- `--timezone <tz>` -- timezone (e.g., America/New_York)

### Creatives

```bash
# List ad creatives for an account (supports pagination)
reddit-ads-cli creatives t2_abc123
reddit-ads-cli creatives t2_abc123 --limit 50 --offset 10

# Get a specific creative
reddit-ads-cli creative t2_abc123 creative_xyz
```

#### creatives options

- `--limit <n>` -- results per page (default: 25)
- `--offset <n>` -- start index (default: 0)

### Custom audiences

```bash
# List custom audiences (supports pagination)
reddit-ads-cli custom-audiences t2_abc123
reddit-ads-cli custom-audiences t2_abc123 --limit 50 --offset 10
```

#### custom-audiences options

- `--limit <n>` -- results per page (default: 25)
- `--offset <n>` -- start index (default: 0)

### Pixels & conversion tracking

```bash
# List conversion pixels for an account
reddit-ads-cli pixels t2_abc123

# List events for a specific pixel
reddit-ads-cli pixel-events t2_abc123 pixel_xyz
```

### Targeting options

```bash
# Search subreddits available for targeting (--query is required)
reddit-ads-cli subreddits --query gaming
reddit-ads-cli subreddits --query technology --limit 50

# List interest targeting categories
reddit-ads-cli interests

# List geographic targeting options (optionally search)
reddit-ads-cli geos
reddit-ads-cli geos --query "United States"
```

#### subreddits options

- `--query <q>` -- search query (required)
- `--limit <n>` -- results per page (default: 25)

#### geos options

- `--query <q>` -- search query (optional)

### Pagination summary

Commands that support pagination via `--limit` and `--offset`: `creatives`, `custom-audiences`, `subreddits`.

Commands without pagination options: `accounts`, `account`, `campaigns`, `adgroups`, `ads`, `pixels`, `pixel-events`, `interests`, `geos`.

## Workflow guidance

### When the user asks for a quick overview

1. Run `reddit-ads-cli accounts` to find accessible accounts
2. Run `reddit-ads-cli campaigns <account-id>` to list campaigns
3. Use `reddit-ads-cli report <account-id> --start-date ... --end-date ...` for a performance snapshot

### When the user asks for deep analysis

1. Start with an account-level report (`--level ACCOUNT`) to see overall performance
2. Drill down to `--level CAMPAIGN` to identify top/bottom campaigns
3. Further drill down with `--level AD_GROUP` or `--level AD` for underperforming campaigns
4. Filter by `--campaign-id` or `--ad-group-id` to focus on specific entities
5. Cross-reference with `creatives` to review ad content

### When the user asks about creative performance

1. Run `report` with `--level AD` to get ad-level metrics
2. Use `ads` to find the ad details
3. Use `creatives` and `creative` to inspect the actual creative content

### When the user asks about targeting options

1. Use `subreddits --query <topic>` to discover targetable subreddits
2. Use `interests` to see available interest categories
3. Use `geos` to explore geographic targeting options

### When the user asks about conversion tracking

1. Run `pixels` to list active conversion pixels
2. Use `pixel-events` with a pixel ID to check what events are being tracked
3. Use `report` with conversion-related metrics to see performance

### When the user asks about audiences

1. Use `custom-audiences` to list existing custom audiences
2. Paginate through results using `--limit` and `--offset`

## Error handling

- **Authentication errors** -- ask the user to verify their access token; check that `~/.config/reddit-ads-cli/credentials.json` exists and contains a valid `access_token`
- **Credentials not found** -- the CLI looks for credentials in three places (flag, env var, default file); ensure at least one is configured
- **Empty reports** -- check date range, entity status, and whether the account had active ads in the period
- **Rate limiting** -- Reddit rate-limits requests without a proper User-Agent; ensure `username` is set in credentials
- **Unknown command** -- run `reddit-ads-cli --help` to see available commands

## API documentation references

- [reddit-ads-cli documentation](https://github.com/Bin-Huang/reddit-ads-cli)
- [Reddit Ads API v3 docs](https://ads-api.reddit.com/docs/v3)
- [Reddit OAuth2 authentication](https://github.com/reddit-archive/reddit/wiki/OAuth2)
