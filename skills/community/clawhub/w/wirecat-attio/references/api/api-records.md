<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Records

## `attio api objects-records-attributes-values-list [options]`

- What: List record attribute values
- Call: `GET /v2/objects/{object}/records/{record_id}/attributes/{attribute}/values`, effect: read
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--attribute <value>` | yes | attribute |
| `--show-historic <value>` | no | show\_historic |
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--all` | no | read every page, as the API pages it |

## `attio api objects-records-attributes-values-replace [options]`

- What: Write record attribute values
- Call: `PUT /v2/objects/{object}/records/{record_id}/attributes/{attribute}/values`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PutV2ObjectsByObjectRecordsByRecordIdAttributesByAttributeValuesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--attribute <value>` | yes | attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-create [options]`

- What: Create a record
- Call: `POST /v2/objects/{object}/records`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PostV2ObjectsByObjectRecordsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-delete [options]`

- What: Delete a record
- Call: `DELETE /v2/objects/{object}/records/{record_id}`, effect: destructive
- Sign-in: oauth2 (object\_configuration:read, record\_permission:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |

## `attio api objects-records-entries-list [options]`

- What: List record entries
- Call: `GET /v2/objects/{object}/records/{record_id}/entries`, effect: read
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read, list\_entry:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--all` | no | read every page, as the API pages it |

## `attio api objects-records-get [options]`

- What: Get a record
- Call: `GET /v2/objects/{object}/records/{record_id}`, effect: read
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |

## `attio api objects-records-merge [options]`

- What: Merge two records
- Call: `POST /v2/objects/{object}/records/merge`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PostV2ObjectsByObjectRecordsMergeRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-query [options]`

- What: List records
- Call: `POST /v2/objects/{object}/records/query`, effect: read
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read)
- Pages: offset: send `offset` (body), raised by the items read so far; items in `data`; page size in `limit` (body)
- Body: `PostV2ObjectsByObjectRecordsQueryRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `attio api objects-records-replace [options]`

- What: Update a record (overwrite multiselect values)
- Call: `PUT /v2/objects/{object}/records/{record_id}`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PutV2ObjectsByObjectRecordsByRecordIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-search [options]`

- What: Search records
- Call: `POST /v2/objects/records/search`, effect: read
- Sign-in: oauth2 (record\_permission:read, object\_configuration:read)
- Body: `PostV2ObjectsRecordsSearchRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-update [options]`

- What: Update a record (append multiselect values)
- Call: `PATCH /v2/objects/{object}/records/{record_id}`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PatchV2ObjectsByObjectRecordsByRecordIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--record-id <value>` | yes | record\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-records-upsert [options]`

- What: Upsert a record
- Call: `PUT /v2/objects/{object}/records`, effect: write
- Sign-in: oauth2 (record\_permission:read-write, object\_configuration:read)
- Body: `PutV2ObjectsByObjectRecordsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--matching-attribute <value>` | yes | matching\_attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
