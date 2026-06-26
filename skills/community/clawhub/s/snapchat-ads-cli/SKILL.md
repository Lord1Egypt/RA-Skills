---
name: snapchat-ads-cli
description: >
  Snapchat Ads data analysis and reporting via snapchat-ads-cli.
  Use when the user wants to check Snapchat ad performance, pull campaign/ad squad/ad stats,
  explore ad account structure, inspect creatives, analyze audiences, debug delivery issues,
  estimate bids and audience size, manage AR lenses, or retrieve billing information.
  Triggers: "Snapchat Ads", "Snap Ads", "snapchat ad performance", "snapchat campaign stats",
  "snapchat ad spend", "snapchat pixel", "snapchat audience", "snapchat creatives",
  "snapchat ad account", "ad squad performance", "snapchat delivery status", "snapchat lenses",
  "snapchat bid estimate", "snapchat audience size", "snapchat billing".
---

# Snapchat Ads CLI Skill

You have access to `snapchat-ads-cli`, a read-only CLI for the Snapchat Marketing API (v1). Use it to query organizations and ad accounts, pull performance stats with attribution windows, inspect creatives, debug delivery issues, estimate bids and audience sizes, manage AR lenses, and retrieve billing information.

## Quick start

```bash
# Check if the CLI is available
snapchat-ads-cli --help

# List organizations
snapchat-ads-cli organizations

# List ad accounts for an organization
snapchat-ads-cli accounts ORG_ID
```

If the CLI is not installed, install it:

```bash
npm install -g snapchat-ads-cli
```

## Authentication

The CLI requires a Snapchat **OAuth2 access token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `SNAPCHAT_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/snapchat-ads-cli/credentials.json`

The credentials file format:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Before running any command, verify credentials are configured by running `snapchat-ads-cli organizations`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Organization
 +-- Ad Account
      +-- Campaign
      |    +-- Ad Squad (= ad group)
      |         +-- Ad -> Creative
      +-- Creative (managed at ad account level)
```

Most list commands require the parent entity ID. Start with `organizations` to find the org, then `accounts <org-id>` to find ad accounts, and drill down from there.

## Monetary values

Snapchat uses **micro-currency**: 1 dollar = 1,000,000 micro. All spend values in stats and budgets are in micro-currency. Divide by 1,000,000 to get the actual dollar amount.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Listing commands that support pagination use `--limit <n>` to control page size (default 50).

## Commands reference

### Organization discovery

```bash
# List all organizations the user has access to
snapchat-ads-cli organizations

# Get a specific organization
snapchat-ads-cli organization ORG_ID
```

Note: `organizations` does not support `--limit` pagination. `organization` fetches a single entity by ID.

### Ad accounts

```bash
# List ad accounts for an organization
snapchat-ads-cli accounts ORG_ID
snapchat-ads-cli accounts ORG_ID --limit 100

# Get a specific ad account
snapchat-ads-cli account ACCOUNT_ID
```

Options for `accounts`: `--limit <n>` (default 50)

### Funding & billing centers

```bash
# List funding sources for an organization
snapchat-ads-cli funding-sources ORG_ID
snapchat-ads-cli funding-sources ORG_ID --limit 100

# List billing centers for an organization
snapchat-ads-cli billing-centers ORG_ID
snapchat-ads-cli billing-centers ORG_ID --limit 100
```

Both support `--limit <n>` (default 50).

### Campaigns

```bash
# List campaigns for an ad account
snapchat-ads-cli campaigns ACCOUNT_ID
snapchat-ads-cli campaigns ACCOUNT_ID --limit 100

# Get a specific campaign
snapchat-ads-cli campaign CAMPAIGN_ID
```

Options for `campaigns`: `--limit <n>` (default 50)

### Ad squads

```bash
# List ad squads for a campaign
snapchat-ads-cli adsquads CAMPAIGN_ID
snapchat-ads-cli adsquads CAMPAIGN_ID --limit 100

# Get a specific ad squad
snapchat-ads-cli adsquad ADSQUAD_ID
```

Options for `adsquads`: `--limit <n>` (default 50)

### Ads

```bash
# List ads for an ad squad
snapchat-ads-cli ads ADSQUAD_ID
snapchat-ads-cli ads ADSQUAD_ID --limit 100

# Get a specific ad
snapchat-ads-cli ad AD_ID
```

Options for `ads`: `--limit <n>` (default 50)

### Creatives

```bash
# List creatives for an ad account
snapchat-ads-cli creatives ACCOUNT_ID
snapchat-ads-cli creatives ACCOUNT_ID --limit 100

# Get a specific creative
snapchat-ads-cli creative CREATIVE_ID
```

Options for `creatives`: `--limit <n>` (default 50)

### Audiences & pixel

```bash
# List custom audience segments for an ad account
snapchat-ads-cli audiences ACCOUNT_ID
snapchat-ads-cli audiences ACCOUNT_ID --limit 100

# Get a specific audience segment
snapchat-ads-cli audience SEGMENT_ID

# Get the Snap Pixel for an ad account
snapchat-ads-cli pixel ACCOUNT_ID
```

Options for `audiences`: `--limit <n>` (default 50). `audience` and `pixel` do not support `--limit`.

### Members & roles

```bash
# List members of an organization
snapchat-ads-cli members ORG_ID
snapchat-ads-cli members ORG_ID --limit 100

# List roles for an organization
snapchat-ads-cli roles ORG_ID
snapchat-ads-cli roles ORG_ID --limit 100
```

Both support `--limit <n>` (default 50).

### Billing

```bash
# List invoices for an ad account
snapchat-ads-cli invoices ACCOUNT_ID
snapchat-ads-cli invoices ACCOUNT_ID --limit 100

# List transactions for an organization
snapchat-ads-cli transactions ORG_ID
snapchat-ads-cli transactions ORG_ID --limit 100
```

Both support `--limit <n>` (default 50).

### Performance stats

Stats commands work on campaigns, ad squads, and ads. All three share the same options.

```bash
# Campaign stats (daily granularity)
snapchat-ads-cli campaign-stats CAMPAIGN_ID \
  --start-time 2026-03-01T00:00:00.000Z \
  --end-time 2026-03-15T00:00:00.000Z \
  --granularity DAY

# Ad squad stats (total granularity, default)
snapchat-ads-cli adsquad-stats ADSQUAD_ID \
  --start-time 2026-03-01T00:00:00.000Z \
  --end-time 2026-03-15T00:00:00.000Z

# Ad stats (hourly granularity with attribution windows)
snapchat-ads-cli ad-stats AD_ID \
  --start-time 2026-03-01T00:00:00.000Z \
  --end-time 2026-03-15T00:00:00.000Z \
  --granularity HOUR \
  --swipe-up-attribution-window 28_DAY \
  --view-attribution-window 7_DAY

# Campaign stats with specific fields and conversion sources
snapchat-ads-cli campaign-stats CAMPAIGN_ID \
  --start-time 2026-03-01T00:00:00.000Z \
  --end-time 2026-03-15T00:00:00.000Z \
  --fields spend,impressions,swipes \
  --conversion-source-types web,app
```

#### Stats options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--start-time <time>` | Yes | Start time in ISO 8601 format | -- |
| `--end-time <time>` | Yes | End time in ISO 8601 format | -- |
| `--granularity <gran>` | No | `TOTAL`, `DAY`, or `HOUR` | `TOTAL` |
| `--fields <fields>` | No | Stat fields to include (comma-separated) | all default fields |
| `--swipe-up-attribution-window <window>` | No | `1_DAY`, `7_DAY`, `28_DAY` | -- |
| `--view-attribution-window <window>` | No | `1_HOUR`, `3_HOUR`, `6_HOUR`, `1_DAY`, `7_DAY`, `28_DAY` | -- |
| `--conversion-source-types <types>` | No | Comma-separated: `web`, `app`, `total` | -- |

The CLI passes `--fields` values directly to the Snapchat Marketing API without validation. When `--fields` is omitted, the API returns its default set. Use `--fields spend,impressions,swipes` to request specific fields. Refer to the [Snapchat Measurement API docs](https://developers.snap.com/api/marketing-api/Ads-API/measurement) for the full list of available fields.

### Delivery debugging

```bash
# Get delivery status for a campaign
snapchat-ads-cli delivery-status campaigns CAMPAIGN_ID

# Get delivery status for an ad squad
snapchat-ads-cli delivery-status adsquads ADSQUAD_ID

# Get delivery status for an ad
snapchat-ads-cli delivery-status ads AD_ID
```

The `entity-type` argument must be one of: `campaigns`, `adsquads`, `ads`.

### Targeting & insights

```bash
# Get targeting insights for an ad account (POST request)
snapchat-ads-cli audience-insights ACCOUNT_ID

# List custom conversions for a pixel
snapchat-ads-cli custom-conversions PIXEL_ID
snapchat-ads-cli custom-conversions PIXEL_ID --limit 100
```

Options for `custom-conversions`: `--limit <n>` (default 50). `audience-insights` does not support `--limit`.

### Audit logs

```bash
# List external changelogs for an entity
snapchat-ads-cli audit-logs campaigns CAMPAIGN_ID
snapchat-ads-cli audit-logs adsquads ADSQUAD_ID
snapchat-ads-cli audit-logs ads AD_ID
snapchat-ads-cli audit-logs campaigns CAMPAIGN_ID --limit 100
```

The `entity-type` argument is passed directly to the API path. Common values: `organizations`, `adaccounts`, `campaigns`, `adsquads`, `ads`, `creatives`. Supports `--limit <n>` (default 50).

### Media & lenses

```bash
# List media files for an ad account
snapchat-ads-cli media ACCOUNT_ID
snapchat-ads-cli media ACCOUNT_ID --limit 100

# List AR lenses for an organization
snapchat-ads-cli lenses ORG_ID
snapchat-ads-cli lenses ORG_ID --limit 100
```

Both support `--limit <n>` (default 50).

### Estimates

```bash
# Get bid estimate for an ad account
snapchat-ads-cli bid-estimate ACCOUNT_ID --optimization-goal IMPRESSIONS

# Get estimated audience size for an ad account
snapchat-ads-cli audience-size ACCOUNT_ID

# Get event quality scores for a pixel
snapchat-ads-cli signal-readiness PIXEL_ID

# Get ad squad outcome configuration
snapchat-ads-cli ad-outcomes ADSQUAD_ID
```

`bid-estimate` has one optional option: `--optimization-goal <goal>` (e.g., `IMPRESSIONS`, `SWIPES`, `APP_INSTALLS`, `VIDEO_VIEWS`). The other estimate commands have no additional options.

## Workflow guidance

### When the user asks for a quick overview

1. Run `snapchat-ads-cli organizations` to find accessible organizations
2. Run `snapchat-ads-cli accounts ORG_ID` to list ad accounts
3. Use `campaign-stats` with a recent date range for a performance snapshot
4. Remember: divide all monetary values by 1,000,000 (micro-currency)

### When the user asks for deep analysis

1. Start with `campaign-stats` at `--granularity TOTAL` for overall performance
2. Switch to `--granularity DAY` to spot daily trends
3. Drill down with `adsquad-stats` and `ad-stats` for underperforming entities
4. Use `--fields` to focus on specific metrics
5. Add attribution windows (`--swipe-up-attribution-window`, `--view-attribution-window`) for conversion analysis
6. Cross-reference with `creatives` to review creative content

### When the user asks about delivery issues

1. Run `delivery-status campaigns CAMPAIGN_ID` to check campaign delivery
2. Drill into `delivery-status adsquads ADSQUAD_ID` for ad squad level issues
3. Check `delivery-status ads AD_ID` for ad-level problems
4. Review the ad squad and ad configurations with `adsquad` and `ad`

### When the user asks about audiences

1. Use `audiences ACCOUNT_ID` to list custom audience segments
2. Use `audience-size ACCOUNT_ID` for reach estimation
3. Use `audience-insights ACCOUNT_ID` for targeting insights
4. Use `pixel ACCOUNT_ID` to check pixel setup
5. Use `custom-conversions PIXEL_ID` to review custom conversion rules

### When the user asks about conversion tracking

1. Run `pixel ACCOUNT_ID` to find the Snap Pixel
2. Use `signal-readiness PIXEL_ID` to check event quality scores
3. Use `custom-conversions PIXEL_ID` to list custom conversion rules
4. Pull stats with `--conversion-source-types web,app` and attribution windows

### When the user asks about billing

1. Run `invoices ACCOUNT_ID` to list invoices for an ad account
2. Run `transactions ORG_ID` to list transactions for an organization
3. Run `funding-sources ORG_ID` to check funding sources
4. Run `billing-centers ORG_ID` to list billing centers

## Error handling

- **Authentication errors** -- ask the user to verify their access token; check that `SNAPCHAT_ADS_ACCESS_TOKEN` is set, `--credentials` points to a valid file, or `~/.config/snapchat-ads-cli/credentials.json` exists
- **Empty results** -- check that the parent entity ID is correct and that the entity has children (e.g., the ad account has campaigns)
- **Missing stats** -- verify the date range covers a period when the entity was active; check that `--start-time` and `--end-time` are in ISO 8601 format
- **Delivery status issues** -- use `delivery-status` to diagnose why an entity is not serving
- **Invalid entity-type** -- for `delivery-status` use `campaigns`, `adsquads`, or `ads`; for `audit-logs` use `campaigns`, `adsquads`, `ads`, or `creatives`.

All errors are written to stderr as JSON with an `error` field and a non-zero exit code:
```json
{"error": "Unauthorized"}
```

## API documentation references

- [snapchat-ads-cli documentation](https://github.com/Bin-Huang/snapchat-ads-cli)
- [Snapchat Marketing API overview](https://developers.snap.com/api/marketing-api/Ads-API)
- [Authentication](https://developers.snap.com/api/marketing-api/Ads-API/authentication)
- [Organizations](https://developers.snap.com/api/marketing-api/Ads-API/organizations)
- [Ad Accounts](https://developers.snap.com/api/marketing-api/Ads-API/ad-accounts)
- [Campaigns](https://developers.snap.com/api/marketing-api/Ads-API/campaigns)
- [Ad Squads](https://developers.snap.com/api/marketing-api/Ads-API/ad-squads)
- [Ads](https://developers.snap.com/api/marketing-api/Ads-API/ads)
- [Creatives](https://developers.snap.com/api/marketing-api/Ads-API/creatives)
- [Audience Segments](https://developers.snap.com/api/marketing-api/Ads-API/audience-creation)
- [Measurement / Stats](https://developers.snap.com/api/marketing-api/Ads-API/measurement)
- [Media](https://developers.snap.com/api/marketing-api/Ads-API/media)
- [Bid Estimates](https://developers.snap.com/api/marketing-api/Ads-API/bid-estimate)
- [Invoices](https://developers.snap.com/api/marketing-api/Ads-API/invoices)
- [Audit Logs](https://developers.snap.com/api/marketing-api/Ads-API/audit-logs)
- [Members & Roles](https://developers.snap.com/api/marketing-api/Ads-API/members)
