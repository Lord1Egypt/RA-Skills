<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: pages

## `wordpress api pages-autosaves-create [options]`

- What: postWpV2PagesByIdAutosaves — write (POST /wp/v2/pages/{id}/autosaves)
- Call: `POST /wp/v2/pages/{id}/autosaves`, effect: write
- Permission keys: `pages.publish`
- Body: `PostWpV2PagesByIdAutosavesRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api pages-autosaves-get [options]`

- What: getWpV2PagesByParentAutosavesById — read (GET…
- Call: `GET /wp/v2/pages/{parent}/autosaves/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api pages-autosaves-list [options]`

- What: getWpV2PagesByIdAutosaves — read (GET /wp/v2/pages/{id}/autosaves)
- Call: `GET /wp/v2/pages/{id}/autosaves`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--parent <value>` | no | The ID for the parent of the autosave. |

## `wordpress api pages-create [options]`

- What: postWpV2Pages — write (POST /wp/v2/pages)
- Call: `POST /wp/v2/pages`, effect: write
- Permission keys: `pages.publish`, `posts.create`
- Body: `PostWpV2PagesRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api pages-delete [options]`

- What: deleteWpV2PagesById — destructive (DELETE /wp/v2/pages/{id})
- Call: `DELETE /wp/v2/pages/{id}`, effect: destructive
- Permission keys: `pages.delete`, `pages.delete.force`, `posts.delete`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api pages-get [options]`

- What: getWpV2PagesById — read (GET /wp/v2/pages/{id})
- Call: `GET /wp/v2/pages/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--excerpt-length <value>` | no | Override the default excerpt length. |
| `--password <value>` | no | The password for the post if it is password protected. |

## `wordpress api pages-list [options]`

- What: getWpV2Pages — read (GET /wp/v2/pages)
- Call: `GET /wp/v2/pages`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | Limit response to posts published after a given ISO8601 compliant date. |
| `--author <value>` | no | Limit result set to posts assigned to specific authors. |
| `--author-exclude <value>` | no | Ensure result set excludes posts assigned to specific authors. |
| `--before <value>` | no | Limit response to posts published before a given ISO8601 compliant date. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--menu-order <value>` | no | Limit result set to posts with a specific menu\_order value. |
| `--modified-after <value>` | no | Limit response to posts modified after a given ISO8601 compliant date. |
| `--modified-before <value>` | no | Limit response to posts modified before a given ISO8601 compliant date. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by post attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--parent <value>` | no | Limit result set to items with particular parent IDs. |
| `--parent-exclude <value>` | no | Limit result set to all items except those of a particular parent ID. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--search-columns <value>` | no | Array of column names to be searched. |
| `--search-semantics <value>` | no | How to interpret the search input. |
| `--slug <value>` | no | Limit result set to posts with one or more specific slugs. |
| `--status <value>` | no | Limit result set to posts assigned one or more statuses. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api pages-revisions-delete [options]`

- What: deleteWpV2PagesByParentRevisionsById — destructive (DELETE…
- Call: `DELETE /wp/v2/pages/{parent}/revisions/{id}`, effect: destructive
- Permission keys: `pages.delete`, `pages.delete.force`

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as revisions do not support trashing. |

## `wordpress api pages-revisions-get [options]`

- What: getWpV2PagesByParentRevisionsById — read (GET…
- Call: `GET /wp/v2/pages/{parent}/revisions/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api pages-revisions-list [options]`

- What: getWpV2PagesByParentRevisions — read (GET /wp/v2/pages/{parent}/revisions)
- Call: `GET /wp/v2/pages/{parent}/revisions`, effect: read
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

## `wordpress api pages-update [options]`

- What: postWpV2PagesById — write (POST /wp/v2/pages/{id})
- Call: `POST /wp/v2/pages/{id}`, effect: write
- Permission keys: `pages.publish`, `posts.update`
- Body: `PostWpV2PagesByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
