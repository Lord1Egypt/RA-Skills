---
name: keywords-rank
description: Keyword ranking analytics based on the Tradebee Website Builder Open API. It is used to retrieve keyword ranking records, the latest rank value, and rank history.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# keywords-rank

## Overview

Use the Tradebee Website Builder Open API to retrieve keyword ranking records and rank history.

Supports exact keyword filtering, exact rank filtering, and paginated queries.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `keywords` (string, Optional)

Exact keyword filter.

- Omit this field to read all keyword ranking records
- If provided, use one exact non-empty keyword string
- `keywords` and `rank` are mutually exclusive: omit both to read all records, or provide exactly one of them

---

### `rank` (integer, Optional)

Top-N rank filter.

- Omit this field to read all keyword ranking records
- If provided, use one integer from `1` to `999`
- `rank=100` means return keywords ranked within the top 100 positions
- This does not mean `rank` must equal `100`
- `keywords` and `rank` are mutually exclusive: omit both to read all records, or provide exactly one of them

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

- **Default:** 10
- **Range:** 10 ~ 50

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

### `data.list[]` (keyword ranking list)

| Field              | Type    | Description                        |
|--------------------|---------|------------------------------------|
| keywords_rank_guid | string  | Unique keyword ranking identifier  |
| keywords           | string  | Keyword                            |
| referer            | string  | Source URL                         |
| rank               | integer | Latest ranking, `-1` means unknown |
| rank_history       | array   | Historical ranking records         |

---

### `rank_history[]` Object

| Field          | Type    | Description                |
|----------------|---------|----------------------------|
| rank_date      | string  | Ranking snapshot date      |
| popularity     | integer | Keyword popularity         |
| rank           | integer | Historical ranking value   |
| current_url    | string  | Ranked page URL            |
| search_context | object  | Search context information |

#### `search_context`

| Field    | Type   | Description       |
|----------|--------|-------------------|
| country  | string | Search country    |
| language | string | Search language   |
| referer  | string | Search source URL |

---

### Notes

1. `data` may be `null` on failure
2. `rank=-1` means the ranking is unknown
3. Whether to continue pagination is decided by the caller

---

## Usage Examples

### 1. Read All Keyword Ranking Records

```json
{
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read One Exact Keyword

```json
{
  "keywords": "activewear clothing manufacturers",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read Keywords Ranked Within the Top 100

```json
{
  "rank": 100,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact Keyword and Continue Pagination

```json
{
  "keywords": "activewear clothing manufacturers",
  "pagination": {
    "current_page": 2,
    "page_size": 5
  }
}
```

### Selection Rules

- Omit both `keywords` and `rank` to read all keyword ranking records.
- Send `keywords` only when reading one exact keyword.
- Send `rank` only when filtering by a top-N rank threshold from `1` to `999`.
- `rank=100` means return keywords ranked within positions `1` through `100`.
- Never send `keywords` and `rank` together.
- When continuing pagination, always use `data.pagination.next_page`.
