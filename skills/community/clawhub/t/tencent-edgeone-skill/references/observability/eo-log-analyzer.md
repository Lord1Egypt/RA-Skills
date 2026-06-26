# eo-log-analyzer

Users describe a fault time period and domain to automatically download logs, parse them locally, extract anomaly details, and provide pattern recognition conclusions with fault inference recommendations. Also supports traffic aggregation analysis (e.g., per-URL download volume breakdown). This is an upgrade from `eo-log-downloader.md`, which only provides download links — this scenario further completes log parsing and analysis.

## APIs & Prerequisites

Same as `eo-log-downloader.md` — this scenario uses the same APIs (`DownloadL7Logs`, `DownloadL4Logs`, `DescribeAccelerationDomains`) and the same prerequisites (`tccli` authentication + ZoneId discovery). Refer to that document for full details.

## Special Design Notes

- **Read-only operations**: All API calls are read-only queries; log downloading and parsing are performed locally
- **Local file writes only**: Log parsing is completed on the client side locally; raw logs are not uploaded or modified
- **Aggregated summaries for high-traffic domains**: For domains with extremely high request volumes, use aggregated summary analysis (grouped statistics by URI/status code/IP) rather than line-by-line output of full logs, to avoid information overload
- **Cross-scenario integration**: Analysis conclusions can guide the user to use `eo-origin-health-check.md` for origin troubleshooting, or `../security/ip-threat-blacklist.md` to block anomalous IPs

## Scenario A: Fault Period Log Analysis

**Trigger**: User says "analyze the logs for example.com from 3 PM to 4 PM today", "too many 502 errors, help me figure out what's going on", "analyze the logs and find the anomalies".

### Workflow

**Step 1**: Confirm analysis parameters

- Confirm the target domain (must be specified by the user or obtained from context)
- Parse the time range (natural language to ISO 8601)
- Confirm the anomaly type of interest (default: 4xx + 5xx; the user may also specify a particular status code such as 502)

**Step 2**: Download log files

Confirm the domain, retrieve download links, and download locally:

- If the user specified a subdomain (e.g., `www.example.com`), use it directly in the `Domains` parameter
- If the user did not specify a domain, or provided a **root domain** (matching the `ZoneName` from `DescribeZones`), follow `eo-log-downloader.md` Scenario A Step 2 to call `DescribeAccelerationDomains` and discover subdomains first, then either let the user choose or omit `Domains` to download all

Call `DownloadL7Logs` with `StartTime`, `EndTime`, `ZoneIds`, and optionally `Domains`. Then download and decompress:
- Use `curl` or `wget` to download log files to a local temporary directory
- Log files are typically in `.gz` compressed format; use `gunzip` to decompress
- ⚠️ **Log format is JSON Lines** (one JSON object per line, newline-separated). Each line is a self-contained JSON object. Do NOT parse as tab-separated or CSV.

> If there are many or large log files, prioritize downloading files that cover the user's time period of interest to avoid unnecessary bulk downloads.

> **If results are empty**, follow the troubleshooting steps in `eo-log-downloader.md` Scenario A — Troubleshooting Empty Results (domain mismatch, time too recent, no traffic, wrong zone).

#### L7 Offline Log Field Reference

The following fields are available in offline logs (subset of all L7 fields). For the full field list, see [L7 Access Logs](https://edgeone.ai/document/61300).

| Field | Type | Description | Common Use |
|---|---|---|---|
| `RequestTime` | ISO8601 | Time the request was received (UTC+0) | Time-window aggregation |
| `RequestHost` | String | Requested hostname (subdomain) | Group by domain |
| `RequestUrl` | String | URL path (without query string) | Group by resource/URI |
| `RequestUrlQueryString` | String | Query string portion of the URL | Full URL reconstruction |
| `RequestMethod` | String | HTTP method (GET/POST/...) | Filter by method |
| `RequestBytes` | Integer | Total bytes sent from client to edge (headers + body + SSL) | Inbound traffic |
| `EdgeResponseStatusCode` | Integer | Status code returned to client | Error filtering (4xx/5xx) |
| `EdgeResponseBytes` | Integer | Total bytes sent from edge to client (headers + body + SSL) | **Outbound traffic / download volume** |
| `EdgeResponseBodyBytes` | Integer | Response body bytes only (no headers) | Content-only traffic |
| `EdgeCacheStatus` | String | Cache hit status: `hit` / `miss` / `dynamic` / `other` | Cache analysis |
| `EdgeInternalTime` | Integer | Time to first byte (ms) | Latency analysis |
| `EdgeResponseTime` | Integer | Time to last byte (ms) | Full response latency |
| `ClientIP` | String | Client IP address | IP concentration analysis |
| `ClientRegion` | String | Client country/region (ISO 3166-1 alpha-2) | Geographic analysis |
| `EdgeServerIP` | String | Edge node IP | Node-level analysis |
| `RequestUA` | String | User-Agent | Bot/crawler identification |
| `RequestReferer` | String | Referer header | Traffic source analysis |

> **Parsing tip**: Use `jq` for JSON Lines processing (install via `brew install jq` on macOS or `apt install jq` on Linux). Example:
> ```sh
> # Count requests grouped by status code
> cat logfile.log | jq -r '.EdgeResponseStatusCode' | sort | uniq -c | sort -rn
> # Sum download traffic by URL
> cat logfile.log | jq -r '[.RequestUrl, .EdgeResponseBytes] | @tsv' | awk -F'\t' '{sum[$1]+=$2} END {for(u in sum) printf "%s\t%.2f MB\n", u, sum[u]/1048576}' | sort -t$'\t' -k2 -rn
> ```
>
> **If `jq` is not available**, use Python as a fallback:
> ```sh
> python3 -c "
> import json, sys
> from collections import defaultdict
> agg = defaultdict(lambda: [0, 0])
> for line in sys.stdin:
>     r = json.loads(line)
>     agg[r.get('RequestUrl','')][0] += 1
>     agg[r.get('RequestUrl','')][1] += r.get('EdgeResponseBytes', 0)
> for url, (cnt, b) in sorted(agg.items(), key=lambda x: -x[1][1]):
>     print(f'{url}\t{cnt}\t{b/1048576:.2f} MB')
> " < logfile.log
> ```

**Step 3**: Parse logs and extract anomalies

Perform structured parsing on the decompressed logs:
- Filter anomalous requests by status code (4xx, 5xx)
- Aggregate anomalous request count and ratio by URI
- Aggregate by client IP to identify request concentration
- Aggregate by time window (e.g., 5-minute granularity) to identify anomaly peak periods

**Step 4**: Pattern recognition

Perform pattern analysis on the aggregated data:

| Pattern | Characteristics | Possible Cause |
|---|---|---|
| Single URI concentrated 502 | One URI has a much higher 502 ratio than others | The backend service for that URI is malfunctioning |
| IP-concentrated anomalous requests | A few IPs generate a large number of anomalous requests | Possible crawler, attack, or malfunctioning client |
| Global 5xx spike | All URIs show concentrated 5xx in the same time period | Overall origin server overload or failure |
| Intermittent 504 | 504 errors appear repeatedly in specific time windows | Origin response timeout, possible performance bottleneck |

**Step 5**: Output analysis report

Summarize the anomaly details table, pattern recognition conclusions, and fault inference recommendations.

**Output recommendation**: Present the response as "overview summary + anomalous URI Top N table + pattern recognition conclusions + recommendations".

## Scenario B: Identify Origin Failure Concentration Periods

**Trigger**: User says "show me when origin failures were concentrated recently", "which time period had the most 5xx errors", "help me find the fault peak periods".

### Workflow

**Step 1**: Confirm query parameters

- Confirm the target domain
- Default query range is the last 6 hours; the user may also specify a different time range

**Step 2**: Download and parse logs

Same as Scenario A Steps 2 and 3, but focus on time-window aggregation:
- Use 5-minute or 10-minute granularity to count 5xx requests per time window
- Calculate the 5xx ratio for each window

**Step 3**: Identify peak periods

- Mark the Top 3 time periods with the highest 5xx count
- Calculate the deviation multiplier of peak periods from the average

**Step 4**: Output time distribution

Organize the time distribution into a table, highlight peak periods, and provide further analysis recommendations.

**Output recommendation**: Present the response as "time distribution table + peak period annotations + next-step recommendations".

## Scenario C: Traffic / Download Volume Aggregation by Domain + URL

**Trigger**: User says "which resources use the most bandwidth", "show me download traffic by URL", "I want to see per-resource traffic breakdown", "which URLs are consuming the most traffic".

### Workflow

**Step 1**: Confirm analysis parameters

- Confirm the target domain (or all domains under the zone)
- Parse the time range (natural language to ISO 8601)
- Confirm the aggregation dimension: by URL only, by domain + URL, or by domain only

**Step 2**: Download log files

Same as Scenario A Step 2. Download and decompress the log files for the target time range.

**Step 3**: Aggregate traffic data

Parse each JSON line and aggregate by the requested dimension:

- **Primary metric**: `EdgeResponseBytes` (total bytes delivered to client, including headers) — this represents the **download traffic** from the user's perspective
- **Secondary metric**: `EdgeResponseBodyBytes` (response body only) — useful when isolating content size from protocol overhead
- Group by `RequestHost` + `RequestUrl` (or `RequestHost` alone, or `RequestUrl` alone, depending on user intent)
- Also count the number of requests per group for context

Example aggregation using `jq` + `awk` (if `jq` is available):
```sh
# Traffic by domain + URL, sorted descending by MB value
cat *.log | jq -r '[.RequestHost, .RequestUrl, (.EdgeResponseBytes | tostring)] | @tsv' \
  | awk -F'\t' '{key=$1"\t"$2; sum[key]+=$3; cnt[key]++} END {for(k in sum) printf "%s\t%d\t%.2f\n", k, cnt[k], sum[k]/1048576}' \
  | sort -t$'\t' -k4 -rn | head -50
```

If `jq` is not available, use Python:
```sh
python3 -c "
import json, sys, os
from collections import defaultdict
agg = defaultdict(lambda: [0, 0, 0])  # [requests, bytes, body_bytes]
for fname in sorted(f for f in os.listdir('.') if f.endswith('.log') or not '.' in f):
    with open(fname) as fh:
        for line in fh:
            line = line.strip()
            if not line: continue
            r = json.loads(line)
            key = (r.get('RequestHost',''), r.get('RequestUrl',''))
            agg[key][0] += 1
            agg[key][1] += r.get('EdgeResponseBytes', 0)
            agg[key][2] += r.get('EdgeResponseBodyBytes', 0)
for (host, url), (cnt, b, bb) in sorted(agg.items(), key=lambda x: -x[1][1]):
    print(f'{host}\t{url}\t{cnt}\t{b/1048576:.2f} MB')
"
```

**Step 4**: Enrich with cache and status insights (optional)

For the Top N resources by traffic, additionally aggregate:
- `EdgeCacheStatus` distribution (`hit` / `miss` / `dynamic`) — helps identify cacheable resources that are not being cached
- `EdgeResponseStatusCode` distribution — detect if high-traffic resources also have high error rates

**Step 5**: Output traffic report

Summarize the aggregation results with the Top N table and optional insights.

**Output recommendation**: Present as "overview summary + Top N traffic table + cache/status insights + optimization recommendations".

## Output Format

### Scenario A: Log Analysis Report

```markdown
## Log Analysis Report — <domain>

**Zone**: <zone name> (ZoneId: <zone-id>)
**Analysis Time Period**: <start time> – <end time>
**Total Requests**: <N> | **Anomalous Requests**: <M> (<ratio>%)

### Anomalous URI Top 10

| URI | Anomaly Count | Ratio of Total Anomalies | Primary Error Code | Source IP Concentration |
|---|---|---|---|---|
| ... | ... | ...% | 502 | Dispersed / Concentrated (N IPs) |

### Pattern Recognition

- <pattern 1 description>
- <pattern 2 description>

### Recommendations

1. <recommendation 1> (consider using eo-origin-health-check for origin troubleshooting)
2. <recommendation 2> (consider using ip-threat-blacklist to block anomalous IPs)
```

### Scenario B: Origin Failure Time Distribution

```markdown
## Origin Failure Time Distribution — <domain> (Last <N> Hours)

**Analysis Time Range**: <start time> – <end time>

| Time Period | 5xx Count | Ratio | Remarks |
|---|---|---|---|
| HH:MM–HH:MM | ... | ...% | Peak ⚠️ |
| ... | ... | ...% | |

### Conclusion

- Failures are concentrated in <time period>. Recommend focusing analysis on logs from that period (use Scenario A for deeper analysis).
```

### Scenario C: Traffic Aggregation Report

```markdown
## Traffic Aggregation Report — <domain / all domains>

**Zone**: <zone name> (ZoneId: <zone-id>)
**Analysis Time Period**: <start time> – <end time>
**Total Requests**: <N> | **Total Download Traffic**: <X> MB

### Top 20 Resources by Download Traffic

| Domain | URL | Requests | Download Traffic | Avg Size | Cache Hit Rate |
|---|---|---|---|---|---|
| example.com | /video/intro.mp4 | 1,234 | 456.78 MB | 380 KB | 92% hit |
| ... | ... | ... | ... MB | ... KB | ...% |

### Insights

- <cache optimization insight, e.g., "Top 3 resources account for 80% of total traffic, all have >90% cache hit rate">
- <anomaly insight, e.g., "/api/data has 45 MB traffic but 0% cache hit — consider enabling caching for this endpoint">

### Recommendations

1. <recommendation 1>
2. <recommendation 2>
```

## Notes

> - Log parsing is performed locally on the client; ensure sufficient disk space for temporary log files.
> - Log files for high-traffic domains can be very large; prefer aggregated statistics over line-by-line analysis.
> - If origin errors (e.g., 502 concentrated on certain IPs) are found, use `eo-origin-health-check.md` for origin health inspection.
> - If anomalous requests are concentrated on a few client IPs, use `../security/ip-threat-blacklist.md` for IP blocking.
