<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Activities

## `attio api activities-create [options]`

- What: Create an activity
- Call: `POST /v2/activities`, effect: write
- Sign-in: oauth2 (activity\_configuration:read-write)
- Body: `PostV2ActivitiesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api activities-delete [options]`

- What: Delete an activity
- Call: `DELETE /v2/activities/{activity}`, effect: destructive
- Sign-in: oauth2 (activity\_configuration:read-write, activity\_record:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |

## `attio api activities-get [options]`

- What: Get an activity
- Call: `GET /v2/activities/{activity}`, effect: read
- Sign-in: oauth2 (activity\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |

## `attio api activities-list [options]`

- What: List activities
- Call: `GET /v2/activities`, effect: read
- Sign-in: oauth2 (activity\_configuration:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |

## `attio api activities-update [options]`

- What: Update an activity
- Call: `PATCH /v2/activities/{activity}`, effect: write
- Sign-in: oauth2 (activity\_configuration:read-write)
- Body: `PatchV2ActivitiesByActivityRequest`, required

| Flag | Required | What |
|---|---|---|
| `--activity <value>` | yes | activity |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
