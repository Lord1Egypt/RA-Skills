<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Lists

## `attio api lists-create [options]`

- What: Create a list
- Call: `POST /v2/lists`, effect: write
- Sign-in: oauth2 (list\_configuration:read-write)
- Body: `PostV2ListsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api lists-get [options]`

- What: Get a list
- Call: `GET /v2/lists/{list}`, effect: read
- Sign-in: oauth2 (list\_configuration:read)

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |

## `attio api lists-list`

- What: List all lists
- Call: `GET /v2/lists`, effect: read
- Sign-in: oauth2 (list\_configuration:read)

## `attio api lists-update [options]`

- What: Update a list
- Call: `PATCH /v2/lists/{list}`, effect: write
- Sign-in: oauth2 (list\_configuration:read-write)
- Body: `PatchV2ListsByListRequest`, required

| Flag | Required | What |
|---|---|---|
| `--list <value>` | yes | list |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
