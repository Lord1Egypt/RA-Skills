<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: navigation

## `wordpress api navigation-autosaves-create [options]`

- What: postWpV2NavigationByIdAutosaves — write (POST /wp/v2/navigation/{id}/autosaves)
- Call: `POST /wp/v2/navigation/{id}/autosaves`, effect: write
- Permission keys: `navigation.publish`
- Body: `PostWpV2NavigationByIdAutosavesRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api navigation-autosaves-get [options]`

- What: getWpV2NavigationByParentAutosavesById — read (GET…
- Call: `GET /wp/v2/navigation/{parent}/autosaves/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api navigation-autosaves-list [options]`

- What: getWpV2NavigationByIdAutosaves — read (GET /wp/v2/navigation/{id}/autosaves)
- Call: `GET /wp/v2/navigation/{id}/autosaves`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--parent <value>` | no | The ID for the parent of the autosave. |

## `wordpress api navigation-create [options]`

- What: postWpV2Navigation — write (POST /wp/v2/navigation)
- Call: `POST /wp/v2/navigation`, effect: write
- Permission keys: `navigation.publish`
- Body: `PostWpV2NavigationRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api navigation-delete [options]`

- What: deleteWpV2NavigationById — destructive (DELETE /wp/v2/navigation/{id})
- Call: `DELETE /wp/v2/navigation/{id}`, effect: destructive
- Permission keys: `navigation.delete`, `navigation.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api navigation-get [options]`

- What: getWpV2NavigationById — read (GET /wp/v2/navigation/{id})
- Call: `GET /wp/v2/navigation/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--password <value>` | no | The password for the post if it is password protected. |

## `wordpress api navigation-list [options]`

- What: getWpV2Navigation — read (GET /wp/v2/navigation)
- Call: `GET /wp/v2/navigation`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | Limit response to posts published after a given ISO8601 compliant date. |
| `--before <value>` | no | Limit response to posts published before a given ISO8601 compliant date. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--modified-after <value>` | no | Limit response to posts modified after a given ISO8601 compliant date. |
| `--modified-before <value>` | no | Limit response to posts modified before a given ISO8601 compliant date. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by post attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--search-columns <value>` | no | Array of column names to be searched. |
| `--search-semantics <value>` | no | How to interpret the search input. |
| `--slug <value>` | no | Limit result set to posts with one or more specific slugs. |
| `--status <value>` | no | Limit result set to posts assigned one or more statuses. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api navigation-revisions-delete [options]`

- What: deleteWpV2NavigationByParentRevisionsById — destructive (DELETE…
- Call: `DELETE /wp/v2/navigation/{parent}/revisions/{id}`, effect: destructive
- Permission keys: `navigation.delete`, `navigation.delete.force`

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as revisions do not support trashing. |

## `wordpress api navigation-revisions-get [options]`

- What: getWpV2NavigationByParentRevisionsById — read (GET…
- Call: `GET /wp/v2/navigation/{parent}/revisions/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api navigation-revisions-list [options]`

- What: getWpV2NavigationByParentRevisions — read (GET…
- Call: `GET /wp/v2/navigation/{parent}/revisions`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by object attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api navigation-update [options]`

- What: postWpV2NavigationById — write (POST /wp/v2/navigation/{id})
- Call: `POST /wp/v2/navigation/{id}`, effect: write
- Permission keys: `navigation.publish`
- Body: `PostWpV2NavigationByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
