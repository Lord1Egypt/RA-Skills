---
name: products-read
description: A product/catalog list retrieval skill based on the "Tradebee Website Builder" Open API. It is used to obtain product data published on the website. It supports filtering by language, product group, or exact product ID, paginated retrieval, and can be used in product display, data analysis, AI content generation, SEO optimization, and similar scenarios.
homepage: https://open.tradew.com
metadata: {"clawdbot":{"emoji":"bee","requires":{"env":["BEE_API_KEY"]},"primaryEnv":"BEE_API_KEY"}}
---

# products-read

## Overview

Use the Tradebee Website Builder Open API to retrieve product/catalog list data.

Supports language filtering, leaf product group filtering, exact product ID filtering, and paginated queries. Returns complete product structure data for use in product display, SEO optimization, data analysis, and content generation.

---

## Input Parameters

Authentication uses only the configured `BEE_API_KEY` environment variable. Never provide API keys in tool inputs, prompts, examples, logs, or chat text. Tradebee requests send site and business data to the external Tradebee Website Builder API, so only send the minimum data needed for the user's stated task.

---

### `language` (string, **Required**)

Site language filter parameter.

> Must be selected manually from the list returned by `languages-get`. AI inference or automatic generation is not allowed.

---

### `products_id` (integer, Optional)

Exact product filter.

> Omit this field to avoid product-ID filtering.
> If provided, use one positive integer (`> 0`) that matches an existing product.
> `products_id` and `productsgroup_id` are mutually exclusive: omit both to read all products, or provide exactly one of them.

---

### `productsgroup_id` (integer, Optional)

Product group filter.

> Omit this field to avoid product-group filtering.
> If provided, use a positive integer (`> 0`) selected from `productsgroup-read` where `is_leaf === true`.
> `products_id` and `productsgroup_id` are mutually exclusive: omit both to read all products, or provide exactly one of them.

---

### `fields` (array of strings, Optional)

Field selection list. If omitted, all supported product fields are returned.

---

### `pagination` (object, **Required**)

Pagination configuration parameters.

#### `current_page` (integer)

- Default: 1
- Minimum: 1
- Pagination rules:
  - Must rely on `data.pagination.has_next_page`
  - Use `data.pagination.next_page` as the next page number
  - Do not infer pages based on `total_page` or manual increments
  - Requests must stop when `has_next_page=false`

---

#### `page_size` (integer)

- Default: 10
- Range: 10 - 50

---

## Output Structure

### Top-Level Structure

| Field  | Type         | Description    |
|--------|--------------|----------------|
| status | boolean      | Request status |
| msg    | string       | Response message |
| data   | object/null  | Returned data  |

---

### `data.pagination`

| Field          | Type         | Description            |
|----------------|--------------|------------------------|
| current_page   | integer      | Current page number    |
| page_size      | integer      | Items per page         |
| total_page     | integer      | Total pages            |
| total_count    | integer      | Total records          |
| has_next_page  | boolean      | Whether a next page exists |
| next_page      | integer/null | Next page number       |

---

### `data.list[]`

Product data list.

| Field               | Type              | Description             |
|---------------------|-------------------|-------------------------|
| products_id         | integer           | Product ID              |
| language            | string            | Site language           |
| group               | object            | Product group           |
| product_name        | string            | Product name            |
| model               | string            | Product model           |
| images              | array             | Product image URL list  |
| tags                | array             | Keywords                |
| attributes          | array             | Attribute list          |
| brief_description   | string            | Brief description       |
| description         | string            | Detailed description (HTML) |
| seo                 | object            | SEO information         |
| view_count          | integer           | View count              |
| inquiry_count       | integer           | Inquiry count           |
| products_url        | string            | Product detail page URL |
| create_time         | string(datetime)  | Creation time           |
| update_time         | string(datetime)  | Update time             |

---

### `group`

| Field             | Type   | Description |
|-------------------|--------|-------------|
| productsgroup_id  | string | Group ID    |
| group_name        | string | Group name  |

---

### `attributes[]`

| Field | Type   | Description     |
|-------|--------|-----------------|
| name  | string | Attribute name  |
| value | string | Attribute value |

---

### `seo`

| Field         | Type   | Description                        |
|---------------|--------|------------------------------------|
| title         | string | SEO title (<= 90 characters)       |
| description   | string | SEO description (<= 200 characters) |
| keywords      | string | SEO keywords (<= 120 characters)   |

---

## Dependencies

| Parameter         | Dependency skill        | Field source            | Mode   |
|-------------------|-------------------------|-------------------------|--------|
| language          | languages-get       | list[].language         | select |
| products_id       | products-read       | list[].products_id      | select |
| productsgroup_id  | productsgroup-read  | list[].productsgroup_id | select (filter: is_leaf=true) |

---

## Usage Examples

### 1. Read All Products

Use this when no exact product or product-group filter is needed.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 2. Read Products Under One Leaf Group

Use this when the user wants products only from one selected leaf group.

```json
{
  "language": "en",
  "productsgroup_id": 3445,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 3. Read One Exact Product

Use this when the user already has one real `products_id`.

```json
{
  "language": "en",
  "products_id": 18468028,
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 4. Read One Exact Product With Selected Fields

Use this when the caller only needs a smaller response payload.

```json
{
  "language": "en",
  "products_id": 18468028,
  "fields": [
    "products_id",
    "language",
    "group",
    "product_name",
    "model",
    "images",
    "brief_description",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 5. Read Products Under One Group With Full Detail Fields

Use this when the caller needs detailed product content for one group.

```json
{
  "language": "en",
  "productsgroup_id": 3445,
  "fields": [
    "products_id",
    "language",
    "group",
    "product_name",
    "model",
    "images",
    "tags",
    "attributes",
    "brief_description",
    "description",
    "seo",
    "view_count",
    "inquiry_count",
    "products_url",
    "create_time",
    "update_time"
  ],
  "pagination": {
    "current_page": 1,
    "page_size": 5
  }
}
```

### 6. Read the Next Page

Use the exact `next_page` value returned by the previous response.

```json
{
  "language": "en",
  "pagination": {
    "current_page": 2,
    "page_size": 5
  }
}
```

### Selection Rules

- Omit both `products_id` and `productsgroup_id` to read all products.
- Send `productsgroup_id` only when filtering by one leaf product group.
- Send `products_id` only when reading one exact product.
- Never send `products_id` and `productsgroup_id` together.
- When returning a list to the user, include one `products_id` and one preview URL in the final answer so the user can decide whether to preview it.
- Do not tell the user they must preview it.
- Send `products_url` and `products_id` in `fields` when the caller needs the product detail URL path or when a list response must include one ID and one preview URL.
- Omit `fields` to return all supported fields.
- When continuing pagination, always use `data.pagination.next_page`.
