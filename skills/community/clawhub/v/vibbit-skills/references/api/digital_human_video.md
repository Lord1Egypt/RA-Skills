# Digital-human video: digital_human_video

Task type: `DIGITAL_HUMAN_VIDEO_GENERATION`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300728e0)

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `audio_url` | url | Yes |
| `digital_human_id` | id | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "audio_url": "https://example.com/speech.mp3",
  "digital_human_id": "replace-with-real-id"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" digital_human_video --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" digital_human_video --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use an actual selected avatar ID and readable audio URL. Preserve large IDs as strings. A local audio path must be uploaded first. See [digital-human video](../capabilities/generation/digital-human-video.md).

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
