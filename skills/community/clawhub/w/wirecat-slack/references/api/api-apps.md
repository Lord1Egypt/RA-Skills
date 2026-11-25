<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: apps

## `slk api apps event-authorizations-list [options]`

- What: apps\_event\_authorizations\_list — read (GET /apps.event.authorizations.list)
- Call: `GET /apps.event.authorizations.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--event-context <value>` | yes | event\_context |
| `--cursor <value>` | no | cursor |
| `--limit <value>` | no | limit |

## `slk api apps permissions-info`

- What: apps\_permissions\_info — read (GET /apps.permissions.info)
- Call: `GET /apps.permissions.info`, effect: read

## `slk api apps permissions-request [options]`

- What: apps\_permissions\_request — write (GET /apps.permissions.request)
- Call: `GET /apps.permissions.request`, effect: write

| Flag | Required | What |
|---|---|---|
| `--scopes <value>` | yes | A comma separated list of scopes to request for |
| `--trigger-id <value>` | yes | Token used to trigger the permissions API |

## `slk api apps permissions-resources-list [options]`

- What: apps\_permissions\_resources\_list — read (GET /apps.permissions.resources.list)
- Call: `GET /apps.permissions.resources.list`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `resources`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--limit <value>` | no | The maximum number of items to return. |
| `--all` | no | read every page, as the API pages it |

## `slk api apps permissions-scopes-list`

- What: apps\_permissions\_scopes\_list — read (GET /apps.permissions.scopes.list)
- Call: `GET /apps.permissions.scopes.list`, effect: read

## `slk api apps permissions-users-list [options]`

- What: apps\_permissions\_users\_list — read (GET /apps.permissions.users.list)
- Call: `GET /apps.permissions.users.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--limit <value>` | no | The maximum number of items to return. |

## `slk api apps permissions-users-request [options]`

- What: apps\_permissions\_users\_request — write (GET /apps.permissions.users.request)
- Call: `GET /apps.permissions.users.request`, effect: write

| Flag | Required | What |
|---|---|---|
| `--scopes <value>` | yes | A comma separated list of user scopes to request for |
| `--trigger-id <value>` | yes | Token used to trigger the request |
| `--user <value>` | yes | The user this scope is being requested for |

## `slk api apps uninstall [options]`

- What: apps\_uninstall — destructive (GET /apps.uninstall)
- Call: `GET /apps.uninstall`, effect: destructive
- Permission keys: `slack.delete`

| Flag | Required | What |
|---|---|---|
| `--client-id <value>` | no | Issued when you created your application. |
| `--client-secret <value>` | no | Issued when you created your application. |
