---
name: x-ads-cli
description: >
  X Ads data analysis and reporting via x-ads-cli.
  Use when the user wants to check X/Twitter ad performance, pull campaign/line item/promoted tweet stats,
  explore ad account structure, inspect media creatives, analyze targeting criteria, check conversion events, or estimate reach.
  Triggers: "X Ads", "Twitter Ads", "X ad performance", "X campaign stats",
  "X ad spend", "X analytics", "X targeting", "X audience", "X creatives",
  "Twitter ad account", "line item performance", "X billing", "promoted tweets".
---

# X Ads CLI Skill

You have access to `x-ads-cli`, a read-only CLI for the X Ads API (v12). Use it to query ad accounts, pull synchronous analytics, inspect promoted tweets and media creatives, review targeting criteria, check funding instruments, and estimate reach. Handles OAuth 1.0a signing natively with Node.js `crypto` -- no external dependencies.

## Quick start

```bash
# Check if the CLI is available
x-ads-cli --help

# List all accessible ad accounts
x-ads-cli accounts

# Get a specific ad account
x-ads-cli account abc1x2
```

If the CLI is not installed, install it:

```bash
npm install -g x-ads-cli
```

## Authentication

The CLI requires four OAuth 1.0a credentials: API Key, API Secret, Access Token, and Access Token Secret. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variables: `X_ADS_API_KEY`, `X_ADS_API_SECRET`, `X_ADS_ACCESS_TOKEN`, `X_ADS_ACCESS_TOKEN_SECRET`
3. Auto-detected file: `~/.config/x-ads-cli/credentials.json`

The credentials file format:

```json
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN",
  "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET"
}
```

The Access Token must belong to a user who has access to at least one X Ads account. Ads API access requires separate approval from the X Developer Portal.

Before running any command, verify credentials are configured by running `x-ads-cli accounts`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Ad Account
 +-- Campaign
 |    +-- Line Item (ad group)
 |         +-- Promoted Tweet
 |         +-- Targeting Criteria
 +-- Media Creative
 +-- Card (website, app install, etc.)
 +-- Custom Audience
 +-- Funding Instrument (payment method)
 +-- Conversion Event (web event tag)
```

Line items sit under campaigns and contain targeting, budget, and bid settings. Promoted tweets are attached to line items.

## Monetary values

The X Ads API returns monetary values (e.g., `billed_charge_local_micro`) in **microcurrency** -- the value multiplied by 1,000,000. Divide by 1,000,000 to get the actual amount in the major currency unit. For example, `5000000` means $5.00.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Pagination for listing commands uses cursor-based `--cursor` values from the `next_cursor` field in the response.

## Commands reference

### Account discovery

```bash
# List all accessible ad accounts
x-ads-cli accounts

# Include deleted accounts
x-ads-cli accounts --with-deleted

# Get a specific ad account
x-ads-cli account abc1x2
```

**accounts** options:
- `--with-deleted` -- include deleted accounts

**account** takes a single required argument: the account ID.

### Campaigns

```bash
# List all campaigns for an account
x-ads-cli campaigns abc1x2

# Filter by specific campaign IDs
x-ads-cli campaigns abc1x2 --campaign-ids id1,id2

# Include deleted campaigns with custom page size
x-ads-cli campaigns abc1x2 --with-deleted --count 500

# Paginate
x-ads-cli campaigns abc1x2 --cursor next_cursor_value
```

Options:
- `--campaign-ids <ids>` -- filter by campaign IDs (comma-separated)
- `--with-deleted` -- include deleted campaigns
- `--count <n>` -- results per page (default 200, max 1000)
- `--cursor <cursor>` -- pagination cursor from previous response

### Line items

```bash
# List all line items for an account
x-ads-cli line-items abc1x2

# Filter by campaign
x-ads-cli line-items abc1x2 --campaign-ids campaign_id_1

# Filter by specific line item IDs
x-ads-cli line-items abc1x2 --line-item-ids li1,li2

# Include deleted, with pagination
x-ads-cli line-items abc1x2 --with-deleted --cursor next_cursor_value
```

Options:
- `--campaign-ids <ids>` -- filter by campaign IDs (comma-separated)
- `--line-item-ids <ids>` -- filter by line item IDs (comma-separated)
- `--with-deleted` -- include deleted line items
- `--count <n>` -- results per page (default 200, max 1000)
- `--cursor <cursor>` -- pagination cursor

### Analytics (stats)

The `stats` command provides synchronous analytics. Supports up to 7 days of data per request.

```bash
# Campaign-level daily metrics
x-ads-cli stats abc1x2 \
  --entity CAMPAIGN \
  --entity-ids campaign_id_1,campaign_id_2 \
  --start-time 2026-03-01T00:00:00Z \
  --end-time 2026-03-07T00:00:00Z \
  --granularity DAY \
  --metric-groups ENGAGEMENT,BILLING

# Line item hourly metrics with video
x-ads-cli stats abc1x2 \
  --entity LINE_ITEM \
  --entity-ids line_item_id_1 \
  --start-time 2026-03-15T00:00:00Z \
  --end-time 2026-03-16T00:00:00Z \
  --granularity HOUR \
  --metric-groups ENGAGEMENT,BILLING,VIDEO

# Promoted tweet total metrics
x-ads-cli stats abc1x2 \
  --entity PROMOTED_TWEET \
  --entity-ids pt_id_1 \
  --start-time 2026-03-01T00:00:00Z \
  --end-time 2026-03-07T00:00:00Z \
  --granularity TOTAL \
  --metric-groups ENGAGEMENT,BILLING
```

Required options:
- `--entity <type>` -- entity type (required). Values: `CAMPAIGN`, `LINE_ITEM`, `PROMOTED_TWEET`, `MEDIA_CREATIVE`, `FUNDING_INSTRUMENT`, `ORGANIC_TWEET`
- `--entity-ids <ids>` -- entity IDs, comma-separated (required)
- `--start-time <time>` -- ISO 8601 start time (required)
- `--end-time <time>` -- ISO 8601 end time (required)

Optional:
- `--granularity <gran>` -- `HOUR`, `DAY`, or `TOTAL` (default `DAY`)
- `--metric-groups <groups>` -- comma-separated metric groups (default `ENGAGEMENT,BILLING`). Available: `ENGAGEMENT`, `BILLING`, `VIDEO`, `MEDIA`, `WEB_CONVERSION`, `MOBILE_CONVERSION`, `LIFE_TIME_VALUE_MOBILE_CONVERSION`
- `--placement <placement>` -- `ALL_ON_TWITTER`, `PUBLISHER_NETWORK`, `SPOTLIGHT`, `TREND` (default `ALL_ON_TWITTER`)

The CLI passes `--metric-groups` directly to the X Ads API, which returns the individual metrics for each group. Refer to the [X Ads Analytics docs](https://docs.x.com/x-ads-api/analytics) for the specific metrics included in each group.

### Promoted tweets

```bash
# List promoted tweets for an account
x-ads-cli promoted-tweets abc1x2

# Filter by line item
x-ads-cli promoted-tweets abc1x2 --line-item-ids li1,li2
```

Options:
- `--line-item-ids <ids>` -- filter by line item IDs (comma-separated)
- `--count <n>` -- results per page (default 200)
- `--cursor <cursor>` -- pagination cursor

### Media creatives

```bash
# List media creatives for an account
x-ads-cli media-creatives abc1x2
```

Options:
- `--count <n>` -- results per page (default 200)
- `--cursor <cursor>` -- pagination cursor

### Cards

```bash
# List all cards for an account
x-ads-cli cards abc1x2

# Filter by card types
x-ads-cli cards abc1x2 --card-types WEBSITE,VIDEO_WEBSITE
```

Options:
- `--card-types <types>` -- filter by types (comma-separated). Values include: `WEBSITE`, `VIDEO_WEBSITE`, `IMAGE_APP_DOWNLOAD`, etc.
- `--count <n>` -- results per page (default 200)
- `--cursor <cursor>` -- pagination cursor

### Targeting criteria

```bash
# List targeting criteria for an account
x-ads-cli targeting-criteria abc1x2

# Filter by line items
x-ads-cli targeting-criteria abc1x2 --line-item-ids li1,li2
```

Options:
- `--line-item-ids <ids>` -- filter by line item IDs (comma-separated)
- `--count <n>` -- results per page (default 200)
- `--cursor <cursor>` -- pagination cursor

### Custom audiences

```bash
# List custom audiences for an account
x-ads-cli custom-audiences abc1x2
```

Options:
- `--count <n>` -- results per page (default 200)
- `--cursor <cursor>` -- pagination cursor

### Funding instruments

```bash
# List funding instruments (payment methods) for an account
x-ads-cli funding-instruments abc1x2
```

Options:
- `--count <n>` -- results per page (default 200)

Note: This command does **not** support `--cursor` pagination.

### Conversion events

```bash
# List web conversion events for an account
x-ads-cli conversion-events abc1x2
```

Options:
- `--count <n>` -- results per page (default 200)

Note: This command does **not** support `--cursor` pagination.

### Reach estimate

```bash
# Get reach estimate for a line item
x-ads-cli reach-estimate abc1x2 --line-item-id li1
```

Required options:
- `--line-item-id <id>` -- line item ID (required)

## Workflow guidance

### When the user asks for a quick overview

1. Run `x-ads-cli accounts` to find accessible accounts
2. Use `campaigns` to list active campaigns
3. Use `stats` with `--granularity TOTAL` and `--metric-groups ENGAGEMENT,BILLING` for a performance snapshot
4. Monetary values from stats are in microcurrency -- divide by 1,000,000

### When the user asks for deep analysis

1. Start with `stats` at the `CAMPAIGN` entity level for an overview
2. Drill into specific campaigns with `line-items` to find their ad groups
3. Use `stats` at the `LINE_ITEM` level for underperforming campaigns
4. Use `--granularity HOUR` for intraday trends or `--granularity DAY` for multi-day trends
5. Cross-reference with `promoted-tweets` to inspect individual tweet performance
6. Check `targeting-criteria` to review targeting setup

### When the user asks about creative performance

1. Run `stats` with `--entity PROMOTED_TWEET` for promoted tweet metrics
2. Use `promoted-tweets` to list tweets and their IDs
3. Use `media-creatives` to inspect media assets
4. Use `cards` to review card-based creatives (website cards, app install cards)

### When the user asks about audience reach

1. Use `custom-audiences` to see existing audiences
2. Use `reach-estimate` with a line item ID to get estimated reach
3. Use `targeting-criteria` to review what targeting is applied to line items

### When the user asks about billing and spend

1. Use `stats` with `--metric-groups BILLING` for billing data
2. Use `funding-instruments` to see payment methods on file
3. Remember: monetary values are in microcurrency (divide by 1,000,000)

### When the user asks about conversion tracking

1. Use `conversion-events` to list web event tags
2. Use `stats` with `--metric-groups WEB_CONVERSION` or `MOBILE_CONVERSION` for conversion data

### Multi-day analytics

The stats command supports up to 7 days per request. For longer date ranges, make multiple requests with consecutive 7-day windows and combine the results.

## Error handling

- **Authentication errors** -- ask the user to verify their OAuth credentials (API Key, API Secret, Access Token, Access Token Secret) and that their app has Ads API access
- **No credentials found** -- the CLI checked all three sources (flag, env vars, default file) and found nothing; ask the user to set up credentials
- **Empty results** -- check that the account ID is correct, the entity exists, and (for stats) the date range contains active ad activity
- **HTTP 403** -- the authenticated user may not have access to the specified ad account
- **HTTP 429** -- rate limited; wait and retry
- **Stats date range too large** -- the API supports max 7 days per request; split into smaller windows

## API documentation references

- [x-ads-cli documentation](https://github.com/Bin-Huang/x-ads-cli)
- [X Ads API introduction](https://docs.x.com/x-ads-api/introduction)
- [Campaign management](https://docs.x.com/x-ads-api/campaign-management)
- [Analytics](https://docs.x.com/x-ads-api/analytics)
- [Getting started with X Ads API](https://docs.x.com/x-ads-api/getting-started)
