<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: stars

## `slk api stars add [options]`

- What: stars\_add — write (POST /stars.add)
- Call: `POST /stars.add`, effect: write
- Permission keys: `messages.star`
- Body: `StarsAddRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api stars list [options]`

- What: stars\_list — read (GET /stars.list)
- Call: `GET /stars.list`, effect: read
- Permission keys: `messages.list`
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `items`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--count <value>` | no | count |
| `--page <value>` | no | page |
| `--cursor <value>` | no | Parameter for pagination. Set \`cursor\` equal to the \`next\_cursor\` attribute returned by the previous request's \`response\_metadata\`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more details. |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. |
| `--all` | no | read every page, as the API pages it |

## `slk api stars remove [options]`

- What: stars\_remove — destructive (POST /stars.remove)
- Call: `POST /stars.remove`, effect: destructive
- Permission keys: `messages.unstar`, `slack.delete`
- Body: `StarsRemoveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
