# content-marketing-dashboard API

- Base: `https://xiaonian.cc/employee-console/dashboard/v2/api`

## Quick-note (used by this skill)

`POST /content/quick-note/generate`

- No auth required
- One-shot generation: title + content + tags (+ optional images)

Request body:

```json
{
  "task_description": "...",
  "audience": "小红书用户",
  "tone": "友好自然",
  "character": "专业分享者",
  "note_type": null,
  "generate_image": true,
  "image_num": 1
}
```

Field constraints:
- `image_num`: 1–10

Response:
- `success` (bool)
- `message` (string)
- `timestamp` (string, ISO 8601)
- `title` (string)
- `content` (string)
- `tags` (string[])
- `image_urls` (string[])
- `note_type` (string|null)

