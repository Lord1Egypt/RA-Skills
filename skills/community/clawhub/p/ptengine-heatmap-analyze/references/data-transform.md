# Data Transformation Reference

This document describes how to transform raw ptengine-cli output into the format expected by the
analysis prompt system.

## Table of Contents

1. [base_metric assembly](#base_metric-assembly)
2. [block_data assembly](#block_data-assembly)
3. [Field mapping](#field-mapping)
4. [Tag computation](#tag-computation)
5. [Rankings computation](#rankings-computation)
6. [Ad performance data assembly](#ad-performance-data-assembly)
7. [Audience analysis data assembly](#audience-analysis-data-assembly)

---

## base_metric assembly

Extract from page_metrics response → `data` object:

```json
{
  "visits": <integer>,
  "bounceRate": <decimal, e.g. 0.45>,
  "fvDropOffRate": <decimal>,
  "avgDuration": <milliseconds, e.g. 45000>,
  "clickRate": <decimal>,
  "ctaClickRate": <decimal>,
  "conversionsRate": <decimal>,
  "avgPageViews": <number>
}
```

All rates are decimals (0.0–1.0). The prompt system expects them as-is; conversion to percentages
happens only in natural-language output text.

---

## block_data assembly

Each block in block_metrics → `data` array gets enriched with Phase 3 results:

```json
{
  "block_id": "<string or integer, from API>",
  "block_index": <integer, 0-based position>,
  "block_name": "<string, from API>",
  "IS_FV": <0 or 1, 1 if block_index == 0>,
  "assigned_phase": <1-4, from Phase 3b>,
  "phase_name": "<string, from single_page_phase_names.json>",
  "module_category": "<string, from Phase 3a>",
  "contentSummary": "<string, from Phase 3a>",
  "impressionRate": <decimal>,
  "avgStayTime": <milliseconds>,
  "exitRate": <decimal>,
  "readingContributionRate": <decimal or null>,
  "avgStayTimeTag": "<High|Medium|Low>",
  "exitTag": "<High|Medium|Low>",
  "cvTag": "<High|Medium|Low or null>",
  "benchmark_fv": <decimal or null>,
  "rankings": {
    "stay_time": { "rank": <int>, "vs_median": <float>, "is_extreme": <bool>, "extreme_type": <string|null> },
    "exit_rate": { "rank": <int>, "vs_median": <float>, "is_extreme": <bool>, "extreme_type": <string|null> },
    "conversion": { "rank": <int>, "vs_median": <float>, "is_extreme": <bool>, "extreme_type": <string|null> }
  }
}
```

**Note**: `benchmark_fv` is the category benchmark for first-view drop-off rate, present only on
first-view blocks (IS_FV = 1). When available, use it to contextualize fvDropOffRate performance.

---

## Field mapping

ptengine-cli API fields may use different names than the prompt system expects. Apply these mappings:

### Page-level field mapping (page_metrics → base_metric)

**Core fields** (used in analysis):

| API field (ptengine-cli) | Analysis field | Notes |
|---|---|---|
| `visits` | `visits` | Same name |
| `fvRate` | `fvDropOffRate` | Rename — API name differs |
| `timeOnPage` | `avgDuration` | Rename — parse "Xm Ys" to milliseconds |
| `conversionRate` | `conversionsRate` | Rename — note trailing 's' |
| `bounceRate` | `bounceRate` | Same name |
| `clickRate` | `clickRate` | Same name |
| `ctaClickRate` | `ctaClickRate` | Same name |
| `avgPageViews` | `avgPageViews` | Same name |

**Supplementary fields** (available from API, use as context when helpful):

| API field | Usage | Notes |
|---|---|---|
| `pv` | Page views count | Total PV, not sessions — use `visits` for session count |
| `uv` | Unique visitors | Visitor count, can be used for context |
| `newVisitsRate` | New visitor percentage | Useful for audience composition context |
| `entrances` | Landing page entries | How many sessions started on this page |
| `clicks` | Total click count | Raw click count on the page |
| `ctaClicks` | CTA click count | Raw CTA click count |
| `completions` | Conversion completions | Raw conversion count (paired with conversionRate) |

These supplementary fields do not need renaming. Cite them in the report when they add useful
context (e.g. "6,324 sessions entered from this page as a landing page").

### Block-level field mapping (block_metrics → block_data)

**Core fields** (used in analysis):

| API field (ptengine-cli) | Analysis field | Notes |
|---|---|---|
| `impressionRate` | `impressionRate` | Same name |
| `dropoffRate` | `exitRate` | Rename — API uses dropoffRate |
| `avgDuration` | `avgStayTime` | Rename — block-level, parse "Xs" to milliseconds |
| `conversionRate` | `readingContributionRate` | Rename — block conversion = reading contribution |

**Metadata fields** (used for identification and enrichment):

| API field | Usage | Notes |
|---|---|---|
| `blockName` | Maps to `block_name` | Display name for the block |
| `screenshotUrl` | Reference only | URL to block screenshot, can be shown to user for context |
| `impression` | Raw impression count | Absolute number of PVs that saw this block |
| `dropoff` | Raw dropoff count | Absolute number of PVs that dropped off at this block |
| `completions` | Raw conversion count | Absolute number, paired with conversionRate |

When the API returns fields not listed above, pass them through unchanged.

### Value format parsing (critical — read carefully)

ptengine-cli returns ALL metric values as **formatted display strings**, not raw numbers. You must
parse them into numeric values before analysis. Getting this wrong will produce nonsensical results.

#### Parsing rules by format

**Percentage strings** (e.g. `"55.08%"`, `"0.00%"`, `"98.97%"`):
- Strip the `%` suffix, parse as float → this IS the percentage value
- For internal calculations: divide by 100 to get decimal (55.08% → 0.5508)
- For display in report: use the percentage directly ("55.1%")
- `"0.00%"` means zero or no data — handle as 0

**Number strings with commas** (e.g. `"6,777"`, `"4,984"`, `"30"`):
- Strip all commas, parse as integer
- `"0"` means zero visits/clicks — may indicate no data for this period

**Duration strings — page level** (`timeOnPage` field):
- Format: `"Xm Ys"` (e.g. `"3m 13s"`) or `"Xs"` (e.g. `"45s"`) or `"0s"`
- Parse: extract minutes and seconds → total seconds → multiply by 1000 for milliseconds
- `"3m 13s"` → 3×60 + 13 = 193 seconds → 193000 ms
- `"45s"` → 45 seconds → 45000 ms
- `"0s"` → 0 ms (no data or instant bounce)

**Duration strings — block level** (`avgDuration` field in block_metrics):
- Format: `"Xs"` (e.g. `"11s"`, `"3s"`, `"1s"`)
- Parse: strip `s`, parse as integer → multiply by 1000 for milliseconds
- `"11s"` → 11000 ms
- `"0s"` → 0 ms

**Decimal strings** (e.g. `"4.24"`):
- Parse as float directly

#### Display rules (when writing the analysis report)

When presenting metrics in the human-readable report:
- **Durations**: Show in seconds with unit. Under 60s: "11秒" / "11s" / "11秒". Over 60s: "3分13秒" / "3m 13s"
- **Rates**: Show as percentage with 1 decimal. "55.1%" not "0.551"
- **Counts**: Show with locale-appropriate formatting. "6,777" not "6777"
- **Always use the target-language metric label** from quality-constraints.md, never camelCase field names

#### All rate fields are percentage strings

`clickRate`, `ctaClickRate`, `bounceRate`, `fvRate`, `impressionRate`, `dropoffRate`,
`conversionRate`, `newVisitsRate` — all return as percentage strings (e.g. `"63.60%"`).
Parse the same way: strip `%`, use as percentage directly for display, divide by 100 for
internal decimal calculations.

#### Common pitfalls

- `timeOnPage` (page-level) uses `"Xm Ys"` format, but block-level `avgDuration` uses `"Xs"` — they look different
- A block showing `"0s"` dwell and `"0.00%"` exit likely has insufficient data — flag this
- API values like `"98.97%"` are already percentages — do NOT multiply by 100 again
- The `value` field is always a string; never assume it's a number

---

## Tag computation

Tags categorize blocks into High / Medium / Low performance tiers. Compute when not provided by API.

### Algorithm

For each metric (avgStayTime, exitRate, readingContributionRate):

1. Collect all block values for the metric (exclude null values)
2. Sort the values
3. Compute Q1 (25th percentile) and Q3 (75th percentile)
4. Assign tags:
   - **avgStayTimeTag**: >= Q3 → "High", <= Q1 → "Low", else "Medium"
   - **exitTag**: >= Q3 → "High" (bad), <= Q1 → "Low" (good), else "Medium"
   - **cvTag**: >= Q3 → "High", <= Q1 → "Low", else "Medium". Set to null if readingContributionRate is null.

Note: For exitRate, "High" means high exit (bad performance). This is counter-intuitive but
consistent with how the prompt system interprets tags.

---

## Rankings computation

Rankings compare blocks against each other and the median.

### Algorithm

For each of the three ranking dimensions:

#### stay_time (higher = better, rank 1 = longest dwell)
1. Sort blocks by avgStayTime descending
2. Assign rank 1..N
3. Compute median avgStayTime
4. `vs_median` = (block_avgStayTime - median) / median
5. `is_extreme` = true if in top 10% or bottom 10% of blocks
6. `extreme_type` = "top" if top 10% (longest dwell = best), "bottom" if bottom 10% (shortest = worst), null otherwise

#### exit_rate (lower = better, rank 1 = lowest exit)
1. Sort blocks by exitRate ascending
2. Assign rank 1..N
3. Compute median exitRate
4. `vs_median` = (block_exitRate - median) / median
5. `is_extreme` = true if in top 10% or bottom 10%
6. `extreme_type` = "top" if bottom 10% of exit values (lowest exit = best), "bottom" if top 10% of exit values (highest exit = worst), null otherwise

**Critical**: For exit_rate, `extreme_type: "bottom"` means the block with the HIGHEST exit rate =
most problematic. Do NOT read "bottom" as "low exit rate".

#### conversion (higher = better, rank 1 = highest contribution)
1. Sort blocks by readingContributionRate descending (null values get worst rank)
2. Same logic as stay_time

---

## Ad performance data assembly

Transform page_insight sourceType/UTM data into the format expected by `references/ad-performance.md`.

### Target format

```json
{
  "ad_data": {
    "<source_name>": {
      "visits": <integer>,
      "bounceRate": <decimal>,
      "avgDuration": <milliseconds>,
      "clickRate": <decimal>,
      "ctaClickRate": <decimal>,
      "conversions": [
        {
          "conversionName": "<name>",
          "completions": <integer>,
          "conversionRate": <decimal>
        }
      ],
      "quadrant": "<Q1|Q2|Q3|Q4|concentrated>"
    }
  },
  "quadrantThresholds": {
    "visitsThreshold": <average visits across sources>,
    "qualityThreshold": <average conversionRate across sources>
  },
  "language": "<CHINESE|ENGLISH|JAPANESE>"
}
```

### Quadrant computation

1. Compute `visitsThreshold` = mean(visits) across all sources
2. Compute `qualityThreshold` = mean(conversionRate) across all sources
3. For each source:
   - If this source has >95% of total visits → `"concentrated"`
   - If visits >= threshold AND cvr >= threshold → `"Q1"`
   - If visits < threshold AND cvr >= threshold → `"Q2"`
   - If visits >= threshold AND cvr < threshold → `"Q3"`
   - If visits < threshold AND cvr < threshold → `"Q4"`

---

## Audience analysis data assembly

Same structure as ad_performance, but keyed by segment name instead of ad source.

### Target format

```json
{
  "audience_data": {
    "<segment_name>": {
      "visits": <integer>,
      "bounceRate": <decimal>,
      "avgDuration": <milliseconds>,
      "clickRate": <decimal>,
      "conversions": [...],
      "quadrant": "<Q1|Q2|Q3|Q4|concentrated>"
    }
  },
  "quadrantThresholds": {
    "visitsThreshold": <average>,
    "qualityThreshold": <average>
  },
  "language": "<CHINESE|ENGLISH|JAPANESE>"
}
```

### Segment key reference

Common segment keys from page_insight visitType/terminalType:
- `newVisitor` / `returningVisitor`
- `NonBounceVisits` / `BounceVisits`
- `Campaign` / `Direct` / `Organic`
- Device names (Android, iOS, Desktop, etc.)
- Geographic regions

These keys appear as-is in the data. The analysis prompt handles translation to the target language.

---

## Compare task: multi-segment data structure

For compare analysis, each segment needs its own set of base_metric and block_data:

```json
{
  "segments": [
    {
      "index": 0,
      "description": "<segment label, e.g. 'New Visitors'>",
      "base_metric": { ... },
      "block_data": [ ... ]
    },
    {
      "index": 1,
      "description": "<segment label, e.g. 'Returning Visitors'>",
      "base_metric": { ... },
      "block_data": [ ... ]
    }
  ],
  "language": "<CHINESE|ENGLISH|JAPANESE>"
}
```

Fetch page_metrics and block_metrics separately for each segment using `--filter` flag:
```bash
# Segment 1: New visitors
ptengine-cli heatmap query --query-type block_metrics \
  --url "<URL>" --start-date <START> --end-date <END> \
  --device-type MOBILE --filter "visitType include newVisitor" --output json

# Segment 2: Returning visitors
ptengine-cli heatmap query --query-type block_metrics \
  --url "<URL>" --start-date <START> --end-date <END> \
  --device-type MOBILE --filter "visitType include returningVisitor" --output json
```
