# eo-traffic-daily-report

Periodically query L7/L4 traffic trends and automatically generate Markdown daily reports with bandwidth peaks, request counts, top domains, and top regions. Supports multi-day trend comparison and per-domain multi-dimensional drill-down analysis (country, province, IP, UA, status code, URL path, referer, etc.).

## APIs Involved

| Action | Description |
|---|---|
| DescribeTimingL7AnalysisData | Query L7 time-series traffic/bandwidth/request data |
| DescribeTopL7AnalysisData | Query L7 top domains, top regions, and other dimensional ranking data |
| DescribeTimingL4Data | Query L4 time-series traffic/bandwidth/connection data |

> **Command usage**: This document only lists API names and workflow guidance.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm complete parameters and response descriptions.
> For full filter condition documentation, see [Metric Analysis Filter Conditions](https://edgeone.ai/document/56985).

### DescribeTopL7AnalysisData Available Dimensions

`MetricName` determines the statistical dimension. Below is the complete dimension list:

| Dimension | Traffic MetricName | Request MetricName | Return Value Meaning |
|---|---|---|---|
| Domain | `l7Flow_outFlux_domain` | `l7Flow_request_domain` | Domain name (e.g. `example.com`) |
| Country/Region | `l7Flow_outFlux_country` | `l7Flow_request_country` | ISO 3166-1 alpha-2 country code (e.g. `CN`, `US`) |
| Province (Mainland China) | `l7Flow_outFlux_province` | `l7Flow_request_province` | Tencent Cloud province code (see mapping table below) |
| Status Code | `l7Flow_outFlux_statusCode` | `l7Flow_request_statusCode` | HTTP status code (e.g. `200`, `404`, `503`) |
| URL Path | `l7Flow_outFlux_url` | `l7Flow_request_url` | Request path (e.g. `/api/v1/data`) |
| Referer | `l7Flow_outFlux_referers` | `l7Flow_request_referers` | Referer source page |
| Client IP | `l7Flow_outFlux_sip` | `l7Flow_request_sip` | Client source IP address |
| User-Agent | `l7Flow_outFlux_ua` | `l7Flow_request_ua` | Full UA string |
| Device Type | `l7Flow_outFlux_ua_device` | `l7Flow_request_ua_device` | Device type (e.g. Mobile, Desktop) |
| Browser Type | `l7Flow_outFlux_ua_browser` | `l7Flow_request_ua_browser` | Browser type (e.g. Chrome, Safari) |
| OS | `l7Flow_outFlux_ua_os` | `l7Flow_request_ua_os` | Operating system (e.g. Windows, iOS) |
| Resource Type | `l7Flow_outFlux_resourceType` | `l7Flow_request_resourceType` | Resource type (e.g. html, jpg, js) |

> **Usage tips**:
> - When drilling down into a domain, select dimension combinations as needed — no need to query all dimensions at once
> - Common combinations: Country + Province + IP (locate traffic sources), Status Code + URL Path (locate abnormal requests), Referer (analyze traffic entry points), UA (identify client types)

## Data Conventions

When processing EdgeOne data analysis API responses and generating reports, the following conventions must be observed:

### Unit Conversion: Base-1000 (SI Standard)

EdgeOne uniformly uses **base-1000** (SI standard), consistent with networking/storage industry conventions:

| Source Unit | Conversion | Target Unit |
|---|---|---|
| Byte | ÷ 1,000 | KB |
| KB | ÷ 1,000 | MB |
| MB | ÷ 1,000 | GB |
| bps | ÷ 1,000 | Kbps |
| Kbps | ÷ 1,000 | Mbps |
| Mbps | ÷ 1,000 | Gbps |

> **Never use base-1024**. All traffic and bandwidth values in output reports must use base-1000 conversion.

### Timestamp Left-Alignment Rule

API time-series data points use **timestamp left-alignment**: a data point at timestamp `T` represents aggregated data for the interval **[T, T + interval)**.

For example, when querying with `day` granularity, timestamp `2026-03-23T00:00:00+08:00` represents the full day of **03-23 (00:00 – next day 00:00)**.

### Full Data vs Post-Mitigation Data

L7 access data query APIs (`DescribeTimingL7AnalysisData`, `DescribeTopL7AnalysisData`) **return post-mitigation clean traffic/request counts by default** (i.e., excluding requests blocked/challenged by the Web Security module).

- When generating **data reports** (daily, weekly, trend analysis, etc.), provide **complete full data** by including both mitigated and non-mitigated data in `Filters`:

```
--Filters '[{"Key":"mitigatedByWebSecurity","Operator":"equals","Value":["yes","no"]}]'
```

- Only filter by mitigation status when the user explicitly requests clean traffic or blocked traffic only.

> `mitigatedByWebSecurity` accepts: `yes` (blocked/challenged by Web Security module), `no` (normal requests not mitigated).
> Multiple values within the same filter key use **Or** logic; different filter keys use **And** logic.

### Domain Filtering

In `DescribeTimingL7AnalysisData` and `DescribeTopL7AnalysisData`, use the `domain` key in `Filters` to filter data for a specific domain:

```
--Filters '[{"Key":"domain","Operator":"equals","Value":["example.com"]},{"Key":"mitigatedByWebSecurity","Operator":"equals","Value":["yes","no"]}]'
```

> Note: `domain` filter and `mitigatedByWebSecurity` filter must be passed together (different keys use And logic).

### Country/Region Codes

The country/region dimension returns [ISO 3166-1 alpha-2](https://www.iso.org/iso-3166-country-codes.html) standard codes. Common mappings:

| Code | Country/Region | Code | Country/Region | Code | Country/Region |
|---|---|---|---|---|---|
| CN | China | US | United States | JP | Japan |
| KR | South Korea | SG | Singapore | DE | Germany |
| GB | United Kingdom | FR | France | AU | Australia |
| CA | Canada | BR | Brazil | IN | India |
| RU | Russia | ID | Indonesia | TH | Thailand |

> Refer to the ISO 3166-1 standard for the complete code table. Reports should display both the code and the country name.

### Province Code Mapping (Mainland China)

The province dimension returns Tencent Cloud internal province codes (integers) that must be mapped to province names. `-1` indicates overseas.
For complete mapping, refer to [Tencent Cloud Region/ISP Mappings](https://www.tencentcloud.com/document/product/228/6316#region.2Fisp-mappings). Common mappings:

| Code | Province | Code | Province | Code | Province | Code | Province |
|---|---|---|---|---|---|---|---|
| -1 | Overseas | 22 | Beijing | 1050 | Shanghai | 4 | Guangdong |
| 1442 | Zhejiang | 120 | Jiangsu | 121 | Anhui | 122 | Shandong |
| 2 | Fujian | 1135 | Hubei | 1465 | Jiangxi | 1466 | Hunan |
| 182 | Henan | 1177 | Hebei | 1051 | Chongqing | 1068 | Sichuan |
| 153 | Yunnan | 118 | Guizhou | 173 | Guangxi | 1441 | Hainan |
| 86 | Inner Mongolia | 1469 | Shanxi | 1464 | Liaoning | 1445 | Jilin |
| 1467 | Heilongjiang | 1468 | Tianjin | 145 | Gansu | 1076 | Ningxia |
| 119 | Qinghai | 152 | Xinjiang | | | | |

> Reports must map codes to province names; never output raw numeric codes.

### IP Segment Aggregation

When querying by client IP (`_sip`) dimension, the top IP list typically contains multiple IPs from the same /24 segment. Reports should include **IP segment aggregation analysis**:
- Aggregate IPs sharing the same /24 prefix (first 3 octets)
- Show total traffic and IP count per /24 segment
- Helps identify NAT gateways, CDN origin IP pools, proxy clusters, etc.

### Adaptive Traffic Unit Display

Traffic values in reports should automatically select appropriate units based on magnitude:

| Condition | Display Format | Example |
|---|---|---|
| ≥ 1 GB (10⁹ Byte) | `xx.xx GB` | 10.39 GB |
| ≥ 1 MB (10⁶ Byte) | `xxx.xx MB` | 138.44 MB |
| ≥ 1 KB (10³ Byte) | `xxx.xx KB` | 716.78 KB |
| < 1 KB | `xxx B` | 494 B |

### Large Number Abbreviation by Language

Request counts and other large numbers should be abbreviated differently based on the **report language context**:

#### Chinese Context (中文语境)

Use Chinese numeric units (万 / 亿):

| Condition | Display Format | Example |
|---|---|---|
| ≥ 1 亿 (10⁸) | `x.xx 亿` | 302,000,000 → `3.02 亿` |
| ≥ 1 万 (10⁴) | `x.xx 万` | 53,581 → `5.36 万` |
| < 1 万 | raw number with comma separator | 8,192 |

> **Rules**:
> - Always use `万` (10⁴) and `亿` (10⁸) as abbreviation tiers — never use `千` (K) in Chinese reports
> - Keep 2 decimal places; trailing zeros may be omitted (e.g. `5.30 万` → `5.3 万`)
> - Examples: `1,592,166 次` → `159.22 万次`, `53,581,130 次` → `5,358.11 万次`, `312,000,000 次` → `3.12 亿次`

#### English Context

Use standard K / M / B suffixes (base-1000):

| Condition | Display Format | Example |
|---|---|---|
| ≥ 1 B (10⁹) | `x.xx B` | 3,020,000,000 → `3.02 B` |
| ≥ 1 M (10⁶) | `x.xx M` | 5,358,113 → `5.36 M` |
| ≥ 1 K (10³) | `x.xx K` | 53,581 → `53.58 K` |
| < 1 K | raw number | 812 |

> **Rules**:
> - K = 10³, M = 10⁶, B = 10⁹ (base-1000, consistent with SI convention)
> - Keep 2 decimal places; trailing zeros may be omitted
> - Examples: `1,592,166 requests` → `1,592.17 K`, `5,358,113 requests` → `5.36 M`

#### Language Detection

- If the user communicates in Chinese or requests a Chinese report → use 万/亿
- If the user communicates in English or requests an English report → use K/M/B
- When in doubt, match the language used in the user's most recent message

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli`. If no credentials are configured in the environment, guide the user to log in first:

```sh
tccli auth login
```

> The terminal will print an authorization link and block until the user completes browser authorization; the command exits automatically upon success.
> Never ask the user for `SecretId` / `SecretKey`, and never execute commands that might expose credential contents.

2. A ZoneId must be obtained first. Refer to `../api/zone-discovery.md`.

3. Obtain the account UIN for report headers by calling:

```sh
tccli cam GetUserAppId
```

> The response contains `Uin` (current operator), `OwnerUin` (root account), and `AppId`.
> - Use **`OwnerUin`** as the account identifier displayed in reports (this is the Tencent Cloud root account UIN).
> - Do **not** use `AppId` (returned in data API responses as `TypeKey`) — it is an internal numeric ID, not the user-facing account identifier.

## Scenario A: Generate a Traffic Daily Report for a Specific Date

**Trigger**: The user says "generate yesterday's traffic report", "what was the peak bandwidth in the last 24 hours", "generate the traffic report for 2026-03-20", "analyze which countries/IPs/UAs the traffic for example.com comes from", "show me the status code distribution for this domain".

### Workflow

**Step 1**: Determine the report date range

- If the user says "yesterday" / "today", automatically calculate the corresponding start and end times (ISO 8601 format)
- Default time range is "yesterday 00:00 to 23:59"
- `DescribeTimingL7AnalysisData` has approximately 10-minute data delay; avoid querying the most recent 10 minutes

**Step 2**: Collect L7 time-series data

Call `DescribeTimingL7AnalysisData` to query the following metrics:
- `l7Flow_outFlux`: EdgeOne response traffic, in Bytes (for total traffic calculation)
- `l7Flow_outBandwidth`: EdgeOne response bandwidth, in bps (for peak bandwidth calculation)
- `l7Flow_request`: Access request count, in requests (for total request count)
- Recommend using `hour` granularity (`Interval=hour`) to identify peak periods
- **Must** include `Filters` for full data (see "Data Conventions > Full Data vs Post-Mitigation Data")

**Step 3**: Collect L7 Top data

Call `DescribeTopL7AnalysisData` to query:
- `l7Flow_outFlux_domain`: Response traffic Top by domain (default Top 10)
- `l7Flow_outFlux_country`: Traffic Top by country/region (default Top 5)
- Increase `Limit` parameter if the zone has many domains
- **Must** include `Filters` for full data (see "Data Conventions > Full Data vs Post-Mitigation Data")

**Step 4**: Collect L4 time-series data (if L4 proxy is enabled)

Call `DescribeTimingL4Data` to query:
- `l4Flow_outBandwidth`: Outbound bandwidth peak
- `l4Flow_connections`: Concurrent connections
- If the zone does not use L4 proxy, skip this step and note it in the report

**Step 5**: Compile and generate the Markdown daily report

Organize the above data into a structured report containing: bandwidth peak (with peak period), total request count, top domain table, top region table, and L4 data summary.

**Output recommendation**: Output as a complete Markdown document with title, time range, key metric summary, and detailed tables.

### Domain Drill-Down: Multi-Dimensional Traffic Distribution Analysis

**Trigger**: After viewing a daily/weekly report, the user requests further analysis of a specific domain's traffic distribution, e.g. "show which countries the traffic for example.com comes from", "analyze the visitor IPs and UAs for this domain", "what abnormal status codes does this domain have".

> This sub-workflow is an on-demand extension of Scenario A / B, invoked when the user needs deep analysis of a specific domain.

**Step 1**: Confirm drill-down parameters

- **Target domain**: Selected from user input or the previous step's top domain ranking
- **Time range**: Inherit the current report's time range, or as specified by the user
- **Analysis dimensions**: Select based on user needs. Common combinations:

| Analysis Purpose | Recommended Dimensions |
|---|---|
| Traffic source analysis | Country/Region (`_country`) + Province (`_province`) + Client IP (`_sip`) |
| Client profiling | User-Agent (`_ua`) + Device Type (`_ua_device`) + Browser (`_ua_browser`) + OS (`_ua_os`) |
| Request pattern analysis | Status Code (`_statusCode`) + URL Path (`_url`) + Referer (`_referers`) |
| Resource type analysis | Resource Type (`_resourceType`) |
| Full profile | All of the above as needed |

> No need to query all dimensions at once — select based on user focus. If the user says "full analysis", recommend: Country + Province + IP + UA + Status Code + URL Path + Referer.

**Step 2**: Collect Top data by dimension

For each selected dimension, call `DescribeTopL7AnalysisData`:
- **Must** include both `domain` filter and `mitigatedByWebSecurity` full-data filter in `Filters`
- Choose between traffic metrics and request count metrics as needed (typically prioritize traffic metrics `l7Flow_outFlux_*`; supplement with request metrics `l7Flow_request_*` when necessary)
- Recommend setting `Limit` to 20; adjust based on user needs
- Dimension queries can be executed in parallel for efficiency

**Step 3**: Collect domain time-series summary data (optional)

Call `DescribeTimingL7AnalysisData` with `domain` filter in `Filters` to query the domain's traffic, bandwidth, and request count totals as core report metrics.

**Step 4**: Data post-processing

- **Province code mapping**: Convert Tencent Cloud province codes to province names (see "Data Conventions > Province Code Mapping")
- **Country code annotation**: Append country names alongside ISO 3166-1 alpha-2 codes
- **IP segment aggregation**: Merge IPs in the same /24 segment (see "Data Conventions > IP Segment Aggregation")
- **Status code classification**: Group by 2xx/3xx/4xx/5xx categories. Note that EdgeOne uses custom status codes in the 520-599 range (e.g., 566 for managed rule blocks, 567 for custom rule/rate limiting/bot management blocks). See [Abnormal Status Code Reference](https://edgeone.ai/document/58009) for full details
- **UA classification**: Identify primary client types (e.g. Dart apps, crawlers, browsers, etc.)

**Step 5**: Generate traffic distribution report

Output the report following the "Output Format > Domain Drill-Down" template below, including core metrics + per-dimension Top tables + comprehensive insights.

## Scenario B: Multi-Day Trend Comparison

**Trigger**: The user says "compare the traffic trend over the last 7 days", "how has bandwidth changed this week vs last week", "what are the daily request counts for the past week".

### Workflow

**Step 1**: Determine the comparison time range

- Parse the user-described time range and calculate start/end times
- `DescribeTimingL7AnalysisData` supports a maximum of 31 days per query

**Step 2**: Collect multi-day aggregated data

Call `DescribeTimingL7AnalysisData` with `day` granularity (`Interval=day`) to query:
- `l7Flow_outFlux`: Daily response traffic (for total and trend calculation)
- `l7Flow_outBandwidth`: Daily bandwidth peak
- `l7Flow_request`: Daily total requests
- **Must** include `Filters` for full data (see "Data Conventions > Full Data vs Post-Mitigation Data")
- When not specifying `ZoneIds` (or passing `["*"]`), account-level aggregated data is returned

**Step 2.1**: Collect L7 Top data (optional but recommended)

Call `DescribeTopL7AnalysisData` to query Top domains by response traffic:
- When not specifying `ZoneIds` (or passing `["*"]`), account-level aggregated data is returned; specify individual ZoneIds to filter by zone
- **Must** include `Filters` for full data

**Step 3**: Calculate trend metrics

For each day's data, calculate:
- Day-over-day change rate (percentage change compared to previous day)
- Week-over-week change rate (if time range exceeds 7 days)
- Peak day and trough day markers

**Output recommendation**: Output as a trend table including date, bandwidth peak, day-over-day change, total requests, day-over-day change, with peak day and anomaly markers.

## Output Format

### Scenario A: Daily Traffic Report

```markdown
## Traffic Daily Report — <Date>

**Account**: <OwnerUin>
**Zone**: <zone name> (ZoneId: <zone-id>)
**Report Time Range**: <start time> – <end time>

### Key Metrics

| Metric | Value | Peak Period |
|---|---|---|
| L7 Total Response Traffic | x.xx GB | — |
| L7 Peak Bandwidth | x.xx Mbps | HH:MM |
| L7 Total Requests | x,xxx K / x.xx 万 | — |
| L4 Peak Bandwidth | x.xx Mbps | HH:MM |
| L4 Peak Concurrent Connections | x,xxx | HH:MM |

### Top N Domains (by Traffic)

| Domain | Traffic | Share |
|---|---|---|
| ... | ... | ... |

### Top 5 Regions (by Traffic)

| Region | Traffic | Share |
|---|---|---|
| ... | ... | ... |
```

### Domain Drill-Down: Traffic Distribution Analysis

```markdown
## Traffic Distribution Report — <Domain>

**Account**: <OwnerUin>
**Domain**: <domain>
**Report Date**: <date> (<day of week>)
**Data Type**: Full data (including requests mitigated by Web Security)
**Unit Conversion**: Base-1000 (SI standard)

---

### Key Metrics

| Metric | Value |
|---|---|
| Total Response Traffic | **xx.xx GB** |

---

### Distribution by Country/Region (Top N)

| Rank | Country Code | Country/Region | Traffic | Share |
|---|---|---|---|---|
| 1 | XX | <country name> | xx.xx GB | xx.xx% |
| ... | ... | ... | ... | ... |

**Analysis**: <summarize traffic geographic concentration>

---

### Distribution by Province (Mainland China + Overseas)

| Rank | Province | Traffic | Share |
|---|---|---|---|
| 1 | Overseas | xx.xx GB | xx.xx% |
| 2 | <province name> | xxx.xx MB | x.xx% |
| ... | ... | ... | ... |

**Analysis**: <summarize domestic vs overseas traffic ratio>

---

### Distribution by Client IP (Top N)

**IP Segment Aggregation**:

| IP Segment | Total Traffic | IP Count |
|---|---|---|
| x.x.x.0/24 | xxx.xx MB | x IPs |
| ... | ... | ... |

**IP Details**:

| Rank | Client IP | Traffic | Share |
|---|---|---|---|
| 1 | x.x.x.x | xx.xx MB | x.xx% |
| ... | ... | ... | ... |

**Analysis**: <analyze IP segment clustering patterns, such as NAT gateways, proxy pools, etc.>

---

### Distribution by User-Agent (Top N)

| Rank | User-Agent | Traffic | Share |
|---|---|---|---|
| 1 | <UA string> | xx.xx GB | xx.xx% |
| ... | ... | ... | ... |

**Analysis**: <identify primary client types, such as app SDKs, crawlers, browsers>

---

### Distribution by Status Code (Top N)

**Status Code Category Summary**:

| Category | Traffic | Share | Description |
|---|---|---|---|
| 2xx | xx.xx GB | xx.xx% | Success |
| 3xx | xxx.xx MB | x.xx% | Redirect |
| 4xx | xxx.xx MB | x.xx% | Client Error |
| 5xx | xxx.xx MB | x.xx% | Server Error |

**Status Code Details**:

| Rank | Status Code | Traffic | Share |
|---|---|---|---|
| 1 | 200 | xx.xx GB | xx.xx% |
| 2 | 304 | xxx.xx MB | x.xx% |
| ... | ... | ... | ... |

**Analysis**: <flag abnormal status code ratios; if 4xx/5xx is disproportionately high, investigate further. For EdgeOne custom status codes (520-599), see [Abnormal Status Code Reference](https://edgeone.ai/document/58009) for details>

---

### Distribution by URL Path (Top N)

| Rank | URL Path | Traffic | Share |
|---|---|---|---|
| 1 | /path/to/resource | xx.xx GB | xx.xx% |
| ... | ... | ... | ... |

**Analysis**: <identify hot paths and large file downloads>

---

### Distribution by Referer (Top N)

| Rank | Referer | Traffic | Share |
|---|---|---|---|
| 1 | https://example.com/page | xx.xx GB | xx.xx% |
| 2 | (empty Referer) | xxx.xx MB | x.xx% |
| ... | ... | ... | ... |

**Analysis**: <analyze traffic entry points, identify external links and direct access>

---

### Comprehensive Insights

1. **Traffic source characteristics**: <summarize geographic distribution and concentration>
2. **Client characteristics**: <summarize primary UA and access patterns>
3. **Request characteristics**: <summarize status code health, hot paths>
4. **Areas of concern**: <list anomalies requiring further investigation>
```

> **Domain drill-down template usage notes**:
> - Dimension sections are optional; include only the dimensions actually queried, omit the rest
> - The "Analysis" paragraph after each dimension table is mandatory — do not list data without analysis
> - Status code dimension must output both "Category Summary" and "Details" tables
> - IP dimension must output both "IP Segment Aggregation" and "IP Details" tables
> - "Comprehensive Insights" is mandatory and must synthesize findings across multiple dimensions

### Scenario B: Multi-Day Trend Comparison

```markdown
## Traffic Trend Report — <Start Date> – <End Date>

**Account**: <OwnerUin>
**Report Time Range**: <start time> – <end time> (UTC+8)
**Data Granularity**: Day
**Data Type**: Full data (including requests mitigated by Web Security)
**Unit Conversion**: Base-1000 (SI standard)

---

### Key Metrics Summary

| Metric | Value |
|---|---|
| L7 Total Response Traffic | **xx.xx GB** |
| L7 Peak Bandwidth | **x.xx Mbps** (<peak date> <day of week>) |
| L7 Total Requests | **x,xxx.xx K** |

---

### Daily Traffic Trend

| Date | Response Traffic | DoD Change | Peak Bandwidth | DoD Change | Total Requests | DoD Change | Notes |
|---|---|---|---|---|---|---|---|
| MM-DD (Day) | xx.xx GB | — | x.xx Mbps | — | xxx.xx K / x.xx 万 | — | 📈 Highest traffic day |
| MM-DD (Day) | xx.xx GB | ±x.x% | x.xx Mbps | ±x.x% | xxx.xx K / x.xx 万 | ±x.x% | |
| ... | ... | ... | ... | ... | ... | ... | |
| MM-DD (Day) | xx.xx GB | ±x.x% | x.xx Mbps | ±x.x% | xxx.xx K / x.xx 万 | ±x.x% | 📉 Lowest traffic day |
| MM-DD (Day) | xx.xx GB | ±x.x% | x.xx Mbps | ±x.x% | xxx.xx K / x.xx 万 | ±x.x% | ⚠️ Peak bandwidth day |

**Trend Analysis**:
- <describe overall traffic trend patterns, such as weekday/weekend differences>
- <flag anomalous fluctuations and analyze possible causes, e.g. bandwidth peak DoD far exceeding traffic growth indicates short bursts>
- <describe correlation between request volume and traffic trends>

---

### Top N Domains (by Response Traffic)

| Rank | Domain | Traffic | Share |
|---|---|---|---|
| 1 | example.com | xx.xx GB | xx.xx% |
| 2 | cdn.example.com | xxx.xx MB | x.xx% |
| ... | ... | ... | ... |

**Domain Analysis**:
- <identify high-traffic domains and their share>
- <group domains by category, such as subdomains of the same site, test domains, etc.>
- <flag anomalous or noteworthy domains>
```

> **Template usage notes**:
> - Date column format: `MM-DD (Day)`, annotate dates according to the timestamp left-alignment rule
> - DoD change: first day shows "—", subsequent days calculate `(current - previous) / previous × 100%`
> - Notes column markers: 📈 Highest traffic day, 📉 Lowest traffic day, ⚠️ Peak bandwidth day
> - Traffic ≥ 1 GB displays as `xx.xx GB`, < 1 GB displays as `xxx.xx MB`
> - Request counts use language-appropriate abbreviation: Chinese → 万/亿, English → K/M/B (see "Data Conventions > Large Number Abbreviation by Language")
> - Trend analysis and domain analysis are mandatory — provide meaningful interpretation based on the data
