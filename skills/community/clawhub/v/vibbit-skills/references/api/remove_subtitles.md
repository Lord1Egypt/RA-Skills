# Subtitle removal: remove_subtitles

Task type: `SUBTITLE_REMOVAL`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/514584287e0)

Subtitle removal may affect scene details. Compare the source and output for remaining text and damage. COMPLETED indicates task completion only.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `video_url` | url | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "video_url": "https://example.com/source.mp4"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" remove_subtitles --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" remove_subtitles --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

One video per task; no documented batch, cancellation, or callback. Poll at least 10 seconds apart. Read progress_percent where present and result.video_url after completion. Compare original/output for damage. [Result reference](https://vibbit.apifox.cn/514584526e0) · [Example](../../examples/remove-subtitles.json)

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
