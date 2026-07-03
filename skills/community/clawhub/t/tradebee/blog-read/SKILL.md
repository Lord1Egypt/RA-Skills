---
name: blog-read
description: A blog list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to retrieve blog data published on the website. It supports filtering by language, blog group, or exact blog ID, paginated retrieval, and can be used in blog display, content analysis, AI content operations, and SEO workflows.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# blog-read

## Overview

Use the Tradebee Website Builder Open API to retrieve blog list data.

Supports language filtering, blog group filtering, exact blog ID filtering, and paginated queries. Returns complete blog structure data for use in blog display, content analysis, SEO workflows, and content operations.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Site language filter parameter.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `blog_id` (integer, Optional)

Exact blog filter.

> Omit this field to avoid blog-ID filtering.  
> If provided, use one positive integer (`> 0`) that matches an existing blog.  
> `blog_id` and `bloggroup_id` are mutually exclusive: omit both to read all blogs, or provide exactly one of them.

---

### `bloggroup_id` (integer, Optional)

Blog group filter.

> Omit this field to avoid blog-group filtering.  
> If provided, use a positive integer (`> 0`) selected from `bloggroup-read` under the same language.  
> `blog_id` and `bloggroup_id` are mutually exclusive: omit both to read all blogs, or provide exactly one of them.

---

### `fields` (array of strings, Optional)

Field selection list. If omitted, all supported blog fields are returned.

Supported field values include:

- `blog_id`
- `language`
- `group`
- `publisher`
- `publication_date`
- `title`
- `images`
- `tags`
- `summary`
- `description`
- `seo`
- `blog_url`
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

- Default: 10
- Range: 10 - 50

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

Blog data list.

| Field            | Type             | Description                       |
|------------------|------------------|-----------------------------------|
| blog_id          | integer          | Blog ID                           |
| language         | string           | Site language                     |
| group            | object           | Blog group                        |
| publisher        | string           | Publisher                         |
| publication_date | string           | Display publication date          |
| title            | string           | Blog title                        |
| images           | array            | Blog cover image URL list         |
| tags             | array            | Keywords                          |
| summary          | string           | Summary                           |
| description      | string           | Detailed description (HTML)       |
| seo              | object           | SEO information                   |
| blog_url         | string           | Blog detail URL path              |
| create_time      | string(datetime) | Creation time in ISO 8601 format  |
| update_time      | string(datetime) | Update time in ISO 8601 format    |

---

### `group`

| Field          | Type    | Description |
|----------------|---------|-------------|
| bloggroup_id   | integer | Group ID    |
| group_name     | string  | Group name  |

---

### `seo`

| Field         | Type   | Description                        |
|---------------|--------|------------------------------------|
| title         | string | SEO title (<= 90 characters)       |
| description   | string | SEO description (<= 200 characters) |
| keywords      | string | SEO keywords (<= 120 characters)   |

---

## Dependencies

| Parameter      | Dependency skill   | Field source        | Mode   |
|----------------|--------------------|---------------------|--------|
| language       | languages-get  | list[].language     | select |
| bloggroup_id   | bloggroup-read | list[].bloggroup_id | select |

---

## Usage Examples

### 1. Read All Blogs

Use this when no exact blog or blog-group filter is needed.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read Blogs Under One Blog Group

Use this when the user wants blogs only from one selected group.

```json
{
  "language": "en",
  "bloggroup_id": 454,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read One Exact Blog

Use this when the user already has one real `blog_id`.

```json
{
  "language": "en",
  "blog_id": 945,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact Blog With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "language": "en",
  "blog_id": 945,
  "fields": [
    "blog_id",
    "language",
    "group",
    "title",
    "summary",
    "blog_url",
    "create_time",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 5. Read Blogs Under One Group With Full Content Fields

Use this when the caller needs full article content for multiple blogs in one group.

```json
{
  "language": "en",
  "bloggroup_id": 454,
  "fields": [
    "blog_id",
    "language",
    "group",
    "publisher",
    "publication_date",
    "title",
    "images",
    "tags",
    "summary",
    "description",
    "seo",
    "blog_url",
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

- Omit both `blog_id` and `bloggroup_id` to read all blogs.
- Send `bloggroup_id` only when filtering by one blog group.
- Send `blog_id` only when reading one exact blog.
- Never send `blog_id` and `bloggroup_id` together.
- When returning a list to the user, include one `blog_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `blog_url` and `blog_id` in `fields` when the caller needs the blog detail URL path or when a list response must include one ID and one preview URL.
- Omit `fields` to return all supported fields.
- When continuing pagination, always use `data.pagination.next_page`.
