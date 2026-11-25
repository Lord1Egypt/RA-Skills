<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: pins

## `slk api pins add [options]`

- What: pins\_add — write (POST /pins.add)
- Call: `POST /pins.add`, effect: write
- Permission keys: `messages.pin`
- Body: `PinsAddRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api pins list [options]`

- What: pins\_list — read (GET /pins.list)
- Call: `GET /pins.list`, effect: read
- Permission keys: `messages.list`

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | Channel to get pinned items for. |

## `slk api pins remove [options]`

- What: pins\_remove — destructive (POST /pins.remove)
- Call: `POST /pins.remove`, effect: destructive
- Permission keys: `messages.unpin`, `slack.delete`
- Body: `PinsRemoveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
