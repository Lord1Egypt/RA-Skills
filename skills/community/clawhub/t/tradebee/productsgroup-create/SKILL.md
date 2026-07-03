---
name: productsgroup-create
description: A product group creation skill based on the "Tradebee Website Builder" Open API. It is used to create a new product group under a specified site language, with support for parent group, group name, tags, and brief description.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# productsgroup-create

## Overview

Use the Tradebee Website Builder Open API to create a new product group.

Supports creating a product group under a specified language with an optional parent group, group name, tags, an optional brief description, and optional custom top/bottom HTML decoration fragments.

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

### `productsgroup` (object, **Required**)

Complete product group payload for the new product group.

#### `productsgroup.parent_productsgroup_id` (integer, Optional)

Parent group ID.

- Omit this field or set `0` to create a top-level group
- If creating a child group, first call `productsgroup-read`
- Copy one exact `productsgroup_id`

#### `productsgroup.group_name` (string, **Required**)

Product group name, up to 200 characters.

#### `productsgroup.tags` (array, **Required**)

Provide 1 to 6 unique keyword tags. Each tag must contain 3 to 50 characters.

#### `productsgroup.brief_description` (string, Optional)

Short plain-text description, up to 4,000 characters.

#### `productsgroup.section` (object, Optional)

Custom HTML decoration fragments for the product group detail page body.

| Field    | Type   | Description |
|----------|--------|-------------|
| `top`    | string | Optional. Product group page header decoration fragment. HTML fragment only. Do not include `<h1>`, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. |
| `bottom` | string | Optional. Product group page footer decoration fragment. HTML fragment only. Do not include `<h1>`, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact product group creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact product group payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact product group payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field               | Type    | Description                  |
|---------------------|---------|------------------------------|
| `productsgroup_id`  | integer | Created product group ID     |
| `url`               | string  | Preview URL for the created product group page. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter                             | Dependency skill         | Field source              | Mode   |
|---------------------------------------|--------------------------|---------------------------|--------|
| language                              | languages-get        | list[].language           | select |
| productsgroup.parent_productsgroup_id | productsgroup-read   | list[].productsgroup_id   | select |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `productsgroup.group_name`
- `productsgroup.tags`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a product group in language en with the shown payload."
  },
  "productsgroup": {
    "parent_productsgroup_id": 0,
    "group_name": "led light",
    "tags": ["light", "led"],
    "brief_description": "a led light",
    "section": {
      "top": "<div style=\"padding:16px;background:#f7f7f7;\">top html</div>",
      "bottom": "<div style=\"padding:16px;background:#f7f7f7;\">bottom html</div>"
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
    "productsgroup_id": 8
  }
}
```
