---
name: productsgroup-read
description: A product group list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to obtain published product category/group data from the website. It supports filtering by language and parent product group, supports multi-level hierarchical group structures, and can be widely used in product category display, querying products under a group, group selection for product publishing, data analysis, AI content generation, SEO optimization, intelligent retrieval, and similar scenarios.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# productsgroup-read

## Overview

Use the Tradebee Website Builder Open API to retrieve product group/category data.

Supports language filtering, querying by parent group, and returning multi-level nested structures. It can be widely used in product category display, querying products under groups, product publishing group selection, data analysis, AI content generation, SEO optimization, and intelligent retrieval.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Site language filter parameter.

> Warning: After user confirmation, it must be selected from the list returned by `languages-get`  
> Not allowed: AI is not allowed to infer or generate it automatically

---

### `parent_productsgroup_id` (integer, Optional)

Parent product group ID, used to retrieve the child group list.

- Omit this field or set `0` to return top-level groups
- If provided as a positive integer (`> 0`), the API returns the direct child groups under that parent group
- `parent_productsgroup_id` and `productsgroup_id` are mutually exclusive: omit both to read top-level groups, or provide exactly one of them

---

### `productsgroup_id` (integer, Optional)

Exact product group filter.

- Omit this field to avoid exact-group filtering
- If provided, use one positive integer (`> 0`) that matches an existing product group
- `parent_productsgroup_id` and `productsgroup_id` are mutually exclusive: omit both to read top-level groups, or provide exactly one of them

---

### `fields` (array of strings, Optional)

Field selection list. If omitted, all supported product group fields are returned.

---

## Output Structure

### Top-Level Structure

| Field  | Type        | Description    |
|--------|-------------|----------------|
| status | boolean     | Request status |
| msg    | string      | Response message |
| data   | object/null | Returned data  |

---

### `data.list[]`

Product group list data.

| Field             | Type             | Description                  |
|-------------------|------------------|------------------------------|
| productsgroup_id  | integer          | Product group ID             |
| language          | string           | Site language code           |
| group_name        | string           | Group name                   |
| tags              | array            | Keyword list                 |
| seo               | object           | SEO information              |
| section           | object           | Custom top/bottom HTML decoration fragments |
| productsgroup_url | string           | Group URL                    |
| create_time       | string(datetime) | Creation time                |
| update_time       | string(datetime) | Update time                  |
| is_leaf           | boolean          | Whether it is a leaf node    |
| children          | array            | Child groups (recursive structure) |

---

### `seo`

| Field         | Type   | Description                        |
|---------------|--------|------------------------------------|
| title         | string | SEO title (<= 90 characters)       |
| description   | string | SEO description (<= 200 characters) |
| keywords      | string | SEO keywords (<= 120 characters)   |

---

### `section`

| Field         | Type   | Description |
|---------------|--------|-------------|
| top           | string | Product group page header decoration fragment. HTML fragment only. |
| bottom        | string | Product group page footer decoration fragment. HTML fragment only. |

---

### `children[]`

Recursive structure with the same node structure as `list[]`.

---

## Dependencies

| Parameter | Dependency skill   | Field source      | Mode   |
|-----------|--------------------|-------------------|--------|
| language  | languages-get  | list[].language   | select |

---

## Usage Rules

- `language` must be obtained through `languages-get`
- `parent_productsgroup_id` is a parent group selector, not a leaf-group validator
- `productsgroup_id` reads one exact product group
- `parent_productsgroup_id` and `productsgroup_id` must not be sent together
- `children` supports unlimited recursive nesting
- The integrity of the tree structure must be preserved

---

## Usage Examples

### 1. Read Top-Level Product Groups

Use this when the caller wants the top-level tree root.

```json
{
  "language": "en"
}
```

### 2. Read Top-Level Product Groups Explicitly

Use this when the caller wants to be explicit that the parent is the root.

```json
{
  "language": "en"
}
```

### 3. Read Child Groups Under One Parent Group

Use this when the user wants the direct child groups under one known parent group.

```json
{
  "language": "en",
  "parent_productsgroup_id": 1797384
}
```

### 4. Read One Exact Product Group

Use this when the user already has one real `productsgroup_id`.

```json
{
  "language": "en",
  "productsgroup_id": 2092360
}
```

### 5. Read One Exact Product Group With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "language": "en",
  "productsgroup_id": 2092360,
  "fields": [
    "productsgroup_id",
    "language",
    "group_name",
    "seo",
    "section",
    "update_time"
  ]
}
```

### 6. Read Child Groups With Selected Fields

Use this when the caller wants a lighter subtree response under one parent.

```json
{
  "language": "en",
  "parent_productsgroup_id": 1797384,
  "fields": [
    "productsgroup_id",
    "language",
    "group_name",
    "productsgroup_url",
    "update_time"
  ]
}
```

### Selection Rules

- Omit both `parent_productsgroup_id` and `productsgroup_id` to read top-level groups.
- Send `parent_productsgroup_id` only when reading direct child groups under one parent.
- Send `productsgroup_id` only when reading one exact product group.
- Never send `parent_productsgroup_id` and `productsgroup_id` together.
- When returning a list to the user, include one `productsgroup_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `productsgroup_url` and `productsgroup_id` in `fields` when the caller needs the group URL or when a list response must include one ID and one preview URL.
- Omit `fields` to return all supported fields.
