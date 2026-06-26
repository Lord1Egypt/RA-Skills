# WhatsApp Cloud API - Media Reference

> **Author:** Bello Sanchez
> **API Version:** v21.0
> **Last Updated:** 2026-02-09

---

## Overview

This document covers all media operations for the WhatsApp Cloud API: uploading, downloading, deleting, and referencing media assets in messages. Media can be sent either by hosting URL or by pre-uploaded Media ID.

---

## Upload Media

Uploads a media file to the WhatsApp servers and returns a reusable Media ID.

### Endpoint

```
POST https://graph.facebook.com/v21.0/{phone-number-id}/media
```

| Header          | Value                       |
|-----------------|-----------------------------|
| `Authorization` | `Bearer {access-token}`     |
| `Content-Type`  | `multipart/form-data`       |

### Request Parameters

| Field                | Type   | Required | Description                                    |
|----------------------|--------|----------|------------------------------------------------|
| `file`               | binary | Yes      | The media file binary data.                    |
| `type`               | string | Yes      | MIME type of the file (e.g., `image/jpeg`).    |
| `messaging_product`  | string | Yes      | Must be `"whatsapp"`.                          |

### Example Request (cURL)

```bash
curl -X POST \
  "https://graph.facebook.com/v21.0/{phone-number-id}/media" \
  -H "Authorization: Bearer {access-token}" \
  -F "file=@/path/to/image.jpg" \
  -F "type=image/jpeg" \
  -F "messaging_product=whatsapp"
```

### Success Response

```json
{
  "id": "MEDIA_ID"
}
```

The returned `id` is valid for 30 days and can be reused across multiple messages.

---

## Retrieve Media URL

Retrieves the download URL for a previously uploaded media asset. This is a two-step process: first get the URL, then download the binary.

### Step 1: Get the Download URL

```
GET https://graph.facebook.com/v21.0/{media-id}
```

| Header          | Value                    |
|-----------------|--------------------------|
| `Authorization` | `Bearer {access-token}`  |

### Success Response

```json
{
  "url": "https://lookaside.fbsbx.com/...",
  "mime_type": "image/jpeg",
  "sha256": "a1b2c3...",
  "file_size": 123456,
  "id": "MEDIA_ID",
  "messaging_product": "whatsapp"
}
```

### Step 2: Download the Binary

```
GET {download-url}
```

| Header          | Value                    |
|-----------------|--------------------------|
| `Authorization` | `Bearer {access-token}`  |

The response body is the raw binary file. The `Content-Type` header indicates the MIME type.

> **Important:** The download URL is temporary and expires. Always retrieve a fresh URL before downloading.

---

## Delete Media

Permanently deletes a media asset from the WhatsApp servers.

### Endpoint

```
DELETE https://graph.facebook.com/v21.0/{media-id}
```

| Header          | Value                    |
|-----------------|--------------------------|
| `Authorization` | `Bearer {access-token}`  |

### Success Response

```json
{
  "success": true
}
```

---

## Supported Formats and Size Limits

| Type              | Supported Formats                         | Max Size |
|-------------------|-------------------------------------------|----------|
| Image             | JPEG, PNG                                 | 5 MB     |
| Video             | MP4, 3GPP                                 | 16 MB    |
| Audio             | AAC, MP4 Audio, MPEG, AMR, OGG (Opus codecs only) | 16 MB    |
| Document          | Any valid MIME type                       | 100 MB   |
| Sticker (static)  | WebP                                      | 100 KB   |
| Sticker (animated)| WebP                                      | 500 KB   |

### Format Notes

- **Video**: Only H.264 video codec and AAC audio codec are supported for MP4.
- **Audio**: OGG files must use Opus codecs specifically; Vorbis is not supported.
- **Sticker**: Must be exactly 512x512 pixels. Static stickers must be under 100 KB, animated under 500 KB.
- **Document**: While any MIME type is accepted, the file must be a valid document. Common types include PDF, DOCX, XLSX, PPTX, and TXT.

---

## Sending Media in Messages

Media can be referenced in outbound messages in two ways: by hosted URL or by pre-uploaded Media ID.

### By Link (Hosted URL)

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "image",
  "image": {
    "link": "https://example.com/photo.jpg",
    "caption": "Check out this image"
  }
}
```

### By Media ID (Pre-uploaded)

```json
{
  "messaging_product": "whatsapp",
  "to": "+18091234567",
  "type": "image",
  "image": {
    "id": "MEDIA_ID",
    "caption": "Check out this image"
  }
}
```

### Comparison: Link vs Media ID

| Aspect           | By Link                                     | By Media ID                                 |
|------------------|---------------------------------------------|---------------------------------------------|
| Setup            | Simpler — just provide a public URL         | Requires a prior upload step                |
| Speed            | Slower — WhatsApp re-downloads each time    | Faster — already cached on WhatsApp servers |
| Reliability      | Depends on URL availability                 | Reliable once uploaded                      |
| Expiration       | URL must remain accessible                  | Media ID valid for 30 days                  |
| Best for         | Quick prototyping, infrequently sent media  | High-volume, repeatedly sent media          |

> **Recommendation:** Use Media ID for any media sent more than once. It avoids redundant downloads and is significantly faster for high-volume messaging.

---

## Media ID Lifecycle

1. **Upload** — Returns a Media ID valid for 30 days.
2. **Use** — Reference the Media ID in as many messages as needed within the 30-day window.
3. **Expiration** — After 30 days the ID becomes invalid. Re-upload the file to get a new ID.
4. **Deletion** — Calling DELETE removes the media immediately, regardless of expiration.

---

## Error Scenarios

| Scenario                          | Error Code | Resolution                                      |
|-----------------------------------|------------|--------------------------------------------------|
| File exceeds size limit           | 100        | Compress or resize the file before uploading.    |
| Unsupported MIME type             | 100        | Convert to a supported format.                   |
| Expired or invalid Media ID      | 100        | Re-upload the file to obtain a new Media ID.     |
| Download URL expired              | 100        | Re-fetch the URL via GET /{media-id}.            |
| Missing `messaging_product` field | 100        | Include `"messaging_product": "whatsapp"`.       |
