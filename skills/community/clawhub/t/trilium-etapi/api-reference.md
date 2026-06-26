# Trilium ETAPI — Full Endpoint Reference

Source: `apps/server/src/assets/etapi.openapi.yaml` (OpenAPI 3.0.3). All paths are prefixed with `/etapi`. Every endpoint requires the `Authorization` header except `/auth/login`.

## Servers

```
http://localhost:37740/etapi   # desktop default
http://localhost:8080/etapi    # self-hosted server default
```

---

## Notes

### `POST /create-note`
Create a note and place it in the tree.

**Request body** (`CreateNoteDef`):
| Field | Required | Notes |
|-------|----------|-------|
| `parentNoteId` | ✓ | Parent noteId (use `"root"` for the tree root) |
| `title` | ✓ | Title |
| `type` | ✓ | `text` / `code` / `file` / `image` / `search` / `book` / `relationMap` / `render` |
| `content` | ✓ | Content string |
| `mime` | code/file/image only | e.g. `application/json`, `image/png` |
| `notePosition` | | Position (step 10); use 5 to be first, 1000000 to be last |
| `prefix` | | Branch-specific title prefix (when the same note is mounted in multiple places) |
| `isExpanded` | | Folder default-expanded state |
| `noteId` | | Force a specific noteId (rarely needed) |
| `branchId` | | Force a specific branchId (rarely needed) |
| `dateCreated` | | Local datetime override |
| `utcDateCreated` | | UTC datetime override |

**Response**: `201 NoteWithBranch` (contains the new `note` and `branch`).

### `GET /notes` — search
**Query params**:
| Name | Required | Notes |
|------|----------|-------|
| `search` | ✓ | Same syntax as the Trilium UI search bar |
| `fastSearch` | | `true` skips content (faster) |
| `includeArchivedNotes` | | Default excludes archived; `true` includes them |
| `ancestorNoteId` | | Restrict to a subtree |
| `ancestorDepth` | | `eq1` / `eq3` / `lt4` / `gt4` etc. |
| `orderBy` | | `title`, `#publicationDate`, `dateCreated`, `dateModified`, `contentSize`, `labelCount`, `relationCount`, ... |
| `orderDirection` | | `asc` (default) / `desc` |
| `limit` | | integer |
| `debug` | | `true` returns query parsing debug info |

**Response 200**: `SearchResponse { results: Note[], debugInfo? }`.

**Search syntax examples**:
- `tolkien` — fuzzy fulltext
- `"Two Towers"` — exact phrase
- `tolkien #book` — keyword + label
- `#book and #author=Tolkien`
- `note.content *= "magic"`
- `~author.title = "Tolkien"` (attribute on a relation target)

### `GET /notes/{noteId}`
Returns note metadata (`Note`, no content).

### `PATCH /notes/{noteId}`
Patches `title`, `type`, `mime`, `dateCreated`, `utcDateCreated` only. Use the content endpoint below to change content. Body is a partial `Note`. Response 200 = updated `Note`.

### `DELETE /notes/{noteId}`
Deletes the note. Response 204.

### `GET /notes/{noteId}/content`
Returns a `text/html` string (or raw bytes for code/file/image).

### `PUT /notes/{noteId}/content`
**Body**: `text/plain` (even if the content is HTML, use `text/plain` content-type). Response 204.

### `GET /notes/{noteId}/export?format=html|markdown`
Returns a ZIP (`application/zip`). Use `noteId=root` to export the whole document.

### `POST /notes/{noteId}/import`
Imports a ZIP into the given note. Response 201 = `NoteWithBranch`.

### `POST /notes/{noteId}/revision?format=html|markdown`
Creates a revision snapshot of the note. Response 204.

---

## Branches

A branch is the parent-child relationship. The same `noteId` can have multiple branches (cloning).

### `POST /branches`
Create or update a branch. If the parent-child branch already exists, this updates its `prefix` / `notePosition` / `isExpanded`.

**Body** (`Branch`):
- `noteId` (child)
- `parentNoteId`
- `prefix` (optional)
- `notePosition` (optional)
- `isExpanded` (optional)

**Responses**:
- `200 Branch` — already existed, was updated
- `201 Branch` — newly created

### `GET /branches/{branchId}`
Returns the `Branch`.

### `PATCH /branches/{branchId}`
**Patches `prefix` and `notePosition` only.** Re-parenting requires DELETE + POST a new branch.

### `DELETE /branches/{branchId}`
**Warning**: if this is the last branch of the (child) note, the note is deleted too. Response 204.

---

## Attributes (labels & relations)

### `POST /attributes`
Create a single attribute.

**Body** (`Attribute`):
| Field | Notes |
|-------|-------|
| `noteId` | Note to attach to |
| `type` | `label` or `relation` |
| `name` | Attribute name (`^[^\s]+`, no whitespace) |
| `value` | label: any string; relation: target noteId |
| `position` | int |
| `isInheritable` | bool; if true, descendants inherit it |

**Response 201**: `Attribute` (with `attributeId`).

### `GET /attributes/{attributeId}`
Returns the `Attribute`.

### `PATCH /attributes/{attributeId}`
- label: `value`, `position` only
- relation: `position` only
- Anything else → delete + recreate.

### `DELETE /attributes/{attributeId}`
Response 204.

---

## Attachments

Attachments hang off a Note or a Revision (the `ownerId` field).

### `POST /attachments`
**Body** (`CreateAttachment`):
| Field | Notes |
|-------|-------|
| `ownerId` | Owning noteId or revisionId |
| `role` | Purpose string, e.g. `image`, `file` |
| `mime` | MIME type |
| `title` | Display name |
| `content` | Content |
| `position` | int |

**Response 201**: `Attachment`.

### `GET /attachments/{attachmentId}`
Returns attachment metadata (no content). Includes `contentLength`, `blobId`, etc.

### `PATCH /attachments/{attachmentId}`
**Patches `role`, `mime`, `title`, `position` only.**

### `DELETE /attachments/{attachmentId}`
Response 204.

### `GET /attachments/{attachmentId}/content`
Returns raw content.

### `PUT /attachments/{attachmentId}/content`
**Body**: `text/plain`. Response 204.

---

## Calendar / Inbox

These GETs auto-create on demand: the first hit for a given day/week/month/year creates the corresponding note.

| Endpoint | Path param | Notes |
|----------|-----------|-------|
| `GET /inbox/{date}` | `YYYY-MM-DD` | Inbox (the note tagged `#inbox`, or that date's day note) |
| `GET /calendar/days/{date}` | `YYYY-MM-DD` | Day note |
| `GET /calendar/weeks/{date}` | `YYYY-MM-DD` | Monday-of-week note for that date |
| `GET /calendar/months/{month}` | `YYYY-MM` | Month note |
| `GET /calendar/years/{year}` | `YYYY-MM` (the spec keeps this pattern) | Year note |

All return `Note`.

---

## Misc

### `POST /refresh-note-ordering/{parentNoteId}`
Call after bulk-updating `branch.notePosition` so connected clients receive the new ordering immediately. Response 204.

### `POST /auth/login`
**No token required.** Body: `{"password": "..."}`. Response 201: `{"authToken": "..."}`. Repeated failures → 429.

### `POST /auth/logout`
Invalidates the current token. Response 204.

### `GET /app-info`
Returns `AppInfo`:
- `appVersion` (e.g. `0.50.2`)
- `dbVersion` (int)
- `syncVersion` (int)
- `buildDate`, `buildRevision`
- `dataDirectory`
- `clipperProtocolVersion`
- `utcDateTime`

Useful as a health/version check.

### `PUT /backup/{backupName}`
The name becomes `backup-<name>.db`, written to the server's `dataDirectory/backup/`. `backupName` matches `[a-zA-Z0-9_]{1,32}`. Response 204.

---

## Schemas

### `EntityId`
`[a-zA-Z0-9_]{4,32}`, e.g. `evnnmvHTCgIn`. Special value: `root` (tree root).

### `LocalDateTime`
`YYYY-MM-DD HH:MM:SS.mmm±ZZZZ`, e.g. `2021-12-31 20:18:11.930+0100`.

### `UtcDateTime`
`YYYY-MM-DD HH:MM:SS.mmmZ`, e.g. `2021-12-31 19:18:11.930Z`.

### `Note`
| Field | RW | Notes |
|-------|----|-------|
| `noteId` | RO | |
| `title` | RW | |
| `type` | RW | `text` / `code` / `render` / `file` / `image` / `search` / `relationMap` / `book` / `noteMap` / `mermaid` / `webView` / `shortcut` / `doc` / `contentWidget` / `launcher` |
| `mime` | RW | |
| `isProtected` | RO | |
| `blobId` | RO | content hash ID |
| `attributes` | RO | `Attribute[]` |
| `parentNoteIds` | RO | |
| `childNoteIds` | RO | |
| `parentBranchIds` | RO | |
| `childBranchIds` | RO | |
| `dateCreated` / `utcDateCreated` | RW | LocalDateTime / UtcDateTime |
| `dateModified` / `utcDateModified` | RO | |

### `Branch`
| Field | RW |
|-------|----|
| `branchId` | RW |
| `noteId` (child) | RO |
| `parentNoteId` | RO |
| `prefix` | RW |
| `notePosition` | RW (int32) |
| `isExpanded` | RW |
| `utcDateModified` | RO |

### `Attribute`
| Field | Notes |
|-------|-------|
| `attributeId` | |
| `noteId` (RO) | |
| `type` | `label` / `relation` |
| `name` | `^[^\s]+` |
| `value` | label: any string; relation: target noteId |
| `position` | int32 |
| `isInheritable` | bool |
| `utcDateModified` | RO |

### `Attachment`
| Field | Notes |
|-------|-------|
| `attachmentId` (RO) | |
| `ownerId` | noteId or revisionId |
| `role` | |
| `mime` | |
| `title` | |
| `position` | int32 |
| `blobId` | content hash |
| `dateModified` / `utcDateModified` (RO) | |
| `utcDateScheduledForErasureSince` (RO) | soft-delete timestamp |
| `contentLength` | int32 |

### `Error`
All error responses:
```json
{
  "status": 400,
  "code": "NOTE_IS_PROTECTED",
  "message": "Note 'evnnmvHTCgIn' is protected and cannot be modified through ETAPI"
}
```
`code` is a stable string constant — branch on it programmatically.

---

## HTTP Status Cheatsheet

| Code | Meaning |
|------|---------|
| 200 | OK (GET / PATCH) |
| 201 | Created (POST resource) |
| 204 | No Content (DELETE / PUT content / backup / refresh-ordering) |
| 400 / 401 / 403 / 404 | Error, body is `Error` |
| 429 | `/auth/login` rate-limited |
