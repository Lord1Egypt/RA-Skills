<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Threads

## `attio api threads-get [options]`

- What: Get a thread and its comments
- Call: `GET /v2/threads/{thread_id}`, effect: read
- Sign-in: oauth2 (comment:read)
- Pages: cursor: send `cursor` (query), read the next one from `pagination.next_cursor`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--thread-id <value>` | yes | thread\_id |
| `--limit <value>` | no | limit |
| `--cursor <value>` | no | cursor |
| `--created-after <value>` | no | created\_after |
| `--all` | no | read every page, as the API pages it |

## `attio api threads-list [options]`

- What: List threads
- Call: `GET /v2/threads`, effect: read
- Sign-in: oauth2 (comment:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--record-id <value>` | no | record\_id |
| `--object <value>` | no | object |
| `--entry-id <value>` | no | entry\_id |
| `--list <value>` | no | list |
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--all` | no | read every page, as the API pages it |
