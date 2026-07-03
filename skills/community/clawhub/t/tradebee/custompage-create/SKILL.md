---
name: custompage-create
description: A custom page creation skill based on the "Tradebee Website Builder" Open API. It is used to create and publish a new custom page under a specified site language, with support for title, HTML content, and SEO fields.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# custompage-create

## Overview

Use the Tradebee Website Builder Open API to create and publish a new custom page.

Supports publishing a custom page under a specified language with title, HTML content, and SEO fields.

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

### `language` (string, **Required**)

Exact site language code to publish into.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

### `custompage` (object, **Required**)

Complete custom page payload for the new custom page.

#### `custompage.title` (string, **Required**)

Custom page title shown to users, up to 100 characters.

#### `custompage.content` (string, **Required**)

HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Before generating this field, call `rule-get` with the exact selected `language` and the exact scene value `custompage.content`. The fragment must follow the returned rule payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method.

#### `custompage.seo` (object, Optional)

SEO metadata for the custom page detail page.

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords` | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact custom page creation request after seeing the final language and payload.

| Field | Type | Description |
|-------|------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact custom page payload to be created. Never set this by assumption. |
| `summary` | string | Restates the language and exact custom page payload shown to the user before execution. |

## Output Structure

| Field | Type | Description |
|-------|------|-------------|
| status | boolean | Request status |
| msg | string | Response message |
| data | object/null | Returned data |

### `data`

| Field | Type | Description |
|-------|------|-------------|
| `custompage_id` | integer | Created custom page ID |
| `url` | string | Preview URL for the created custom page. Return this to the user and ask the user to preview it. |

## Dependencies

| Parameter | Dependency skill | Field source | Mode |
|-----------|------------------|--------------|------|
| language | languages-get | list[].language | select |

## Usage Example

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a custom page in language en with the shown payload."
  },
  "custompage": {
    "title": "About Our Manufacturing",
    "content": "<section><h2>About Our Manufacturing</h2><p>...</p></section>",
    "seo": {
      "title": "About Our Manufacturing",
      "description": "Learn more about our manufacturing capabilities.",
      "keywords": "manufacturing,factory,company"
    }
  }
}
```
