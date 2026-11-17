# Update a product: update_product

Task type: `ECOM_PRODUCT_UPDATE`. [Public API](https://vibbit.apifox.cn/519688859e0)

## Input

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

## Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Read current detail and retain the intended difference plus supported writable values that must survive. The client requires name; reuse the current name when appropriate. Omission, null, clearing, and concurrent overwrite semantics are unspecified; arbitrary partial updates cannot be promised lossless. Readable image_urls, target_market, forbidden_expressions, and product_profile are not accepted writable fields here. The returned id must match the request.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
