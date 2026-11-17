# Delete a product: delete_product

Task type: `ECOM_PRODUCT_DELETE`. [Public API](https://vibbit.apifox.cn/519690178e0)

## Input

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

## Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" delete_product --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" delete_product --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Call only for an explicit deletion request with an identified target. Do not automatically clean up candidates or duplicates. Verify product_id and deleted; report deletion only for a matching ID and deleted=true. A false value yields ok=false even when the request is COMPLETED.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
