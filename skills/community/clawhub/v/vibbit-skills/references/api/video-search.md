# External video search APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Google short-video search: search_videos](#search-videos)
- [TikTok video search: search_tiktok](#search-tiktok)

<a id="search-videos"></a>

## Google short-video search: search_videos

Task type: `GOOGLE_SHORT_VIDEO_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300732e0)

<a id="search-videos-inputs"></a>

### Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `query` | string | Yes |
| `google_domain` | string | No |
| `gl` | string | No |
| `hl` | string | No |
| `limit` | integer | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "query": "portable projector",
  "gl": "us",
  "hl": "en",
  "limit": 5
}
~~~

<a id="search-videos-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_videos --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_videos --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Respect the requested language, region, and count. Search links can be share pages rather than direct media.

<a id="search-videos-results"></a>

### Results

The public success example encodes `task_result.result` as a JSON string containing an array. Each row has `position`, `title`, `link`, `thumbnail`, `source`, `channel`, and `duration`. Keep the actual platform; Google search is not limited to YouTube results.

The client projects these candidate fields, retains row count and ordering, and adds `source_content`. When needed, `full_result_file` retains complete fields. Select relevant candidates before deeper analysis; authorized analysis/creation needs no individual approval. See [external source data and execution scope](../runtime/external-content.md) for full text and future response shapes.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

<a id="search-tiktok"></a>

## TikTok video search: search_tiktok

Task type: `TIKTOK_VIDEO_SEARCH`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300735e0)

Preserve the exact casing of sortType and publishTime; do not convert them to snake_case.

<a id="search-tiktok-inputs"></a>

### Inputs

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

<a id="search-tiktok-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_tiktok --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" search_tiktok --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Preserve sortType/publishTime casing and pagination/sort semantics.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
