<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: chat

## `slk api chat delete [options]`

- What: chat\_delete — destructive (POST /chat.delete)
- Call: `POST /chat.delete`, effect: destructive
- Permission keys: `messages.delete`
- Body: `ChatDeleteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat delete-scheduled-message [options]`

- What: chat\_deleteScheduledMessage — destructive (POST /chat.deleteScheduledMessage)
- Call: `POST /chat.deleteScheduledMessage`, effect: destructive
- Permission keys: `messages.scheduled.cancel`, `slack.delete`
- Body: `ChatDeleteScheduledMessageRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat get-permalink [options]`

- What: chat\_getPermalink — read (GET /chat.getPermalink)
- Call: `GET /chat.getPermalink`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | The ID of the conversation or channel containing the message |
| `--message-ts <value>` | yes | A message's \`ts\` value, uniquely identifying it within a channel |

## `slk api chat me-message [options]`

- What: chat\_meMessage — write (POST /chat.meMessage)
- Call: `POST /chat.meMessage`, effect: write
- Permission keys: `messages.send`
- Body: `ChatMeMessageRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat post-ephemeral [options]`

- What: chat\_postEphemeral — write (POST /chat.postEphemeral)
- Call: `POST /chat.postEphemeral`, effect: write
- Permission keys: `messages.send`
- Body: `ChatPostEphemeralRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat post-message [options]`

- What: chat\_postMessage — write (POST /chat.postMessage)
- Call: `POST /chat.postMessage`, effect: write
- Permission keys: `messages.send`
- Body: `ChatPostMessageRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat schedule-message [options]`

- What: chat\_scheduleMessage — write (POST /chat.scheduleMessage)
- Call: `POST /chat.scheduleMessage`, effect: write
- Permission keys: `messages.send`
- Body: `ChatScheduleMessageRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat scheduled-messages-list [options]`

- What: chat\_scheduledMessages\_list — read (GET /chat.scheduledMessages.list)
- Call: `GET /chat.scheduledMessages.list`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `scheduled_messages`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | no | The channel of the scheduled messages |
| `--latest <value>` | no | A UNIX timestamp of the latest value in the time range |
| `--oldest <value>` | no | A UNIX timestamp of the oldest value in the time range |
| `--limit <value>` | no | Maximum number of original entries to return. |
| `--cursor <value>` | no | For pagination purposes, this is the \`cursor\` value returned from a previous call to \`chat.scheduledmessages.list\` indicating where you want to start this call from. |
| `--all` | no | read every page, as the API pages it |

## `slk api chat unfurl [options]`

- What: chat\_unfurl — write (POST /chat.unfurl)
- Call: `POST /chat.unfurl`, effect: write
- Body: `ChatUnfurlRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api chat update [options]`

- What: chat\_update — write (POST /chat.update)
- Call: `POST /chat.update`, effect: write
- Permission keys: `messages.edit`
- Body: `ChatUpdateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
