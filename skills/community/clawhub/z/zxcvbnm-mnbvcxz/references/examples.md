# Usage Examples

## 1) End-to-end generation workflow (`t2v`)

Command:
```bash
node scripts/run-workflow.mjs --model <model> --payload '<json_payload>'
```

Skill runtime output:
```json
{
  "ok": true,
  "status": "COMPLETED",
  "taskId": "ckxxxxxxxx",
  "data": {
    "id": "ckxxxxxxxx",
    "output": {
      "videoUrl": "https://..."
    }
  }
}
```

Raw API create response (from `POST /api/v1/generate/{model}`):
```json
{
  "status": "SUBMITTED",
  "taskId": "ckxxxxxxxx",
  "responseUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx",
  "statusUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/status",
  "cancelUrl": "https://aivideomaker.ai/api/v1/tasks/ckxxxxxxxx/cancel"
}
```

## 2) Query task status

```bash
node scripts/run-workflow.mjs --action getStatus --taskId ckxxxxxxxx
```

Skill runtime output:
```json
{
  "ok": true,
  "status": "PROGRESS",
  "taskId": "ckxxxxxxxx",
  "data": {
    "status": "PROGRESS"
  }
}
```

Raw API status response (from `GET /api/v1/tasks/{taskId}/status`):
```json
{
  "status": "COMPLETED"
}
```

## 3) Cancel task

```bash
node scripts/run-workflow.mjs --action cancelTask --taskId ckxxxxxxxx
```

Possible output:
```json
{
  "ok": true,
  "status": "CANCEL",
  "taskId": "ckxxxxxxxx",
  "data": {
    "status": "CANCEL"
  }
}
```

## 4) Handling insufficient credits

Typical API error:
```json
{
  "status": "FAILED",
  "message": "Insufficient credits"
}
```

Skill runtime output:
```json
{
  "ok": false,
  "status": "FAILED",
  "errorCode": "INSUFFICIENT_CREDITS",
  "errorMessage": "Insufficient credits",
  "taskId": null
}
```

Recommended next actions:
- Reduce `duration` or use a lower-cost model.
- Ensure the account has enough credits.
- Retry after top-up.

## 5) Handling 429 rate limit

Skill behavior:
1. Detect `429`.
2. Parse `Retry-After` if present.
3. Sleep and retry (up to max retries).
4. Return `RATE_LIMITED` when retries are exhausted.

Output example:
```json
{
  "ok": false,
  "status": "FAILED",
  "errorCode": "RATE_LIMITED",
  "errorMessage": "Rate limited by upstream API",
  "retryAfter": 2
}
```

## 6) List tasks raw API response

Endpoint:
```bash
GET /api/v1/tasks
```

Raw API response example:
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
