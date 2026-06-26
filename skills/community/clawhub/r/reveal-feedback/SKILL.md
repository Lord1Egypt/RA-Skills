---
name: reveal-feedback
description: Interact with Reveal feedback infrastructure to manage products, create review tasks, read AI-analyzed user feedback, get sentiment insights, view submissions, manage notifications, register webhooks, and generate marketing content (scripts, images, videos). Use when the user asks about product feedback, user reviews, testing tasks, sentiment analysis, top issues, review submissions, marketing videos, marketing images, video scripts, or anything related to their Reveal account.
metadata: {"openclaw":{"requires":{"env":["REVEAL_API_KEY"]},"primaryEnv":"REVEAL_API_KEY","emoji":"📊","homepage":"https://testreveal.ai"}}
---

# Reveal Feedback Infrastructure

Reveal is a universal feedback platform where human reviewers screen-record themselves using products and provide AI-analyzed feedback. This skill connects to the Reveal REST API to manage the full feedback lifecycle — from collecting reviews to generating marketing content from that feedback.

## Authentication

All API calls require the `REVEAL_API_KEY` environment variable. The key is a vendor API key generated from the Reveal dashboard under Settings → API Keys.

Every request uses this header:
```
Authorization: Bearer $REVEAL_API_KEY
```

Base URL: `https://www.testreveal.ai/api/v1`
(Override with `REVEAL_BASE_URL` env var if set.)

## Capabilities

### 1. Check dashboard overview

Fetch products, active review tasks, and unread notifications to give the user a quick status update.

Steps:
1. GET `/products` to list vendor products
2. GET `/review-tasks?status=active` to list active tasks
3. GET `/notifications?unread=true&limit=5` to get unread notifications
4. Summarize: product count, active tasks with submission progress, and recent notifications

### 2. Get feedback insights for a product

Fetch AI-aggregated insights: top issues, top positives, sentiment distribution, and suggestions.

Steps:
1. GET `/products` to find the product ID matching the user's request
2. GET `/insights/{productId}` to get aggregated insights
3. Present: sentiment breakdown, top issues ranked by frequency, top positives, unique issue count

### 3. Get product analytics

Fetch quantitative metrics for a product.

Steps:
1. GET `/products/{productId}/analytics`
2. Present: total submissions, analyzed count, average completion rate, sentiment distribution, top issues, top positives

### 4. View review submissions

Get individual review submissions with transcripts, AI analysis, sentiment, and issue counts.

Steps:
1. GET `/review-tasks?status=active&limit=5` to find the relevant task (or use a task ID if provided)
2. GET `/review-tasks/{taskId}/submissions` to get all submissions
3. For each submission, present: status, sentiment, issue count, positive count, transcript preview

### 5. Create a review task

Create a new user-testing task so reviewers can test a product.

Steps:
1. GET `/products` to find the product matching the user's description
2. Extract from the user's message: title, objective, steps, feedback focus, reviewer count
3. POST `/review-tasks` with body:
```json
{
  "title": "extracted title",
  "productId": "matched product ID",
  "requiredReviewers": 5,
  "instructions": {
    "objective": "what the reviewer should accomplish",
    "steps": "step-by-step instructions",
    "feedback": "what feedback to focus on"
  }
}
```
4. Confirm creation with task ID and details

### 6. Update a review task

Close, pause, or modify an existing review task.

Steps:
1. PATCH `/review-tasks/{taskId}` with fields to update (status, title, description, requiredReviewers)
2. Confirm the update

### 7. List products

Show all products registered on the vendor's Reveal account.

Steps:
1. GET `/products?limit=50`
2. Present each product: name, category, platform support (web/mobile), website

### 8. Get notifications

Check for new activity on Reveal.

Steps:
1. GET `/notifications?unread=true&limit=20`
2. Present notification messages with timestamps
3. If user says to mark as read: PATCH `/notifications` with `{"markAllRead": true}`

### 9. Register a webhook

Set up real-time event notifications.

Steps:
1. POST `/webhooks` with body:
```json
{
  "url": "https://user-provided-url",
  "events": ["review.submitted", "review.analyzed", "task.completed", "video.generated"]
}
```
2. Return the webhook ID and signing secret. Instruct user to store the secret securely.

### 10. List webhooks

Steps:
1. GET `/webhooks`
2. Present each webhook: URL, subscribed events, active status

### 11. Summarize feedback into marketing highlights

Turn raw user feedback into polished, persuasive marketing statements.

Steps:
1. Collect the positive feedback strings (from insights or submissions)
2. POST `/marketing/summarize-highlights` with body:
```json
{
  "highlights": ["feedback string 1", "feedback string 2", "..."]
}
```
3. Response contains `summary` — an array of marketing-ready highlight strings

### 12. Generate a marketing video script

Generate a 30-second video script from product feedback or the product description.

Steps:
1. GET `/products` to find the product ID
2. Optionally GET `/insights/{productId}` to extract positive highlights
3. POST `/marketing/generate-script` with body:
```json
{
  "productId": "the product ID",
  "positiveHighlights": ["highlight 1", "highlight 2"],
  "scriptType": "problem-solution"
}
```
   - `positiveHighlights` is optional; if omitted the product description is used
   - `scriptType` options: `problem-solution`, `empathetic`, `aspirational`, `story-driven`
4. Response contains `script` — a formatted script with `[Scene X: Title]` headers, Visual and Narration per scene

### 13. Generate a marketing image

Create a marketing image for a product with AI.

Steps:
1. GET `/products` to find the product ID
2. POST `/marketing/generate-image` with body:
```json
{
  "productId": "the product ID",
  "prompt": "Modern dashboard showcasing the key analytics features",
  "styleName": "Modern Gradient",
  "tagline": "Insights that drive growth"
}
```
   - `prompt` is required — the creative direction for the image
   - `styleName` and `tagline` are optional
3. Response contains `imageUrl` — a public URL to the generated image

### 14. Edit and refine a script

Parse a script into structured scenes and apply edits — change narration/visuals, add new scenes, or remove scenes.

Steps:
1. POST `/marketing/edit-script` with body:
```json
{
  "script": "the current script text",
  "operations": [
    { "action": "edit", "sceneNumber": 3, "narration": "Updated narration text" },
    { "action": "add", "position": 4, "title": "New CTA", "visual": "Happy customer using phone", "narration": "Try it free today!" },
    { "action": "remove", "sceneNumber": 6 }
  ]
}
```
   - `operations` is optional — omit it to just parse the script into structured scenes
   - `action: "edit"` — update title, visual, or narration of an existing scene (only include fields to change)
   - `action: "add"` — insert a new scene at `position` (or append if omitted)
   - `action: "remove"` — delete a scene by number (scenes renumber automatically)
2. Response contains both the updated `script` string and a `scenes` array with structured scene objects

### 15. Search stock media for video scenes

Find stock images and videos from the Pictory library to use in specific video scenes.

Steps:
1. GET `/marketing/media-search?keyword=business+meeting&page=1`
   - `keyword` is required — the search term
   - `category` and `page` are optional
2. Response contains `results` — array of `{ url, type, thumbnail }`
3. Use the `url` values in the `customMediaUrls` field of generate-video to assign media to specific scenes

### 16. Generate a marketing video (full pipeline)

Create a full marketing video from a script. This is a multi-step async workflow.

Steps:
1. Generate a script first (capability 12) or have the user provide one
2. Optionally refine the script (capability 14) — edit scenes, add/remove as needed
3. Optionally search for stock media (capability 15) to use in specific scenes
4. POST `/marketing/generate-video` with body:
```json
{
  "productId": "the product ID",
  "script": "the full script with [Scene X: Title] headers",
  "voiceOver": { "speaker": "Jackson", "speed": 100 },
  "musicVolume": 0.4,
  "customMediaUrls": {
    "1": "https://stock-media-url-for-scene-1",
    "3": "https://stock-media-url-for-scene-3"
  }
}
```
   - `customMediaUrls` is optional — map scene numbers to stock media URLs from media-search
   - Scenes without a custom URL will get auto-matched stock media based on the visual description
   Response: `{ "data": { "jobId": "...", "accessToken": "...", "productId": "..." } }`
5. Wait ~30 seconds, then trigger rendering:
   PUT `/marketing/render-video/{jobId}` with body:
```json
{
  "accessToken": "the accessToken from step 4",
  "webhook": "https://optional-callback-url"
}
```
6. Poll for completion:
   GET `/marketing/video-status?jobId={jobId}`
   Response: `{ "data": { "status": "in-progress" | "completed" | "failed", "videoUrl": "..." } }`
   - Keep polling every 15-30 seconds until `status` is `completed`
   - When complete, `videoUrl` contains the final video URL

## Response format

All API responses follow this structure:
- Success: `{ "data": { ... } }`
- Error: `{ "error": { "code": "ERROR_CODE", "message": "description" } }`

## Guardrails

- Never expose or log the API key in responses to the user
- If an API call fails with 401, tell the user their API key may be invalid or expired
- If a product is not found, suggest listing products first
- When creating review tasks, always confirm the details with the user before sending the POST
- Do not fabricate feedback data — only report what the API returns
- Marketing endpoints require a vendor API key — reviewer keys will get a 403
- Video generation is async — always poll `video-status` rather than assuming immediate completion
- When generating videos, save the `accessToken` from generate-video — it's needed for render-video
