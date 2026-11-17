# TikTok video search: search_tiktok

Task type: `TIKTOK_VIDEO_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300735e0)

Preserve the exact casing of sortType and publishTime; do not convert them to snake_case.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `query` | string | Yes |
| `offset` | integer | No |
| `limit` | integer | No |
| `sortType` | integer | No |
| `publishTime` | integer | No |
| `region` | string | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "query": "portable projector",
  "offset": 0,
  "limit": 5,
  "sortType": 0,
  "publishTime": 0,
  "region": "US"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_tiktok --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_tiktok --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Preserve sortType/publishTime casing and pagination/sort semantics.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
