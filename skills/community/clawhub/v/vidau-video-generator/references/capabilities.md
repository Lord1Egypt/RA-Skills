# Model List API and Capability Validation

Before creating a task, call `scripts/query_models.py` to get the model list. The response is cached for 10 minutes.

## GET /v1/models

- **URL**: `https://api.superaiglobal.com/v1/models`
- **Method**: GET
- **Headers**: `Authorization: Bearer {API_KEY}`

Response example:

```json
{
  "code": "200",
  "message": "success",
  "data": [
    {
      "model": "veo@3.1:normal",
      "scaleList": ["16:9", "9:16"],
      "durationList": { "1080p": [5, 10], "720p": [5, 8, 10] },
      "resolutionList": ["1080p", "720p"],
      "generateAudio": true
    }
  ]
}
```

- **scaleList**: Allowed aspect ratios (e.g. `16:9`, `9:16`). Validate user `--ratio` against this.
- **durationList**: Object mapping resolution to allowed durations in seconds. Key = resolution (e.g. `1080p`), value = list of allowed durations. Validate user `--duration` for the chosen `--resolution`: `duration` must be in `durationList[resolution]`.
- **resolutionList**: Allowed resolutions (e.g. `720p`, `1080p`). Validate user `--resolution` against this.
- **generateAudio**: Whether the model supports audio generation. If user requests `--generate-audio true`, the model entry must have `generateAudio: true`.

## Validation rules (before create_task)

1. Find the entry in `data` where `model` equals the chosen model. If not found, skip validation and proceed.
2. **resolution**: Must be in `resolutionList`. If not, do not create task; tell the user and list allowed values.
3. **ratio** (if provided): Must be in `scaleList`. If not, do not create task; tell the user and list allowed values.
4. **duration** (if provided): Must be in `durationList[resolution]`. If not, do not create task; tell the user allowed durations for that resolution.
5. **generate_audio** (if user requested true): Model must have `generateAudio: true`. If false, do not create task; tell the user the model does not support audio.

Do not auto-correct or change user parameters; only report what does not meet requirements and the allowed values.

## Model parameters (reference)

Below is the capability matrix from the models API (use `scripts/query_models.py` for live data; API may return resolution keys as `720P`/`1080P`).

| model | scaleList (ratio) | resolutionList | durationList (resolution → seconds) | generateAudio |
|-------|-------------------|----------------|------------------------------------|---------------|
| `sora@2:normal` | 16:9, 9:16 | 720P | 720P: 4, 8, 12 | false |
| `sora@2:pro` | 16:9, 9:16 | 720P, 1080P | 720P: 4, 8, 12; 1080P: 4, 8, 12 | false |
| `veo@3.1:normal` | 9:16, 16:9 | 720P, 1080P | 720P: 4, 6, 8; 1080P: 8 | false |
| `veo@3.1:fast` | 9:16, 16:9 | 720P, 1080P | 720P: 4, 6, 8; 1080P: 8 | false |
| `seedance@1:pro` | 1:1, 16:9, 4:3, 9:16, 3:4, Adaptive | 480P, 720P, 1080P | 480P: 5, 10; 720P: 5, 10; 1080P: 5, 10 | false |
| `seedance@1:pro_fast` | 1:1, 16:9, 4:3, 9:16, 3:4, Adaptive | 720P, 1080P | 720P: 5, 12; 1080P: 5, 12 | false |
| `vidu@q2:turbo` | 1:1, 16:9, 4:3, 9:16, 3:4 | 720P | 720P: 4, 8 | false |
| `vidu@q2:pro` | 1:1, 16:9, 4:3, 9:16, 3:4 | 1080P | 1080P: 4, 8 | false |
| `wan@2.5:preview` | 1:1, 16:9, 4:3, 9:16, 3:4, Adaptive | 720P, 1080P | 720P: 5, 10; 1080P: 5, 10 | **true** |
| `veo@3:normal` | 9:16, 16:9 | 720P, 1080P | 720P: 8; 1080P: 8 | **true** |

- **ratio** must be in the model’s `scaleList`.
- **resolution** must be in `resolutionList` (API may use 720P/1080P; treat case-insensitively when validating).
- **duration** must be in `durationList[resolution]` for the chosen resolution.
- **generate_audio**: only `wan@2.5:preview` and `veo@3:normal` support `generateAudio: true`.

## Cache

- Default path: `~/.vidau_models_cache.json`. Override with env `VIDAU_MODELS_CACHE`.
- TTL: 10 minutes. Use `--no-cache` to force refresh.
