# skill-amazon-ads-reporter

## Description
Fetch Amazon Ads Sponsored Products campaign performance reports using a decoupled async pattern. Avoids timeout issues with the v3 Reporting API (2–10 min generation time) by splitting request and poll into separate steps. Also includes keyword-level winner/dead analysis and a quick bid inspector.

## Why two steps?
Amazon's Reporting API v3 is async — you request a report, get a `reportId`, and poll until it's ready. Doing this inline in a cron causes timeouts. The correct pattern:

```
request → save reportId → (wait 1-2 min) → poll + download
```

## Usage

### Campaign-level report (step-by-step, recommended for crons)
```bash
# Step 1: Request report — exits immediately with reportId
node scripts/request-report.js --days 7

# Step 2: Poll + download (run 1-2 min later, or from a separate cron)
node scripts/poll-report.js
```

### Campaign-level report (all-in-one, for manual runs)
```bash
node scripts/get-report.js --days 7
```

### Keyword-level winner/dead analysis (14-day async report)
```bash
node scripts/keyword-report.js
```
Output: table of all ENABLED keywords with clicks > 0 OR impressions ≥ 50 (winners), plus count of dead keywords (0 clicks, <50 imp).

### Quick bid inspector (live, across campaigns)
```bash
node scripts/get-bids.js
```
Output: all ENABLED + PAUSED keywords per campaign with current bids. Reads live data (no report needed).

## Arguments
| Arg | Default | Description |
|-----|---------|-------------|
| `--days N` | `7` | Number of days to include in report (campaign and keyword reports) |

## Configuration
Reads credentials from `AMAZON_ADS_PATH` env var, defaulting to `~/amazon-ads-api.json`.

### `amazon-ads-api.json` format
```json
{
  "refreshToken": "...",
  "lwaClientId": "...",
  "lwaClientSecret": "...",
  "profileId": "...",
  "region": "EU"
}
```

Regions: `EU` (default, includes UAE), `NA` (North America), `FE` (Far East).

## Output
- `~/.openclaw/workspace/tmp/amazon-report-pending.json` — created by request-report.js
- `~/.openclaw/workspace/tmp/amazon-report-latest.json` — created by poll-report.js after success
- Console table: Campaign | Impressions | Clicks | CTR% | Spend | Sales | ACOS%

## Report columns (campaign-level)
`campaignName`, `campaignId`, `impressions`, `clicks`, `spend`, `purchases7d`, `sales7d`

Paused campaigns are automatically filtered out by cross-referencing `GET /sp/campaigns/list`.

## Report columns (keyword-level — keyword-report.js)
`keywordId`, `keywordText`, `matchType`, `impressions`, `clicks`, `cost`, `purchases7d`, `sales7d`

## Dependencies
Node.js built-ins only (`https`, `zlib`, `fs`, `path`). No npm install required.

## Notes
- Access tokens expire — refresh via Amazon Login with Advertising if needed
- The `GZIP_JSON` format is gunzipped automatically by poll-report.js
- Reports are only available for the previous day and earlier (endDate = yesterday)
- `get-bids.js` uses the live v3 keyword list endpoint — no async report needed, instant response
- keyword-report.js uses the same async pattern as campaign reports (30s poll intervals, up to 10 min)
