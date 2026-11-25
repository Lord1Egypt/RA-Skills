<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Entries

## `attio api lists-entries-attributes-values-list [options]`

- What: List attribute values for a list entry
- Call: `GET /v2/lists/{list}/entries/{entry_id}/attributes/{attribute}/values`, effect: read
- Sign-in: oauth2 (list\_entry:read, list\_configuration:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |
| `--attribute <value>` | yes | attribute |
| `--show-historic <value>` | no | show\_historic |
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--all` | no | read every page, as the API pages it |

## `attio api lists-entries-attributes-values-replace [options]`

- What: Write list entry attribute values
- Call: `PUT /v2/lists/{list}/entries/{entry_id}/attributes/{attribute}/values`, effect: write
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Body: `PutV2ListsByListEntriesByEntryIdAttributesByAttributeValuesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |
| `--attribute <value>` | yes | attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-entries-create [options]`

- What: Create an entry (add record to list)
- Call: `POST /v2/lists/{list}/entries`, effect: write
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Body: `PostV2ListsByListEntriesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-entries-delete [options]`

- What: Delete a list entry
- Call: `DELETE /v2/lists/{list}/entries/{entry_id}`, effect: destructive
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |

## `attio api lists-entries-get [options]`

- What: Get a list entry
- Call: `GET /v2/lists/{list}/entries/{entry_id}`, effect: read
- Sign-in: oauth2 (list\_entry:read, list\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |

## `attio api lists-entries-query [options]`

- What: List entries
- Call: `POST /v2/lists/{list}/entries/query`, effect: read
- Sign-in: oauth2 (list\_entry:read, list\_configuration:read)
- Pages: offset: send `offset` (body), raised by the items read so far; items in `data`; page size in `limit` (body)
- Body: `PostV2ListsByListEntriesQueryRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `attio api lists-entries-replace [options]`

- What: Update a list entry (overwrite multiselect values)
- Call: `PUT /v2/lists/{list}/entries/{entry_id}`, effect: write
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Body: `PutV2ListsByListEntriesByEntryIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-entries-update [options]`

- What: Update a list entry (append multiselect values)
- Call: `PATCH /v2/lists/{list}/entries/{entry_id}`, effect: write
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Body: `PatchV2ListsByListEntriesByEntryIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--entry-id <value>` | yes | entry\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-entries-upsert [options]`

- What: Upsert a list entry by parent
- Call: `PUT /v2/lists/{list}/entries`, effect: write
- Sign-in: oauth2 (list\_entry:read-write, list\_configuration:read)
- Body: `PutV2ListsByListEntriesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
