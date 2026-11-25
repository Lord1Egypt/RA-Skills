<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Activity records

## `attio api activities-records-create [options]`

- What: Create an activity record
- Call: `POST /v2/activities/{activity}/records`, effect: write
- Sign-in: oauth2 (activity\_record:read-write, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Body: `PostV2ActivitiesByActivityRecordsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api activities-records-delete [options]`

- What: Delete an activity record
- Call: `DELETE /v2/activities/{activity}/records/{record_id}`, effect: destructive
- Sign-in: oauth2 (activity\_record:read-write, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--record-id <value>` | yes | record\_id |

## `attio api activities-records-get [options]`

- What: Get an activity record
- Call: `GET /v2/activities/{activity}/records/{record_id}`, effect: read
- Sign-in: oauth2 (activity\_record:read, activity\_configuration:read, object\_configuration:read, record\_permission:read)

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--record-id <value>` | yes | record\_id |

## `attio api activities-records-query [options]`

- What: List activity records
- Call: `POST /v2/activities/{activity}/records/query`, effect: read
- Sign-in: oauth2 (activity\_record:read, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Pages: offset: send `offset` (body), raised by the items read so far; items in `data`; page size in `limit` (body)
- Body: `PostV2ActivitiesByActivityRecordsQueryRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
| `--all` | no | read every page, as the API pages it |

## `attio api activities-records-replace [options]`

- What: Update an activity record (overwrite multiselect values)
- Call: `PUT /v2/activities/{activity}/records/{record_id}`, effect: write
- Sign-in: oauth2 (activity\_record:read-write, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Body: `PutV2ActivitiesByActivityRecordsByRecordIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--record-id <value>` | yes | record\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api activities-records-update [options]`

- What: Update an activity record (append multiselect values)
- Call: `PATCH /v2/activities/{activity}/records/{record_id}`, effect: write
- Sign-in: oauth2 (activity\_record:read-write, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Body: `PatchV2ActivitiesByActivityRecordsByRecordIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--record-id <value>` | yes | record\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api activities-records-upsert [options]`

- What: Upsert an activity record
- Call: `PUT /v2/activities/{activity}/records`, effect: write
- Sign-in: oauth2 (activity\_record:read-write, activity\_configuration:read, object\_configuration:read, record\_permission:read)
- Body: `PutV2ActivitiesByActivityRecordsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--matching-attribute <value>` | yes | matching\_attribute |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
