<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Views

## `attio api lists-views-create [options]`

- What: Create a list view
- Call: `POST /v2/lists/{list}/views`, effect: write
- Sign-in: oauth2 (view:read-write, list\_configuration:read)
- Body: `PostV2ListsByListViewsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-views-delete [options]`

- What: Delete a list view
- Call: `DELETE /v2/lists/{list}/views/{view_id}`, effect: destructive
- Sign-in: oauth2 (view:read-write, list\_configuration:read)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--view-id <value>` | yes | view\_id |

## `attio api lists-views-get [options]`

- What: Get a list view
- Call: `GET /v2/lists/{list}/views/{view_id}`, effect: read
- Sign-in: oauth2 (view:read, list\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--view-id <value>` | yes | view\_id |

## `attio api lists-views-list [options]`

- What: List views for list
- Call: `GET /v2/lists/{list}/views`, effect: read
- Sign-in: oauth2 (list\_configuration:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--show-archived <value>` | no | show\_archived |
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |

## `attio api lists-views-update [options]`

- What: Update a list view
- Call: `PATCH /v2/lists/{list}/views/{view_id}`, effect: write
- Sign-in: oauth2 (view:read-write, list\_configuration:read)
- Body: `PatchV2ListsByListViewsByViewIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--view-id <value>` | yes | view\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-views-create [options]`

- What: Create an object view
- Call: `POST /v2/objects/{object}/views`, effect: write
- Sign-in: oauth2 (view:read-write, object\_configuration:read)
- Body: `PostV2ObjectsByObjectViewsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-views-delete [options]`

- What: Delete an object view
- Call: `DELETE /v2/objects/{object}/views/{view_id}`, effect: destructive
- Sign-in: oauth2 (view:read-write, object\_configuration:read)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--view-id <value>` | yes | view\_id |

## `attio api objects-views-get [options]`

- What: Get an object view
- Call: `GET /v2/objects/{object}/views/{view_id}`, effect: read
- Sign-in: oauth2 (view:read, object\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--view-id <value>` | yes | view\_id |

## `attio api objects-views-list [options]`

- What: List views for object
- Call: `GET /v2/objects/{object}/views`, effect: read
- Sign-in: oauth2 (object\_configuration:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--show-archived <value>` | no | show\_archived |
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--all` | no | read every page, as the API pages it |

## `attio api objects-views-update [options]`

- What: Update an object view
- Call: `PATCH /v2/objects/{object}/views/{view_id}`, effect: write
- Sign-in: oauth2 (view:read-write, object\_configuration:read)
- Body: `PatchV2ObjectsByObjectViewsByViewIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--view-id <value>` | yes | view\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
