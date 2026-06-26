# Tencent Cloud RUM MCP Tool Parameter Reference

## MCP Server Configuration

- **URL**: `https://app.rumt-zh.com/sse`
- **Transport Protocol**: `sse`
- **Authentication**: Via HTTP Headers — `SecretId` and `SecretKey` (Obtain at: [Tencent Cloud API Key Management](https://console.tencentcloud.com/cam/capi))

```json
{
  "mcpServers": {
    "rum": {
      "transportType": "sse",
      "url": "https://app.rumt-zh.com/sse",
      "headers": {
        "SecretId": "<YOUR_SECRET_ID>",
        "SecretKey": "<YOUR_SECRET_KEY>"
      }
    }
  }
}
```

---

## Tool 1: QueryRumWebProjects

### Description
Query the list of RUM-WEB applications. Shows up to 50 entries. If you have more than 50 applications, use ProjectName or ProjectId parameters to filter.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ProjectId` | string | No | Application ID, numeric string, e.g. "123456" |
| `ProjectName` | string | No | Application name, exact match |
| `ProjectNameLike` | string | No | Fuzzy search, finds all apps containing the specified string. Cannot be used with ProjectName simultaneously |

### Usage Scenarios
- User provided only a ProjectId — call `QueryRumWebProjects({ProjectId: "<ID>"})` first to verify existence
- User doesn't know their ProjectId — call without parameters to get the full list
- View all RUM-WEB applications under the current account
- User provides app name — try exact match (`ProjectName`) first, then fuzzy match (`ProjectNameLike`)

### Calling Notes
- `ProjectId` must be a pure numeric string (e.g. `"123456"`); if the format is invalid, verify with the user first
- If exact name match returns nothing, try `ProjectNameLike` for fuzzy search
- If fuzzy search also returns nothing, call without any parameters to get the full list for comparison
- When the full-list call returns exactly 50 records → the limit has been hit; ask the user for an application-name keyword
- If another tool reports "no permission", come back here to validate the `ProjectId` — it may be wrong
- The complete four-scenario lookup flow is in `SKILL.md` under "Application Info Lookup Rules"

---

## Tool 2: QueryRumWebMetric

### Description
Query RUM-WEB metric data. Supports network metrics (request count, avg API latency, status code error rate, retcode error rate), JS Errors, resource loading exceptions, PV, UV, page performance, and static resources.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ProjectId` | string | ✅ Yes | Application ID |
| `Metric` | string(enum) | ✅ Yes | Metric type: `network`/`exception`/`pv`/`uv`/`performance`/`resource` |
| `Limit` | number | ✅ Yes | Number of results, **default recommended 100**, max 1000 |
| `StartTime` | number | No | Start timestamp (seconds), default 12 hours ago |
| `EndTime` | number | No | End timestamp (seconds), default current time |
| `Region` | string | No | Region: `ap-guangzhou`(default)/`ap-singapore`/`na-siliconvalley` |
| `Filters` | array | No | Filter conditions array |
| `GroupBy` | array | No | Aggregation grouping fields (MUST be an array even for single field) |

### Metric Parameter Selection Guide

| User Need | Metric Value | Notes |
|-----------|-------------|-------|
| API request count, latency, error rate | `network` | — |
| HTTP status codes, retcode | `network` | — |
| Network errors | `network` | Not `exception` |
| All exception types | `exception` | No level filter |
| JS errors | `exception` | Filter level=4 |
| JS + Promise errors | `exception` | Filter level in ('4','8') |
| Page performance (LCP/FCP/TTFB, etc.) | `performance` | Default: use LCP |
| PV | `pv` | — |
| UV | `uv` | — |
| Static resource loading | `resource` | Does not support `from` filter |

### Filters

**Supported fields**: `brand`, `browser`, `device`, `env`, `error_msg`(exception only), `ext1`~`ext10`, `from`(resource not supported), `is_abroad`, `is_err`, `isp`, `level`(exception only), `method`, `net_type`, `os`, `platform`, `region`, `ret`, `status`, `url`, `version`

**Operators**: `=`(equals), `!=`(not equals), `like`(fuzzy match), `not like`(fuzzy not match)

**Note**: `is_err` only filters retcode errors; usually not needed.

Filter example:
```json
[
    {"Key": "env", "Operator": "=", "Value": "production"},
    {"Key": "version", "Operator": "=", "Value": "2.0.0"},
    {"Key": "level", "Operator": "in", "Value": "('4','8')"}
]
```

### GroupBy Aggregation Dimensions

**Available values**: `brand`, `browser`, `device`, `env`, `ext1`~`ext10`, `from`, `is_abroad`, `is_err`, `isp`, `method`, `net_type`, `os`, `platform`, `region`, `ret`, `status`, `url`, `version`, `time(1m)`, `time(5m)`, `time(1h)`, `time(1d)`

**Key notes**:
- MUST pass as array even for single field, e.g. `["from"]`
- **For multi-dimensional analysis, query each dimension separately — never GroupBy all dimensions at once**
- Metric sorting defaults by data volume; sort by metric value manually after query

### Critical: `from` vs `url` vs `originFrom` Field Semantics in Queries

When using RUM query tools, these URL-related fields have distinct meanings:

| Field | Meaning in Query Context | Usage |
|-------|--------------------------|-------|
| `from` | **Page URL** — the page where the event occurred (processed by SDK's `urlHandler`) | Use in `GroupBy: ["from"]` or `Filters` to analyze by page dimension. Applies to: performance, network, exception, pv/uv metrics |
| `url` | **API/Resource URL** — the monitored network request or resource address | Use in `GroupBy: ["url"]` or `Filters` to analyze specific API endpoints or resources. Applies to: network and resource metrics. **Note**: `resource` metric does NOT support `from` filter — use `QueryResourceByPage` tool instead |
| `originFrom` | **Raw page URL** (unprocessed, from browser address bar) | NOT available as a GroupBy/Filter dimension in metric queries. Only visible in individual log details (via `QueryRumWebLog`). Web-only; returns empty on RN/Mini Program |

**Common mistakes to avoid**:
- Do NOT confuse `from` (page) with `url` (API/resource) — they answer different questions
- When user asks "which page has the most errors" → use `GroupBy: ["from"]`
- When user asks "which API is slowest" → use `GroupBy: ["url"]`
- When user asks about the "original page URL" in log details → that's `originFrom`

### Common Response Fields

**network type**:
- `allCount` - Total request count
- `duration_avg` - Average latency
- `error_rate_percent` - Status code error rate
- `retcode_error_percent` - Retcode error rate

**performance type**:
- `lcp_avg` - LCP average
- `fcp_avg` - FCP average
- `dns_avg` - DNS lookup time
- `tcp_avg` - TCP connection time
- `ssl_avg` - SSL handshake time
- `ttfb_avg` - TTFB time
- `content_download_avg` - Content download time
- `dom_parse_avg` - DOM parse time
- `resource_download_avg` - Resource download time
- `fmp_avg` - First meaningful paint time

**resource type**:
- `allCount` - Total request count
- `duration_avg` - Average loading time
- `error_rate_percent` - Loading error rate
- `connect_time_avg` - Connection time
- `domain_lookup_avg` - Domain lookup time
- `transfer_size_avg` - Transfer size (negative value means cross-origin prevents size retrieval)

**exception type**:
- `allCount` - Total exception count
- `affectCount` - Affected user count
- `error_rate_percent` - Error rate

---

## Tool 3: QueryRumWebLog

### Description
Query full RUM-WEB logs with rich filtering and pagination support.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ProjectId` | string | ✅ Yes | Application ID |
| `Limit` | number | ✅ Yes | Number of results, **default recommended 10**, max 1000 |
| `StartTime` | number | No | Start timestamp (seconds), default 2 hours ago |
| `EndTime` | number | No | End timestamp (seconds), default current time |
| `Region` | string | No | Region, default `ap-guangzhou` |
| `Filters` | array | No | Filter conditions array (**MUST be JSON objects, not strings**) |
| `RespFields` | array | No | Specify return fields; omit to return all (**use wisely to avoid oversized responses**) |
| `LastRowId` | number | No | For pagination — last row_id from previous response |
| `LastTime` | number | No | For pagination — last ts from previous response |

### Filters

**Supported fields**: `aid`, `brand`, `browser`, `city`, `country`, `device`, `env`, `errorMsg`, `ext1`~`ext10`, `from`, `ip`, `isAbroad`, `isp`, `level`, `method`, `msg`, `netType`, `os`, `platform`, `province`, `region`, `sessionId`, `sr`, `trace`, `ts`, `uin`, `userAgent`, `version`, `vp`

**Operators**: `eq`(equals), `neq`(not equals), `like`(fuzzy match), `nlike`(fuzzy not match), `in`

**Key notes**:
- Log tool operators (`eq`/`neq`/`like`/`nlike`/`in`) **differ from Metric tool operators** (`=`/`!=`/`like`/`not like`)
- `level` field **only supports** `eq`, `neq`, `in` operators
- Most info (including urls) is in the `msg` field — use `msg` with `like` to search URLs
- Region fields use `city` and `country` (not `region`)

### RespFields Options

`aid`, `brand`, `browser`, `city`, `country`, `device`, `env`, `errorMsg`, `ext1`~`ext10`, `from`, `ip`, `isAbroad`, `isp`, `level`, `method`, `msg`, `netType`, `os`, `platform`, `province`, `region`, `sessionId`, `sr`, `trace`, `ts`, `uin`, `userAgent`, `version`, `vp`

---

## Tool 4: QueryResourceByPage

### Description
Query resource metrics by page. Filter conditions only support the `from` field. For other filters or GroupBy, use `QueryRumWebMetric`.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ProjectId` | string | ✅ Yes | Application ID |
| `From` | string | ✅ Yes | Page URL to query |
| `StartTime` | number | No | Start timestamp (seconds), default 12 hours ago |
| `EndTime` | number | No | End timestamp (seconds), default current time |

### Response Metrics
- `duration_avg` - Average resource loading time
- `connect_time_avg` - Connection time
- `domain_lookup_avg` - Domain lookup time
- `transfer_size_avg` - Transfer size (**negative value means cross-origin prevents retrieval**; suggest configuring `Timing-Allow-Origin` in response headers)
- `error_rate_percent` - Resource loading error rate

---

## Tool 5: QueryApmLinkId

### Description
Get the APM application ID linked to a RUM application, enabling RUM-APM trace correlation.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ProjectId` | string | ✅ Yes | RUM application ID |
| `Region` | string | No | Region, default `ap-guangzhou` |

### Usage Scenario
When the `trace` field in logs is non-empty, call this tool to get the linked APM project ID, then use APM tools for deeper backend trace analysis.
