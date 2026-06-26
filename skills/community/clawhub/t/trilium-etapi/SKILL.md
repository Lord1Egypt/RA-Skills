---
name: trilium-etapi
description: Use when interacting with a Trilium Notes server via the ETAPI REST API - creating, reading, updating, searching, or deleting notes, branches, attributes, attachments, day/week/month notes; obtaining auth tokens; or scripting Trilium operations from the shell. Triggers on mentions of Trilium, ETAPI, noteId, branchId, or any /etapi/ URL.
---

# Trilium ETAPI

## Overview

ETAPI is the external REST API for Trilium Notes (Trilium ≥ 0.50). All requests require token auth. Resources are addressed by 12-char IDs: `noteId`, `branchId`, `attributeId`, `attachmentId`.

**Core concepts:**
- **Note** — a content unit (HTML/code/file/image/...), identified by `noteId`
- **Branch** — the parent-child relationship between two notes (the same note can be cloned under multiple parents)
- **Attribute** — a label or relation attached to a note
- **Attachment** — a binary or text payload owned by a note

## When to Use

- Bulk-create or import notes via script (daily notes, inbox, capture)
- Push content into Trilium from external systems (RSS, email, webhooks)
- Search/export Trilium content for consumption by other tools
- Trigger server-side database backups, export subtrees
- Debug ETAPI integrations (clients like trilium-py / trilium-client just wrap this API)

**Do not use** for scripts running *inside* Trilium — use the frontend/backend Script API directly, no HTTP needed.

## Setup

All examples below assume:

```bash
export TRILIUM_URL="http://localhost:8080"   # no trailing /etapi
export TRILIUM_TOKEN="<generate via Trilium → Options → ETAPI>"
```

If you only have a password (and the server allows password login), exchange it for a token:

```bash
curl -sX POST "$TRILIUM_URL/etapi/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"password":"YOUR_PASSWORD"}' | jq -r .authToken
```

**Three auth styles** (pick one, in the `Authorization` header):
1. `Authorization: $TRILIUM_TOKEN` — raw token (works on every version)
2. `Authorization: Bearer $TRILIUM_TOKEN` — Bearer form (v0.93+)
3. `Authorization: Basic $(echo -n "etapi:$TRILIUM_TOKEN" | base64)` — Basic auth (v0.56+)

## Quick Reference

| Operation | Method | Path |
|-----------|--------|------|
| Health / version | GET | `/etapi/app-info` |
| Search notes | GET | `/etapi/notes?search=...` |
| Read note metadata | GET | `/etapi/notes/{noteId}` |
| Read note content | GET | `/etapi/notes/{noteId}/content` |
| Write note content | PUT | `/etapi/notes/{noteId}/content` (text/plain) |
| Create note | POST | `/etapi/create-note` |
| Patch note metadata | PATCH | `/etapi/notes/{noteId}` |
| Delete note | DELETE | `/etapi/notes/{noteId}` |
| Export subtree as ZIP | GET | `/etapi/notes/{noteId}/export?format=html\|markdown` |
| Import ZIP | POST | `/etapi/notes/{noteId}/import` |
| Create / move branch | POST | `/etapi/branches` |
| Create attribute | POST | `/etapi/attributes` |
| Create attachment | POST | `/etapi/attachments` |
| Day note (auto-create) | GET | `/etapi/calendar/days/{YYYY-MM-DD}` |
| Inbox | GET | `/etapi/inbox/{YYYY-MM-DD}` |
| Trigger DB backup | PUT | `/etapi/backup/{name}` |

Full endpoint, parameter, and schema reference: [api-reference.md](api-reference.md).

## Core Patterns (curl + jq)

All snippets below assume `TRILIUM_URL` and `TRILIUM_TOKEN` are exported.

### 1. Health check

```bash
curl -s "$TRILIUM_URL/etapi/app-info" -H "Authorization: $TRILIUM_TOKEN" | jq
```

### 2. Create a text note

```bash
curl -sX POST "$TRILIUM_URL/etapi/create-note" \
  -H "Authorization: $TRILIUM_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "parentNoteId": "root",
    "title": "Hello from ETAPI",
    "type": "text",
    "content": "<p>Created via curl</p>"
  }' | jq '{noteId: .note.noteId, branchId: .branch.branchId}'
```

Returns `NoteWithBranch`: the new `note` plus the `branch` mounting it.

### 3. Replace note content

Content lives on a separate endpoint and the body is `text/plain` **even when the content is HTML**:

```bash
curl -sX PUT "$TRILIUM_URL/etapi/notes/$NOTE_ID/content" \
  -H "Authorization: $TRILIUM_TOKEN" \
  -H 'Content-Type: text/plain' \
  --data-binary @body.html
```

### 4. Search

```bash
# fulltext + label
curl -sG "$TRILIUM_URL/etapi/notes" \
  -H "Authorization: $TRILIUM_TOKEN" \
  --data-urlencode 'search=tolkien #book' \
  --data-urlencode 'limit=10' | jq '.results[] | {noteId, title}'
```

Search syntax matches the Trilium UI search bar. Common forms: `#tag`, `#tag=value`, `note.content *= "..."`, `~relation.title = "..."`.

### 5. Tag a note

```bash
curl -sX POST "$TRILIUM_URL/etapi/attributes" \
  -H "Authorization: $TRILIUM_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"noteId\": \"$NOTE_ID\",
    \"type\": \"label\",
    \"name\": \"book\",
    \"value\": \"\",
    \"isInheritable\": false
  }"
```

### 6. Day note (auto-created on demand)

```bash
TODAY=$(date +%F)
curl -s "$TRILIUM_URL/etapi/calendar/days/$TODAY" \
  -H "Authorization: $TRILIUM_TOKEN" | jq -r .noteId
```

### 7. Clone a note to another location (branch)

```bash
curl -sX POST "$TRILIUM_URL/etapi/branches" \
  -H "Authorization: $TRILIUM_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{
    \"noteId\": \"$CHILD_ID\",
    \"parentNoteId\": \"$NEW_PARENT_ID\",
    \"prefix\": \"\",
    \"notePosition\": 100,
    \"isExpanded\": false
  }"
```

### 8. Export a subtree as ZIP

```bash
curl -s "$TRILIUM_URL/etapi/notes/$NOTE_ID/export?format=markdown" \
  -H "Authorization: $TRILIUM_TOKEN" -o subtree.zip
# Whole document: use noteId="root"
```

### 9. Trigger a server-side backup

```bash
curl -sX PUT "$TRILIUM_URL/etapi/backup/now" \
  -H "Authorization: $TRILIUM_TOKEN"
# Writes to dataDirectory/backup/backup-now.db
```

## Common Pitfalls

- **Don't add a `Bearer` prefix to `Authorization`** unless you're on v0.93+ and explicitly want Bearer. The raw token form works on every version.
- **`PUT /notes/{id}/content` body is `text/plain`** (NOT `text/html`). The OpenAPI spec is explicit on this.
- **`PATCH /notes/{id}` only patches a subset**: `title`, `type`, `mime`, `dateCreated`, `utcDateCreated`. Use `PUT .../content` to change content.
- **`PATCH /branches/{id}` only patches `prefix` and `notePosition`**. To re-parent a note you must DELETE the branch and POST a new one.
- **`PATCH /attributes/{id}`**: labels can only patch `value` and `position`; relations can only patch `position`. Anything else means delete + recreate.
- **Deleting the last branch of a note also deletes the note.** Watch out when DELETE-ing branches.
- **`notePosition` defaults to step 10** (10/20/30...). To insert in front, use 5; to push to the end, use a large value like 1000000. After bulk reorders, call `POST /refresh-note-ordering/{parentNoteId}` so connected clients refresh.
- **EntityId pattern is `[a-zA-Z0-9_]{4,32}`.** `root` is the special root noteId.
- **Error responses are always `{status, code, message}`.** Branch on the stable `code` constant (e.g. `NOTE_IS_PROTECTED`), not on the human-readable message.
- **`/auth/login` is rate-limited.** Too many failures returns 429 and temporarily blacklists the client IP.

## Note Types

| type | Use | mime required? |
|------|-----|----------------|
| `text` | Rich text (HTML) | no |
| `code` | Source code | yes (e.g. `text/x-python`) |
| `file` | Binary file | yes |
| `image` | Image | yes (e.g. `image/png`) |
| `search` | Saved search | no |
| `book` | Folder-style container | no |
| `relationMap` | Relation map | no |
| `render` | Custom renderer | no |

You may also see these on read: `noteMap`, `mermaid`, `webView`, `shortcut`, `doc`, `contentWidget`, `launcher`.

## Workflow: Append to today's day note

A typical inbox / capture flow — append arbitrary text to today's day note:

```bash
TODAY=$(date +%F)
NOTE_ID=$(curl -s "$TRILIUM_URL/etapi/calendar/days/$TODAY" \
  -H "Authorization: $TRILIUM_TOKEN" | jq -r .noteId)

OLD=$(curl -s "$TRILIUM_URL/etapi/notes/$NOTE_ID/content" \
  -H "Authorization: $TRILIUM_TOKEN")

NEW="${OLD}<p>$(date +%H:%M) — $1</p>"

curl -sX PUT "$TRILIUM_URL/etapi/notes/$NOTE_ID/content" \
  -H "Authorization: $TRILIUM_TOKEN" \
  -H 'Content-Type: text/plain' \
  --data-binary "$NEW"
```

## When You Need More

- Full endpoint, parameter, and schema reference → [api-reference.md](api-reference.md)
- Python clients: [trilium-py](https://github.com/Nriver/trilium-py) or [trilium-client](https://pypi.org/project/trilium-client/)
- TypeScript types: [trilium-api](https://www.npmjs.com/package/trilium-api)
- Search syntax: see Trilium docs → Search
