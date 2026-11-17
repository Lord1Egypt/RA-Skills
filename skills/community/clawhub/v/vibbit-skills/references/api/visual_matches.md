# Visual product matches: visual_matches

Task type: `GOOGLE_VISUAL_MATCH_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300733e0)

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `image_url` | url | Yes |
| `hl` | string | No |
| `country` | string | No |
| `limit` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "image_url": "https://example.com/product.jpg",
  "country": "US",
  "limit": 5
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" visual_matches --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" visual_matches --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use a real image URL. Visual similarity does not establish identical brand, specification, or authenticity.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
