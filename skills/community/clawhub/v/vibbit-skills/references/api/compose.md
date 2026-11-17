# Media composition: compose

Task type: `MEDIA_PRODUCTION`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300741e0)

Preserve track-field casing and use the documented composition configuration. Inspect the actual rendered result.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `packing_origin` | object | Yes |
| `video_packing_template` | object | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "packing_origin": {
    "video_track_list": [
      {
        "MainTrack": true,
        "VideoTrackClips": [
          {
            "MediaURL": "https://example.com/source.mp4",
            "Type": "Video",
            "In": 0,
            "Out": 5
          }
        ]
      }
    ]
  },
  "video_packing_template": {
    "background": {
      "type": "color",
      "width": 1920,
      "height": 1080,
      "color": "#000000"
    },
    "video": {
      "x": 0,
      "y": 0,
      "width": 1,
      "height": 1,
      "adapt_mode": "Contain"
    }
  }
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" compose --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" compose --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Both packing_origin and video_packing_template must be objects. Preserve nested PascalCase, including MainTrack, VideoTrackClips, and MediaURL. The example illustrates shape, not a verified minimum successful video request. Do not infer track units or template defaults; the CLI does not fully validate nested tracks.

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)
