---
name: productsgroup-update
description: A product group update skill based on the "Tradebee Website Builder" Open API. Before sending the update request, it automatically reads the current product group and writes a local JSON backup file containing the pre-update backup bundle. It then updates an existing product group under a specified site language and supports updating group name, tags, brief description, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# productsgroup-update

## Overview

Use the Tradebee Website Builder Open API to update an existing product group after automatically reading the current record and writing a local JSON backup file containing the pre-update backup bundle.

Supports updating group name, tags, brief description, custom top/bottom HTML decoration fragments, and SEO data under a specified language.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code to update.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `productsgroup` (object, **Required**)

Product group fields to update.

#### `productsgroup.productsgroup_id` (integer, **Required**)

Existing product group ID to update.

- First call `productsgroup-read`
- Copy one exact `productsgroup_id`

#### `productsgroup.group_name` (string, Optional)

Product group name, up to 200 characters. Omit this field unless the user explicitly wants to change it.

#### `productsgroup.tags` (array, Optional)

Provide up to 6 unique keyword tags. Each tag must contain 3 to 50 characters. Omit this field unless the user explicitly wants to change tags.

#### `productsgroup.brief_description` (string, Optional)

Short plain-text description, up to 4,000 characters. Omit this field unless the user explicitly wants to change it.

#### `productsgroup.section` (object, Optional)

Custom HTML decoration fragments for the product group detail page body.

Omit the whole object to keep the current section unchanged. Inside the object, omit `top` or `bottom` when that fragment should stay unchanged.

| Field    | Type   | Description |
|----------|--------|-------------|
| `top`    | string | Optional. Product group page header decoration fragment. HTML fragment only. Do not include `<h1>`, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. |
| `bottom` | string | Optional. Product group page footer decoration fragment. HTML fragment only. Do not include `<h1>`, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. |

#### `productsgroup.seo` (object, Optional)

Product group page SEO fields. Omit the whole object unless the user explicitly wants to change SEO.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact product group update request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact product group payload to be updated. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact product group payload shown to the user before execution. |

This skill also performs an automatic pre-update backup before it sends the update request.

- It reads the current product group record first.
- It writes a local JSON backup file under `backups/productsgroup-update/` relative to the current installed skill root.
- That backup file may contain sensitive business data copied from the current product group record and the requested update payload, so the user should explicitly approve that local persistence before execution.
- If backup capture fails, or if the backup file cannot be written, the update must not run.
- On success, the response includes `backup.storage.file_path`, `backup.raw_read_response`, `backup.snapshot`, and a best-effort `backup.restore_payload`.

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |
| backup | object/null  | Automatic pre-update backup metadata, snapshot, and restore payload |

### `data`

| Field               | Type    | Description                  |
|---------------------|---------|------------------------------|
| `productsgroup_id`  | integer | Updated product group ID     |
| `url`               | string  | Preview URL for the updated product group page. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter                        | Dependency skill        | Field source            | Mode   |
|----------------------------------|-------------------------|-------------------------|--------|
| language                         | languages-get       | list[].language         | select |
| productsgroup.productsgroup_id   | productsgroup-read  | list[].productsgroup_id | select |

---

## Usage Example

Minimum practical required fields for update:

- `language`
- `productsgroup.productsgroup_id`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update product group 8 in language en with the shown payload."
  },
  "productsgroup": {
    "productsgroup_id": 8,
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
  "msg": "update successfully",
  "data": {
    "productsgroup_id": 8
  },
  "backup": {
    "storage": {
      "file_path": "backups/productsgroup-update/example.json"
    },
    "restore_payload": {
      "language": "en",
      "productsgroup": {
        "productsgroup_id": 8
      }
    }
  }
}
```
