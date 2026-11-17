# Save parsed products: batch_create_products

Task type: `ECOM_PRODUCT_BATCH_CREATE`. [Public API](https://vibbit.apifox.cn/519696014e0)

## Input

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

## Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" batch_create_products --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" batch_create_products --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

products is a nonempty object array and may contain one parsed product. Submit selected successful items using documented fields, omitting unknown/null values. Match returned records by real id and source identity, not array position. Do not assume server deduplication. Analysis states may remain PENDING.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
