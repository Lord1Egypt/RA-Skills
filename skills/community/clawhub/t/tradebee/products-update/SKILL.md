---
name: products-update
description: A product update skill based on the "Tradebee Website Builder" Open API. Before sending the update request, it automatically reads the current product and writes a local JSON backup file containing the pre-update backup bundle. It then updates an existing product under a specified site language and supports updating product information such as group, name, model, images, attributes, tags, descriptions, and SEO data.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# products-update

## Overview

Use the Tradebee Website Builder Open API to update an existing product after automatically reading the current record and writing a local JSON backup file containing the pre-update backup bundle.

Supports updating product information under a specified language, including group, name, model, images, attributes, tags, brief description, detailed description, and SEO data.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Exact site language code of the product being edited.

- First call `languages-get`
- Show the returned language list to the user
- Copy one exact `language` value from that list after the user confirms it
- Do not guess, translate, or invent the language code

---

### `products` (object, **Required**)

Product fields to update.

- `products.products_id` is required
- Every other field is optional
- Omit any field that should stay unchanged
- Do not send guessed IDs or guessed replacement values

#### `products.products_id` (integer, **Required**)

Product ID to update.

This must be the real existing product ID.

#### `products.productsgroup_id` (integer, Optional)

Product group ID used to update the product group.

- Omit this field to keep the current group unchanged
- Only send it when the user explicitly wants to move the product
- If provided, it must be a positive integer (`> 0`) selected from `productsgroup-read` where `is_leaf === true`
- Parent groups and `0` are not allowed

#### `products.product_name` (string, Optional)

New product title, up to 300 characters. Omit this field if the title should stay unchanged.

#### `products.model` (string, Optional)

New product model, up to 50 characters. Omit this field if the model should stay unchanged.

#### `products.upload_images` (array, Optional)

New image list, up to 5 images. The first image becomes the main image. Omit this field if images should stay unchanged.

Each item contains:

| Field    | Type   | Description |
|----------|--------|-------------|
| `name`   | string | Image file label used to identify this image inside the payload |
| `base64` | string | Base64 image data with MIME prefix, for example `image/jpeg;base64,...`. Each image must be 500 kB or smaller. |

#### `products.attributes` (array, Optional)

New product attribute list, up to 15 items. Omit this field if attributes should stay unchanged.

Each item contains:

| Field   | Type   | Description |
|---------|--------|-------------|
| `name`  | string | Attribute name, up to 100 characters |
| `value` | string | Attribute value, up to 100 characters |

#### `products.tags` (array, Optional)

New search keyword tag list, up to 6 items. Omit this field if tags should stay unchanged.

#### `products.brief_description` (string, Optional)

New short plain-text summary, up to 127 characters. Omit this field if the brief description should stay unchanged.

#### `products.description` (string, Optional)

New HTML fragment only. Do not include any `<h1>` tag, and prefer `<h2>` to `<h6>`. `<img src>` may use a normal URL or `data:image/...;base64,...`. At most 50 `<img>` tags are allowed. Each single `<img>` image must be 500 kB or smaller. The 100,000-character limit is checked after removing `<img>` tags, and the server uploads supported base64 images and replaces them with URL addresses. Follow the `rule-get` payload, including the current tenant structure rules such as one root `<section>` element and one embedded `<style>` block placed at the end of the fragment. Do not use inline style attributes as the main styling method. Omit this field if the detailed description should stay unchanged.

#### `products.seo` (object, Optional)

New SEO metadata. Omit the whole `seo` object if SEO should stay unchanged.

| Field         | Type   | Description |
|---------------|--------|-------------|
| `title`       | string | New SEO title, up to 90 characters. Omit this field if unchanged. |
| `description` | string | New SEO description, up to 200 characters. Omit this field if unchanged. |
| `keywords`    | string | New SEO keywords as one comma-separated string, with up to 6 keywords and total length 120 characters or fewer. Omit this field if unchanged. |

### `confirmation` (object, **Required**)

Proof that the user explicitly approved this exact product edit request after seeing the final language, product ID, and payload.

| Field      | Type    | Description |
|------------|---------|-------------|
| `approved` | boolean | Must be `true` only after the user explicitly confirms the language, target product ID, and exact payload to be changed. Never set this by assumption. |
| `summary`  | string  | Restates the language, target product ID, and exact payload shown to the user before execution. |

This skill also performs an automatic pre-update backup before it sends the update request.

- It reads the current product record first.
- It writes a local JSON backup file under `backups/products-update/` relative to the current installed skill root.
- That backup file may contain sensitive business data copied from the current product record and the requested update payload, so the user should explicitly approve that local persistence before execution.
- If backup capture fails, or if the backup file cannot be written, the update must not run.
- On success, the response includes `backup.storage.file_path`, `backup.raw_read_response`, `backup.snapshot`, and a best-effort `backup.restore_payload`.
- Uploaded images are only partially restorable because the read API does not return the original image base64 content.

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description    |
|--------|--------------|----------------|
| status | boolean      | Request status |
| msg    | string       | Response message |
| data   | object/null  | Returned data  |
| backup | object/null  | Automatic pre-update backup metadata, snapshot, and restore payload |

### `data`

| Field         | Type    | Description        |
|---------------|---------|--------------------|
| `products_id` | integer | Updated product ID |
| `url`         | string  | Preview URL for the updated product. Return this to the user and ask the user to preview it. |

---

## Dependencies

| Parameter                    | Dependency skill        | Field source            | Mode   |
|-----------------------------|-------------------------|-------------------------|--------|
| language                    | languages-get       | list[].language         | select |
| products.productsgroup_id   | productsgroup-read  | list[].productsgroup_id | select (filter: is_leaf=true) |

---

## Usage Example

Update rules:

- `products.products_id` is required
- Any field other than `products_id` should be omitted unless the user explicitly wants to change it
- Omitting a field means keep the existing value
- Do not move the product group unless the user explicitly asks for that change

```json
{
  "language": "en",
  "confirmation": {
    "approved": true,
    "summary": "Confirmed by user: update product 456 in language en with the shown payload."
  },
  "products": {
    "products_id": 456,
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
  "msg": "update successfully",
  "data": {
    "products_id": 8
  },
  "backup": {
    "storage": {
      "file_path": "backups/products-update/example.json"
    },
    "restore_payload": {
      "language": "en",
      "products": {
        "products_id": 8
      }
    }
  }
}
```
