<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Notes

## `attio api notes-create [options]`

- What: Create a note
- Call: `POST /v2/notes`, effect: write
- Sign-in: oauth2 (note:read-write, object\_configuration:read, record\_permission:read)
- Body: `PostV2NotesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api notes-delete [options]`

- What: Delete a note
- Call: `DELETE /v2/notes/{note_id}`, effect: destructive
- Sign-in: oauth2 (note:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | note\_id |

## `attio api notes-get [options]`

- What: Get a note
- Call: `GET /v2/notes/{note_id}`, effect: read
- Sign-in: oauth2 (note:read, object\_configuration:read, record\_permission:read)

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | note\_id |

## `attio api notes-list [options]`

- What: List notes
- Call: `GET /v2/notes`, effect: read
- Sign-in: oauth2 (note:read, object\_configuration:read, record\_permission:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--parent-object <value>` | no | parent\_object |
| `--parent-record-id <value>` | no | parent\_record\_id |
| `--all` | no | read every page, as the API pages it |

## `attio api notes-update [options]`

- What: Update a note
- Call: `PATCH /v2/notes/{note_id}`, effect: write
- Sign-in: oauth2 (note:read-write, object\_configuration:read, record\_permission:read)
- Body: `PatchV2NotesByNoteIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--note-id <value>` | yes | note\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
