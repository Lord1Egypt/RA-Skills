# ip-threat-blacklist

Analyze high-concentration threat IPs based on EdgeOne L7 access data, write them to a designated blocklist IP group, and automate IP banning.

## APIs Involved

| Action | Description |
|---|---|
| `DescribeTopL7AnalysisData` | Query L7 traffic Top data (analyze access concentration by IP dimension) |
| `DescribeSecurityIPGroup` | Query the security IP group list under the zone (confirm target blocklist group) |
| `ModifySecurityIPGroup` | Modify security IP group entries (write blocklist IPs) |

> **Command usage**: This document only lists API names and process guidelines.
> Before execution, consult the API documentation via `../api/api-discovery.md` to confirm the complete parameters and response descriptions.

## Prerequisites

1. All Tencent Cloud API calls are executed via `tccli`. If no valid credentials are configured in the environment, you must first guide the user to complete login:

```sh
tccli auth login
```

> After execution, the terminal will print an authorization link and block until the user completes browser authorization — the command ends automatically upon success.
> Never ask the user for `SecretId` / `SecretKey`, and do not execute commands that might expose credential contents.

2. You need to obtain the ZoneId first — see `../api/zone-discovery.md`.

3. **Write operation security red lines**:
   - Before executing `ModifySecurityIPGroup`, you **must** show the complete change Diff to the user and wait for explicit confirmation before executing.
   - **Only write to the blocklist IP group specified by the user** — never select or create an IP group on your own.
   - If the user has not explicitly specified a target IP group, guide them to first use `domain-blacklist-inspector.md` to identify the target blocklist group ID before proceeding.

## Scenario A: Analyze High-Concentration Threat IPs

**Trigger**: User says "help me analyze recent attack IP concentration", "which IPs have abnormal access volume", "help me check for suspicious IPs".

### Process

1. Confirm the analysis time range (default "last 24 hours"), and explicitly state the start and end time in the report
2. Call the `DescribeTopL7AnalysisData` API, querying Top access data by IP dimension:
   - Recommended metrics: request count (`l7Flow_request`) or bandwidth (`l7Flow_flux`)
   - Results are sorted by request volume in descending order, take Top N (default Top 20)
3. Perform concentration analysis on the returned IP list:

| Analysis Dimension | Description |
|---|---|
| Request share | Single IP request count / total requests — a high share (e.g., > 5%) indicates abnormal concentration |
| Request rate | Average QPS for a single IP within the time window — significantly exceeding normal levels is suspicious |
| Concentration ranking | Gap between Top 1 IP and Top 10 IP request volumes — a large gap suggests a single-point concentrated attack |

4. Output the analysis report, flag suspected threat IPs, and ask the user whether to proceed with banning

**Output suggestion**: Respond with "Top IP list + concentration analysis + threat assessment", and at the end prompt the user whether to enter Scenario B for banning.

## Scenario B: Execute IP Blocklist Banning

**Trigger**: User says "block these IPs", "IP ban", "add top attack IPs to blocklist".

> ⚠️ **This scenario involves write operations — the double confirmation process must be strictly followed and cannot be skipped.**

### Process

#### Step 1: Confirm Target Blocklist IP Group

1. Ask the user which blocklist IP group to write to (must be explicitly specified by the user — never decide on your own)
2. If the user is unsure about the target IP group, guide them to first execute `domain-blacklist-inspector.md` to look it up
3. Call the `DescribeSecurityIPGroup` API to query and display the target IP group's current status (name, ID, existing entry count)

#### Step 2: Confirm IPs to Be Blocked

1. If the user is coming from Scenario A, use the threat IP list analyzed in Scenario A
2. If the user directly provides an IP list, use it as-is
3. Perform basic validation on the IP list to be blocked:
   - Format validation: Ensure each entry is a valid IP address or CIDR (e.g., `1.2.3.4` or `1.2.3.0/24`)
   - Duplicate check: Filter out entries already existing in the target IP group to avoid duplicate writes
   - Range warning: If large CIDR ranges like `/8` or `/16` exist, specifically alert the user for confirmation

#### Step 3: Display Change Diff + Double Confirmation

Before executing the write operation, you **must** show the following Diff to the user:

```
The following changes will be applied to the IP group:

Target IP group: <IP group name> (ID: ipg-xxxxxxxx)
Current entry count: N entries

New entries (M total):
  + 1.2.3.4
  + 5.6.7.8
  + 9.10.11.0/24
  ...

Entry count after change: N + M entries

⚠️ This operation takes effect immediately — requests from blocked IPs will be intercepted.
Do you want to proceed? (Yes/No)
```

**You must wait for the user to explicitly reply "Yes" or "Confirm" before calling `ModifySecurityIPGroup`.**

#### Step 4: Execute Write and Verify

1. Call the `ModifySecurityIPGroup` API to write the new IPs to the target blocklist group
2. After writing, call `DescribeSecurityIPGroup` again to query the target IP group and verify the entry count matches expectations
3. Output the operation result summary

## Scenario C: Query Current Blocklist IP Group Status

**Trigger**: User says "check what IPs are in the blocklist", "how many entries are in the blocklist group now".

Call the `DescribeSecurityIPGroup` API to query and display the current entry list of the specified IP group.

> To find the blocklist IP group ID associated with a domain, see `domain-blacklist-inspector.md`.

## Output Format

> **Language note**: Adapt the report language to match the user's language. The templates below are examples — output should be in the same language the user is using.

### Scenario A: Threat IP Analysis Report

```markdown
## Threat IP Concentration Analysis Report

**Zone**: example.com (ZoneId: zone-xxx)
**Analysis Time Range**: 2026-03-16 00:00 – 2026-03-23 00:00
**Data Source**: `DescribeTopL7AnalysisData` (Metric: request count)

### Top IP Access Ranking

| Rank | IP Address | Request Count | Share of Total | Avg QPS | Threat Assessment |
|---|---|---|---|---|---|
| 1 | 1.2.3.4 | 1,200,000 | 12.5% | 1,984/s | 🔴 High risk |
| 2 | 5.6.7.8 | 800,000 | 8.3% | 1,322/s | 🔴 High risk |
| 3 | 9.10.11.12 | 200,000 | 2.1% | 330/s | 🟡 Suspicious |
| ... | ... | ... | ... | ... | ... |

### Concentration Analysis

- Total requests: 9,600,000
- Top 1 IP share: 12.5% (exceeds 5% threshold — abnormally concentrated)
- Top 3 IPs combined share: 22.9%
- Concentration assessment: **Clear signs of single-point concentrated attack**

### Suggested IPs to Block

The following IPs have request share exceeding the threshold or abnormal QPS — recommended for blocklist:

- `1.2.3.4` (share 12.5%, QPS 1,984/s)
- `5.6.7.8` (share 8.3%, QPS 1,322/s)

> To add the above IPs to the blocklist, specify the target blocklist IP group, or reply "block" to proceed.
```

### Scenario B: Banning Operation Result

```markdown
## IP Blocklist Write Result

**Target IP Group**: blacklist-prod (ID: ipg-xxxxxxxx)
**Operation Time**: 2026-03-23 19:00:00
**Data Source**: `ModifySecurityIPGroup`

### Change Summary

| Item | Count |
|---|---|
| New entries added | 2 |
| Skipped (already exist) | 0 |
| Total entries after operation | 44 |

### New Entry Details

| IP / CIDR | Source | Notes |
|---|---|---|
| 1.2.3.4 | Top L7 analysis | Request share 12.5% |
| 5.6.7.8 | Top L7 analysis | Request share 8.3% |

### Verification Result

✅ Write successful — IP group currently has 44 entries, matching expectations.
```

## Important Notes

> ⚠️ **Operation safety notice**:
> - `ModifySecurityIPGroup` is a **full overwrite** API — when calling it, you must pass the complete entry list of the IP group (existing entries + new entries), not just the new entries. Always query existing entries first, merge them, then write — **never overwrite directly and lose existing entries**.
> - Banning takes effect immediately — requests from banned IPs will be intercepted in real time. Execute only after confirming threat IPs.
> - For bulk banning of many IPs (e.g., more than 50), prefer writing a script for one-time execution to avoid omissions from multiple calls.
