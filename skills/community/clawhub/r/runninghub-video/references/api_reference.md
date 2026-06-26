# RunningHub Video API Reference

This file captures the official RunningHub endpoints that the skill currently automates.

## Authentication

- Header: `Authorization: Bearer <API_KEY>`
- Content type for submit/query: `application/json`
- Content type for file upload: `multipart/form-data`

## Upload Local Media First

Use this when the user gives a local image path instead of a public URL.

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/media/upload/binary`
- Form field: `file=@/path/to/image.png`
- Important response field: `data.download_url`

Observed from RunningHub official API pages:

- resource parameters can accept a public URL or a Base64 data URI
- the upload endpoint returns a reusable `download_url`
- uploaded links may expire after about 1 day on some endpoint pages, so download final outputs promptly

## Poll Task Status

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/query`
- Body:

```json
{
  "taskId": "2009217245938851841"
}
```

Typical success shape:

```json
{
  "taskId": "2009191190196789249",
  "status": "SUCCESS",
  "errorCode": "",
  "errorMessage": "",
  "results": [
    {
      "url": "https://...",
      "outputType": "mp4"
    }
  ]
}
```

## Supported Model Mappings

### `kling-v3.0-std`

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/kling-v3.0-std/image-to-video`
- Explicit example fields from the official doc:
  - `prompt`
  - `firstImageUrl`
  - `lastImageUrl`
  - `duration`
  - `cfgScale`
  - `sound`
  - `multiShot`
  - `shotType`

### `seedance-2.0-global`

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/bytedance/seedance-2.0-global/image-to-video`
- Explicit example fields from the official doc:
  - `prompt`
  - `resolution`
  - `duration`
  - `firstFrameUrl`
  - `generateAudio`
  - `ratio`
  - `realPersonMode`
  - `conversionSlots`
  - `returnLastFrame`
- Inference from the doc description: the endpoint text says it supports both single-frame and start/end-frame generation, so `lastFrameUrl` is treated as a likely optional field when an end frame is supplied.

### `seedance-2.0-global-fast`

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/bytedance/seedance-2.0-global-fast/image-to-video`
- Payload pattern follows the same documented shape as `seedance-2.0-global`, but uses the fast endpoint.

### `wan-2.2`

- Endpoint: `POST https://www.runninghub.cn/openapi/v2/rhart-video/wan-2.2/image-to-video`
- Explicit example fields from the official doc:
  - `imageUrl`
  - `prompt`
  - `duration`
  - `resolution`

Observed from a live API validation on 2026-04-26:

- the old numeric field ids such as `219##image` and `183##text` now return `errorCode=1007`
- the endpoint explicitly asks for `imageUrl` and `prompt`
- `duration` must be passed as a string
- `resolution` is required; `auto` is accepted

## Notes For Extension

- If the user names a different RunningHub endpoint, add a new payload builder rather than overloading an existing one.
- Prefer preserving the exact field names shown in RunningHub docs, especially for `wan-*` endpoints with numeric field ids.
