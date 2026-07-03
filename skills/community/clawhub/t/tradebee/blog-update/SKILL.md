---
name: blog-update
description: A blog update skill based on the "Tradebee Website Builder" Open API. Before sending the update request, it automatically reads the current blog and writes a local JSON backup file containing the pre-update backup bundle. It then updates an existing blog under a specified site language and supports updating the blog group, publisher, publication date, title, cover image, tags, summary, description, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# blog-update

## Overview

Use the Tradebee Website Builder Open API to update an existing blog after automatically reading the current record and writing a local JSON backup file containing the pre-update backup bundle.

Supports updating blog information under a specified language, including blog group, publisher, publication date, title, cover image, tags, summary, detailed description, and SEO data.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code of the blog being edited.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `blog` (object, **Required**)

Blog fields to update.

- `blog.blog_id` is required
- Every other field is optional
- Omit any field that should stay unchanged
- Do not send guessed IDs or guessed replacement values

#### `blog.blog_id` (integer, **Required**)

Blog ID to update.

This must be the real existing blog ID.

#### `blog.bloggroup_id` (integer, Optional)

Blog group ID used to update the blog group.

- Omit this field to keep the current group unchanged
- Only send it when the user explicitly wants to move the blog
- If provided, it must be a positive integer (`> 0`) selected from `bloggroup-read`

#### `blog.publisher` (string, Optional)

New publisher name, up to 100 characters. Omit this field if the publisher should stay unchanged.

#### `blog.publication_date` (string, Optional)

New display publication date in `yyyy/M/d` format, for example `2026/4/24`. Omit this field if the publication date should stay unchanged.

#### `blog.title` (string, Optional)

New blog title, up to 500 characters. Omit this field if the title should stay unchanged.

#### `blog.cover_image` (object, Optional)

New cover image payload, up to 500 kB. Omit this field if the cover image should stay unchanged.

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...` |

#### `blog.tags` (array, Optional)

New keyword tag list, up to 6 items. Omit this field if tags should stay unchanged.

#### `blog.summary` (string, Optional)

New blog summary as plain text, up to 500 characters. Omit this field if the summary should stay unchanged.

#### `blog.description` (string, Optional)

New HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit this field if the detailed description should stay unchanged.

#### `blog.seo` (object, Optional)

New SEO metadata. Omit the whole `seo` object if SEO should stay unchanged.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | New SEO title, up to 90 characters. Omit this field if unchanged. |
| `description` | string | New SEO description, up to 200 characters. Omit this field if unchanged. |
| `keywords`    | string | New SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. Omit this field if unchanged. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact blog edit request after seeing the final language, blog ID, and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language, target blog ID, and exact payload to be changed. Never set this by assumption. |
| `summary`  | string  | Restates the language, target blog ID, and exact payload shown to the user before execution. |

This skill also performs an automatic pre-update backup before it sends the update request.

- It reads the current blog record first.
- It writes a local JSON backup file under `backups/blog-update/` relative to the current installed skill root.
- That backup file may contain sensitive business data copied from the current blog record and the requested update payload, so the user should explicitly approve that local persistence before execution.
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

| Field     | Type    | Description     |
|-----------|---------|-----------------|
| `blog_id` | integer | Updated blog ID |
| `url`     | string  | Preview URL for the updated blog. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter          | Dependency skill  | Field source     | Mode   |
|-------------------|-------------------|------------------|--------|
| language          | languages-get | list[].language  | select |
| blog.blog_id      | blog-read     | list[].blog_id   | select |
| blog.bloggroup_id | bloggroup-read| list[].bloggroup_id | select |

---

## Usage Example

Update rules:

- `blog.blog_id` is required
- Any field other than `blog_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the blog group unless the user explicitly asks for that change

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update blog 456 in language en with the shown payload."
  },
  "blog": {
    "blog_id": 456,
    "bloggroup_id": 216,
    "publisher": "huafeng",
    "publication_date": "2026/4/24",
    "title": "updated blog title",
    "cover_image": {
      "name": "cover",
      "base64": "image/jpeg;base64,..."
    },
    "tags": ["tag1", "tag2"],
    "summary": "updated summary",
    "description": "<p>updated description</p>",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "keyword1,keyword2"
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
    "blog_id": 456
  },
  "backup": {
    "storage": {
      "file_path": "backups/blog-update/example.json"
    },
    "restore_payload": {
      "language": "en",
      "blog": {
        "blog_id": 456
      }
    }
  }
}
```
