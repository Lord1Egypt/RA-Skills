---
name: bloggroup-update
description: A blog group update skill based on the "Tradebee Website Builder" Open API. Before sending the update request, it automatically reads the current blog group and writes a local JSON backup file containing the pre-update backup bundle. It then updates an existing blog group under a specified site language and supports updating group name, tags, brief description, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# bloggroup-update

## Overview

Use the Tradebee Website Builder Open API to update an existing blog group after automatically reading the current record and writing a local JSON backup file containing the pre-update backup bundle.

Supports updating blog group information under a specified language, including group name, tags, brief description, and SEO data.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code of the blog group being edited.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `bloggroup` (object, **Required**)

Blog group fields to update.

- `bloggroup.bloggroup_id` is required
- Every other field is optional
- Omit any field that should stay unchanged
- Do not send guessed IDs or guessed replacement values

#### `bloggroup.bloggroup_id` (integer, **Required**)

Blog group ID to update.

This must be the real existing blog group ID.

#### `bloggroup.group_name` (string, Optional)

New blog group name, up to 100 characters. Omit this field unless the user explicitly wants to change it.

#### `bloggroup.tags` (array, Optional)

New keyword tag list, up to 6 items. Omit this field unless the user explicitly wants to change tags.

#### `bloggroup.brief_description` (string, Optional)

New short plain-text description, up to 300 characters. Omit this field unless the user explicitly wants to change it.

#### `bloggroup.seo` (object, Optional)

New SEO metadata. Omit the whole `seo` object if SEO should stay unchanged.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | New SEO title, up to 90 characters. Omit this field if unchanged. |
| `description` | string | New SEO description, up to 200 characters. Omit this field if unchanged. |
| `keywords`    | string | New SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. Omit this field if unchanged. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact blog group edit request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact payload to be changed. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact payload shown to the user before execution. |

This skill also performs an automatic pre-update backup before it sends the update request.

- It reads the current blog group record first.
- It writes a local JSON backup file under `backups/bloggroup-update/` relative to the current installed skill root.
- That backup file may contain sensitive business data copied from the current blog group record and the requested update payload, so the user should explicitly approve that local persistence before execution.
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

| Field          | Type    | Description           |
|----------------|---------|-----------------------|
| `bloggroup_id` | integer | Updated blog group ID |
| `url`          | string  | Preview URL for the updated blog group page. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter              | Dependency skill   | Field source          | Mode   |
|-----------------------|--------------------|-----------------------|--------|
| language              | languages-get  | list[].language       | select |
| bloggroup.bloggroup_id| bloggroup-read | list[].bloggroup_id   | select |

---

## Usage Example

Update rules:

- `bloggroup.bloggroup_id` is required
- Any field other than `bloggroup_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update blog group 216 in language en with the shown payload."
  },
  "bloggroup": {
    "bloggroup_id": 216,
    "group_name": "updated group name",
    "tags": ["tag1", "tag2"],
    "brief_description": "updated description",
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
    "bloggroup_id": 216
  },
  "backup": {
    "storage": {
      "file_path": "backups/bloggroup-update/example.json"
    },
    "restore_payload": {
      "language": "en",
      "bloggroup": {
        "bloggroup_id": 216
      }
    }
  }
}
```
