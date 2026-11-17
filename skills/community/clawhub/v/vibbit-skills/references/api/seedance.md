# Seedance video: seedance

Task type: `SEEDANCE_VIDEO_GENERATION`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/514565013e0)

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

Construct requests under [paid video settings](../capabilities/generation/video-generation.md#paid-video-settings): explicitly send `resolution: "720p"` when unspecified, without inheriting 1080p/4k from source media or old requests. The client still requires `model` and `resolution`; this is an execution rule, not server-side automatic defaulting.

| Field | Type | Required |
| --- | --- | --- |
| `model` | string | Yes |
| `prompt` | string | Yes |
| `duration_seconds` | integer | Yes |
| `resolution` | string | Yes |
| `aspect_ratio` | string | Yes |
| `generate_audio` | boolean | No |
| `tools` | objects | No |
| `omni_reference_task_type` | string | No |
| `image_url` | url | No |
| `first_frame_image_url` | url | No |
| `last_frame_image_url` | url | No |
| `reference_image_urls` | urls | No |
| `reference_video_urls` | urls | No |
| `reference_audio_urls` | urls | No |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "model": "doubao-seedance-2-5-260628",
  "prompt": "A paper boat crosses a misty lake at dawn as the camera gently follows.",
  "duration_seconds": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" seedance --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" seedance --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Models and cross-field constraints

| Model | Resolutions | Duration | Max image/video/audio references |
| --- | --- | --- | --- |
| doubao-seedance-2-0-fast-260128 | 480p, 720p | -1 or 4-15 seconds | 9 / 3 / 3 |
| doubao-seedance-2-0-260128 | 480p, 720p, 1080p, 4k | -1 or 4-15 seconds | 9 / 3 / 3 |
| doubao-seedance-2-0-mini-260615 | 480p, 720p | -1 or 4-15 seconds | 9 / 3 / 3 |
| doubao-seedance-2-5-260628 | 480p, 720p, 1080p | -1 or 4-30 seconds | 30 / 10 / 10 |

Ratios: 16:9, 4:3, 1:1, 3:4, 9:16, 21:9, adaptive. Single-image, first/last-frame, and reference_* groups are mutually exclusive. A last frame requires a first frame. Do not reuse the same URL in different media roles. Version 2.0 requires an image or video alongside audio references.

| 2.5 omni mode | Requirements |
| --- | --- |
| reference | At least one reference; normal ratios/durations |
| auto | Reference media, adaptive ratio, duration -1; reference videos 4-30 seconds |
| edit | At least one reference video, adaptive, duration -1; reference videos 4-30 seconds |
| extend | At least one reference video and adaptive ratio; duration semantics still require verification |

The model guide requires adaptive for true 2.5 first/last-frame mode; the Vibbit page does not explicitly state this. Omitted omni types may be inferred by the service; specify known intent explicitly.

## Media limits checked by the service

- 2.5 images: jpeg/png/webp/bmp/tiff/gif/heic/heif; each below 30 MB; 300-6000 px per dimension; ratio 0.4-2.5.
- 2.5 videos: mp4/mov, H.264/H.265, each at most 200 MB; each 2-30 seconds (auto/edit 4-30), at most 30 seconds total; dimensions 300-6000, ratio 0.4-2.5, 409600-8295044 total pixels, 24-60 FPS. Optional AAC/MP3 audio.
- 2.5 audio: wav/mp3, each at most 15 MB, each 2-30 seconds, total at most 30 seconds.
- 2.0 reference video: each 2-15 seconds, total at most 15 seconds, each below 50 MB. Audio: each 2-15 seconds, total below 15 seconds, each below 15 MB. Images: each below 30 MB.

The CLI checks static fields, URL syntax, and counts; it does not remotely probe media. Do not report all limits as verified without metadata. Results use video_url; poll at least 5 seconds apart.

[2.5 guide](../models/seedance-2.5/overview.md) · [2.0 differences](../models/seedance-2.0.md) · Examples: [text](../../examples/seedance-text.json), [references](../../examples/seedance-reference.json), [editing](../../examples/seedance-edit.json), [frames](../../examples/seedance-frames.json).
