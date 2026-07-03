---
name: visitor-recent
description: A latest visitor data retrieval skill based on the "Tradebee Website Builder" Open API. It is used to obtain the latest visitor list and generate structured analysis data. Use it only when the user explicitly wants Tradebee visitor analytics or one exact Tradebee visitor record, not for generic analytics, traffic, or monitoring requests outside Tradebee visitor data context. Visitor data may include privacy-sensitive telemetry such as IP addresses, referrer URLs, current URLs, user-agent strings, screen resolution, and visit timestamps, so request and expose only the minimum data needed for the user's stated Tradebee visitor-analysis task.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# visitor-recent

## Overview

Use the Tradebee Website Builder Open API to retrieve the latest visitor data and generate a structured analysis report.

Supports exact IP filtering and paginated queries.

Privacy reminder:

- Visitor records may contain IP addresses, referrer URLs, current URLs, user-agent strings, screen resolution, and visit timestamps.
- Treat this data as privacy-sensitive telemetry.
- Prefer the narrowest possible request, and use exact IP filtering only when the user clearly needs one specific visitor record.
- Do not retrieve, summarize, export, or retain more visitor telemetry than the user's stated Tradebee task requires.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and visitor data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `ip` (string, Optional)

Exact visitor IP filter.

- Omit this field to read recent visitors for all IPs
- If provided, use one exact IPv4 or IPv6 address
- IP data is privacy-sensitive; request it only when the user clearly needs one exact visitor IP

---

### `pagination` (object, **Required**)

Pagination configuration parameters.

#### `current_page` (integer)

- Default: 1
- Minimum: 1
- Pagination rules:
  - Must rely on `data.pagination.has_next_page`
  - Use `data.pagination.next_page` as the next page number
  - Do not infer pages based on `total_page` or manual increments
  - Requests must stop when `has_next_page=false`

#### `page_size` (integer)

- **Default:** 5
- **Range:** 1 ~ 10

---

## Output Structure

### Top-Level Fields

| Field  | Type           | Description                            |
|--------|----------------|----------------------------------------|
| status | boolean        | Request status, `true` for success / `false` for failure |
| msg    | string         | Response message                       |
| data   | object \| null | Response data, `null` on failure       |

---

### `data.pagination`

| Field          | Type         | Description            |
|----------------|--------------|------------------------|
| current_page   | integer      | Current page number    |
| page_size      | integer      | Items per page         |
| total_page     | integer      | Total pages            |
| total_count    | integer      | Total records          |
| has_next_page  | boolean      | Whether a next page exists |
| next_page      | integer/null | Next page number       |

---

### `data.list[]` (visitor data list)

Privacy handling note:

- `ip`, `referer`, `current_url`, `user_agent`, `screen`, `first_visit_time`, `last_visit_time`, and `recent_visits` are privacy-sensitive visitor telemetry.
- Return or summarize only the minimum fields needed for the user's stated task.
- If the user does not explicitly need one exact visitor IP or visit-trace detail, avoid unnecessary broad retrieval or downstream exposure of those fields.

| Field            | Type    | Description                   |
|------------------|---------|-------------------------------|
| ip               | string  | Visitor IP (IPv4 / IPv6)      |
| country_code     | string  | Country code (ISO 3166-1)     |
| page_views       | integer | Page view count               |
| first_visit      | object  | First visit record            |
| recent_visits    | array   | Recent visit records (up to 50) |
| first_visit_time | string  | First visit time (ISO 8601)   |
| last_visit_time  | string  | Last visit time (ISO 8601)    |

---

### `first_visit` Object

| Field        | Type   | Description              |
|--------------|--------|--------------------------|
| page         | object | First visited page info  |
| screen       | object | Screen resolution        |
| visit_time   | string | First visit time         |
| referer      | string | Referrer URL             |
| current_url  | string | Current visit URL        |
| user_agent   | string | Browser User-Agent       |

#### `first_visit.page`

| Field | Type    | Description     |
|-------|---------|-----------------|
| id    | integer | Page ID         |
| name  | string  | Page name       |
| code  | string  | Page identifier |

#### `first_visit.screen`

| Field  | Type    | Description   |
|--------|---------|---------------|
| width  | integer | Screen width  |
| height | integer | Screen height |

---

### `recent_visits[]` Object

| Field        | Type   | Description         |
|--------------|--------|---------------------|
| page         | object | Page information    |
| screen       | object | Screen resolution   |
| visit_time   | string | Visit time          |
| referer      | string | Referrer URL        |
| current_url  | string | Current URL         |
| user_agent   | string | Browser User-Agent  |

#### `recent_visits.page`

| Field | Type    | Description     |
|-------|---------|-----------------|
| id    | integer | Page ID         |
| name  | string  | Page name       |
| code  | string  | Page identifier |

#### `recent_visits.screen`

| Field  | Type    | Description |
|--------|---------|-------------|
| width  | integer | Width       |
| height | integer | Height      |

---

### Notes

1. `data` may be `null` on failure
2. `recent_visits` contains at most 50 entries
3. All time fields use ISO 8601
4. `next_page` is valid only when `has_next_page=true`
5. Whether to continue pagination is decided by the caller
6. Do not add `api_key` or any other credential field to request JSON examples or live requests; authentication must come only from the configured `BEE_API_KEY` environment variable
7. Exact IP queries are privacy-sensitive and should be used only when the user clearly needs one specific visitor record for the stated Tradebee task

---

## Usage Examples

### 1. Read Recent Visitors From All IPs

Authentication note: do not add `api_key` to the request body. Authentication comes only from the configured `BEE_API_KEY` environment variable.

```json
{
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read One Exact IPv4 Visitor

Privacy note: use an exact IP query only when the user clearly needs one specific visitor record.

```json
{
  "ip": "127.0.0.1",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read One Exact IPv6 Visitor

Privacy note: use an exact IP query only when the user clearly needs one specific visitor record.

```json
{
  "ip": "2001:db8::1",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact IP and Continue Pagination

Privacy note: continue exact IP pagination only when the user still needs more records for that same specific visitor.

```json
{
  "ip": "127.0.0.1",
  "pagination": {
    "current_page": 2,
    "page_size": 5
  }
}
```

### Selection Rules

- Omit `ip` to read recent visitors for all IPs.
- Send `ip` only when the caller wants one exact visitor IP.
- Because IP and visit-trace data are privacy-sensitive, prefer one exact IP over broad visitor retrieval whenever the user's task can be narrowed that way.
- `ip` supports both IPv4 and IPv6 string values.
- When continuing pagination, always use `data.pagination.next_page`.
