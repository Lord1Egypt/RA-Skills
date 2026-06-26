# ptengine-cli Command Reference

ptengine-cli is a CLI tool for querying Ptengine heatmap analytics data via their Open API.

## Installation

```bash
# Via official install script (recommended)
curl -sSL https://raw.githubusercontent.com/Kocoro-lab/ptengine-cli/v0.1.0/scripts/install.sh | sh

# Or use the project's wrapper
sh install.sh
```

## Configuration

```bash
# Set credentials
ptengine-cli config set --api-key <KEY> --profile-id <PROFILE_ID>

# View current config (API key is masked)
ptengine-cli config show
```

Config file location: `~/.config/ptengine-cli/config.yaml`

Configuration priority (highest → lowest):
1. Command-line flags (`--api-key`, `--profile-id`)
2. Environment variable (`PTENGINE_API_KEY`)
3. Config file

## Global Flags

| Flag | Description |
|------|-------------|
| `--api-key` | API authentication key |
| `--base-url` | API endpoint (default: `https://xbackend.ptengine.com`) |
| `--output, -o` | Output format: `json` (default), `json-pretty`, `table` |

---

## Commands

### heatmap query

Fetch analytics data from Ptengine.

```bash
ptengine-cli heatmap query \
  --query-type <type> \
  --url <page-url> \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  [options]
```

#### Query Types

| Type | Description | Device constraint |
|------|-------------|-------------------|
| `page_metrics` | Page-level aggregates (visits, bounceRate, conversionsRate, etc.) | Any (ALL OK) |
| `page_insight` | Page metrics grouped by dimension (requires --fun-name) | Any (ALL OK) |
| `block_metrics` | Per-block performance (impressionRate, exitRate, avgStayTime, etc.) | **PC or MOBILE only** |
| `element_metrics` | Per-element interaction (click, conversion) | **PC or MOBILE only** |

#### Options

| Flag | Description |
|------|-------------|
| `--query-type` | Required. One of: page_metrics, page_insight, block_metrics, element_metrics |
| `--url` | Required. Target page URL |
| `--start-date` | Required. Start date (YYYY-MM-DD) |
| `--end-date` | Required. End date (YYYY-MM-DD) |
| `--profile-id` | Site identifier (8-char hex; defaults to config) |
| `--device-type` | ALL, PC, MOBILE, or TABLET. **block_metrics and element_metrics cannot use ALL** |
| `--metrics` | Specific metrics to return (comma-separated) |
| `--conversion-names` | Conversion goal names (fuzzy match) |
| `--fun-name` | Grouping dimension for page_insight (see below) |
| `--filter` | Repeatable filter: `--filter "name include\|exclude val1,val2"` |
| `--filter-json` | Alternative JSON array format for complex filters |

#### fun-name Values (for page_insight)

| Value | Groups by |
|-------|-----------|
| `sourceType` | Traffic source |
| `visitType` | Visit classification (new/returning) |
| `terminalType` | Device type |
| `utmSource` | UTM source parameter |
| `utmMedium` | UTM medium parameter |
| `utmCampaign` | UTM campaign parameter |
| `week` | Weekly aggregation |
| `day` | Daily aggregation |

### heatmap filter-values

Discover available filter values for a given dimension.

```bash
ptengine-cli heatmap filter-values \
  --name <filter-name> \
  --profile-id <ID> \
  [--start-date YYYY-MM-DD] \
  [--end-date YYYY-MM-DD] \
  [--search <term>]
```

Note: `--name` is a required flag (not a positional argument).

### heatmap describe

View API schema (no API key required).

```bash
ptengine-cli heatmap describe [--query-type <type>]
```

### config set / config show

```bash
ptengine-cli config set --api-key <KEY> --profile-id <ID>
ptengine-cli config show
```

### version

```bash
ptengine-cli version
```

---

## Response Format

All query responses are wrapped in a structured envelope:

```json
{
  "success": true,
  "data": { ... },
  "meta": { ... },
  "error": null,
  "rateLimit": {
    "limitPerMinute": 60,
    "remainingMinute": 55,
    "limitPerDay": 10000,
    "remainingDay": 9990
  }
}
```

On error:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 4010,
    "message": "Invalid API key",
    "hint": "Check your API key with: ptengine-cli config show"
  }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Validation error (missing params) |
| 2 | Authentication error |
| 3 | Invalid parameters |
| 4 | Rate limit exceeded |
| 5 | Server error |
| 6 | Network error |

## Common Examples

```bash
# Page metrics for last 30 days
ptengine-cli heatmap query --query-type page_metrics \
  --url "https://example.com/lp" \
  --start-date 2026-03-17 --end-date 2026-04-16 \
  --output json-pretty

# Block metrics for mobile
ptengine-cli heatmap query --query-type block_metrics \
  --url "https://example.com/lp" \
  --start-date 2026-03-17 --end-date 2026-04-16 \
  --device-type MOBILE --output json-pretty

# Traffic source insights
ptengine-cli heatmap query --query-type page_insight \
  --url "https://example.com/lp" \
  --fun-name sourceType \
  --start-date 2026-03-17 --end-date 2026-04-16 \
  --output json-pretty

# Block metrics filtered by new visitors
ptengine-cli heatmap query --query-type block_metrics \
  --url "https://example.com/lp" \
  --start-date 2026-03-17 --end-date 2026-04-16 \
  --device-type MOBILE \
  --filter "visitType include newVisitor" \
  --output json-pretty

# Discover available countries
ptengine-cli heatmap filter-values --name country --search "japan"

# View available metrics for block queries
ptengine-cli heatmap describe --query-type block_metrics
```
