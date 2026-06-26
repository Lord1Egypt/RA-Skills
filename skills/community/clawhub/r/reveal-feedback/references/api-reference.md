# Reveal REST API v1 Reference

Base URL: `https://www.testreveal.ai/api/v1`
Auth: `Authorization: Bearer <REVEAL_API_KEY>`

## Products

### GET /products
List vendor's products.
Query params: `limit` (int, default 20, max 50)
Response: `{ "data": { "products": [...], "total": n } }`

### GET /products/{id}
Get product details with review task count and total submissions.

### GET /products/{id}/analytics
Get product analytics.
Response fields: `productId`, `productName`, `reviewTasks`, `totalSubmissions`, `analyzedSubmissions`, `averageCompletionRate` (int, percent), `sentimentDistribution` (object), `topIssues` (array of {issue, mentions}), `topPositives` (array of {positive, mentions})

## Review Tasks

### GET /review-tasks
List review tasks.
Query params: `status` (active|completed|all), `productId`, `limit` (max 50)
Response: `{ "data": { "reviewTasks": [...], "total": n } }`

Each task: `id`, `title`, `description`, `status`, `taskType` (web|mobile), `productId`, `product`, `website`, `requiredReviewers`, `completedReviews`, `submissionCount`, `createdAt`

### POST /review-tasks
Create a review task.
Required body fields: `title` (string), `productId` (string), `instructions` (object with `objective`, `steps`, `feedback`)
Optional: `description`, `website`, `taskType` (web|mobile), `requiredReviewers` (int, default 5)

### GET /review-tasks/{id}
Get full task details including instructions and store URLs.

### PATCH /review-tasks/{id}
Update a task. Body: `status`, `title`, `description`, `requiredReviewers` (all optional)

## Submissions

### GET /review-tasks/{id}/submissions
Get all submissions for a task.
Query params: `status` (pending|completed|all)

Each submission: `index`, `status`, `videoUrl`, `submittedAt`, `notes`, `hasAnalysis`, `sentiment`, `issueCount`, `positiveCount`, `visualSummaryUrl`, `transcript`, `analysis` (object with `issues`, `positives`, `suggestions`, `sentiment`, `usabilityFriction`, `visualEvents`, `userExperience`)

## Insights

### GET /insights/{productId}
Aggregated AI insights across all submissions for a product.
Response: `totalAnalyzedSubmissions`, `sentimentDistribution`, `topIssues` (array of {text, mentions}), `topPositives`, `topSuggestions`, `uniqueIssues`, `uniquePositives`

## Marketing

### POST /marketing/summarize-highlights
Transform raw user feedback into persuasive marketing highlight statements.
Required body: `highlights` (array of strings — raw feedback to transform)
Response: `{ "data": { "summary": ["polished marketing statement 1", "..."] } }`

### POST /marketing/generate-script
Generate a 30-second marketing video script for a product.
Required body: `productId` (string)
Optional body: `positiveHighlights` (array of strings — if omitted, product description is used), `scriptType` (string: `problem-solution` | `empathetic` | `aspirational` | `story-driven`, default `problem-solution`)
Response: `{ "data": { "script": "formatted script with [Scene X: Title] headers", "productId": "...", "scriptType": "..." } }`
The script contains 7 scenes, each with Visual and Narration sections.

### POST /marketing/generate-image
Generate a marketing image using AI.
Required body: `productId` (string), `prompt` (string — creative direction)
Optional body: `styleName` (string — e.g. "Modern Gradient"), `tagline` (string — text to include)
Response: `{ "data": { "imageUrl": "https://...", "productId": "...", "prompt": "...", "styleName": "..." } }`
Returns 422 if image generation fails — try a different prompt.

### POST /marketing/edit-script
Parse a script into structured scenes and optionally apply edit operations.
Required body: `script` (string — the script text with `[Scene X: Title]` headers)
Optional body: `operations` (array — if omitted, just parses the script)

Operation types:
- `{ "action": "edit", "sceneNumber": 3, "title": "...", "visual": "...", "narration": "..." }` — update fields on an existing scene (only include fields to change)
- `{ "action": "add", "position": 4, "title": "...", "visual": "...", "narration": "..." }` — insert a new scene at position (appends if omitted)
- `{ "action": "remove", "sceneNumber": 2 }` — delete a scene (cannot remove the last one)

Operations are applied in order. Scenes renumber automatically after add/remove.

Response: `{ "data": { "script": "updated script text", "scenes": [{ "number": 1, "title": "...", "visual": "...", "narration": "..." }, ...] } }`

### GET /marketing/media-search
Search Pictory's stock media library for images and videos.
Query params: `keyword` (required), `category` (optional), `page` (int, optional, default 1)
Response: `{ "data": { "results": [{ "url": "...", "type": "image"|"video", "thumbnail": "..." }], "total": n, "page": 1, "keyword": "..." } }`
Use the `url` values in the `customMediaUrls` field of generate-video to assign media to specific scenes.

### POST /marketing/generate-video
Create a Pictory video storyboard from a formatted script.
Required body: `productId` (string), `script` (string — must contain `[Scene X: Title]` headers with Visual/Narration)
Optional body: `voiceOver` (object: `speaker` string default "Jackson", `speed` int default 100), `musicVolume` (number 0-1, default 0.4), `customMediaUrls` (object — map scene number strings to media URLs, e.g. `{ "1": "https://...", "3": "https://..." }`)
Response: `{ "data": { "jobId": "...", "accessToken": "...", "productId": "..." } }`
Save both `jobId` and `accessToken` — needed for subsequent render and status calls.
Scenes with a `customMediaUrls` entry use that media; others get auto-matched stock media from the visual description.

### PUT /marketing/render-video/{jobId}
Trigger rendering of a completed storyboard job.
Required body: `accessToken` (string — from generate-video response)
Optional body: `webhook` (string — HTTPS callback URL for completion notification)
Response: `{ "data": { "jobId": "...", "status": "rendering", "message": "..." } }`
Returns 404 if job not found, 409 if storyboard is not yet ready (retry after a few seconds).

### GET /marketing/video-status?jobId={jobId}
Poll the status of a video job.
Query params: `jobId` (required)
Response: `{ "data": { "jobId": "...", "status": "in-progress" | "completed" | "failed", "videoUrl": "..." | null } }`
Poll every 15-30 seconds. `videoUrl` is populated when `status` is `completed`.

**Typical video workflow:**
1. `POST /marketing/generate-script` → get script
2. `POST /marketing/edit-script` → parse, review, and refine scenes (edit/add/remove)
3. `GET /marketing/media-search?keyword=...` → find stock media for specific scenes
4. `POST /marketing/generate-video` (with `customMediaUrls` for stock media) → get `jobId` + `accessToken`
5. Wait ~30s, then `PUT /marketing/render-video/{jobId}` → trigger render
6. `GET /marketing/video-status?jobId=...` → poll until `completed` → get `videoUrl`

## Webhooks

### GET /webhooks
List registered webhooks.

### POST /webhooks
Register a webhook.
Body: `url` (string, HTTPS required), `events` (array of: review.submitted, review.analyzed, task.completed, video.generated)
Response includes `secret` for HMAC-SHA256 signature verification via `X-Reveal-Signature` header.

### DELETE /webhooks?id={webhookId}
Delete a webhook.

## Notifications

### GET /notifications
Query params: `unread` (true|false, default true), `limit` (max 50)

### PATCH /notifications
Mark as read. Body: `{ "notificationId": "..." }` or `{ "markAllRead": true }`

## Error format

All errors: `{ "error": { "code": "ERROR_CODE", "message": "human readable" } }`
Common codes: UNAUTHORIZED (401), FORBIDDEN (403), NOT_FOUND (404), VALIDATION_ERROR (400), PICTORY_ERROR (502), CONFIGURATION_ERROR (503), GENERATION_FAILED (422)
