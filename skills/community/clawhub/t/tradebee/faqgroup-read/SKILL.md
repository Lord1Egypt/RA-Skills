---
name: faqgroup-read
description: A FAQ group list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to retrieve FAQ group data configured on the website. It supports filtering by language, exact FAQ group ID, field selection, and paginated retrieval for FAQ navigation, content organization, SEO planning, and content operations workflows.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faqgroup-read

## Overview

Use the Tradebee Website Builder Open API to retrieve FAQ group list data.

Supports language filtering, exact FAQ group ID filtering, field selection, and paginated queries. It can be used for FAQ navigation building, group selection, content analysis, SEO organization, and similar FAQ-content workflows.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Site language filter parameter.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `faqgroup_id` (integer, Optional)

Exact FAQ group filter.

- Omit this field to read all FAQ groups
- If provided, use one positive integer (`> 0`) that matches an existing FAQ group

---

### `fields` (array of strings, Optional)

Field selection list. If omitted, all supported FAQ group fields are returned.

Supported fields include:

- `faqgroup_id`
- `language`
- `group_name`
- `brief_description`
- `seo`
- `faqgroup_url`
- `create_time`
- `update_time`

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

- Default: 5
- Range: 1 - 10

---

## Output Structure

### Top-Level Structure

| Field  | Type        | Description      |
|--------|-------------|------------------|
| status | boolean     | Request status   |
| msg    | string      | Response message |
| data   | object/null | Returned data    |

---

### `data.pagination`

| Field         | Type         | Description                   |
|---------------|--------------|-------------------------------|
| current_page  | integer      | Current page number           |
| page_size     | integer      | Items per page                |
| total_page    | integer      | Total pages                   |
| total_count   | integer      | Total records                 |
| has_next_page | boolean      | Whether a next page exists    |
| next_page     | integer/null | Next page number              |

---

### `data.list[]`

FAQ group data list.

| Field               | Type             | Description                       |
|---------------------|------------------|-----------------------------------|
| `faqgroup_id`       | integer          | FAQ group ID                      |
| `language`          | string           | Site language                     |
| `group_name`        | string           | FAQ group name                    |
| `brief_description` | string           | Short FAQ group description       |
| `seo`               | object           | SEO information                   |
| `faqgroup_url`      | string           | FAQ group page URL path           |
| `create_time`       | string(datetime) | Creation time in ISO 8601 format  |
| `update_time`       | string(datetime) | Update time in ISO 8601 format    |

---

### `seo`

| Field         | Type   | Description                         |
|---------------|--------|-------------------------------------|
| `title`       | string | SEO title (<= 90 characters)        |
| `description` | string | SEO description (<= 200 characters) |
| `keywords`    | string | SEO keywords (<= 120 characters)    |

---

## Dependencies

| Parameter | Dependency skill | Field source    | Mode   |
|-----------|------------------|-----------------|--------|
| language  | languages-get    | list[].language | select |

---

## Usage Rules

- `language` must be obtained through `languages-get`
- `faqgroup_id` reads one exact FAQ group when provided
- Treat `create_time` and `update_time` as ISO 8601 date-time strings
- If pagination continues, use `next_page` instead of guessing the next page number

---

## Usage Examples

### 1. Read All FAQ Groups

Use this when no exact group filter is needed.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read One Exact FAQ Group

Use this when the user already has one real `faqgroup_id`.

```json
{
  "language": "en",
  "faqgroup_id": 216,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read FAQ Groups With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "language": "en",
  "fields": [
    "faqgroup_id",
    "language",
    "group_name",
    "faqgroup_url",
    "create_time",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact FAQ Group With SEO Fields

Use this when the caller needs metadata for one exact group.

```json
{
  "language": "en",
  "faqgroup_id": 216,
  "fields": [
    "faqgroup_id",
    "language",
    "group_name",
    "brief_description",
    "seo",
    "faqgroup_url",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 5. Read the Next Page

Use the exact `next_page` value returned by the previous response.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 2,
    "page_size": 5
  }
}
```

### Selection Rules

- Omit `faqgroup_id` to read all FAQ groups.
- Send `faqgroup_id` only when reading one exact FAQ group.
- When returning a list to the user, include one `faqgroup_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `faqgroup_url` and `faqgroup_id` in `fields` when the caller needs the FAQ group page URL path or when a list response must include one ID and one preview URL.
- Omit `fields` to return all supported fields.
- When continuing pagination, always use `data.pagination.next_page`.
