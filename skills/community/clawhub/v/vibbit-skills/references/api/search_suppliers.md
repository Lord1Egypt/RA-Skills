# 1688 supplier search: search_suppliers

Task type: `ALIBABA_1688_SUPPLIER_SEARCH`. Mode: `unknown`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300734e0)

Use the actual returned fields. If results cannot be interpreted, report the query status without inventing supplier details.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `image_url` | url | Yes |
| `sort` | string | No |
| `limit` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "image_url": "https://example.com/product.jpg",
  "sort": "default",
  "limit": 5
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_suppliers --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_suppliers --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

A successful response schema is not fully documented. Preserve actual results; an empty or unrecognized response does not mean no supplier exists. A real product image is required, not a keyword substituted for image_url.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
