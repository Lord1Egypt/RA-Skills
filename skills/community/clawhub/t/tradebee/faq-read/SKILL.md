---
name: faq-read
description: A FAQ list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to retrieve FAQ data published on the website. It supports filtering by language, FAQ group, or exact FAQ ID, paginated retrieval, and can be used in FAQ display, content analysis, AI content operations, and SEO workflows.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faq-read

## Overview

Use the Tradebee Website Builder Open API to retrieve FAQ list data.

Supports language filtering, FAQ group filtering, exact FAQ ID filtering, and paginated queries. Returns complete FAQ structure data for use in FAQ display, content analysis, SEO workflows, and content operations.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Site language filter parameter.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `faq_id` (integer, Optional)

Exact FAQ filter.

> Omit this field to avoid FAQ-ID filtering.  
> If provided, use one positive integer (`> 0`) that matches an existing FAQ.  
> `faq_id` and `faqgroup_id` are mutually exclusive: omit both to read all FAQs, or provide exactly one of them.

---

### `faqgroup_id` (integer, Optional)

FAQ group filter.

> Omit this field to avoid FAQ-group filtering.  
> If provided, use a positive integer (`> 0`) selected from `faqgroup-read` under the same language.  
> `faq_id` and `faqgroup_id` are mutually exclusive: omit both to read all FAQs, or provide exactly one of them.

---

### `fields` (array of strings, Optional)

Field selection list. If omitted, all supported FAQ fields are returned.

Supported field values include:

- `faq_id`
- `language`
- `group`
- `images`
- `question`
- `tags`
- `summary`
- `answer`
- `seo`
- `faq_url`
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

| Field         | Type         | Description                |
|---------------|--------------|----------------------------|
| current_page  | integer      | Current page number        |
| page_size     | integer      | Items per page             |
| total_page    | integer      | Total pages                |
| total_count   | integer      | Total records              |
| has_next_page | boolean      | Whether a next page exists |
| next_page     | integer/null | Next page number           |

---

### `data.list[]`

FAQ data list.

| Field         | Type             | Description                              |
|---------------|------------------|------------------------------------------|
| `faq_id`      | integer          | FAQ ID                                   |
| `language`    | string           | Site language                            |
| `group`       | object           | FAQ group                                |
| `images`      | array            | FAQ image URL list. The current API returns up to one image and keeps the array shape for future expansion. |
| `question`    | string           | FAQ question                             |
| `tags`        | array            | FAQ keywords                             |
| `summary`     | string           | FAQ summary                              |
| `answer`      | string           | FAQ answer HTML                          |
| `seo`         | object           | SEO information                          |
| `faq_url`     | string           | FAQ detail URL path                      |
| `create_time` | string(datetime) | Creation time in ISO 8601 format         |
| `update_time` | string(datetime) | Update time in ISO 8601 format           |

---

### `group`

| Field         | Type    | Description |
|---------------|---------|-------------|
| `faqgroup_id` | integer | Group ID    |
| `group_name`  | string  | Group name  |

---

### `seo`

| Field         | Type   | Description                         |
|---------------|--------|-------------------------------------|
| `title`       | string | SEO title (<= 90 characters)        |
| `description` | string | SEO description (<= 200 characters) |
| `keywords`    | string | SEO keywords (<= 120 characters)    |

---

## Dependencies

| Parameter   | Dependency skill | Field source        | Mode   |
|-------------|------------------|---------------------|--------|
| language    | languages-get    | list[].language     | select |
| faqgroup_id | faqgroup-read    | list[].faqgroup_id  | select |

---

## Usage Examples

### 1. Read All FAQs

Use this when no exact FAQ or FAQ-group filter is needed.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read FAQs Under One FAQ Group

Use this when the user wants FAQs only from one selected group.

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

### 3. Read One Exact FAQ

Use this when the user already has one real `faq_id`.

```json
{
  "language": "en",
  "faq_id": 945,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact FAQ With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "language": "en",
  "faq_id": 945,
  "fields": [
    "faq_id",
    "language",
    "group",
    "question",
    "summary",
    "faq_url",
    "create_time",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 5. Read FAQs Under One Group With Full Content Fields

Use this when the caller needs full FAQ content for multiple items in one group.

```json
{
  "language": "en",
  "faqgroup_id": 216,
  "fields": [
    "faq_id",
    "language",
    "group",
    "images",
    "question",
    "tags",
    "summary",
    "answer",
    "seo",
    "faq_url",
    "create_time",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 6. Read the Next Page

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

- Omit both `faq_id` and `faqgroup_id` to read all FAQs.
- Send `faqgroup_id` only when filtering by one FAQ group.
- Send `faq_id` only when reading one exact FAQ.
- Never send `faq_id` and `faqgroup_id` together.
- When returning a list to the user, include one `faq_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `faq_url` and `faq_id` in `fields` when the caller needs the FAQ detail URL path or when a list response must include one ID and one preview URL.
- Omit `fields` to return all supported fields.
- When continuing pagination, always use `data.pagination.next_page`.
