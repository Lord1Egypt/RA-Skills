<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: users

## `slk api users conversations [options]`

- What: users\_conversations — read (GET /users.conversations)
- Call: `GET /users.conversations`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `channels`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--user <value>` | no | Browse conversations by a specific user ID's membership. Non-public channels are restricted to those where the calling user shares membership. |
| `--types <value>` | no | Mix and match channel types by providing a comma-separated list of any combination of \`public\_channel\`, \`private\_channel\`, \`mpim\`, \`im\` |
| `--exclude-archived <value>` | no | Set to \`true\` to exclude archived channels from the list |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. Must be an integer no larger than 1000. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--all` | no | read every page, as the API pages it |

## `slk api users get-presence [options]`

- What: users\_getPresence — read (GET /users.getPresence)
- Call: `GET /users.getPresence`, effect: read

| Flag | Required | What |
|---|---|---|
| `--user <value>` | no | User to get presence info on. Defaults to the authed user. |

## `slk api users identity`

- What: users\_identity — read (GET /users.identity)
- Call: `GET /users.identity`, effect: read

## `slk api users info [options]`

- What: users\_info — read (GET /users.info)
- Call: `GET /users.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--include-locale <value>` | no | Set this to \`true\` to receive the locale for this user. Defaults to \`false\` |
| `--user <value>` | no | User to get info on |

## `slk api users list [options]`

- What: users\_list — read (GET /users.list)
- Call: `GET /users.list`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `members`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the users list hasn't been reached. Providing no \`limit\` value will result in Slack attempting to deliver you the entire result set. If the collection is too large you may experience \`limit\_required\` or HTTP 500 errors. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--include-locale <value>` | no | Set this to \`true\` to receive the locale for users. Defaults to \`false\` |
| `--all` | no | read every page, as the API pages it |

## `slk api users lookup-by-email [options]`

- What: users\_lookupByEmail — read (GET /users.lookupByEmail)
- Call: `GET /users.lookupByEmail`, effect: read

| Flag | Required | What |
|---|---|---|
| `--email <value>` | yes | An email address belonging to a user in the workspace |

## `slk api users profile-get [options]`

- What: users\_profile\_get — read (GET /users.profile.get)
- Call: `GET /users.profile.get`, effect: read

| Flag | Required | What |
|---|---|---|
| `--include-labels <value>` | no | Include labels for each ID in custom profile fields |
| `--user <value>` | no | User to retrieve profile info for |

## `slk api users profile-set [options]`

- What: users\_profile\_set — write (POST /users.profile.set)
- Call: `POST /users.profile.set`, effect: write
- Body: `UsersProfileSetRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api users set-active`

- What: users\_setActive — write (POST /users.setActive)
- Call: `POST /users.setActive`, effect: write

## `slk api users set-presence [options]`

- What: users\_setPresence — write (POST /users.setPresence)
- Call: `POST /users.setPresence`, effect: write
- Body: `UsersSetPresenceRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
