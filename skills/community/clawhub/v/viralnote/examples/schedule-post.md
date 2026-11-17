# Workflow: Schedule a post

Use this when the user wants to schedule a post to one or more platforms at a future time.

## Step 1: Confirm what's being scheduled

Before calling the API, restate to the user:

- Platforms (e.g. "Instagram and X")
- Caption (verbatim — show them what you'll send)
- Scheduled time (in their local timezone — convert to ISO 8601 UTC before sending)
- Media (which library item — by name or recent upload)

Get a yes before continuing.

## Step 2: Find the media if needed

If the user referenced media by name ("the photo I just uploaded"), list the library to find the ID:

```bash
curl -sS https://viralnote.app/api/v1/media?type=image&limit=10 \
  -H "x-api-key: $VIRALNOTE_API_KEY"
```

Identify the item by `name` or most-recent `createdAt`. Capture its `id` field.

## Step 3: Create the scheduled post

```bash
curl -sS -X POST https://viralnote.app/api/v1/posts \
  -H "x-api-key: $VIRALNOTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Big day ahead. Here we go.",
    "platforms": ["instagram", "twitter"],
    "libraryItemId": "<media-id-from-step-2>",
    "scheduledFor": "2026-05-19T13:00:00Z",
    "status": "scheduled"
  }'
```

The response contains the new `id` and confirms the scheduled time. Show the user the post id and the scheduled time (converted back to their timezone).

## Step 4 (optional): Verify it appears in the dashboard

```bash
curl -sS https://viralnote.app/api/v1/posts/<post-id> \
  -H "x-api-key: $VIRALNOTE_API_KEY"
```

If `status: scheduled` and `scheduledFor` matches what was sent, you're done.

## Multi-image carousel

If the user wants to attach more than one image (Instagram or X carousel), pass `mediaIds` array instead of `libraryItemId`:

```json
{
  "caption": "...",
  "platforms": ["instagram"],
  "mediaIds": ["id1", "id2", "id3"],
  "scheduledFor": "2026-05-19T13:00:00Z",
  "status": "scheduled"
}
```

Max 10 images per carousel (Instagram cap; X caps at 4).

## Common errors

- `400 validation-error: "Caption required"` — caption is mandatory for most platforms.
- `400 validation-error: "Platform not connected"` — user hasn't connected that social account yet. Tell them to connect in dashboard → Social Accounts.
- `402 plan-limit: "Daily scheduled limit reached"` — user is on a plan with a cap. Surface to them; don't try a workaround.
