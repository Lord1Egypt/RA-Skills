<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Files

## `attio api files-create [options]`

- What: Create a folder
- Call: `POST /v2/files`, effect: write
- Sign-in: oauth2 (file:read-write, object\_configuration:read, record\_permission:read)
- Body: `PostV2FilesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api files-delete [options]`

- What: Delete a file
- Call: `DELETE /v2/files/{file_id}`, effect: destructive
- Sign-in: oauth2 (file:read-write, object\_configuration:read, record\_permission:read)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--file-id <value>` | yes | file\_id |

## `attio api files-download-list [options]`

- What: Download a file
- Call: `GET /v2/files/{file_id}/download`, effect: read
- Sign-in: oauth2 (object\_configuration:read, record\_permission:read, file:read)

| Flag | Required | What |
|---|---|---|
| `--file-id <value>` | yes | file\_id |

## `attio api files-get [options]`

- What: Get a file
- Call: `GET /v2/files/{file_id}`, effect: read
- Sign-in: oauth2 (file:read, object\_configuration:read, record\_permission:read)

| Flag | Required | What |
|---|---|---|
| `--file-id <value>` | yes | file\_id |

## `attio api files-list [options]`

- What: List files
- Call: `GET /v2/files`, effect: read
- Sign-in: oauth2 (object\_configuration:read, record\_permission:read, file:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--storage-provider <value>` | no | storage\_provider |
| `--parent-folder-id <value>` | no | parent\_folder\_id |
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |
