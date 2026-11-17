# Product library list: list_products

Task type: `ECOM_PRODUCT_LIST`. [Public API](https://vibbit.apifox.cn/519653477e0)

## Input

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

## Call and result

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_products --input /absolute/path/product.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_products --input /absolute/path/product.json
```

POST /openapi/v1/tasks with input_info.input as a native object, not a JSON-encoded string. Public examples return data.request_id and data.task_result.result (a JSON string) synchronously. The client parses and preserves it. Do not invent polling/resume IDs when no task_id exists. Preserve uncertain write records and investigate the original operation rather than automatically issuing another POST.

Returns summaries in content with total_elements, total_pages, number, and size. Pages start at 0; size must be positive. Read selected detail before production; the first page is not the entire library.

[Product library and creative inputs](../resources/products.md) · [Task records and recovery](../runtime/task-lifecycle.md) · [Authentication](../runtime/authentication.md)
