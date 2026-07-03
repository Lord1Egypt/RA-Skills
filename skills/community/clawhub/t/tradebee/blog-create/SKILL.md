---
name: blog-create
description: A blog creation skill based on the "Tradebee Website Builder" Open API. It is used to create and publish a new blog under a specified site language and blog group, with support for publisher, publication date, cover image, tags, summary, and HTML description.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# blog-create

## Overview

Use the Tradebee Website Builder Open API to create and publish a new blog.

Supports publishing a blog under a specified language and blog group with publisher, publication date, cover image, tags, summary, and HTML description.

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

### `blog` (object, **Required**)

Complete blog payload for the new blog.

#### `blog.bloggroup_id` (integer, **Required**)

Blog group ID for the new blog.

- First call `bloggroup-read`
- Copy one exact `bloggroup_id`

#### `blog.publisher` (string, Optional)

Publisher name, up to 100 characters.

#### `blog.publication_date` (string, Optional)

Display publication date in `yyyy/M/d` format, for example `2026/4/24`. If omitted, the server uses the current date.

#### `blog.title` (string, **Required**)

Blog title shown to users, up to 500 characters.

#### `blog.cover_image` (object, **Required**)

Cover image payload, up to 500 kB.

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...` |

#### `blog.tags` (array, **Required**)

Provide 1 to 6 search keyword tags. Each tag must contain 3 to 50 characters.

#### `blog.summary` (string, **Required**)

Blog summary as plain text, up to 500 characters.

#### `blog.description` (string, **Required**)

HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method.

#### `blog.seo` (object, Optional)

SEO metadata for search engines.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact blog creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact blog payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact blog payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field      | Type    | Description      |
|------------|---------|------------------|
| `blog_id`  | integer | Created blog ID  |
| `url`      | string  | Preview URL for the created blog. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter          | Dependency skill   | Field source        | Mode   |
|-------------------|--------------------|---------------------|--------|
| language          | languages-get  | list[].language     | select |
| blog.bloggroup_id | bloggroup-read | list[].bloggroup_id | select |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `blog.bloggroup_id`
- `blog.title`
- `blog.cover_image`
- `blog.tags`
- `blog.summary`
- `blog.description`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a blog in language en with the shown payload."
  },
  "blog": {
    "bloggroup_id": 245,
    "publisher": "huafeng",
    "publication_date": "2025/5/15",
    "title": "blog title",
    "tags": ["tags 1", "tags 2"],
    "cover_image": {
      "name": "image1",
      "base64": "image/jpeg;base64,..."
    },
    "summary": "summary",
    "description": "detailed description",
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
    "blog_id": 8
  }
}
```
