# Create a product: create_product

Task type: `ECOM_PRODUCT_CREATE`. [Public API](https://vibbit.apifox.cn/519655769e0)

## Input

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

## Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" create_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" create_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Save supplied facts and omit unknown optional values. A saved record has a real id; analysis states may remain PENDING. Saving and analysis completion are separate. Use batch_create_products, even for one item, to retain parsed image_urls and third-party identity/source URLs.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
