# Files API

Upload, retrieve, and delete files.

## Supported Formats

`jpg`, `png`, `bmp`, `tiff`, `heic`, `pdf`, `doc`, `docx`, `ppt`, `pptx`, `xls`, `xlsx`, `hwp`, `hwpx`

- Max file size: **500 MB**
- Max pages: **1,000**

## POST /v2/files — Upload File

`multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | File to upload |
| `purpose` | string | No | Default: `"user_data"` |
| `expires_after[anchor]` | string | No | `"created_at"` |
| `expires_after[seconds]` | int | No | Seconds until expiry. Default: 30 days |

**Response:**

```json
{
  "id": "file_abc123",
  "object": "file",
  "bytes": 102400,
  "filename": "document.pdf",
  "purpose": "user_data",
  "created_at": 1700000000,
  "expires_at": 1702592000
}
```

After upload, page image conversion runs automatically. The file is usable in Jobs once conversion completes.

## GET /v2/files — List Files

Cursor pagination applied.

## GET /v2/files/{file_id} — Get File

| Parameter | Values | Description |
|-----------|--------|-------------|
| `pages` | `all` \| `none` | Include page info (default: `none`) |
| `view` | `none` \| `status` \| `all` | Extended fields (default: `none`) |

**Response with `view=all` + `pages=all`:**

```json
{
  "id": "file_abc123",
  "object": "file",
  "bytes": 102400,
  "filename": "document.pdf",
  "purpose": "user_data",
  "created_at": 1700000000,
  "expires_at": 1702592000,
  "hash": "sha256_abc...",
  "file_url": "https://cdn.example.com/documents/doc_xxx/document.pdf",
  "num_pages": 5,
  "status": "uploaded",
  "pages": [
    {
      "id": "page_xxx",
      "idx": 0,
      "status": "UPLOADED",
      "image_url": "https://cdn.example.com/documents/doc_xxx/pages/0.jpg"
    }
  ]
}
```

## DELETE /v2/files/{file_id} — Delete File

```json
{ "id": "file_abc123", "object": "file", "deleted": true }
```

## File Status

| Status | Description |
|--------|-------------|
| `PROCESSING` | Conversion in progress. Cannot be used in Jobs |
| `UPLOADED` | Conversion complete. Ready for Jobs |
| `READY` | Parsing complete |
| `FAILED` | Conversion failed |

Creating a Job with a `PROCESSING` file returns `409`.

## Errors

| Code | Cause |
|------|-------|
| 400 | Missing file, invalid parameter |
| 404 | Non-existent file_id |
| 409 | File still in PROCESSING status |
| 415 | Unsupported file extension |
