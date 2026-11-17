# Packaging templates: list_templates

Task type: `VIDEO_PACKING_TEMPLATE_LIST`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300738e0)

Query the list directly and use returned detail; template application must match the destination operation.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `business_type` | string | No |
| `template_type` | string | No |
| `scope` | string | No |
| `keyword` | text | No |
| `page` | integer | No |
| `size` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "business_type": "scrolling_subtitle",
  "template_type": "video-editor",
  "scope": "common",
  "keyword": "",
  "page": 1,
  "size": 20
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_templates --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_templates --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use the returned detail; no separate template-detail command exists.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
