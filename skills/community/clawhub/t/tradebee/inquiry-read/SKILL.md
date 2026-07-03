---
name: inquiry-read
description: Read, paginate, and analyze inquiry data from the Tradebee Website Builder platform, with support for multi-language filtering, field selection, and structured report generation. Inquiry data may include privacy-sensitive fields such as contact details, IP addresses, message content, and attachment URLs, so prefer explicit minimal field selection and request sensitive fields only when clearly needed for the stated Tradebee inquiry task.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# inquiry-read

## Overview

Use the Tradebee Website Builder Open API to read inquiry data and generate a structured analysis report.

Supports full-field retrieval, on-demand field selection (`fields`), multi-language filtering, and paginated queries.

Privacy reminder:

- Inquiry records may contain contact details, IP addresses, message content, and attachment URLs.
- Prefer explicit minimal field selection instead of full-field retrieval.
- Request sensitive fields only when they are clearly needed for the user's stated Tradebee inquiry task.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and inquiry data to the external Tradebee Website Builder API, so only send the minimum data and request the minimum fields needed for the user's stated task.

---

### `language` (string, Optional)

Site language filter.

> Warning: **Constraint:** If this parameter is provided, it must be selected manually from the list returned by the `languages-get` skill. AI inference is not allowed.

---

### `recent_days` (integer, Optional)

Time-range filter for inquiries.

> Warning: **Constraint:** Returns inquiry data from the most recent specified number of days, with a range of 0-36500. The default value is `0`, meaning no time limit and all inquiries are returned.

---

### `fields` (array of strings, Optional)

Field whitelist. Specifies which inquiry fields to return. If omitted, all fields are returned.

> Privacy warning: Inquiry data may contain personal or business-sensitive information such as IP addresses, contact names, email addresses, phone numbers, physical addresses, attachments, and freeform message content. Prefer an explicit minimal `fields` list whenever possible instead of omitting `fields`.

> Data-minimization rule: Request `ip`, `contact`, `attachment`, `content`, or broad all-field responses only when the user clearly needs those exact fields for the stated Tradebee inquiry task. Do not request, summarize, export, or retain those fields unnecessarily.

**Available values:**

| Field             | Description              |
|------------------|--------------------------|
| `inquiry_id`     | Unique inquiry ID        |
| `language`       | Language                 |
| `is_read`        | Whether it has been read |
| `title`          | Inquiry title            |
| `content`        | Inquiry content          |
| `country_code`   | Country code             |
| `ip`             | IP address               |
| `contact`        | Contact information object |
| `source`         | Source channel           |
| `target_products`| Related product list     |
| `attachment`     | Inquiry attachment list  |
| `create_time`    | Creation time            |

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

### `data.pagination`

| Field          | Type         | Description            |
|----------------|--------------|------------------------|
| current_page   | integer      | Current page number    |
| page_size      | integer      | Items per page         |
| total_page     | integer      | Total pages            |
| total_count    | integer      | Total records          |
| has_next_page  | boolean      | Whether a next page exists |
| next_page      | integer/null | Next page number       |

### `data.list[]` (array of objects)

Each inquiry record contains the following fields:

Privacy handling note:

- `content`, `ip`, `contact`, and `attachment` may contain personal data or sensitive business data.
- Return or summarize only the minimum fields needed for the user's stated task.
- If the user does not explicitly need contact details, IPs, addresses, attachments, or freeform inquiry content, exclude those fields from `fields`.

| Field           | Type              | Description                             |
|----------------|-------------------|-----------------------------------------|
| inquiry_id     | integer           | Unique inquiry ID                       |
| language       | string            | Site language                           |
| is_read        | boolean           | Whether it has been read                |
| title          | string            | Inquiry title                           |
| content        | string            | Inquiry content, which may contain an HTML form |
| country_code   | string            | Country code (ISO 3166-1)               |
| ip             | string            | IPv4 or IPv6 address                    |
| contact        | object            | Contact information                     |
| source         | string            | Inquiry source channel                  |
| target_products| array of objects  | Related product list                    |
| attachment     | array of objects  | Inquiry attachment list                 |
| create_time    | string (datetime) | Creation time (ISO 8601 format)         |

#### `contact` Object

| Field   | Type   | Description     |
|---------|--------|-----------------|
| name    | string | Contact name    |
| email   | string | Email address   |
| tel     | string | Contact phone   |
| address | string | Contact address |

#### `target_products[]` Object

| Field         | Type    | Description  |
|---------------|---------|--------------|
| products_id   | integer | Product ID   |
| product_name  | string  | Product name |
| products_url  | string  | Product URL  |

#### `attachment[]` Object

| Field       | Type   | Description                 |
|-------------|--------|-----------------------------|
| file_name   | string | Original uploaded file name |
| file_url    | string | Attachment download URL     |

---

## Dependencies

| Parameter  | Dependency skill      | Related field       | Mode   |
|------------|-----------------------|---------------------|--------|
| language   | `languages-get`   | `list[].language`   | select |

The value of the `language` parameter must be selected manually from the list returned by `languages-get`.

---

## Usage Examples

### 1. Read All Inquiries

Use this when no filter is needed.

```json
{
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read Inquiries With a Language Filter

Use this when the caller only wants inquiries from one exact site language.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read Inquiries From the Last 7 Days

Use this when the caller wants a recent time window only.

```json
{
  "recent_days": 7,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read Inquiries With Both Language and Time Filters

Use this when the caller wants one language within a recent time window.

```json
{
  "language": "en",
  "recent_days": 30,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 5. Read Inquiries With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "fields": [
    "inquiry_id",
    "language",
    "country_code",
    "contact",
    "source",
    "create_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 10
  }
}
```

### 6. Read Inquiries With All Optional Filters Combined

Use this when the caller wants one language, one time window, and only selected fields.

```json
{
  "language": "en",
  "recent_days": 7,
  "fields": [
    "inquiry_id",
    "language",
    "is_read",
    "contact",
    "target_products",
    "create_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 10
  }
}
```

### 7. Read the Next Page

Use the exact `next_page` value returned by the previous response.

```json
{
  "pagination": {
    "current_page": 2,
    "page_size": 5
  }
}
```

### Selection Rules

- Omit `language` to read inquiries from all enabled languages.
- Omit `recent_days` or set it to `0` to remove the time limit.
- Omit `fields` to return all supported inquiry fields, but prefer an explicit minimal field list whenever inquiry data may include personal or sensitive content.
- Combine `language`, `recent_days`, and `fields` freely when needed.
- When continuing pagination, always use `data.pagination.next_page`.

---

## Notes

1. Configure `BEE_API_KEY` in the environment before using this skill. Never provide API keys in tool inputs, prompts, examples, logs, or chat text.
2. `pagination` must comply with the allowed range (`page_size` 1-10, `current_page` >= 1)
3. `language` must be manually selected from `languages-get` and must not be inferred by the system
4. Pagination rules: `data.pagination.has_next_page` indicates whether a next page exists; `data.pagination.next_page` provides the next page number and is `null` if there is no next page; **whether to continue is decided by the user**
5. `fields` is optional. If omitted, all fields are returned; if provided, only the specified fields are returned
6. Request `contact`, `ip`, `attachment`, and `content` only when those exact fields are required for the user's stated Tradebee inquiry task

---

## Applicable Scenarios

- Foreign trade inquiry data retrieval
- Customer source channel statistics
- Product popularity and conversion analysis
- Customer profiling and identity tag analysis
- Paginated export and CRM data synchronization
