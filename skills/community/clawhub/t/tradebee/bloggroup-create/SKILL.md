---
name: bloggroup-create
description: A blog group creation skill based on the "Tradebee Website Builder" Open API. It is used to create and publish a new blog group under a specified site language, with support for group name, tags, and brief description.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# bloggroup-create

## Overview

Use the Tradebee Website Builder Open API to create and publish a new blog group.

Supports publishing a blog group under a specified language with group name, tags, and an optional brief description.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code to publish into.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `bloggroup` (object, **Required**)

Complete blog group payload for the new blog group.

#### `bloggroup.group_name` (string, **Required**)

Blog group name, up to 100 characters.

#### `bloggroup.tags` (array, **Required**)

Provide 1 to 6 keyword tags. Each tag must be 50 characters or fewer.

#### `bloggroup.brief_description` (string, Optional)

Short plain-text description, up to 300 characters.

#### `bloggroup.seo` (object, Optional)

SEO metadata for search engines.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact blog group creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact blog group payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact blog group payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field           | Type    | Description            |
|-----------------|---------|------------------------|
| `bloggroup_id`  | integer | Created blog group ID  |
| `url`           | string  | Preview URL for the created blog group page. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter | Dependency skill  | Field source    | Mode   |
|-----------|-------------------|-----------------|--------|
| language  | languages-get | list[].language | select |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `bloggroup.group_name`
- `bloggroup.tags`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a blog group in language en with the shown payload."
  },
  "bloggroup": {
    "group_name": "name",
    "tags": ["tags 1", "tags 2"],
    "brief_description": "brief description",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "keyword1,keyword2,keyword3"
    }
  }
}
```

## Response Example

```json
{
  "status": true,
  "msg": "create successfully",
  "data": {
    "bloggroup_id": 8
  }
}
```
