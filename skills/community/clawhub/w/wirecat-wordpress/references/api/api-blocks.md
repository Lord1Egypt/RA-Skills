<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: blocks

## `wordpress api blocks-autosaves-create [options]`

- What: postWpV2BlocksByIdAutosaves — write (POST /wp/v2/blocks/{id}/autosaves)
- Call: `POST /wp/v2/blocks/{id}/autosaves`, effect: write
- Permission keys: `blocks.publish`
- Body: `PostWpV2BlocksByIdAutosavesRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api blocks-autosaves-get [options]`

- What: getWpV2BlocksByParentAutosavesById — read (GET…
- Call: `GET /wp/v2/blocks/{parent}/autosaves/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api blocks-autosaves-list [options]`

- What: getWpV2BlocksByIdAutosaves — read (GET /wp/v2/blocks/{id}/autosaves)
- Call: `GET /wp/v2/blocks/{id}/autosaves`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--parent <value>` | no | The ID for the parent of the autosave. |

## `wordpress api blocks-create [options]`

- What: postWpV2Blocks — write (POST /wp/v2/blocks)
- Call: `POST /wp/v2/blocks`, effect: write
- Permission keys: `blocks.publish`
- Body: `PostWpV2BlocksRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api blocks-delete [options]`

- What: deleteWpV2BlocksById — destructive (DELETE /wp/v2/blocks/{id})
- Call: `DELETE /wp/v2/blocks/{id}`, effect: destructive
- Permission keys: `blocks.delete`, `blocks.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api blocks-get [options]`

- What: getWpV2BlocksById — read (GET /wp/v2/blocks/{id})
- Call: `GET /wp/v2/blocks/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--excerpt-length <value>` | no | Override the default excerpt length. |
| `--password <value>` | no | The password for the post if it is password protected. |

## `wordpress api blocks-list [options]`

- What: getWpV2Blocks — read (GET /wp/v2/blocks)
- Call: `GET /wp/v2/blocks`, effect: read
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
| `--tax-relation <value>` | no | Limit result set based on relationship between multiple taxonomies. |
| `--wp-pattern-category <value>` | no | Limit result set to items with specific terms assigned in the wp\_pattern\_category taxonomy. |
| `--wp-pattern-category-exclude <value>` | no | Limit result set to items except those with specific terms assigned in the wp\_pattern\_category taxonomy. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api blocks-revisions-delete [options]`

- What: deleteWpV2BlocksByParentRevisionsById — destructive (DELETE…
- Call: `DELETE /wp/v2/blocks/{parent}/revisions/{id}`, effect: destructive
- Permission keys: `blocks.delete`, `blocks.delete.force`

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as revisions do not support trashing. |

## `wordpress api blocks-revisions-get [options]`

- What: getWpV2BlocksByParentRevisionsById — read (GET…
- Call: `GET /wp/v2/blocks/{parent}/revisions/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api blocks-revisions-list [options]`

- What: getWpV2BlocksByParentRevisions — read (GET /wp/v2/blocks/{parent}/revisions)
- Call: `GET /wp/v2/blocks/{parent}/revisions`, effect: read
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

## `wordpress api blocks-update [options]`

- What: postWpV2BlocksById — write (POST /wp/v2/blocks/{id})
- Call: `POST /wp/v2/blocks/{id}`, effect: write
- Permission keys: `blocks.publish`
- Body: `PostWpV2BlocksByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
