# Tomoviee Text-to-Music API Reference

## Provenance and Endpoint Mapping

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Gateway host used by this skill package: `https://openapi.wondershare.cc`
- Primary capacity for this skill: `tm_text2music`

All runtime requests from this skill call only:

1. `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2music`
2. `https://openapi.wondershare.cc/v1/open/pub/task`

## Text-to-Music (tm_text2music)

Generate background music from a text prompt.

### Endpoint

`https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2music`

### Parameters

- `prompt` (required): text prompt for genre, mood, instruments, and usage context
- `duration` (required): target music duration in seconds, range `0-95`
- `qty` (required): number of generated tracks, range `1-4`
- `disable_translate` (optional): whether to disable translation
- `callback` (optional): callback URL for async notification
- `params` (optional): transparent passthrough parameter

### Result Endpoint

`https://openapi.wondershare.cc/v1/open/pub/task`

### Status Codes

- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

### Example

```python
from scripts.tomoviee_text2music_client import TomovieeText2MusicClient

client = TomovieeText2MusicClient("app_key", "app_secret")
task_id = client.text_to_music(
    prompt="Upbeat corporate technology music, modern and energetic",
    duration=30,
    qty=1,
    disable_translate=False,
)
result = client.poll_until_complete(task_id)
```

### Credential Handling

- Build auth header as `Authorization: Basic <base64(app_key:app_secret)>`
- Do not hardcode or persist credentials in source files
- Prefer environment variables or secure secret stores
