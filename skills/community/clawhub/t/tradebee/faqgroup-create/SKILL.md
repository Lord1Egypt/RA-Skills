---
name: faqgroup-create
description: A FAQ group creation skill based on the "Tradebee Website Builder" Open API. It is used to create and publish a new FAQ group under a specified site language, with support for group name, brief description, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faqgroup-create

## Overview

Use the Tradebee Website Builder Open API to create and publish a new FAQ group.

Supports publishing a FAQ group under a specified language with group name, an optional brief description, and SEO data.

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

### `faqgroup` (object, **Required**)

Complete FAQ group payload for the new FAQ group.

#### `faqgroup.group_name` (string, **Required**)

FAQ group name, up to 100 characters.

#### `faqgroup.brief_description` (string, Optional)

Short plain-text description, up to 300 characters.

#### `faqgroup.seo` (object, Optional)

SEO metadata for search engines.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact FAQ group creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact FAQ group payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact FAQ group payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field           | Type    | Description |
|-----------------|---------|-------------|
| `faqgroup_id`   | integer | Created FAQ group ID |
| `url`           | string  | Preview URL for the created FAQ group page. Return this to the user so the user can decide whether to preview it. |

---

## Dependencies

| Parameter | Dependency skill | Field source    | Mode   |
|-----------|------------------|-----------------|--------|
| language  | languages-get    | list[].language | select |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `faqgroup.group_name`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a FAQ group in language en with the shown payload."
  },
  "faqgroup": {
    "group_name": "Shipping FAQ",
    "brief_description": "Frequently asked questions about shipping.",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "shipping,delivery,faq"
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
    "faqgroup_id": 8,
    "url": "example.com/faqid8/shipping-faq.htm"
  }
}
```
