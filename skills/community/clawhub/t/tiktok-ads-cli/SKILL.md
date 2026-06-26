---
name: tiktok-ads-cli
description: >
  TikTok Ads data analysis and reporting via tiktok-ads-cli.
  Use when the user wants to check TikTok ad performance, pull campaign/ad group/ad stats,
  manage audiences, inspect creatives, check pixel tracking, or create async reports.
  Triggers: "TikTok Ads", "TikTok ad performance", "TikTok campaign stats",
  "TikTok ad spend", "TikTok report", "TikTok pixel", "TikTok audience",
  "TikTok creatives", "TikTok ad account", "TikTok ad groups", "TikTok async report".
---

# TikTok Ads CLI Skill

You have access to `tiktok-ads-cli`, a read-only CLI for the TikTok Marketing API (v1.3). Use it to query advertiser accounts, pull synchronous and async performance reports, inspect ad creatives and assets, manage custom and lookalike audiences, and check pixel tracking.

## Quick start

```bash
# Check if the CLI is available
tiktok-ads-cli --help

# Get advertiser account info
tiktok-ads-cli advertiser 7000000000000

# List campaigns
tiktok-ads-cli campaigns 7000000000000
```

If the CLI is not installed, install it:

```bash
npm install -g tiktok-ads-cli
```

## Authentication

The CLI requires a TikTok **OAuth access token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `TIKTOK_ADS_ACCESS_TOKEN` (also reads `TIKTOK_ADS_APP_ID` and `TIKTOK_ADS_SECRET` if set)
3. Auto-detected file: `~/.config/tiktok-ads-cli/credentials.json`

The credentials JSON file requires only `access_token`. The `app_id` and `secret` fields are optional:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Before running any command, verify credentials are configured by running `tiktok-ads-cli advertiser <id>`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Advertiser Account
 +-- Campaign
 |    +-- Ad Group
 |         +-- Ad -> Creative
 +-- Custom Audience
 +-- Lookalike Audience
 +-- Pixel
```

Advertiser IDs are numeric strings (e.g., `7000000000000`). Every command that operates on entities within an account takes the advertiser ID as its first positional argument.

## Monetary values

The TikTok Marketing API returns monetary values (e.g., `spend`, `cpc`, `cpm`) as decimal strings in the major currency unit (e.g., `"12.34"` means $12.34). No conversion needed.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Listing commands use page-based pagination with `--page` and `--page-size` options. Check the `page_info` object in the response for `total_number`, `page`, and `total_page` to determine if more pages exist.

## Commands reference

### Advertiser info

```bash
# Get advertiser account details (supports comma-separated IDs for multiple accounts)
tiktok-ads-cli advertiser 7000000000000
tiktok-ads-cli advertiser 7000000000000,7000000000001
```

### Campaign hierarchy

```bash
# List campaigns
tiktok-ads-cli campaigns 7000000000000
tiktok-ads-cli campaigns 7000000000000 --status CAMPAIGN_STATUS_ENABLE
tiktok-ads-cli campaigns 7000000000000 --page 2 --page-size 50

# List ad groups
tiktok-ads-cli adgroups 7000000000000
tiktok-ads-cli adgroups 7000000000000 --campaign-ids 123,456
tiktok-ads-cli adgroups 7000000000000 --status ADGROUP_STATUS_DELIVERY_OK
tiktok-ads-cli adgroups 7000000000000 --campaign-ids 123 --status ADGROUP_STATUS_ENABLE

# List ads
tiktok-ads-cli ads 7000000000000
tiktok-ads-cli ads 7000000000000 --campaign-ids 123,456
tiktok-ads-cli ads 7000000000000 --adgroup-ids 789
tiktok-ads-cli ads 7000000000000 --status AD_STATUS_DELIVERY_OK
tiktok-ads-cli ads 7000000000000 --campaign-ids 123 --adgroup-ids 789 --status AD_STATUS_ENABLE
```

#### campaigns options

| Option | Description | Default |
|--------|-------------|---------|
| `--status <status>` | Filter by primary status (e.g., `CAMPAIGN_STATUS_ENABLE`, `CAMPAIGN_STATUS_DISABLE`) | all |
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size (max 1000) | `100` |

#### adgroups options

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | Filter by campaign IDs (comma-separated) | all |
| `--status <status>` | Filter by primary status | all |
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size (max 1000) | `100` |

#### ads options

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | Filter by campaign IDs (comma-separated) | all |
| `--adgroup-ids <ids>` | Filter by ad group IDs (comma-separated) | all |
| `--status <status>` | Filter by primary status | all |
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size (max 1000) | `100` |

### Synchronous report

The `report` command is the primary tool for performance analysis. All options marked required must be provided.

```bash
# Campaign-level daily report
tiktok-ads-cli report 7000000000000 \
  --report-type BASIC \
  --data-level AUCTION_CAMPAIGN \
  --dimensions campaign_id,stat_time_day \
  --metrics spend,impressions,clicks,ctr,cpc \
  --start-date 2026-03-01 \
  --end-date 2026-03-15

# Ad-level report
tiktok-ads-cli report 7000000000000 \
  --report-type BASIC \
  --data-level AUCTION_AD \
  --dimensions ad_id,stat_time_day \
  --metrics spend,impressions,clicks,conversion,cost_per_conversion \
  --start-date 2026-03-01 \
  --end-date 2026-03-15

# With filtering
tiktok-ads-cli report 7000000000000 \
  --report-type BASIC \
  --data-level AUCTION_CAMPAIGN \
  --dimensions campaign_id \
  --metrics spend,impressions \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --filters '[{"field_name":"campaign_ids","filter_type":"IN","filter_value":"123,456"}]'
```

#### report options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--report-type <type>` | yes | `BASIC`, `AUDIENCE`, `PLAYABLE_MATERIAL`, `CATALOG` | -- |
| `--data-level <level>` | yes | `AUCTION_ADVERTISER`, `AUCTION_CAMPAIGN`, `AUCTION_ADGROUP`, `AUCTION_AD` | -- |
| `--dimensions <dims>` | yes | Comma-separated (e.g., `campaign_id,stat_time_day`) | -- |
| `--metrics <metrics>` | yes | Comma-separated (e.g., `spend,impressions,clicks,ctr,cpc`) | -- |
| `--start-date <date>` | yes | Start date (`YYYY-MM-DD`) | -- |
| `--end-date <date>` | yes | End date (`YYYY-MM-DD`) | -- |
| `--filters <json>` | no | Filtering conditions as JSON string | none |
| `--page <n>` | no | Page number | `1` |
| `--page-size <n>` | no | Page size (max 1000) | `100` |

#### Common dimensions

Dimensions documented in CLI help text: `ad_id`, `adgroup_id`, `campaign_id`, `stat_time_day`, `stat_time_hour`, `country_code`

The CLI passes dimension names directly to the TikTok Business API without validation. Audience dimensions (e.g., `gender`, `age`) are used with `--report-type AUDIENCE`.

#### Common metrics

Metrics documented in CLI help text: `spend`, `impressions`, `clicks`, `ctr`, `cpc`, `cpm`, `conversion`, `cost_per_conversion`

The CLI passes metric names directly to the TikTok Business API without validation. Refer to the [TikTok Marketing API docs](https://business-api.tiktok.com/portal/docs) for the full list of available metrics (e.g., video engagement, ROAS, social interaction metrics).

### Async report

For large reports, create an async task and check its status later.

```bash
# Create async report task
tiktok-ads-cli async-report 7000000000000 \
  --report-type BASIC \
  --dimensions ad_id,stat_time_day \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --metrics spend,impressions,clicks

# Check task status (poll until complete; returns download URL when done)
tiktok-ads-cli report-status 7000000000000 task_abc123
```

#### async-report options

| Option | Required | Description |
|--------|----------|-------------|
| `--report-type <type>` | yes | `BASIC`, `AUDIENCE`, `PLAYABLE` |
| `--dimensions <dims>` | yes | Comma-separated dimension names |
| `--start-date <date>` | yes | Start date (`YYYY-MM-DD`) |
| `--end-date <date>` | yes | End date (`YYYY-MM-DD`) |
| `--metrics <metrics>` | no | Comma-separated metric names |

Note: The async report always uses `data_level: AUCTION_AD` internally.

### Audience report

```bash
# Audience analysis by gender and age
tiktok-ads-cli audience-report 7000000000000 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --dimensions gender,age

# Audience report filtered by campaigns
tiktok-ads-cli audience-report 7000000000000 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --dimensions gender,age \
  --campaign-ids 123,456
```

#### audience-report options

| Option | Required | Description |
|--------|----------|-------------|
| `--start-date <date>` | yes | Start date (`YYYY-MM-DD`) |
| `--end-date <date>` | yes | End date (`YYYY-MM-DD`) |
| `--dimensions <dims>` | no | Dimensions: `gender`, `age`, `country_code`, `language`, `platform`, etc. |
| `--campaign-ids <ids>` | no | Filter by campaign IDs (comma-separated) |

### Creative assets

```bash
# List image assets
tiktok-ads-cli images 7000000000000
tiktok-ads-cli images 7000000000000 --page 2 --page-size 50

# List video assets
tiktok-ads-cli videos 7000000000000
tiktok-ads-cli videos 7000000000000 --page 2 --page-size 50

# List ad creatives (creative details for ads)
tiktok-ads-cli ad-creatives 7000000000000
tiktok-ads-cli ad-creatives 7000000000000 --ad-ids 123,456
```

#### images / videos options

| Option | Description | Default |
|--------|-------------|---------|
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size (max 1000) | `100` |

#### ad-creatives options

| Option | Description | Default |
|--------|-------------|---------|
| `--ad-ids <ids>` | Filter by ad IDs (comma-separated) | all |
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size | `100` |

### Audiences

```bash
# List custom audiences
tiktok-ads-cli custom-audiences 7000000000000
tiktok-ads-cli custom-audiences 7000000000000 --page 2 --page-size 50

# List lookalike audiences (a type of custom audience)
tiktok-ads-cli lookalike-audiences 7000000000000
tiktok-ads-cli lookalike-audiences 7000000000000 --page 2 --page-size 50
```

#### custom-audiences / lookalike-audiences options

| Option | Description | Default |
|--------|-------------|---------|
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size | `100` |

### Pixels

```bash
# List all pixels
tiktok-ads-cli pixels 7000000000000
tiktok-ads-cli pixels 7000000000000 --page 2

# Get a specific pixel by code
tiktok-ads-cli pixel 7000000000000 PIXEL_CODE_123
```

#### pixels options

| Option | Description | Default |
|--------|-------------|---------|
| `--page <n>` | Page number | `1` |
| `--page-size <n>` | Page size | `100` |

The `pixel` command takes no additional options -- just the advertiser ID and the pixel code.

## Workflow guidance

### When the user asks for a quick overview

1. Run `tiktok-ads-cli campaigns <advertiser-id>` to see all campaigns
2. Use `tiktok-ads-cli report` with `--report-type BASIC --data-level AUCTION_CAMPAIGN` for a performance snapshot
3. Present the data (report `spend` is already in major currency units, no conversion needed)

### When the user asks for deep analysis

1. Start with a campaign-level report to see overall performance
2. Use `--data-level AUCTION_ADGROUP` to identify top/bottom ad groups
3. Drill down with `--data-level AUCTION_AD` for underperforming ad groups
4. Use `audience-report` with `--dimensions gender,age` for demographic analysis
5. Use `--dimensions stat_time_day` for daily trends to spot anomalies
6. Cross-reference with `ad-creatives` to review creative content

### When the user asks about creative performance

1. Run a report with `--data-level AUCTION_AD` to get ad-level metrics
2. Use `ads` to list ads and find their IDs
3. Use `ad-creatives` to inspect creative details
4. Use `images` and `videos` to browse available creative assets

### When the user asks about audience reach

1. Use `custom-audiences` to see existing custom audiences
2. Use `lookalike-audiences` to check lookalike audience setups
3. Use `audience-report` with demographic dimensions to see who is being reached

### When the user asks about conversion tracking

1. Run `pixels` to list active TikTok Pixels
2. Use `pixel` to get details about a specific pixel
3. Check the report with `conversions` and `cost_per_conversion` metrics

### When the user asks for large date-range reports

1. Use `async-report` to create an async task (avoids timeout for large datasets)
2. Use `report-status` to poll for completion
3. The completed task response will include a download URL

## Error handling

- **Authentication errors** -- ask the user to verify their access token; run `tiktok-ads-cli advertiser <id>` to test
- **"No credentials found"** -- ask the user to set up one of: `--credentials` flag, `TIKTOK_ADS_ACCESS_TOKEN` env var, or `~/.config/tiktok-ads-cli/credentials.json`
- **Empty report results** -- check the date range, data level, and whether the account had active ads in the period
- **API error codes** -- the CLI surfaces the TikTok API error message; common issues include invalid advertiser IDs, expired tokens, or insufficient permissions
- **Page out of range** -- check `page_info.total_page` in the response to avoid requesting pages beyond the total

## API documentation references

- [tiktok-ads-cli documentation](https://github.com/Bin-Huang/tiktok-ads-cli)
- [TikTok Marketing API portal](https://business-api.tiktok.com/portal/docs)
- [TikTok Reporting API](https://business-api.tiktok.com/portal/docs?id=1738864915188737)
- [TikTok Audience Management](https://business-api.tiktok.com/portal/docs?id=1739940570793985)
- [TikTok Pixel API](https://business-api.tiktok.com/portal/docs?id=1739585700402178)
