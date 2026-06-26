# Microsoft Graph OneDrive — Full API Reference

All paths are relative to `https://graph.microsoft.com/v1.0` unless noted. Send `Authorization: Bearer <access_token>` on every request.

> The `v1.0` endpoint is the stable production API. Some advanced features (richer permissions, retention labels, large-list pagination tweaks) live at `https://graph.microsoft.com/beta`. The auth and tokens are identical.

---

## Common addressing

### Drive prefixes

| Prefix | Meaning |
|--------|---------|
| `/me/drive` | Current user's default drive |
| `/drives/{drive-id}` | Any drive by ID |
| `/users/{user-id}/drive` | Another user's drive (needs `Files.Read.All`) |
| `/groups/{group-id}/drive` | A Microsoft 365 group's drive |
| `/sites/{site-id}/drive` | Default doc library of a SharePoint site |
| `/sites/{site-id}/drives/{drive-id}` | A specific doc library on a site |

All of the operations below work under any of these prefixes — just replace `/me/drive` with the prefix that targets the drive you want.

### Item addressing

```
By ID    → /me/drive/items/{item-id}
By path  → /me/drive/root:/path/to/file.ext
Root     → /me/drive/root
Special  → /me/drive/special/{name}     ; name ∈ {documents, photos, cameraroll, approot, music}
Hybrid   → /me/drive/items/{id}:/relative/path
```

The colon (`:`) marks the boundary between the addressing and the action. Examples:

- List children of a folder by path: `/me/drive/root:/Documents:/children`
- Get content of a file by path: `/me/drive/root:/Documents/file.txt:/content`

Special characters in paths must be percent-encoded (`#` → `%23`, `?` → `%3F`).

---

## Drives

### Get default drive

```
GET /me/drive
```

Response (truncated):

```json
{
  "id": "...",
  "driveType": "personal",
  "owner": { "user": { "displayName": "Jane Doe", "email": "jane@example.com" } },
  "quota": { "total": 5368709120, "used": 1024, "remaining": 5368708096, "state": "normal" }
}
```

`driveType` is one of: `personal`, `business`, `documentLibrary`.

### List drives the user can access

```
GET /me/drives
```

### Get specific drive

```
GET /drives/{drive-id}
```

---

## DriveItem (files & folders)

The DriveItem resource represents everything: files, folders, and special folders. Key properties:

- `id` — stable per drive
- `name` — leaf filename
- `size` — bytes
- `folder` (object) — present if folder; contains `childCount`
- `file` (object) — present if file; contains `mimeType`, `hashes`
- `parentReference` — `{driveId, id, path, name}`
- `createdDateTime`, `lastModifiedDateTime`
- `createdBy`, `lastModifiedBy`
- `webUrl` — UI link
- `@microsoft.graph.downloadUrl` — short-lived direct download URL (file only)

### Get item

```
GET /me/drive/root                              # root folder
GET /me/drive/items/{item-id}
GET /me/drive/root:/Documents/file.txt
```

### List children

```
GET /me/drive/items/{folder-id}/children
GET /me/drive/root/children
GET /me/drive/root:/Documents:/children
```

Useful query parameters: `$top`, `$select`, `$expand`, `$orderby`, `$filter`.

### Create folder

```
POST /me/drive/items/{parent-id}/children
Content-Type: application/json

{
  "name": "Reports",
  "folder": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

To create under root: `POST /me/drive/root/children`.

### Update metadata (rename, move, set facets)

```
PATCH /me/drive/items/{item-id}
Content-Type: application/json

{
  "name": "renamed.docx",
  "parentReference": { "id": "{new-parent-folder-id}" }
}
```

Including both `name` and `parentReference` does a single rename+move atomically.

### Copy

```
POST /me/drive/items/{item-id}/copy
Content-Type: application/json

{
  "parentReference": { "driveId": "...", "id": "{dest-folder-id}" },
  "name": "copy-of-thing.pdf"
}
```

Copies are asynchronous. Response is `202 Accepted` with a `Location` header pointing at a monitor URL:

```
GET <monitor-url>
→ { "operation": "ItemCopy", "percentageComplete": 100.0, "status": "completed", "resourceId": "{new-item-id}" }
```

### Delete

```
DELETE /me/drive/items/{item-id}
→ 204 No Content
```

Goes to the user's recycle bin. Not recoverable via v1.0 Graph for personal accounts — the user must visit onedrive.live.com → Recycle bin.

### Search

```
GET /me/drive/search(q='budget')
GET /me/drive/root/search(q='*.xlsx')
GET /me/drive/items/{folder-id}/search(q='draft')   # scoped to a subtree
```

Returns DriveItem array. Searches over filename, content (for indexed types), and metadata.

### Recent / shared with me

```
GET /me/drive/recent
GET /me/drive/sharedWithMe
```

`sharedWithMe` returns `remoteItem` references — to do anything with them, follow `remoteItem.parentReference.driveId` + `remoteItem.id`:

```
GET /drives/{remoteItem.parentReference.driveId}/items/{remoteItem.id}
```

### Special folders

```
GET /me/drive/special/documents
GET /me/drive/special/photos
GET /me/drive/special/cameraroll
GET /me/drive/special/approot
GET /me/drive/special/music
```

These are locale-independent. `approot` is unique per app registration — a sandboxed folder.

---

## Upload

### Simple (≤ 4 MiB)

```
PUT /me/drive/root:/path/to/file.ext:/content
Content-Type: <mime-type or application/octet-stream>
Body: <raw bytes>
```

Optional query/header:

- `?@microsoft.graph.conflictBehavior=rename|replace|fail`

### Create-from-children (empty file or with content)

```
POST /me/drive/items/{parent-id}/children
Content-Type: application/json

{
  "name": "new.txt",
  "file": {},
  "@microsoft.graph.conflictBehavior": "rename"
}
```

Then PUT to `/me/drive/items/{new-id}/content` to set bytes.

### Resumable upload (> 4 MiB, recommended for anything > 4 MiB)

**Step 1 — create session:**

```
POST /me/drive/root:/big-video.mp4:/createUploadSession
Content-Type: application/json

{
  "item": {
    "@microsoft.graph.conflictBehavior": "rename",
    "name": "big-video.mp4"
  },
  "deferCommit": false
}
```

Response:

```json
{
  "uploadUrl": "https://api.onedrive.com/rup/...",
  "expirationDateTime": "2026-05-19T11:00:00Z",
  "nextExpectedRanges": ["0-"]
}
```

**Step 2 — upload chunks:**

```
PUT <uploadUrl>
Content-Length: <chunk-size>
Content-Range: bytes {start}-{end}/{total}
Body: <chunk bytes>
```

Rules:

- Chunk size must be a multiple of **320 KiB** (320 × 1024 = 327680 bytes), except the final chunk.
- Recommended chunk size: **5–10 MiB**.
- Send chunks sequentially (parallel is not supported).
- The `uploadUrl` is pre-authenticated — do **not** send the `Authorization` header on the PUTs.

**Step 3 — final chunk** returns the completed DriveItem (HTTP 200 or 201).

If a chunk fails or you need to resume:

```
GET <uploadUrl>
→ { "expirationDateTime": "...", "nextExpectedRanges": ["12345678-"] }
```

Then continue from `nextExpectedRanges[0].start`.

**Cancel an upload session:** `DELETE <uploadUrl>`.

---

## Download

The most reliable pattern is to first GET the item metadata and follow `@microsoft.graph.downloadUrl`:

```
GET /me/drive/items/{id}?$select=id,name,@microsoft.graph.downloadUrl

→ { "name": "...", "@microsoft.graph.downloadUrl": "https://...-1drv.com/..." }
```

That URL is pre-authenticated (no auth header needed), valid for a few minutes. Stream it.

Alternative one-shot endpoint:

```
GET /me/drive/items/{id}/content
→ 302 redirect to a downloadUrl
```

Use `curl -L` to follow the redirect. Some clients have trouble with the redirect — the metadata→downloadUrl pattern is more robust.

---

## Sharing

### Create a sharing link

```
POST /me/drive/items/{id}/createLink
Content-Type: application/json

{
  "type": "view",          // view | edit | embed | block-download
  "scope": "anonymous",    // anonymous | organization | users
  "password": "optional",
  "expirationDateTime": "2026-12-31T00:00:00Z",
  "retainInheritedPermissions": true
}
```

Calling `createLink` multiple times with the same `type`+`scope` returns the **same** link object — sharing links are idempotent per item/type/scope tuple.

### Invite specific users

```
POST /me/drive/items/{id}/invite
Content-Type: application/json

{
  "recipients": [{ "email": "alice@example.com" }, { "email": "bob@example.com" }],
  "roles": ["read"],          // read | write
  "requireSignIn": true,
  "sendInvitation": true,
  "message": "Have a look!",
  "expirationDateTime": "2026-12-31T00:00:00Z",
  "password": "secret"
}
```

Response is an array of created `permission` objects.

### List permissions

```
GET /me/drive/items/{id}/permissions
```

Each permission has:

- `id`
- `roles` — `["read"]` / `["write"]` / `["owner"]`
- `grantedToV2` — `{user, group, application, device}`
- `link` — present for sharing-link permissions: `{type, scope, webUrl, preventsDownload}`
- `invitation` — present for outstanding email invitations
- `expirationDateTime`, `hasPassword`, `inheritedFrom`

### Update a permission

```
PATCH /me/drive/items/{id}/permissions/{perm-id}
Content-Type: application/json

{
  "roles": ["write"],
  "expirationDateTime": "2027-01-01T00:00:00Z"
}
```

### Revoke a permission

```
DELETE /me/drive/items/{id}/permissions/{perm-id}
→ 204
```

Revoking a sharing-link permission invalidates the link for everyone.

### Resolve a sharing URL to a DriveItem

```
GET /shares/{share-id}/driveItem
```

`{share-id}` is `u!` + base64url(URL) **without padding**:

```python
import base64
b = base64.urlsafe_b64encode(url.encode()).rstrip(b'=').decode()
share_id = "u!" + b
```

Or, in bash:

```bash
SHARE_ID="u!$(echo -n "$URL" | base64 -w0 | tr '+/' '-_' | tr -d '=')"
```

You can also access:

- `/shares/{share-id}/root` — the root of the shared content
- `/shares/{share-id}/items/{item-id}` — by ID within the share

This is how `1drv.ms/...` and SharePoint share URLs are resolved.

---

## Versions

```
GET   /me/drive/items/{id}/versions
GET   /me/drive/items/{id}/versions/{version-id}              # metadata
GET   /me/drive/items/{id}/versions/{version-id}/content      # download a previous version
POST  /me/drive/items/{id}/versions/{version-id}/restoreVersion
```

Versions are kept for 30 days (personal) / per retention policy (business).

---

## Thumbnails

```
GET /me/drive/items/{id}/thumbnails
GET /me/drive/items/{id}/thumbnails/0/{size}
GET /me/drive/items/{id}/thumbnails/0/{size}/content   # 302 → image bytes
```

Sizes: `small` (≤96 px), `medium` (≤176 px), `large` (≤800 px), or a custom dimension like `c1000x1000` / `c500x500_crop`.

---

## Preview

```
POST /me/drive/items/{id}/preview
Content-Type: application/json
{ "page": "1", "zoom": 90 }

→ { "getUrl": "...", "postUrl": "...", "postParameters": "..." }
```

`getUrl` is an iframe-ready embed URL.

---

## Delta (change feed)

```
GET /me/drive/root/delta                          # initial snapshot
GET /me/drive/root/delta?token={prev-token}       # incremental
GET /me/drive/items/{folder-id}/delta             # scoped to a subtree
```

Responses:

- `value[]` — list of changed DriveItems. A `deleted` facet indicates removal.
- `@odata.nextLink` — more pages of the current sync.
- `@odata.deltaLink` — when the sync is complete; contains the next sync token.

Save the `token=` parameter from `@odata.deltaLink` and pass it back on the next call to fetch only changes since then.

---

## Activities

```
GET /me/drive/activities                          # tenant-wide (business)
GET /me/drive/items/{id}/activities               # per-item
```

Returns an `itemActivity` array with `action.create/edit/delete/rename/move/share/...` facets.

---

## Workbook (Excel) — quick pointers

If the DriveItem is an `.xlsx`:

```
GET   /me/drive/items/{id}/workbook/worksheets
GET   /me/drive/items/{id}/workbook/worksheets/Sheet1/range(address='A1:D10')
POST  /me/drive/items/{id}/workbook/createSession           # for transactional edits
PATCH /me/drive/items/{id}/workbook/worksheets/Sheet1/range(address='A1:D10')/values
```

Workbook calls accept a `workbook-session-id` header for ACID-like transactional editing.

---

## OData query parameters

| Param | Example | Notes |
|-------|---------|-------|
| `$select` | `?$select=id,name,size,folder` | Project specific fields — reduces payload size |
| `$expand` | `?$expand=children($top=10)` | Inline related resources |
| `$filter` | `?$filter=file ne null` | OData filter expressions |
| `$orderby` | `?$orderby=lastModifiedDateTime desc` | Sort |
| `$top` | `?$top=200` | Page size — max 200 for `children` |
| `$skip` | `?$skip=100` | Offset (rarely needed — prefer `@odata.nextLink`) |
| `$count` | `?$count=true` | Returns total alongside results |
| `$search` | `?$search="budget"` | Full-text — only on some endpoints |

URL encoding tip: `$` does not need to be encoded, but `,` inside `$select` does not need it either. Quotes do (`%22`).

### Pagination

```
GET /me/drive/root/children?$top=100
→ {
    "value": [ ... 100 items ... ],
    "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/drive/root/children?$top=100&$skiptoken=..."
  }
```

Follow `@odata.nextLink` blindly — it already encodes everything needed.

---

## Conflict behavior

When creating/uploading items, set `@microsoft.graph.conflictBehavior`:

- `fail` (default) — 409 if an item with that name exists.
- `replace` — overwrite existing item content (same ID).
- `rename` — append ` (1)`, ` (2)`, … to the new item's name.

Pass it in:

- The JSON body for `POST .../children`, `POST .../copy`, `POST .../createUploadSession`.
- The query string for `PUT .../content?@microsoft.graph.conflictBehavior=replace`.

---

## Throttling

OneDrive / Graph applies per-app and per-user throttling. When throttled:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

Pause for `Retry-After` seconds (default several hundred ms if missing) and retry. Backoff exponentially on repeated 429s.

Use `$select` to minimize response sizes and batch unrelated calls with the [JSON batch endpoint](https://learn.microsoft.com/en-us/graph/json-batching):

```
POST https://graph.microsoft.com/v1.0/$batch
Content-Type: application/json

{
  "requests": [
    { "id": "1", "method": "GET", "url": "/me/drive/root/children?$top=50" },
    { "id": "2", "method": "GET", "url": "/me/drive/recent?$top=10" }
  ]
}
```

Up to 20 requests per batch.

---

## Errors

Standard shape:

```json
{
  "error": {
    "code": "itemNotFound",
    "message": "The resource could not be found.",
    "innerError": {
      "date": "2026-05-19T10:11:12",
      "request-id": "abcd-1234",
      "client-request-id": "..."
    }
  }
}
```

Common codes: `accessDenied`, `activityLimitReached`, `generalException`, `invalidRequest`, `invalidRange`, `itemNotFound`, `malwareDetected`, `nameAlreadyExists`, `notAllowed`, `notSupported`, `resourceModified`, `resyncRequired`, `serviceNotAvailable`, `quotaLimitReached`, `unauthenticated`.

For `resyncRequired` (from `/delta`): drop your delta token and start a fresh full sync.
