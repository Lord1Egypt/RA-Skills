# Workflow: Import media from a URL

Use this when the user wants to pull a file from a third-party source (Dropbox, Canva export, any direct download URL) into their ViralNote media library — without manually downloading and re-uploading it themselves.

## When to use POST /media/import vs POST /media

- `POST /media/import` — when the file already exists at a public/signed HTTPS URL and you can hand that URL to the server
- `POST /media` (multipart upload) — when you have raw bytes (e.g. just downloaded the file yourself, or the user pasted it)

If the user shared a Dropbox link, Canva export URL, or any similar direct-download URL, prefer `/media/import` — it skips the round-trip through the agent.

## Step 1: Confirm the URL is direct-download

The URL must serve the actual file bytes when fetched, not a webpage. Dropbox shared-link URLs ending in `?dl=1` work; the Chooser-generated direct links work; Canva export URLs work. A URL that requires a login does not work.

If you're not sure, ask the user to verify the URL opens the file directly in a fresh incognito browser.

## Step 2: Call the import endpoint

```bash
curl -sS -X POST https://viralnote.app/api/v1/media/import \
  -H "x-api-key: $VIRALNOTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "dropbox",
    "url": "https://dl.dropboxusercontent.com/.../photo.jpg",
    "name": "spring-launch-hero.jpg",
    "mimeType": "image/jpeg"
  }'
```

The `source` field must be one of: `dropbox`, `canva`. It surfaces as `originalSource` on the resulting library item so users can see where it came from.

The `mimeType` is optional but recommended — speeds up the type detection. `bytes` is also optional (declared file size in bytes); supplying it lets the server reject oversized files before downloading.

## Step 3: Confirm to the user

The response shape:

```json
{
  "data": {
    "id": "lib_abc123",
    "storagePath": "library/<uid>/image/...",
    "publicUrl": "https://firebasestorage.googleapis.com/...",
    "contentType": "image/jpeg",
    "size": 2473928,
    "originalSource": "dropbox",
    "createdAt": "2026-05-18T03:42:00.000Z"
  }
}
```

Tell the user the file is now in their library and ready to attach to a post. Offer to chain into `examples/schedule-post.md` if they want to schedule it.

## Limits

- Max file size: 200MB per import (vs 500MB on direct upload — bandwidth cost reasons)
- Supported types: JPG, PNG, GIF, WebP (images); MP4, MOV, WebM (video)
- Upstream fetch timeout: 60 seconds

## Common errors

- `400 validation-error: "Invalid source"` — `source` must be `dropbox` or `canva` exactly
- `413 validation-error: "File too large"` — split the file or use a different distribution method
- `502 upstream-error` — the URL didn't serve the file. Re-check the URL, especially that it's a direct-download (not a webpage)
