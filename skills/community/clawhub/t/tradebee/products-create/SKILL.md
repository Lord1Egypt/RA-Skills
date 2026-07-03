---
name: products-create
description: A product creation skill based on the "Tradebee Website Builder" Open API. It is used to create a new product under a specified site language and product group, with support for images, attributes, tags, product descriptions, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# products-create

## Overview

Use the Tradebee Website Builder Open API to create a new product.

Supports creating products under a specified language and product group, with images, attributes, tags, brief description, detailed description, and SEO data.

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

### `products` (object, **Required**)

Complete product payload for the new product.

#### `products.productsgroup_id` (integer, **Required**)

Leaf product group ID for the new product.

- First call `productsgroup-read`
- Copy one exact `productsgroup_id` where `is_leaf === true`
- Do not use parent group IDs
- Do not use `0`

#### `products.product_name` (string, **Required**)

Product title shown to users, up to 300 characters.

#### `products.model` (string, Optional)

Product model, up to 50 characters.

#### `products.upload_images` (array, **Required**)

Provide 1 to 5 images. The first image becomes the main image.

Each item contains:

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...`. Each image must be 500 kB or smaller. |

#### `products.attributes` (array, Optional)

Visible product attribute list, up to 15 items, for values like material, size, or color.

Each item contains:

| Field   | Type   | Description |
|---------|--------|-------------|
| `name`  | string | Attribute name, up to 100 characters |
| `value` | string | Attribute value, up to 100 characters |

#### `products.tags` (array, Optional)

Search keyword tag list. Provide 1 to 6 unique tags. Each tag must contain 3 to 50 characters.

#### `products.brief_description` (string, Optional)

Short plain-text summary, up to 127 characters.

#### `products.description` (string, Optional)

HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method.

#### `products.seo` (object, Optional)

SEO metadata for search engines.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | Optimized title, up to 90 characters. |
| `description` | string | Optimized description, up to 200 characters. |
| `keywords`    | string | SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact product creation request after seeing the final language and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language and exact product payload to be created. Never set this by assumption. |
| `summary`  | string  | Restates the language and exact product payload shown to the user before execution. |

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description    |
|--------|--------------|----------------|
| status | boolean      | Request status |
| msg    | string       | Response message |
| data   | object/null  | Returned data  |

### `data`

| Field         | Type    | Description         |
|---------------|---------|---------------------|
| `products_id` | integer | Created product ID  |
| `url`         | string  | Preview URL for the created product. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter                    | Dependency skill        | Field source            | Mode   |
|-----------------------------|-------------------------|-------------------------|--------|
| language                    | languages-get       | list[].language         | select |
| products.productsgroup_id   | productsgroup-read  | list[].productsgroup_id | select (filter: is_leaf=true) |

---

## Usage Example

Minimum practical required fields for create:

- `language`
- `products.productsgroup_id`
- `products.product_name`
- `products.upload_images`
- `products.tags`
- `products.brief_description`
- `products.description`
- `confirmation.approved=true`
- `confirmation.summary`

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: create a product in language en with the shown payload."
  },
  "products": {
    "productsgroup_id": 3445,
    "product_name": "product name",
    "model": "A1386",
    "upload_images": [
      {
        "name": "image1",
        "base64": "image/jpeg;base64,..."
      }
    ],
    "attributes": [
      {
        "name": "color",
        "value": "red"
      }
    ],
    "tags": ["tags 1", "tags 2"],
    "brief_description": "brief description",
    "description": "detailed description",
    "seo": {
      "title": "SEO title",
      "description": "SEO description up to 200 characters.",
      "keywords": "keyword1,keyword2,keyword3"
    }
  }
}
```

### Response Example

```json
{
  "status": true,
  "msg": "create successfully",
  "data": {
    "products_id": 8
  }
}
```
