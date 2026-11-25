<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Objects

## `attio api objects-create [options]`

- What: Create an object
- Call: `POST /v2/objects`, effect: write
- Sign-in: oauth2 (object\_configuration:read-write)
- Body: `PostV2ObjectsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api objects-delete [options]`

- What: Delete an object
- Call: `DELETE /v2/objects/{object}`, effect: destructive
- Sign-in: oauth2 (object\_configuration:read-write, record\_permission:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |

## `attio api objects-get [options]`

- What: Get an object
- Call: `GET /v2/objects/{object}`, effect: read
- Sign-in: oauth2 (object\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |

## `attio api objects-list`

- What: List objects
- Call: `GET /v2/objects`, effect: read
- Sign-in: oauth2 (object\_configuration:read)

## `attio api objects-update [options]`

- What: Update an object
- Call: `PATCH /v2/objects/{object}`, effect: write
- Sign-in: oauth2 (object\_configuration:read-write)
- Body: `PatchV2ObjectsByObjectRequest`, required

| Flag | Required | What |
|---|---|---|
| `--object <value>` | yes | object |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
