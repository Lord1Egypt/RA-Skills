# eo-log-downloader

Users describe a time range and domain in natural language to automatically retrieve the corresponding offline log download links, eliminating the tedious steps of manually selecting time ranges and domains in the console.

## APIs Involved

| Action | Description |
|---|---|
| DownloadL7Logs | Retrieve L7 offline log download links |
| DownloadL4Logs | Retrieve L4 offline log download links |
| DescribeAccelerationDomains | List acceleration domains under a zone — used to discover subdomains when user provides a root domain |

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

## Scenario A: Download L7 Logs by Time and Domain

**Trigger**: User says "get me the logs for example.com from yesterday afternoon", "download the last 6 hours of logs for example.com", "help me download the logs".

### Workflow

**Step 1**: Parse time range

- Convert the user's natural language time description to ISO 8601 format start and end times
- Example: "yesterday from 2 PM to 4 PM" → `2026-03-24T14:00:00+08:00` to `2026-03-24T16:00:00+08:00`
- If the user only says "last N hours", calculate backward from the current time
- If the user does not specify a time range, ask for confirmation

**Step 2**: Confirm domain

- If the user specified a domain, use it directly
- If the user did not specify a domain, ask for confirmation (the `Domains` parameter can be omitted to download logs for all domains, but inform the user first)

> ⚠️ **Root domain vs subdomain**: The `Domains` parameter requires the **actual acceleration subdomain** (e.g., `www.example.com`, `singapore.example.com`), not the zone root domain (e.g., `example.com`). Logs are recorded per subdomain.
> If the user provides a root domain (which matches the `ZoneName` from `DescribeZones`), you must:
> 1. Call `DescribeAccelerationDomains` with the `ZoneId` to list all subdomains under the zone
> 2. Present the subdomain list to the user and ask which one(s) to download, or omit `Domains` to download all

**Step 3**: Retrieve log download links

Call `DownloadL7Logs` with:
- `StartTime` / `EndTime`: Start and end times parsed in Step 1
- `ZoneIds`: Zone ID
- `Domains`: Target subdomain list (optional; omit to get logs for all domains under the zone)
- If there are many results, use `Limit` and `Offset` for pagination (default Limit=20, max 300)

#### Troubleshooting Empty Results

If `Data` is empty, check in order:
1. **Domain mismatch** — Did you pass the zone root domain instead of a subdomain? Remove the `Domains` parameter and retry to see if logs exist for other subdomains
2. **Time too recent** — Offline logs have a delay of approximately 1–2 hours. If the user requested logs for a very recent period, suggest retrying later
3. **No traffic** — The domain may have no actual traffic in the queried time range. Use `DescribeTimingL7AnalysisData` or check the console to confirm
4. **Wrong zone** — If the account has multiple zones, the domain may belong to a different zone. Try `ZoneIds=["*"]` to query across all zones

**Step 4**: Organize output

Organize the returned log file list into a clickable download link table with directly accessible download links.
- The API returns `Size` in **bytes**; convert to human-readable units (KB/MB) in the output table
- If the user's intent goes beyond downloading (e.g., "I want to analyze traffic by URL", "which resources use the most bandwidth"), proactively suggest using `eo-log-analyzer.md` for local log parsing and aggregation

**Output recommendation**: Present the response as "query parameter summary + download link table" with directly clickable download links.

## Scenario B: Download L4 Logs

**Trigger**: User says "download L4 logs", "get me the L4 logs", "download the layer 4 proxy logs".

### Workflow

**Step 1**: Parse time range

Same as Scenario A Step 1.

**Step 2**: Confirm L4 proxy instance

- If the user specified a ProxyId, use it directly
- If the user did not specify, ask whether to download logs for all L4 instances

**Step 3**: Retrieve log download links

Call `DownloadL4Logs` with:
- `StartTime` / `EndTime`: Start and end times
- `ZoneIds`: Zone ID
- `ProxyIds`: L4 instance ID list (optional)
- Handle pagination (default Limit=20, max 300)

**Step 4**: Organize output

Same as Scenario A Step 4.

**Output recommendation**: Same format as Scenario A, with log type labeled as "L4 logs".

## Output Format

```markdown
## Log Download Links

**Zone**: <zone name> (ZoneId: <zone-id>)
**Domain**: <domain> / All domains
**Time Range**: <start time> – <end time>
**Log Type**: L7 Access Logs / L4 Proxy Logs

| Log File | Size | Log Start Time | Log End Time | Download Link |
|---|---|---|---|---|
| ... | ... KB/MB | ... | ... | [Download](url) |

Total: N log files.
```

## Notes

> - Offline logs have a certain delay (approximately 1–2 hours); logs for very recent time periods may not yet be generated. If results are empty, suggest the user retry later.
> - Download links have a limited validity period; please download promptly.
> - **Log format**: Offline logs use **JSON Lines** format (one JSON object per line). For field descriptions, see [L7 Access Logs](https://edgeone.ai/document/61300) and [L4 Proxy Logs](https://edgeone.ai/document/61301). For output format customization (CSV, TSV, etc.), see [Customizing Log Output Formats](https://edgeone.ai/document/64485).
> - **For further analysis**: If the user wants to analyze log content (anomaly detection, traffic breakdown by URL, per-resource bandwidth, etc.), use `eo-log-analyzer.md` which handles download + local parsing + aggregation automatically.
