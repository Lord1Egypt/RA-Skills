---
name: faq-create
description: A FAQ creation skill based on the "Tradebee Website Builder" Open API. It is used to create and publish a new FAQ under a specified site language and FAQ group, with support for cover image, question, tags, summary, HTML answer, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# faq-create

## Overview

Use the Tradebee Website Builder Open API to create and publish a new FAQ.

Supports publishing an FAQ under a specified language and FAQ group with cover image, question, tags, summary, HTML answer, and SEO data.

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

### `faq` (object, **Required**)

Complete FAQ payload for the new FAQ.

#### `faq.faqgroup_id` (integer, **Required**)

FAQ group ID for the new FAQ.

- First call `faqgroup-read`
- Copy one exact `faqgroup_id`

#### `faq.cover_image` (object, Optional)

Optional cover image payload, up to 500 kB.

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...` |

#### `faq.question` (string, **Required**)

FAQ question shown to users, up to 100 characters.

#### `faq.tags` (array, **Required**)

Provide 1 to 6 unique FAQ keyword tags. Each tag must contain 3 to 50 characters.

#### `faq.summary` (string, **Required**)

FAQ summary as plain text, up to 500 characters.

#### `faq.answer` (string, **Required**)

HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Before generating this field, call `rule-get` with the exact selected `language` and the exact scene value `faq.answer`. Follow the returned rule payload instead of guessing layout, styling, or structure rules. Do not use inline style attributes as the main styling method.

#### `faq.seo` (object, Optional)

SEO metadata for search engines.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact FAQ creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact FAQ payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact FAQ payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description      |
|--------|--------------|------------------|
| status | boolean      | Request status   |
| msg    | string       | Response message |
| data   | object/null  | Returned data    |

### `data`

| Field    | Type    | Description |
|----------|---------|-------------|
| `faq_id` | integer | Created FAQ ID |
| `url`    | string  | Preview URL for the created FAQ. Return this to the user so the user can decide whether to preview it. |

---

## Dependencies

| Parameter        | Dependency skill | Field source        | Mode   |
|-----------------|------------------|---------------------|--------|
| language        | languages-get    | list[].language     | select |
| faq.faqgroup_id | faqgroup-read    | list[].faqgroup_id  | select |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `faq.faqgroup_id`
- `faq.question`
- `faq.tags`
- `faq.summary`
- `faq.answer`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create an FAQ in language en with the shown payload."
  },
  "faq": {
    "faqgroup_id": 245,
    "cover_image": {
      "name": "cover",
      "base64": "image/jpeg;base64,..."
    },
    "question": "How long is the sample lead time?",
    "tags": ["lead time", "sample"],
    "summary": "Usually 5-7 working days.",
    "answer": "<section><p>Usually 5-7 working days.</p><style></style></section>",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "lead time,sample"
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
    "faq_id": 8,
    "url": "example.com/f8/how-long-is-the-sample-lead-time.htm"
  }
}
```
