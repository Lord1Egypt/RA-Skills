---
name: custompage-update
description: A custom page update skill based on the "Tradebee Website Builder" Open API. It is used to update one existing custom page under a specified site language. Before sending the update request, it automatically reads the current record and writes a local JSON backup file for restore use.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# custompage-update

## Overview

Use the Tradebee Website Builder Open API to update one existing custom page.

Before sending the update request, this skill:

- reads the current custom page
- writes a local JSON backup file under `backups/custompage-update/`
- returns a best-effort `restore_payload` for later restore use

## Input Parameters

### `language` (string, **Required**)

Exact site language code to update in.

### `custompage` (object, **Required**)

Update payload for one existing custom page.

#### `custompage.custompage_id` (integer, **Required**)

Existing custom page ID to update.

#### `custompage.title` (string, Optional)

Custom page title, up to 100 characters. Omit it if the title should stay unchanged.

#### `custompage.content` (string, Optional)

HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags. Before generating this field, call `rule-get` with the exact selected `language` and the exact scene value `custompage.content`. The fragment must follow the returned rule payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit this field if the content should stay unchanged.

#### `custompage.seo` (object, Optional)

SEO fields for the custom page detail page.

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords` | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact custom page update request after seeing the final language, target custom page ID, payload, and automatic local backup behavior.

## Output Structure

| Field | Type | Description |
|-------|------|-------------|
| status | boolean | Request status |
| msg | string | Response message |
| data | object/null | Returned data |
| backup | object/null | Automatic pre-update backup metadata, snapshot, and restore payload |

### `data`

| Field | Type | Description |
|-------|------|-------------|
| `custompage_id` | integer | Updated custom page ID |
| `url` | string | Preview URL for the updated custom page. Return this to the user and ask the user to preview it. |

### `backup`

| Field | Type | Description |
|-------|------|-------------|
| `storage.file_path` | string | Local backup JSON file path |
| `raw_read_response` | object | Raw custom page read response captured before update |
| `snapshot` | object | Extracted pre-update custom page snapshot |
| `restore_payload` | object | Best-effort payload that can be passed back into `custompage-update` to restore the previous state |

## Usage Example

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update custom page 23 in language en with the shown payload."
  },
  "custompage": {
    "custompage_id": 23,
    "title": "Updated title",
    "content": "<section><h2>Updated title</h2><p>...</p></section>",
    "seo": {
      "title": "Updated title",
      "description": "Updated SEO description.",
      "keywords": "custom page,company,about"
    }
  }
}
```
