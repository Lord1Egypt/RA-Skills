<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: calls

## `slk api calls add [options]`

- What: calls\_add — write (POST /calls.add)
- Call: `POST /calls.add`, effect: write
- Body: `CallsAddRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api calls end [options]`

- What: calls\_end — write (POST /calls.end)
- Call: `POST /calls.end`, effect: write
- Body: `CallsEndRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api calls info [options]`

- What: calls\_info — read (GET /calls.info)
- Call: `GET /calls.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | \`id\` of the Call returned by the \[\`calls.add\`\](https://api.slack.com/methods/calls.add) method. |

## `slk api calls participants-add [options]`

- What: calls\_participants\_add — write (POST /calls.participants.add)
- Call: `POST /calls.participants.add`, effect: write
- Body: `CallsParticipantsAddRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api calls participants-remove [options]`

- What: calls\_participants\_remove — destructive (POST /calls.participants.remove)
- Call: `POST /calls.participants.remove`, effect: destructive
- Permission keys: `slack.delete`
- Body: `CallsParticipantsRemoveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api calls update [options]`

- What: calls\_update — write (POST /calls.update)
- Call: `POST /calls.update`, effect: write
- Body: `CallsUpdateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
