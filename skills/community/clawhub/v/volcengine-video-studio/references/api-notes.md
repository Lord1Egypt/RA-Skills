# API notes

Use these notes when the task needs deeper parameter tuning or response debugging.

## Endpoint pattern

Base endpoint typically resolves to:

- `https://ark.cn-beijing.volces.com/api/v3`

Task endpoints:

- `POST /contents/generations/tasks`
- `GET /contents/generations/tasks/{task_id}`

## Practical payload shape used by this skill

The bundled script sends a request body shaped like:

```json
{
  "model": "<model-id>",
  "content": [
    {"type": "text", "text": "..."},
    {"type": "image_url", "image_url": {"url": "..."}},
    {"type": "video_url", "video_url": {"url": "..."}}
  ],
  "ratio": "16:9",
  "duration": 5,
  "frames": 120,
  "seed": 123,
  "resolution": "1080p",
  "camera_fixed": false,
  "watermark": false,
  "callback_url": "https://example.com/callback"
}
```

## Parameter notes pulled from docs

- `duration` and `frames` are alternatives; `frames` takes priority when both are supplied.
- `duration` is generally the easier control for whole-second clips.
- `camera_fixed` defaults to `false`.
- `watermark` defaults to `false`.
- `ratio=adaptive` can be model-dependent; for some text-to-video flows the platform chooses the final ratio automatically.
- Model support varies. When a model rejects a parameter, use the returned HTTP error or raw task payload instead of inventing behavior.

## Response handling guidance

Task payloads may evolve. Do not hardcode a single finished-response schema in explanations.

The bundled script therefore:

- extracts `task_id` from common keys (`task_id`, `id`, `taskId`)
- extracts `status` from common keys (`status`, `state`)
- recursively scans the returned task payload for likely output URLs
- preserves the full raw payload in stdout JSON for debugging

## Safe customization rule

If the public API shape changes or a model needs a slightly different `content` object schema, prefer passing `--content-json` with the exact body you want rather than rewriting the script on every run.
