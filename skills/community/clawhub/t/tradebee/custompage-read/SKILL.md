---
name: custompage-read
description: A custom page read skill based on the "Tradebee Website Builder" Open API. It is used to read one exact custom page or list custom pages under a specified site language, with support for field selection and pagination.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# custompage-read

## Overview

Use the Tradebee Website Builder Open API to read one exact custom page or list custom pages under a selected language.

Supports exact custom page filtering, field selection, and pagination.

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

### `language` (string, **Required**)

Exact site language code to read from.

### `custompage_id` (integer, Optional)

Exact custom page filter.

- Omit this field to read all custom pages
- Provide one exact positive `custompage_id` to read one custom page

### `fields` (array, Optional)

Field selection list.

Supported values:

- `custompage_id`
- `custompage_url`
- `language`
- `title`
- `content`
- `seo`
- `create_time`
- `update_time`

### `pagination` (object, Optional)

```json
{
  "current_page": 1,
  "page_size": 5
}
```

## Selection Rules

- Omit `custompage_id` to read all custom pages.
- Send `custompage_id` only when reading one exact custom page.
- When returning a list to the user, include one `custompage_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `custompage_url` and `custompage_id` in `fields` when the caller needs the custom page URL path or when a list response must include one ID and one preview URL.

## Usage Example

```json
{
  "language": "en",
  "custompage_id": 23,
  "fields": ["custompage_id", "title", "content", "seo"],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```
