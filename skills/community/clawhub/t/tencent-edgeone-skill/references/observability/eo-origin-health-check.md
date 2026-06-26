# eo-origin-health-check

Query the origin status code distribution and origin health ratio for a specified domain or the entire account over a given time range, to quickly determine whether the issue lies with the CDN or the origin server.

## APIs Involved

| Action | Description |
|---|---|
| DescribeTimingL7AnalysisData | Query L7 time-series data (response status code analysis at edge nodes) |
| DescribeTimingL7OriginPullData | Query L7 origin-pull time-series data (origin status code distribution, origin traffic/bandwidth) |
| DescribeTopL7AnalysisData | Query top N domains/URLs/status codes by request count or traffic — used to discover which domains carry traffic |

> **Command usage**: This document only lists API names and workflow guidance.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm complete parameters and response descriptions.

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli`. If no valid credentials are configured in the environment, guide the user to log in first:

```sh
tccli auth login
```

> The terminal will print an authorization link after execution and remain blocked until the user completes browser authorization, after which the command ends automatically.
> Never ask the user for `SecretId` / `SecretKey`, and do not execute any commands that could expose credential contents.

2. ZoneId must be obtained first. Refer to `../api/zone-discovery.md`.
   - **Shortcut**: Both `DescribeTimingL7OriginPullData` and `DescribeTimingL7AnalysisData` support `ZoneIds=["*"]` to query account-level aggregated data across all zones. Use this when the user does not specify a particular zone or wants an overview.

## Key API Parameter Notes

### Interval (applies to both DescribeTimingL7OriginPullData and DescribeTimingL7AnalysisData)

- ⚠️ **Do NOT use `min` (1-minute) granularity** — it generates excessive data volume and frequently triggers API errors (response size limit exceeded). It also puts unnecessary pressure on the data query cluster.
- Recommended granularity by query time range:

| Query Time Range | Recommended Interval | Notes |
|---|---|---|
| ≤ 2 hours | `5min` | Good balance of precision and data volume |
| 2–24 hours | `hour` | Suitable for most troubleshooting scenarios |
| 1–7 days | `hour` or `day` | Use `hour` if you need to identify anomaly time windows |
| > 7 days | `day` | Avoid finer granularity for long ranges |

- If a query returns empty or errors with a finer granularity, try a coarser granularity or narrow the time range.

### DescribeTimingL7OriginPullData

- `ZoneIds` is **required**. Pass `["*"]` for account-level data, or one or more specific ZoneIds.
- `DimensionName` controls grouping:
  - `origin-status-code-category`: Group by category (1XX/2XX/3XX/4XX/5XX)
  - `origin-status-code`: Group by exact status code (200, 301, 404, 502, etc.) — useful for pinpointing specific error codes
  - ⚠️ **`DimensionName` does NOT support `domain`**. You cannot group origin-pull data by domain in a single call. To find which domains have origin errors, use `DescribeTopL7AnalysisData` to get the domain list first, then query each domain individually with the `domain` filter.
- **Do NOT** include `Filters` with key `mitigatedByWebSecurity` — this filter is not supported by this API and will cause errors.
- The `domain` filter works with both `ZoneIds=["*"]` and specific ZoneIds. The value must be the **actual domain that carries traffic** (typically a subdomain like `www.example.com` or `api.example.com`), not the zone root domain (e.g., `example.com`). If filtering returns empty results, try without the domain filter first to confirm data exists, then check what domains are carrying traffic.

#### Troubleshooting Empty Results

> This applies to both `DescribeTimingL7OriginPullData` and `DescribeTimingL7AnalysisData`.

If a query returns empty `TimingDataRecords` or `Data`, follow these steps in order:

1. **Remove the `domain` filter** and query at zone or account level (`ZoneIds=["*"]`) to confirm data exists in the time range
2. **If zone-level is also empty**, try `ZoneIds=["*"]` (account-level) — the domain may belong to a different zone than expected
3. **If account-level has data but domain filter returns empty**, the domain name may be wrong. Use `DescribeTopL7AnalysisData` with `MetricName=l7Flow_request_domain` to discover which domains actually carry traffic
4. **Use a coarser `Interval`** (e.g., `day` instead of `hour`) — finer granularity with wide time ranges can exceed API response limits
5. **Check the time range** — API data typically has a 5–10 minute delay; avoid querying the most recent 10 minutes

### DescribeTimingL7AnalysisData

- `ZoneIds` supports `["*"]` for account-level data.
- Use `Filters` with key `statusCode` (Operator: `equals`, Value: `["2XX"]`, `["4XX"]`, `["5XX"]`, etc.) to filter by status code category. Each filter call returns the time-series for that specific category.
  - ⚠️ **You must make separate calls for each status code category** (2XX, 3XX, 4XX, 5XX). There is no single-call way to get the full breakdown.
- The `domain` filter follows the same rules as described above — use the actual traffic-carrying domain, not the zone root domain.
- **Response structure**: Returns `Data[].TypeValue[].Sum` for the aggregated count. The per-interval breakdown is in `Data[].TypeValue[].Detail[]` (each with `Timestamp` and `Value`). Do NOT use `Data[].Value[]` — that field does not exist.

### DescribeTopL7AnalysisData

- `ZoneIds` supports `["*"]` for account-level data.
- `MetricName` (singular, not array) controls the ranking dimension. Key values for origin health check:
  - `l7Flow_request_domain`: Top domains by request count — **use this to discover all domains with traffic**.
- `Limit`: Maximum number of top entries to return (default 10, max 1000). Set to 50+ when scanning for anomalous domains.
- Returns `Data[].TypeKey` (grouping key, e.g., AppId) and `Data[].DetailData[]` where each entry has `Key` (the domain name) and `Value` (the count).
- This is an **edge-side** metric (not origin-pull), but it serves as the domain discovery step before per-domain origin queries.

## Scenario A: Query Origin Status Code Distribution

**Trigger**: User says "check the origin status for example.com", "are there any origin issues", "is the origin healthy", "which domains have origin errors".

> This scenario has two sub-flows depending on whether the user asks about a **specific domain** or wants an **account-wide scan**.

### Workflow A1: Specific Domain Origin Health Check

Use when the user specifies a domain (e.g., "check origin health for api.example.com").

**Step 1**: Confirm query parameters

- Confirm the target domain (must be specified by the user or obtained from context)
- Default query range is the last 1 hour; the user may also specify a different time range
- Recommend avoiding the most recent 10 minutes (API data has a delay)

**Step 2**: Query origin status code distribution

Call `DescribeTimingL7OriginPullData` with:
- `ZoneIds`: `["*"]` for account-level, or specific ZoneId(s) for targeted query
- `DimensionName=origin-status-code-category`: Group by origin status code category (2XX/3XX/4XX/5XX)
- `MetricNames=["l7Flow_request_hy"]`: Origin-pull request count
- `Interval`: `5min` or `hour` for identifying anomaly periods; `day` for longer time ranges (see Interval guidelines above)
- Use the `domain` key in `Filters` to filter for the target subdomain

> **Tip**: To identify the exact error codes (e.g., 502 vs 504), make a follow-up call with `DimensionName=origin-status-code`.

**Step 3**: Calculate health metrics

- Health ratio = 2xx requests / total origin requests × 100%
- Anomaly ratio = (4xx + 5xx) requests / total origin requests × 100%
- If 5xx ratio > 5%, mark as ⚠️ Anomaly

**Output recommendation**: Present as "health score + status code distribution table", with anomaly indicators highlighted.

### Workflow A2: Account-Wide Origin Anomaly Scan

Use when the user asks "which domains have origin errors", "are there any origin issues across all domains", or does not specify a particular domain.

**Step 1**: Get account-level overview

Call `DescribeTimingL7OriginPullData` with:
- `ZoneIds=["*"]`
- `DimensionName=origin-status-code-category`
- `MetricNames=["l7Flow_request_hy"]`
- `Interval=day` (or as appropriate for the time range)

Calculate overall health metrics. If 4xx + 5xx ratio is low (e.g., < 1%), report healthy and stop. Otherwise proceed to identify anomalous domains.

**Step 2**: Discover domains with traffic

Call `DescribeTopL7AnalysisData` with:
- `MetricName=l7Flow_request_domain`
- `ZoneIds=["*"]`
- `Limit=50` (or higher if the account has many domains)

This returns the top domains ranked by edge request count. Extract the domain list from `Data[].DetailData[].Key`.

**Step 3**: Per-domain origin status code check

For each domain from Step 2, call `DescribeTimingL7OriginPullData` with:
- `ZoneIds=["*"]`
- `DimensionName=origin-status-code-category`
- `MetricNames=["l7Flow_request_hy"]`
- `Filters`: `[{"Key": "domain", "Operator": "equals", "Value": ["<domain>"]}]`

Collect each domain's 2XX/3XX/4XX/5XX counts and calculate error ratios.

> ⚠️ This step requires one API call per domain. For large domain lists, consider only checking the top 20–30 domains, or parallelize calls where possible.

**Step 4**: Drill down into anomalous domains

For domains with error ratio > 5%, make a follow-up call with `DimensionName=origin-status-code` to get the exact error code breakdown (e.g., 404 vs 502 vs 503).

**Output recommendation**: Present as "account overview + anomalous domain table (sorted by error ratio descending) + top error codes for the worst domains".

## Scenario B: Quick Fault Root Cause Analysis

**Trigger**: User says "is it a CDN issue or an origin issue", "help me troubleshoot the origin failure", "where are the 5xx errors coming from", "is EO the problem or the origin".

### Workflow

> ⚠️ **Time alignment**: When comparing edge vs origin data, **always use the same `StartTime`, `EndTime`, and `Interval`** for both `DescribeTimingL7AnalysisData` and `DescribeTimingL7OriginPullData` calls. Mismatched time ranges or granularity will produce misleading comparisons.

**Step 1**: Collect edge node status code data

Call `DescribeTimingL7AnalysisData` **4 times** (once per status code category) to query edge-to-client response status codes:
- `MetricNames=["l7Flow_request"]`
- `ZoneIds`: `["*"]` for account-level, or specific ZoneId(s)
- `Interval`: use the same granularity as Step 2 (see Interval guidelines above)
- `Filters`: include `{"Key": "statusCode", "Operator": "equals", "Value": ["2XX"]}` (repeat for `"3XX"`, `"4XX"`, `"5XX"`)
- Optionally add `{"Key": "domain", "Operator": "equals", "Value": ["<domain>"]}` to `Filters` to scope to a specific subdomain

Extract the count for each category from `Data[].TypeValue[].Sum`.

**Step 2**: Collect origin status code data

Call `DescribeTimingL7OriginPullData` to query origin status codes (single call returns all categories):
- `DimensionName=origin-status-code-category`
- `MetricNames=["l7Flow_request_hy"]`
- `ZoneIds`: same scope as Step 1
- `Interval`: same as Step 1 (must match for accurate comparison)
- Optionally filter for a specific subdomain via `domain` in `Filters`

Extract the count for each category from `TimingDataRecords[].TypeValue[].Sum` where `TypeKey` is the category (2XX/3XX/4XX/5XX).

**Step 3**: Comparative analysis for root cause

Compare edge vs origin error counts side by side:

**5XX comparison:**

| Edge 5XX | Origin 5XX | Preliminary Conclusion |
|---|---|---|
| High | High (similar count) | 5XX errors originate from the origin server — **origin issue** |
| High | Low or zero | 5XX generated by CDN/EO nodes — **CDN issue** |
| Zero or low | High | Origin has 5XX but CDN cache/retry absorbs them — **origin issue, CDN mitigates** |

**4XX comparison:**

| Edge 4XX | Origin 4XX | Preliminary Conclusion |
|---|---|---|
| High | High (similar count) | 4XX errors originate from the origin (missing resources, auth issues) — **origin issue** |
| High | Low or zero | 4XX generated by EO rules (WAF, rate limiting, ACL) — **EO configuration issue** |
| Low | High | Origin returns 4XX but CDN cache serves valid responses — **origin issue, CDN mitigates** |

**Additional signals:**
- If edge has 3XX responses but origin does not, these are typically EO-generated redirects (e.g., HTTP→HTTPS forced redirect).
- If edge total ≈ origin total, most requests are being forwarded to origin (low cache hit rate).

**Step 4**: Provide root cause conclusion and recommendations

- Clearly label as "origin issue", "CDN/EO issue", or "mixed / further investigation needed"
- For origin issues: recommend checking origin server logs, resource availability, and backend health
- For CDN issues: recommend checking EO security rules, cache configuration, and node status
- For deeper analysis: recommend using `eo-log-analyzer.md` for log-level troubleshooting

**Output recommendation**: Present the response as "edge vs origin comparison table + root cause conclusion + recommendations".

## Output Format

### Scenario A: Origin Health Inspection Report

#### A1: Single Domain Report

```markdown
## Origin Health Inspection — <domain> (Last <N> Hours/Days)

**Zone**: <zone name> (ZoneId: <zone-id>) or "All Zones (account-level)"
**Query Time Range**: <start time> – <end time>
**Health Score**: <score> (✅ Healthy / ⚠️ Anomaly Detected / 🔴 Critical Anomaly)

### Origin Status Code Distribution

| Status Code Category | Request Count | Ratio |
|---|---|---|
| 2xx | ... | ...% |
| 3xx | ... | ...% |
| 4xx | ... | ...% ⚠️ (if > 5%) |
| 5xx | ... | ...% ⚠️ (if > 5%) |

### Top Error Codes (if anomaly detected)

| Status Code | Request Count | Ratio |
|---|---|---|
| 502 | ... | ...% |
| 404 | ... | ...% |
| ... | ... | ... |

> Use `DimensionName=origin-status-code` to get exact error code breakdown.

### Quick Root Cause

- <one-sentence root cause conclusion>
- Recommendation: <next step>
```

#### A2: Account-Wide Anomaly Scan Report

```markdown
## Origin Health Scan — Account Overview (Last <N> Hours/Days)

**Query Time Range**: <start time> – <end time>
**Scope**: All Zones (account-level)

### Account-Level Summary

| Status Code Category | Request Count | Ratio |
|---|---|---|
| 2xx | ... | ...% |
| 3xx | ... | ...% |
| 4xx | ... | ...% ⚠️ (if > 5%) |
| 5xx | ... | ...% |

### Anomalous Domains (Error Ratio > 5%)

| Domain | Total Requests | 2XX | 4XX | 5XX | Error Ratio |
|---|---|---|---|---|---|
| xxx.example.com | ... | ... | ... | ... | ...% ⚠️ |
| yyy.example.com | ... | ... | ... | ... | ...% ⚠️ |
| ... | ... | ... | ... | ... | ... |

### Top Error Code Breakdown (worst domains)

**xxx.example.com**:
| Status Code | Count | Ratio |
|---|---|---|
| 404 | ... | ...% |
| 502 | ... | ...% |

### Recommendations

1. <recommendation for most critical domain>
2. <recommendation for next domain>
```

### Scenario B: Fault Root Cause Analysis

```markdown
## Fault Root Cause Analysis — <domain> (Last <N> Hours)

**Query Time Range**: <start time> – <end time>

### Edge vs Origin Comparison

| Metric | Edge Node | Origin |
|---|---|---|
| Total Requests | ... | ... |
| 2XX Count | ... | ... |
| 4XX Count | ... | ... |
| 5XX Count | ... | ... |
| Error Ratio (4XX+5XX) | ...% | ...% |

### Root Cause Conclusion

**5XX Analysis**: <Edge 5XX vs Origin 5XX comparison and conclusion>
**4XX Analysis**: <Edge 4XX vs Origin 4XX comparison and conclusion>

**Overall**: <"origin issue" / "CDN/EO issue" / "mixed">
- <supporting evidence>

### Recommendations

1. <recommendation 1>
2. <recommendation 2>
```

## Common Abnormal Status Code Reference

When origin-pull or edge responses contain error status codes, use the following reference to understand the cause and guide troubleshooting. For the full list and detailed troubleshooting steps, see: [Abnormal Status Code Reference](https://edgeone.ai/document/58009) and [4XX/5XX Troubleshooting Guide](https://edgeone.ai/document/67228).

### Standard Status Codes (returned by EO edge nodes)

| Status Code | Meaning | Common Cause |
|---|---|---|
| 400 | Bad Request | Request method not allowed by EdgeOne. See [HTTP Limits](https://edgeone.ai/document/63624) |
| 403 | Forbidden | Token authentication failure (rule engine), or compliance interception |
| 416 | Range Not Satisfiable | Invalid Range request (e.g., `rangeStart < 0`, `rangeStart > rangeEnd`, or `rangeStart > FileSize`) |
| 418 | Config Not Found | Node cannot read domain config — check CNAME, domain binding, or dispatch |
| 423 | Request Loop | CDN-Loop detected (loops ≥ 16). See [CDN-Loop](https://edgeone.ai/document/54211) |

### EdgeOne Custom Status Codes (520–599)

> ⚠️ Business origins should **avoid using 520–599** status codes to prevent confusion with EO's custom codes.

#### Connection & Origin Communication Errors

| Status Code | Meaning | Troubleshooting |
|---|---|---|
| 520 / 550 | Origin connection reset (after request sent) | Origin sent RST after connection was established. Check origin server logs for forced disconnections (overload, firewall) |
| 521 / 551 | Origin refused connection (TCP handshake) | Origin sent RST during TCP handshake. Check origin port availability and firewall rules for EO IP ranges |
| 522 / 552 | Origin connection timeout (TCP handshake) | Origin did not respond during TCP handshake. Check if origin is down or network path is blocked |
| 523 / 553 | Origin DNS resolution failure | Domain-based origin DNS lookup failed. Verify the origin domain's DNS configuration |
| 524 / 554 | Origin response timeout | Connection established but origin did not respond in time. Check origin load and processing latency |
| 525 / 555 | SSL handshake failure | HTTPS origin SSL handshake failed. Check origin SSL certificate validity, port (443), and protocol compatibility |

#### Security & Rule Interception

| Status Code | Meaning | Troubleshooting |
|---|---|---|
| 566 | Managed Rules block | Blocked by [Web Protection — Managed Rules](https://edgeone.ai/document/56828). Check managed rule logs |
| 567 | Custom Rules / Rate Limiting / Bot Management block | Blocked by custom rules, rate limiting, or bot management. Review rule conditions and whitelist |

#### Platform Errors

| Status Code | Meaning | Troubleshooting |
|---|---|---|
| 545 | Edge Function execution error | Edge function runtime error (e.g., undefined variable). Check function code |
| 570 | Platform global rate limit | Hit platform-level rate limit. Contact EdgeOne support |
