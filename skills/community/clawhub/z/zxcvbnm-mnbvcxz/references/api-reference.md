# AIVideoMaker API Reference (Aligned with `ApiV1Docs.tsx`)

## Base URL
- `https://aivideomaker.ai`

## Authentication
All requests require header:
- `key: <AIVIDEO_API_KEY>`

`POST /api/v1/generate/{model}` also supports:

## Endpoints

### 1) Create generation task
- `POST /api/v1/generate/{model}`
- Allowed `model`: `t2v`, `i2v`, `lv`, `t2v_v3`, `i2v_v3`

#### Model parameters

##### `t2v` (Text to Video)
- `prompt`: string, required
- `aspectRatio`: `16:9` | `9:16` | `1:1`, required
- `filterMode`: `strict` | `custom`, required
- `duration`: `5` | `8`, required
- Credits: `duration * 1`

##### `i2v` (Image to Video)
- `image`: string (public image URL or `data:image/...;base64,...`), required
- `prompt`: string | null, optional
- `filterMode`: `strict` | `custom`, required
- `duration`: `5` | `8`, required
- Credits: `duration * 1`

##### `lv` (Long Video)
- `image`: string (first frame URL or `data:image/...;base64,...`), required
- `prompt`: string[] (max 6), required
- `filterMode`: `strict` | `custom`, required
- Credits: `prompt.length * 5 * 15`
- Duration rule: each prompt segment equals 5 seconds

##### `t2v_v3` (Text to Video V3)
- `prompt`: string, required
- `aspectRatio`: `16:9` | `9:16` | `1:1`, required
- `duration`: `5` | `10` | `15` | `20`, required
- Credits: `duration * 10`

##### `i2v_v3` (Image to Video V3)
- `image`: string (public image URL or `data:image/...;base64,...`), required
- `prompt`: string | null, optional
- `duration`: `5` | `10` | `15` | `20`, required
- Credits: `duration * 10`

## Image input note
- Skill contract accepts both public image URLs and `data:image/...;base64,...` for image inputs.
- Prefer `data:image/...;base64,...` in OpenClaw to avoid unreachable URL issues.
- Backend uploads base64 image to R2 first.
- Task input stored in `/api/v1/tasks/{taskId}` keeps the R2 URL instead of the full base64 string.

#### Raw API success response (from docs)
```json
{
  "status": "SUBMITTED",
  "taskId": "ckxxxxxxxx",
  "responseUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx",
  "statusUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/status",
  "cancelUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/cancel"
}
```

#### Raw API error response (from docs)
```json
{
  "status": "FAILED",
  "message": "Insufficient credits"
}
```

### 2) List tasks
- `GET /api/v1/tasks`
- Returns all tasks for current API key, newest first

#### Raw API response example (from docs)
```json
{
  "tasks": [
    {
      "id": "ckxxxxxxxx",
      "createdAt": "2026-03-19T08:00:00.000Z",
      "model": "t2v",
      "input": { "prompt": "...", "aspectRatio": "16:9" },
      "output": null,
      "status": "PROGRESS",
      "completedAt": null
    }
  ]
}
```

### 3) Get task details
- `GET /api/v1/tasks/{taskId}`
- Returns full task data: input, output, status, completion time

### 4) Get task status
- `GET /api/v1/tasks/{taskId}/status`
- Returns only current status; suitable for polling

#### Raw API response example (from docs)
```json
{
  "status": "COMPLETED"
}
```

### 5) Cancel task
- `PUT /api/v1/tasks/{taskId}/cancel`
- Only works when task status is still `SUBMITTED`

## Task status values
- `SUBMITTED`
- `PROGRESS`
- `COMPLETED`
- `FAILED`
- `CANCEL`

## Rate limiting
- Task query endpoints are limited to `60 requests/minute/IP`
- Exceeded limit returns HTTP `429` with `Retry-After` header

## Note on Skill runtime output
The scripts in this skill wrap raw API responses into a normalized shape for automation (`ok`, `errorCode`, `httpStatus`, etc.), but the raw endpoint contract above is copied from `ApiV1Docs.tsx`.
