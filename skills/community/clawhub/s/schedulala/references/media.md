# Media reference — how files get into posts

Every post's media is a `mediaItems` array of `{ type, url, caption? }` where
`type` is `image` (default), `video`, or `pdf` (LinkedIn documents only) and
`url` must be publicly reachable. Multiple items = carousel (instagram,
facebook, threads, tiktok, pinterest; mastodon up to 4 images).

Pick the path by where the file lives:

## 1. User's device or chat attachment → `attach_media`

**ALWAYS** use `attach_media` when the user wants to post a photo, video, or
PDF from their device or attached in the chat. What happens next depends on
your client:

- **Widget-capable clients (claude.ai):** it opens an upload widget (drop
  zone) IN the conversation — drag-and-drop or file picker, multiple files at
  once for carousels. The file goes browser → S3 through a ticket-authenticated
  presigned upload; the bytes never touch the model or the MCP transport, so
  quality is preserved end-to-end. Never tell the user the widget doesn't
  exist there.
- **No widget rendering (Cursor, self-hosted agents, custom clients):** the
  tool still works — its result carries a complete programmatic upload API in
  `structuredContent`. Drive it yourself; see "The programmatic path" below.
  Never claim a widget rendered if your client shows no widgets.

- Limits: images to 20MB (GIF 15MB), videos to 500MB, PDFs to 100MB.
- When the upload finishes, the media's url and type arrive ready for
  `create_post`'s `mediaItems` (widget path pushes them into your context;
  they're also visible via `list_media`).
- A PDF becomes `type: "pdf"` — LinkedIn document posts only.
- For an Instagram Reel, also set `platformSettings.instagram.postType: "reel"`.
- **NEVER read and base64-encode an attached file yourself.** Chat channels
  truncate large payloads, forcing destructive compression (a 6MB photo
  becomes a 6KB thumbnail).

### The programmatic path (no widget)

`attach_media`'s `structuredContent` contains `ticket` (a 15-minute
single-purpose auth token), `presignUrl`, `confirmUrl`, `maxBytes`, and
`acceptedTypes`. Three plain-HTTP steps (CORS-open, no API key needed — the
ticket is the auth):

1. **Presign** — `POST` to `presignUrl` with JSON
   `{ ticket, fileName, mimeType, sizeBytes }` (all four required) →
   `{ media: { id, uploadUrl, fallbackUploadUrl?, method: "PUT", headers, publicUrl, expiresIn } }`
2. **Upload** — HTTP `PUT` the raw file bytes to `uploadUrl` with header
   `Content-Type` set to the EXACT `mimeType` you presigned (a mismatch
   breaks the S3 signature). If the PUT fails and `fallbackUploadUrl` is
   present, retry against it.
3. **Confirm** — `POST` to `confirmUrl` with JSON `{ ticket, id }` →
   `{ media: { id, url, type, mimeType, sizeBytes, fileName, status: "ready" } }`.
   A 409 means the PUT hasn't settled in storage yet — retry the confirm.
   The returned `type` (`image` / `video` / `pdf`) is exactly what
   `create_post`'s `mediaItems` wants.

If your client exposes no `structuredContent` at all, fall back to
`upload_media` (public URLs) or the chunked upload in §3 (generated images) —
or have the user upload once on the dashboard Media page
(https://schedulala.com/dashboard) and find it with `list_media`.

## 2. Public http(s) URL → `upload_media` (mode: url)

The server downloads and re-hosts the file on Schedulala's CDN, returning a
stable url + media id. Use for web images, expiring links, or generated-image
URLs.

- Images up to 20MB (jpeg, png, webp); gif up to 15MB.
- Videos up to 50MB (mp4, mov, webm). **Videos larger than 50MB: skip
  upload_media entirely and pass the public URL directly in `mediaItems`** —
  media is fetched at publish time.
- Re-hosted media expires after 30 days if unused.
- The real file type is detected from the bytes; `type` is only a hint.
- `altText` is stored with the media (recommended for images).

## 3. Image YOU generated in this conversation → chunked upload

For charts, quote cards, or edited images the model created itself, whose
base64 is too large for one tool call (~8000+ chars):

1. `begin_generated_media_upload` (`mimeType` required, e.g. `image/png`) →
   returns `uploadId`.
2. `append_generated_media_chunk` repeatedly: sequential `seq` starting at 0,
   **at most 8000 base64 characters per chunk** (larger payloads are silently
   truncated by the chat channel). On a 409 conflict, resume from the
   `expectedSeq` in the error details. On a 429, wait briefly and resend the
   SAME seq.
3. `finish_generated_media_upload` → server assembles, validates, hosts;
   returns url + media id.

Rules: **images only, 3MB decoded max, session expires in 30 minutes.** NEVER
use this flow for user-attached files or files on the user's device — those go
through `attach_media`. Tiny generated images (base64 under ~8000 chars) can
use `upload_media` mode `data` (with `mimeType`) in a single call instead.

## 4. Already uploaded → `list_media`

When the user references media they've already uploaded — "my latest upload",
"the video I uploaded", "that reel from earlier" — call `list_media` (filter
by `type`) instead of asking for a URL. This is THE path for posting big
videos from chat.

## CLI

`schedulala post "…" --media "https://…/a.jpg,https://…/b.mp4"` — comma list
of public URLs; type inferred from extension (mp4/mov/webm/m4v/avi = video,
else image).

## Platform media requirements (quick recall)

- instagram: ≥1 media item required; reel needs `postType: "reel"`.
- youtube: video required.
- google-business: exactly one image, no video.
- linkedin pdf: `type: "pdf"` + `platformSettings.linkedin.documentTitle`.
- Thread entries (`create_thread`): max 1 media item per entry.
