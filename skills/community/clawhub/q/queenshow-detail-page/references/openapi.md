# Queenshow Detail Page OpenAPI

Base path:

- Through the frontend/proxy: `/api/promotion`
- Direct local backend: `http://localhost:8890/promotion`

Auth: send one of:

```http
Authorization: Bearer qs_live_xxx
X-API-Key: qs_live_xxx
```

All JSON responses use:

```json
{
  "errorNo": 200,
  "errorDesc": "",
  "result": {}
}
```

Send JSON request bodies as UTF-8. For Windows PowerShell raw requests, pass UTF-8 bytes and set `Content-Type: application/json; charset=utf-8`; otherwise non-ASCII text can be converted to `?`. The bundled Python client handles this correctly.

## Product Input

`product` matches editor-next product information:

```json
{
  "mainImages": ["https://example.com/main-1.png"],
  "intro": "Product selling points, material, target user, scene, and constraints.",
  "brandLogo": "https://example.com/logo.png",
  "watermark": {
    "enabled": false,
    "type": "text",
    "text": "",
    "image": "",
    "opacity": 0.16
  },
  "skus": [
    { "id": "sku_1", "name": "Black / 42", "price": 399 }
  ],
  "detailStyle": "Premium, minimal, strong product close-ups."
}
```

Rules:

- `mainImages` is required for detail page creation. The API keeps the first 3 URLs.
- `skus` can be empty.
- `detailStyle` should include visual tone, layout requirements, platform constraints, and category notes.

## Workflow Endpoints

### Upload Materials

`POST /openapi/materials/upload`

Content type: `multipart/form-data`

Fields:

- `files`: one or more image/video files.
- `fileType`: optional, `image` or `video`.

Result:

```json
{
  "sources": [
    {
      "url": "https://cdn.example.com/file.png",
      "type": "image",
      "source": { "_id": "...", "name": "file.png", "fileType": "image" }
    }
  ]
}
```

### List Materials

`GET /openapi/materials?fileType=image&limit=50`

Result:

```json
{ "materials": [] }
```

### Create Detail Page And Outline Task

`POST /openapi/detail-pages`

```json
{
  "title": "Product Detail Page",
  "desc": "Optional short description",
  "thumbnail": "https://example.com/main-1.png",
  "viewportId": "mobile-750-long",
  "product": {
    "mainImages": ["https://example.com/main-1.png"],
    "intro": "Product facts and selling points.",
    "skus": [],
    "detailStyle": "Clean ecommerce detail page."
  }
}
```

Result:

```json
{
  "detailPageId": "...",
  "outlineTaskId": "task_xxx",
  "status": "outline_pending",
  "task": {}
}
```

Viewport IDs:

- `mobile-750-long`
- `desktop-1440-long`
- `desktop-1920-long`

### Query Detail Page Status

`GET /openapi/detail-pages/{detailPageId}/status`

Result:

```json
{
  "detailPageId": "...",
  "status": "outline_ready",
  "tasks": [],
  "spent": 0,
  "updated": false
}
```

Status values:

- `draft`: no task exists.
- `outline_running`: outline task is pending or running.
- `outline_ready`: outline task succeeded and can be applied.
- `generating`: section image tasks exist and are not all done.
- `completed`: all section image tasks are done and synced into the document.
- `failed`: one or more tasks failed or were cancelled.

The outline task result is available in `tasks[].result.sections`.

### Apply Outline Sections

`POST /openapi/detail-pages/{detailPageId}/outline/apply`

Use the latest outline task result:

```json
{
  "taskId": "task_xxx",
  "viewportId": "mobile-750-long"
}
```

Override or provide sections manually:

```json
{
  "taskId": "task_xxx",
  "sections": [
    {
      "title": "Hero",
      "goal": "Present product identity.",
      "coreIdea": "Show the product in a premium studio scene.",
      "copy": {
        "headline": "Built for everyday speed",
        "subhead": "Lightweight comfort for city runs",
        "bullets": ["Breathable mesh", "Rebound foam"]
      },
      "imagePrompt": "A premium ecommerce hero image...",
      "productImageUsage": "Use the first product main image as the subject.",
      "layout": {
        "mobile": "Full-width image with centered title.",
        "desktop": "Split visual and copy."
      },
      "qualityChecks": ["Product is clear", "Text area is readable"]
    }
  ]
}
```

Result:

```json
{
  "detailPageId": "...",
  "outlineTaskId": "task_xxx",
  "sections": [
    { "sectionId": "...", "imageNodeId": "...", "outline": {} }
  ],
  "imageTasks": [],
  "status": "generating"
}
```

### Fetch Detail Page

`GET /openapi/detail-pages/{detailPageId}`

Returns the stored page, full `document`, `product`, tasks, aggregate status, and page spend. This endpoint also syncs completed image task outputs into `document` before returning.

```json
{
  "detailPageId": "...",
  "detailPage": {
    "_id": "...",
    "title": "...",
    "document": {}
  },
  "status": "completed",
  "tasks": [],
  "spent": 0,
  "updated": true
}
```

### List Detail Pages

`GET /openapi/detail-pages?limit=50`

Result:

```json
{ "detailPages": [] }
```

### Update Detail Page

`POST /openapi/detail-pages/{detailPageId}/update`

Allowed fields:

```json
{
  "title": "Updated title",
  "desc": "Updated description",
  "thumbnail": "https://example.com/thumb.png",
  "product": {},
  "document": {}
}
```

`document` can be a complete editor-next document. Use this for agent-authored layout fixes after generation.

Convenience pattern for updating only `document.title` or `document.desc`:

1. Fetch `GET /openapi/detail-pages/{detailPageId}`.
2. Modify `result.detailPage.document.title` or `result.detailPage.document.desc`.
3. Post `{ "desc": "...", "document": <full document> }` to `/openapi/detail-pages/{detailPageId}/update`.

The bundled client can do this with `update --document-title "..."` or `update --document-desc "..."`.

### Query Task

`GET /openapi/tasks/{taskId}`

Result is the full task record owned by the current API key, including `payload`, `result`, `progress`, `billing.amount`, and `billing.status`.

### Query API Key Usage

`GET /openapi/usage`

Result:

```json
{
  "usage": {
    "spent": 0,
    "reserved": 0,
    "materialCount": 0,
    "pageCount": 0,
    "taskCount": 0
  },
  "key": {
    "_id": "...",
    "name": "...",
    "keyPrefix": "qs_live_xxxxx",
    "priceLimit": 1000
  }
}
```

The API may include `key.plainKey` for the current key. Treat it as sensitive. The bundled client redacts sensitive fields by default unless `--show-sensitive` is used.

## Recommended Agent Loop

1. Use existing URLs or upload local materials.
2. Create the detail page.
3. Poll status every 5 to 10 seconds until `outline_ready` or `failed`.
4. If `outline_ready`, call `outline/apply`.
5. Poll status every 10 to 20 seconds until `completed` or `failed`.
6. Fetch final detail page.
7. Verify final document integrity:
   - status is `completed`.
   - one section placeholder exists for each outline section.
   - one image node exists for each section.
   - each image node has `value.url` and `value.generationStatus == "succeeded"`.
8. Optionally update `document` with layout or copy corrections.

## Error Handling

- `401`: missing, invalid, revoked, or expired API key.
- `402`: wallet check failed or API key total price limit is insufficient.
- `errorNo != 200`: inspect `errorDesc`.
- If status is `failed`, fetch every failed task with `/openapi/tasks/{taskId}` and inspect `error`, `message`, and `progress`.
