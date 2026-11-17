# Video breakdown: breakdown

Task type: `VIDEO_BREAKDOWN`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/452941686e0)

sub_tasks is an array of strings: asr, hot, transition, bgm. Select only the analyses needed.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `video_url` | url | Yes |
| `sub_tasks` | strings | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "video_url": "https://example.com/source.mp4",
  "sub_tasks": [
    "asr",
    "hot"
  ]
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" breakdown --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" breakdown --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use only the requested sub_tasks. [Input example](../../examples/breakdown.json). Inspect individual sub-results and distinguish partial failures.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
