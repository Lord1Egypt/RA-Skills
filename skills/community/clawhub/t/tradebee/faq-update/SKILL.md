---
name: faq-update
description: A FAQ update skill based on the "Tradebee Website Builder" Open API. Before sending the update request, it automatically reads the current FAQ and writes a local JSON backup file containing the pre-update backup bundle. It then updates an existing FAQ under a specified site language and supports updating the FAQ group, cover image, question, tags, summary, HTML answer, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faq-update

## Overview

Use the Tradebee Website Builder Open API to update an existing FAQ after automatically reading the current record and writing a local JSON backup file containing the pre-update backup bundle.

Supports updating FAQ information under a specified language, including FAQ group, cover image, question, tags, summary, HTML answer, and SEO data.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code of the FAQ being edited.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `faq` (object, **Required**)

FAQ fields to update.

- `faq.faq_id` is required
- Every other field is optional
- Omit any field that should stay unchanged
- Do not send guessed IDs or guessed replacement values

#### `faq.faq_id` (integer, **Required**)

FAQ ID to update.

This must be the real existing FAQ ID.

#### `faq.faqgroup_id` (integer, Optional)

FAQ group ID used to move the FAQ to another group.

- Omit this field to keep the current group unchanged
- Only send it when the user explicitly wants to move the FAQ
- If provided, it must be a positive integer (`> 0`) selected from `faqgroup-read`

#### `faq.cover_image` (object, Optional)

New cover image payload, up to 500 kB. Omit this field if the cover image should stay unchanged.

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...` |

#### `faq.question` (string, Optional)

New FAQ question, up to 100 characters. Omit this field if the question should stay unchanged.

#### `faq.tags` (array, Optional)

New FAQ tag list, up to 6 unique items. Omit this field if tags should stay unchanged.

#### `faq.summary` (string, Optional)

New FAQ summary as plain text, up to 500 characters. Omit this field if the summary should stay unchanged.

#### `faq.answer` (string, Optional)

New HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Before generating this field, call `rule-get` with the exact selected `language` and the exact scene value `faq.answer`. Follow the returned rule payload instead of guessing layout, styling, or structure rules. Omit this field if the answer should stay unchanged.

#### `faq.seo` (object, Optional)

New SEO metadata. Omit the whole `seo` object if SEO should stay unchanged.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | New SEO title, up to 90 characters. Omit this field if unchanged. |
| `description` | string | New SEO description, up to 200 characters. Omit this field if unchanged. |
| `keywords`    | string | New SEO keywords as one comma-separated string, with total length 120 characters or fewer. Omit this field if unchanged. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact FAQ edit request after seeing the final language, FAQ ID, and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language, target FAQ ID, and exact payload to be changed. Never set this by assumption. |
| `summary`  | string  | Restates the language, target FAQ ID, and exact payload shown to the user before execution. |

This skill also performs an automatic pre-update backup before it sends the update request.

- It reads the current FAQ record first.
- It writes a local JSON backup file under `backups/faq-update/` relative to the current installed skill root.
- That backup file may contain sensitive business data copied from the current FAQ record and the requested update payload, so the user should explicitly approve that local persistence before execution.
- If backup capture fails, or if the backup file cannot be written, the update must not run.
- On success, the response includes `backup.storage.file_path`, `backup.raw_read_response`, `backup.snapshot`, and a best-effort `backup.restore_payload`.
- Uploaded images are only partially restorable because the read API does not return the original image base64 content.

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

| Field    | Type    | Description |
|----------|---------|-------------|
| `faq_id` | integer | Updated FAQ ID |
| `url`    | string  | Preview URL for the updated FAQ. Return this to the user so the user can decide whether to preview it. |

---

## Dependencies

| Parameter        | Dependency skill | Field source        | Mode   |
|-----------------|------------------|---------------------|--------|
| language        | languages-get    | list[].language     | select |
| faq.faq_id      | faq-read         | list[].faq_id       | select |
| faq.faqgroup_id | faqgroup-read    | list[].faqgroup_id  | select |

---

## Usage Example

Update rules:

- `faq.faq_id` is required
- Any field other than `faq_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the FAQ group unless the user explicitly asks for that change

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update FAQ 456 in language en with the shown payload."
  },
  "faq": {
    "faq_id": 456,
    "faqgroup_id": 216,
    "cover_image": {
      "name": "cover",
      "base64": "image/jpeg;base64,..."
    },
    "question": "Can you support rush orders?",
    "tags": ["rush order", "capacity"],
    "summary": "Rush orders depend on current capacity.",
    "answer": "<section><p>Rush orders depend on current production capacity.</p><style></style></section>",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "rush order,capacity"
    }
  }
}
```

### Response Example

```json
{
  "status": true,
  "msg": "update successfully",
  "data": {
    "faq_id": 456,
    "url": "example.com/f456/can-you-support-rush-orders.htm"
  },
  "backup": {
    "storage": {
      "file_path": "backups/faq-update/example.json"
    },
    "restore_payload": {
      "language": "en",
      "faq": {
        "faq_id": 456
      }
    }
  }
}
```
