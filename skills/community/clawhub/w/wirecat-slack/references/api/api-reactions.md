<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: reactions

## `slk api reactions add [options]`

- What: reactions\_add — write (POST /reactions.add)
- Call: `POST /reactions.add`, effect: write
- Permission keys: `reactions.add`
- Body: `ReactionsAddRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api reactions get [options]`

- What: reactions\_get — read (GET /reactions.get)
- Call: `GET /reactions.get`, effect: read
- Permission keys: `messages.list`

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | no | Channel where the message to get reactions for was posted. |
| `--file <value>` | no | File to get reactions for. |
| `--file-comment <value>` | no | File comment to get reactions for. |
| `--full <value>` | no | If true always return the complete reaction list. |
| `--timestamp <value>` | no | Timestamp of the message to get reactions for. |

## `slk api reactions list [options]`

- What: reactions\_list — read (GET /reactions.list)
- Call: `GET /reactions.list`, effect: read
- Permission keys: `messages.list`
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `items`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--user <value>` | no | Show reactions made by this user. Defaults to the authed user. |
| `--full <value>` | no | If true always return the complete reaction list. |
| `--count <value>` | no | count |
| `--page <value>` | no | page |
| `--cursor <value>` | no | Parameter for pagination. Set \`cursor\` equal to the \`next\_cursor\` attribute returned by the previous request's \`response\_metadata\`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more details. |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. |
| `--all` | no | read every page, as the API pages it |

## `slk api reactions remove [options]`

- What: reactions\_remove — destructive (POST /reactions.remove)
- Call: `POST /reactions.remove`, effect: destructive
- Permission keys: `reactions.remove`, `slack.delete`
- Body: `ReactionsRemoveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
