# Ingest API Reference

## Use When
- You need to upload documents or files to Eve for processing (extraction, indexing, analysis).
- You need to download or render ingested files in-browser.
- You need to track processing status or receive callbacks on completion.
- You need to understand the ingest lifecycle (upload → confirm → process → done/failed).

## Load Next
- `references/events.md` for the `system.doc.ingest` event that triggers processing workflows.
- `references/pipelines-workflows.md` for wiring ingest events to workflow steps.
- `references/object-store-filesystem.md` for the underlying object store and org buckets.
- `references/eve-sdk.md` for authenticating app requests to the ingest API.

## Ask If Missing
- Confirm the target project ID before running any ingest command.
- Confirm whether the app needs callback notifications or will poll for status.
- Confirm whether the app needs to render files in-browser (JS fetch requires CORS).

## Overview

The Ingest API provides a three-step lifecycle for uploading, processing, and accessing files:

1. **Create** -- register the file and get a presigned upload URL
2. **Upload** -- PUT the file directly to S3/MinIO (no bytes through the API)
3. **Confirm** -- trigger processing (emits `system.doc.ingest` event)

Processing runs asynchronously via a workflow triggered by the event. When processing completes, the ingest record status updates to `done` or `failed`, and the optional callback URL is invoked.

## CLI Commands

```bash
# Upload a file (create + upload + confirm in one step)
eve ingest <file> --project proj_xxx
  [--title <title>] [--description <desc>]
  [--instructions <text>] [--tags <a,b>]
  [--mime-type <type>] [--source-channel <channel>]
  [--json]

# Explicit subcommands
eve ingest create <file> [same flags]
eve ingest list [--status <status>] [--limit <n>] [--offset <n>] [--json]
eve ingest show <ingest_id> [--json]
```

Notes:
- `eve ingest <file>` is shorthand for create -- it handles the full upload lifecycle.
- The CLI auto-infers MIME type from file extension.
- `source_channel` defaults to `cli`. Allowed values: `upload`, `cli`, `slack`, `api`.
- `show` returns `download_url` and `download_url_expires_at` (presigned, 5-min TTL).

## API Endpoints

All endpoints are scoped under `projects/:project_id/ingest`.

| Method | Path | Permission | Description |
|--------|------|-----------|-------------|
| `POST` | `/projects/{id}/ingest` | `projects:write` | Create ingest record, returns presigned upload URL |
| `POST` | `/projects/{id}/ingest/{ingest_id}/confirm` | `projects:write` | Confirm upload and trigger processing |
| `GET` | `/projects/{id}/ingest` | `projects:read` | List ingest records (filterable by status) |
| `GET` | `/projects/{id}/ingest/{ingest_id}` | `projects:read` | Show record details with `download_url` |
| `GET` | `/projects/{id}/ingest/{ingest_id}/download` | `projects:read` | 302 redirect to presigned S3 download URL |

### Create Request Body

```json
{
  "file_name": "report.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1048576,
  "title": "Q1 Report",
  "description": "Quarterly financial summary",
  "instructions": "Extract key metrics and trends",
  "tags": ["finance", "quarterly"],
  "source_channel": "api",
  "callback_url": "https://myapp.example.com/webhooks/ingest"
}
```

Required: `file_name`, `mime_type`, `size_bytes`. Max file size: 500 MB.

### Create Response

```json
{
  "ingest_id": "ingest_abc123",
  "upload_url": "https://s3.../ingest/ingest_abc123/report.pdf?X-Amz-...",
  "upload_method": "PUT",
  "upload_expires_at": "2026-03-13T10:05:00.000Z",
  "max_bytes": 524288000,
  "storage_key": "ingest/ingest_abc123/report.pdf"
}
```

### Upload

PUT the file content directly to `upload_url` with the matching `Content-Type`. No Eve auth needed -- the URL is self-authenticating.

```bash
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/pdf" \
  --data-binary @report.pdf
```

### Confirm Response

```json
{
  "ingest_id": "ingest_abc123",
  "status": "processing",
  "event_id": "evt_xyz",
  "job_id": null
}
```

Confirm is idempotent -- calling it again on a `processing` or `done` record returns the current state.

### Show Response

```json
{
  "id": "ingest_abc123",
  "org_id": "org_xxx",
  "project_id": "proj_xxx",
  "file_name": "report.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1048576,
  "storage_key": "ingest/ingest_abc123/report.pdf",
  "status": "done",
  "download_url": "https://s3.../ingest/ingest_abc123/report.pdf?X-Amz-...",
  "download_url_expires_at": "2026-03-13T10:10:00.000Z",
  "callback_url": "https://myapp.example.com/webhooks/ingest",
  "event_id": "evt_xyz",
  "job_id": "proj-abc12345",
  "created_at": "2026-03-13T10:00:00.000Z",
  "completed_at": "2026-03-13T10:02:30.000Z"
}
```

Notes:
- `download_url` is a presigned S3 URL (5-min TTL). Refresh by calling show again.
- List responses do NOT include `download_url` (too expensive per-item). Call show for individual records.

### Download Redirect

`GET /projects/{id}/ingest/{ingest_id}/download` returns a 302 redirect to a presigned S3 URL. Use this for:

- `<img src="...">` -- browser follows redirect, renders image
- `<embed src="...">` -- PDF viewer in-browser
- `<a href="...">` -- download link
- `window.open(url)` -- open in new tab

No file bytes flow through the API. The S3 response includes the correct `Content-Type` from the original upload.

## Callback Notifications

When an ingest record has a `callback_url` set and processing completes (success or failure), the platform POSTs a notification:

```
POST <callback_url>
Content-Type: application/json
X-Eve-Event: ingest.completed
```

```json
{
  "ingest_id": "ingest_abc123",
  "status": "done",
  "job_id": "proj-abc12345",
  "file_name": "report.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 1048576,
  "storage_key": "ingest/ingest_abc123/report.pdf",
  "completed_at": "2026-03-13T10:02:30.000Z",
  "error_message": null
}
```

Behavior:
- Fire-and-forget (does not block status sync).
- 3 retries with exponential backoff (5s, 15s, 45s).
- 10s timeout per attempt.
- Never fails the ingest status update.
- `download_url` is NOT included in the callback (call `GET /ingest/{id}` to get it).

## CORS on Org Buckets

Org buckets are automatically created with CORS headers that allow browser-based JS access:

- **Allowed origins**: `*` (safe because presigned URLs are self-authenticating)
- **Allowed methods**: `GET`, `PUT`, `HEAD`
- **Allowed headers**: `*`
- **Max age**: 3600s

This means `fetch()`, `XMLHttpRequest`, PDF.js, and other JS-based file loaders work against presigned download URLs without CORS errors.

Simple HTML elements (`<img>`, `<embed>`, `<a>`) do not need CORS -- browsers load them directly. CORS only matters for JS-initiated requests.

## Ingest Lifecycle Diagram

```
App                      Eve API                    S3/MinIO
 |                          |                          |
 |-- POST /ingest --------->|                          |
 |<-- upload_url, ingest_id-|                          |
 |                          |                          |
 |-- PUT upload_url --------|------------------------->|
 |<-- 200 OK --------------|--------------------------|
 |                          |                          |
 |-- POST /confirm -------->|                          |
 |<-- status: processing ---|                          |
 |                          |                          |
 |      [workflow runs, processing completes]          |
 |                          |                          |
 |<-- POST callback_url ----|  (if callback_url set)   |
 |                          |                          |
 |-- GET /ingest/{id} ----->|                          |
 |<-- download_url ---------|                          |
 |                          |                          |
 |-- GET download_url ------|------------------------->|
 |<-- file bytes -----------|--------------------------|
```

## Event Integration

Confirming an upload emits a `system.doc.ingest` event:

```json
{
  "type": "system.doc.ingest",
  "source": "system",
  "payload": {
    "org_id": "org_xxx",
    "project_id": "proj_xxx",
    "ingest_id": "ingest_abc123",
    "file_name": "report.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 1048576,
    "storage_key": "ingest/ingest_abc123/report.pdf",
    "title": "Q1 Report",
    "callback_url": "https://myapp.example.com/webhooks/ingest"
  }
}
```

Wire this to a workflow trigger to run processing jobs:

```yaml
workflows:
  document-processing:
    trigger:
      system:
        event: doc.ingest    # matches system.doc.ingest events
    steps:
      - name: process
        agent:
          name: doc-processor
```

To manually test with input (e.g., to pass ingest context):

```bash
eve workflow run document-processing --input '{"payload":{"ingest_id":"ing_xxx","file_name":"doc.pdf"}}'
```

## Common Patterns

### App Backend: Upload with Callback

```typescript
// Create ingest record with callback
const resp = await fetch(`${EVE_API_URL}/projects/${projectId}/ingest`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    file_name: file.name,
    mime_type: file.type,
    size_bytes: file.size,
    callback_url: `${APP_URL}/api/webhooks/ingest`,
  }),
});
const { upload_url, ingest_id } = await resp.json();

// Upload directly to S3
await fetch(upload_url, { method: 'PUT', body: fileBuffer, headers: { 'Content-Type': file.type } });

// Confirm
await fetch(`${EVE_API_URL}/projects/${projectId}/ingest/${ingest_id}/confirm`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
});
```

### App Frontend: Render Ingested File

```tsx
// Use the download redirect endpoint as src (no CORS needed for <img>/<embed>)
<embed src={`${API_URL}/projects/${projectId}/ingest/${ingestId}/download`} type="application/pdf" />

// For JS-based rendering (e.g. PDF.js), use download_url from show response
const record = await fetch(`${API_URL}/projects/${projectId}/ingest/${ingestId}`).then(r => r.json());
const pdfData = await fetch(record.download_url).then(r => r.arrayBuffer());
```
