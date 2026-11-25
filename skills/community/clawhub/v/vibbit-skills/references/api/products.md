# Product APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Parse product links: parse_products](#parse-products)
- [Product library list: list_products](#list-products)
- [Product detail: get_product](#get-product)
- [Create a product: create_product](#create-product)
- [Update a product: update_product](#update-product)
- [Delete a product: delete_product](#delete-product)
- [Save parsed products: batch_create_products](#batch-create-products)

<a id="parse-products"></a>

## Parse product links: parse_products

Task type: `ECOM_PRODUCT_PARSE_LINKS`. [Public API](https://vibbit.apifox.cn/519694921e0)

<a id="parse-products-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.

| Field | Type | Required by client |
| --- | --- | --- |
| `links` | urls | Yes |

The client preserves result and adds item_summary (succeeded / failed / unknown). Partial success sets partial_failure=true; all-failed responses have ok=false. Unmatched items are not marked saved. Public documentation does not specify every partial-failure shape, count limit, or deduplication guarantee.

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "links": [
    "https://example.com/products/projector"
  ]
}
```

<a id="parse-products-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" parse_products --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" parse_products --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

links is a nonempty product URL array. Per-link results may include url, name, price, price_unit, image_url, image_urls, description, source_asin, third_product_id, third_product_url, platform, and status. Check each status and its facts. Parsing does not save products or assign platform product IDs. This differs from video share-link parsing.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="list-products"></a>

## Product library list: list_products

Task type: `ECOM_PRODUCT_LIST`. [Public API](https://vibbit.apifox.cn/519653477e0)

<a id="list-products-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.

| Field | Type | Required by client |
| --- | --- | --- |
| `keyword` | text | No |
| `page` | integer | No |
| `size` | integer | No |

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "keyword": "",
  "page": 0,
  "size": 20
}
```

<a id="list-products-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_products --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_products --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Returns summaries in content with total_elements, total_pages, number, and size. Pages start at 0; size must be positive. Read selected detail before production; the first page is not the entire library.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="get-product"></a>

## Product detail: get_product

Task type: `ECOM_PRODUCT_DETAIL`. [Public API](https://vibbit.apifox.cn/519653734e0)

<a id="get-product-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.

| Field | Type | Required by client |
| --- | --- | --- |
| `product_id` | id | Yes |

Use real positive platform ID strings for product_id, preserving integer precision. Third-party IDs/ASINs are not platform IDs.

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "product_id": "2102324709335007232"
}
```

<a id="get-product-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

May return id, facts, multiple images, source identity, product_profile, ai_analysis_status, and selection_info_status. PENDING/PROCESSING are business analysis states, not this query status. AI profiles inform creative choices; they do not prove features or outcomes.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="create-product"></a>

## Create a product: create_product

Task type: `ECOM_PRODUCT_CREATE`. [Public API](https://vibbit.apifox.cn/519655769e0)

<a id="create-product-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.Writable fields are conservatively limited to the public example, not a complete server model.

| Field | Type | Required by client |
| --- | --- | --- |
| `name` | string | Yes |
| `price` | number | No |
| `price_unit` | string | No |
| `image_url` | url | No |
| `description` | text | No |
| `source` | string | No |
| `selling_points` | strings | No |

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "name": "Portable projector",
  "price": 99,
  "price_unit": "USD",
  "source": "manual"
}
```

<a id="create-product-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" create_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" create_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Save supplied facts and omit unknown optional values. A saved record has a real id; analysis states may remain PENDING. Saving and analysis completion are separate. Use batch_create_products, even for one item, to retain parsed image_urls and third-party identity/source URLs.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="update-product"></a>

## Update a product: update_product

Task type: `ECOM_PRODUCT_UPDATE`. [Public API](https://vibbit.apifox.cn/519688859e0)

<a id="update-product-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.Writable fields are conservatively limited to the public example, not a complete server model.

| Field | Type | Required by client |
| --- | --- | --- |
| `product_id` | id | Yes |
| `name` | string | Yes |
| `price` | number | No |
| `price_unit` | string | No |
| `description` | text | No |
| `selling_points` | strings | No |

Use real positive platform ID strings for product_id, preserving integer precision. Third-party IDs/ASINs are not platform IDs.

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "product_id": "2102324709335007232",
  "name": "Portable projector",
  "price": 89,
  "price_unit": "USD"
}
```

<a id="update-product-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Read current detail and retain the intended difference plus supported writable values that must survive. The client requires name; reuse the current name when appropriate. Omission, null, clearing, and concurrent overwrite semantics are unspecified; arbitrary partial updates cannot be promised lossless. Readable image_urls, target_market, forbidden_expressions, and product_profile are not accepted writable fields here. The returned id must match the request.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="delete-product"></a>

## Delete a product: delete_product

Task type: `ECOM_PRODUCT_DELETE`. [Public API](https://vibbit.apifox.cn/519690178e0)

<a id="delete-product-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.

| Field | Type | Required by client |
| --- | --- | --- |
| `product_id` | id | Yes |

Use real positive platform ID strings for product_id, preserving integer precision. Third-party IDs/ASINs are not platform IDs.

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "product_id": "2102324709335007232"
}
```

<a id="delete-product-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" delete_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" delete_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Call only for an explicit deletion request with an identified target. Do not automatically clean up candidates or duplicates. Verify product_id and deleted; report deletion only for a matching ID and deleted=true. A false value yields ok=false even when the request is COMPLETED.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)

<a id="batch-create-products"></a>

## Save parsed products: batch_create_products

Task type: `ECOM_PRODUCT_BATCH_CREATE`. [Public API](https://vibbit.apifox.cn/519696014e0)

<a id="batch-create-products-input"></a>

### Input

These are accepted client fields and minimum requirements; the server may validate actual data further. Unknown fields and null values are not silently discarded.Writable fields are conservatively limited to the public example, not a complete server model.

| Field | Type | Required by client |
| --- | --- | --- |
| `products` | objects | Yes |

Accepted item fields: `url / name / price / price_unit / image_url / image_urls / description / selling_points / third_product_id / third_product_url / source / platform / status`. The client requires a nonempty name; a supplied status must be SUCCESS. Image arrays must be nonempty, URLs public, and prices nonnegative. source_asin, error_code, and profile fields are rejected. Do not forward whole parse objects.

The client preserves result and adds item_summary (succeeded / failed / unknown). Partial success sets partial_failure=true; all-failed responses have ok=false. Unmatched items are not marked saved. Public documentation does not specify every partial-failure shape, count limit, or deduplication guarantee.

The URLs, product facts, and IDs below are placeholders; replace them with actual inputs.

```json
{
  "products": [
    {
      "url": "https://example.com/products/projector",
      "name": "Portable projector",
      "price": 99,
      "price_unit": "USD",
      "image_url": "https://example.com/projector.jpg",
      "image_urls": [
        "https://example.com/projector.jpg"
      ],
      "description": "A portable projector",
      "selling_points": [
        "Compact design"
      ],
      "third_product_id": "projector-001",
      "third_product_url": "https://example.com/products/projector",
      "source": "shopline",
      "platform": "shopline",
      "status": "SUCCESS"
    }
  ]
}
```

<a id="batch-create-products-call-and-result"></a>

### Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" batch_create_products --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" batch_create_products --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

products is a nonempty object array and may contain one parsed product. Submit selected successful items using documented fields, omitting unknown/null values. Match returned records by real id and source identity, not array position. Do not assume server deduplication. Analysis states may remain PENDING.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
