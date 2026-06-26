---
name: spotify-ads-cli
description: >
  Spotify Ads data analysis and reporting via spotify-ads-cli.
  Use when the user wants to check Spotify ad performance, pull aggregate or insight reports,
  explore businesses and ad accounts, manage audio creatives, analyze targeting and audiences,
  track measurement pixels and datasets, or estimate audience/bid ranges.
  Triggers: "Spotify Ads", "Spotify ad performance", "Spotify campaign stats",
  "Spotify ad spend", "Spotify insight report", "Spotify aggregate report",
  "Spotify pixel", "Spotify audience", "Spotify ad account", "Spotify targeting",
  "Spotify audio ads", "Spotify ad set", "Spotify CSV report", "Spotify bid estimate".
---

# Spotify Ads CLI Skill

You have access to `spotify-ads-cli`, a read-only CLI for the Spotify Ads API (v3). Use it to query businesses and ad accounts, pull aggregate and insight reports, create async CSV reports, estimate audience sizes and bid ranges, explore targeting options, manage audiences and assets, and track measurement pixels and datasets.

## Quick start

```bash
# Check if the CLI is available
spotify-ads-cli --help

# List businesses for the current user
spotify-ads-cli businesses

# List ad accounts for a business
spotify-ads-cli ad-accounts biz_abc123
```

If the CLI is not installed, install it:

```bash
npm install -g spotify-ads-cli
```

## Authentication

The CLI requires a Spotify **OAuth access token** from a Spotify Developer App with Ads API access. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `SPOTIFY_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/spotify-ads-cli/credentials.json`

The credentials file format:

```json
{
  "access_token": "your_access_token"
}
```

Before running any command, verify credentials are configured by running `spotify-ads-cli businesses`. If it fails with a credentials error, ask the user to set up authentication. To request Ads API access, contact ads-api-support@spotify.com.

## Entity hierarchy

```
Business
 +-- Ad Account
      +-- Campaign
      |    +-- Ad Set (targeting, budget, schedule)
      |         +-- Ad (creative)
      +-- Asset (audio, images)
      +-- Audience (custom, lookalike)
      +-- Pixel / Dataset (measurement)
```

## Monetary values

Spotify uses **micros** for input parameters: 1 dollar = 1,000,000 micros. Bid amounts (`bid_micro_amount`) and budgets (`budget_micro_amount`) are in micros -- divide by 1,000,000 for the actual amount. Reporting endpoints (aggregate and insight reports) return spend in standard currency units (no conversion needed).

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Listing commands use offset-based pagination with `--offset` and `--limit` (max 50). Reporting commands use continuation tokens via `--continuation-token`.

## Commands reference

### Account discovery

```bash
# List businesses for the current user
spotify-ads-cli businesses

# Get a specific business
spotify-ads-cli business biz_abc123

# List ad accounts for a business (supports pagination)
spotify-ads-cli ad-accounts biz_abc123
spotify-ads-cli ad-accounts biz_abc123 --offset 0 --limit 50

# Get a specific ad account
spotify-ads-cli ad-account acc_abc123
```

### Campaign hierarchy

```bash
# List campaigns for an ad account (filter by status: ACTIVE, PAUSED, COMPLETED, DRAFT)
spotify-ads-cli campaigns acc_abc123
spotify-ads-cli campaigns acc_abc123 --status ACTIVE
spotify-ads-cli campaigns acc_abc123 --offset 0 --limit 25

# Get a specific campaign
spotify-ads-cli campaign camp_abc123

# List ad sets for an ad account (filter by status: ACTIVE, PAUSED, COMPLETED, DRAFT)
spotify-ads-cli adsets acc_abc123
spotify-ads-cli adsets acc_abc123 --status ACTIVE

# Get a specific ad set
spotify-ads-cli adset adset_abc123

# List ads for an ad account (filter by status: ACTIVE, PAUSED, COMPLETED, DRAFT)
spotify-ads-cli ads acc_abc123
spotify-ads-cli ads acc_abc123 --status PAUSED

# Get a specific ad
spotify-ads-cli ad ad_abc123
```

All listing commands for campaigns, ad sets, and ads support `--offset <n>` (default 0), `--limit <n>` (default 50, max 50), and `--status <status>`.

### Reporting

#### Aggregate report

Get aggregate performance metrics for an ad account.

```bash
# Basic aggregate report (--start and --end are required)
spotify-ads-cli aggregate-report acc_abc123 --start 2026-01-01 --end 2026-01-31

# With entity type and time granularity
spotify-ads-cli aggregate-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --entity-type CAMPAIGN --granularity DAY

# Filter by specific campaigns or ad sets
spotify-ads-cli aggregate-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --campaign-ids camp_1,camp_2
spotify-ads-cli aggregate-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --adset-ids adset_1,adset_2

# Continue paginating with a continuation token
spotify-ads-cli aggregate-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --continuation-token TOKEN
```

Options:
- `--start <date>` -- start date YYYY-MM-DD (required)
- `--end <date>` -- end date YYYY-MM-DD (required)
- `--entity-type <type>` -- CAMPAIGN, AD_SET, or AD
- `--granularity <granularity>` -- DAY, WEEK, or MONTH
- `--campaign-ids <ids>` -- comma-separated campaign IDs
- `--adset-ids <ids>` -- comma-separated ad set IDs
- `--continuation-token <token>` -- pagination token from previous response

#### Insight report

Get insight reports with audience demographics, platform breakdowns, genre breakdowns, etc.

```bash
# Insight report by age dimension
spotify-ads-cli insight-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --insight-dimension AGE

# Insight report by gender
spotify-ads-cli insight-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --insight-dimension GENDER

# Insight report filtered to specific campaigns
spotify-ads-cli insight-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --insight-dimension PLATFORM --campaign-ids camp_1
```

Options:
- `--start <date>` -- start date YYYY-MM-DD (required)
- `--end <date>` -- end date YYYY-MM-DD (required)
- `--entity-type <type>` -- CAMPAIGN, AD_SET, or AD
- `--insight-dimension <dimension>` -- AGE, GENDER, PLATFORM, GENRE, etc. The CLI passes the value directly to the Spotify Ads API.
- `--campaign-ids <ids>` -- comma-separated campaign IDs
- `--continuation-token <token>` -- pagination token from previous response

#### CSV report (async)

Create an async CSV report and poll for status.

```bash
# Create an async CSV report (POST request)
spotify-ads-cli csv-report acc_abc123 --start 2026-01-01 --end 2026-01-31
spotify-ads-cli csv-report acc_abc123 --start 2026-01-01 --end 2026-01-31 --entity-type CAMPAIGN --granularity DAY

# Check report generation status
spotify-ads-cli csv-report-status acc_abc123 rpt_abc123
```

csv-report options:
- `--start <date>` -- start date YYYY-MM-DD (required)
- `--end <date>` -- end date YYYY-MM-DD (required)
- `--entity-type <type>` -- CAMPAIGN, AD_SET, or AD
- `--granularity <granularity>` -- DAY, WEEK, or MONTH

csv-report-status takes two positional arguments: `<ad-account-id>` and `<report-id>`. Poll until the report is complete.

### Targeting

```bash
# Estimate audience size for targeting criteria (--targeting is required, JSON string)
spotify-ads-cli estimate-audience --targeting '{"geo_targets":["US"],"age_range":{"min":18,"max":35}}'

# Estimate bid range for targeting criteria
spotify-ads-cli estimate-bid --targeting '{"geo_targets":["US"]}'

# List geographic targeting options
spotify-ads-cli geo-targets
spotify-ads-cli geo-targets --query "United States"
spotify-ads-cli geo-targets --limit 20

# List interest targeting options
spotify-ads-cli interest-targets
spotify-ads-cli interest-targets --query "music"
spotify-ads-cli interest-targets --limit 20
```

`geo-targets` and `interest-targets` support `--query <q>` for search and `--limit <n>` (default 50). They do not support `--offset`.

`estimate-audience` and `estimate-bid` both require `--targeting <json>` with a JSON targeting spec.

### Audiences

```bash
# List custom/lookalike audiences for an ad account (supports pagination)
spotify-ads-cli audiences acc_abc123
spotify-ads-cli audiences acc_abc123 --offset 0 --limit 25

# Get a specific audience
spotify-ads-cli audience aud_abc123
```

`audiences` supports `--offset <n>` (default 0) and `--limit <n>` (default 50).

### Assets

```bash
# List assets (audio, images, etc.) for an ad account
spotify-ads-cli assets acc_abc123
spotify-ads-cli assets acc_abc123 --offset 0 --limit 25

# Filter by specific asset IDs
spotify-ads-cli assets acc_abc123 --asset-ids asset_1,asset_2
```

`assets` supports `--offset <n>` (default 0), `--limit <n>` (default 50), and `--asset-ids <ids>` (comma-separated).

### Measurement (pixels & datasets)

```bash
# List Spotify Pixels for a business
spotify-ads-cli pixels biz_abc123

# Get a specific pixel
spotify-ads-cli pixel biz_abc123 pix_abc123

# List measurement datasets for a business
spotify-ads-cli datasets biz_abc123

# Get a specific dataset
spotify-ads-cli dataset ds_abc123

# Get diagnostics for a dataset
spotify-ads-cli dataset-diagnostics ds_abc123
```

`pixels` and `datasets` do not support pagination options. `pixel` takes two positional arguments: `<business-id>` and `<pixel-id>`.

## Workflow guidance

### When the user asks for a quick overview

1. Run `spotify-ads-cli businesses` to find accessible businesses
2. Run `spotify-ads-cli ad-accounts <business-id>` to list ad accounts
3. Use `aggregate-report` with a recent date range for a performance snapshot
4. Remember that monetary values are in micros -- divide by 1,000,000

### When the user asks for deep analysis

1. Start with `aggregate-report` at the account level for overall performance
2. Add `--entity-type CAMPAIGN` to identify top/bottom campaigns
3. Drill down with `--entity-type AD_SET` or `--entity-type AD` for granular analysis
4. Use `--granularity DAY` for daily trends to spot anomalies
5. Use `insight-report` with `--insight-dimension AGE` or `--insight-dimension GENDER` for demographic analysis
6. Use `insight-report` with `--insight-dimension PLATFORM` or `--insight-dimension GENRE` for platform/genre breakdowns

### When the user asks about audience planning

1. Use `geo-targets` and `interest-targets` to explore available targeting options
2. Use `estimate-audience` with targeting JSON to estimate potential reach
3. Use `estimate-bid` to understand bid ranges for the targeting
4. Use `audiences` to see existing custom/lookalike audiences

### When the user asks about creatives and assets

1. Use `ads` to list ads for an ad account
2. Use `ad` to inspect a specific ad's creative details
3. Use `assets` to list audio, image, and other creative assets

### When the user asks about measurement

1. Use `pixels` to list Spotify Pixels for a business
2. Use `pixel` to inspect a specific pixel's configuration
3. Use `datasets` to list measurement datasets
4. Use `dataset-diagnostics` to check dataset health and data quality

### When the user needs a CSV export

1. Run `csv-report` to create an async report (this is a POST request)
2. Poll `csv-report-status` with the returned report ID until completion
3. Download the CSV from the URL provided in the completed status response

## Error handling

- **Authentication errors** -- ask the user to verify their access token; check that `SPOTIFY_ADS_ACCESS_TOKEN` is set or credentials file exists at `~/.config/spotify-ads-cli/credentials.json`
- **Empty reports** -- check the date range, entity status, and whether the account had active ads in the period
- **HTTP errors** -- the CLI surfaces the API error message; common issues include invalid IDs, expired tokens, or insufficient API access
- **JSON parse errors** -- ensure `--targeting` values are valid JSON strings with proper quoting

## API documentation references

- [spotify-ads-cli documentation](https://github.com/Bin-Huang/spotify-ads-cli)
- [Spotify Ads API documentation](https://developer.spotify.com/documentation/ads-api)
