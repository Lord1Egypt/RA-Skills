<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: menu-items

## `wordpress api menu-items-autosaves-create [options]`

- What: postWpV2MenuItemsByIdAutosaves — write (POST /wp/v2/menu-items/{id}/autosaves)
- Call: `POST /wp/v2/menu-items/{id}/autosaves`, effect: write
- Permission keys: `menu-items.publish`
- Body: `PostWpV2MenuItemsByIdAutosavesRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api menu-items-autosaves-get [options]`

- What: getWpV2MenuItemsByParentAutosavesById — read (GET…
- Call: `GET /wp/v2/menu-items/{parent}/autosaves/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api menu-items-autosaves-list [options]`

- What: getWpV2MenuItemsByIdAutosaves — read (GET /wp/v2/menu-items/{id}/autosaves)
- Call: `GET /wp/v2/menu-items/{id}/autosaves`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--parent <value>` | no | The ID for the parent of the autosave. |

## `wordpress api menu-items-create [options]`

- What: postWpV2MenuItems — write (POST /wp/v2/menu-items)
- Call: `POST /wp/v2/menu-items`, effect: write
- Permission keys: `menu-items.publish`
- Body: `PostWpV2MenuItemsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api menu-items-delete [options]`

- What: deleteWpV2MenuItemsById — destructive (DELETE /wp/v2/menu-items/{id})
- Call: `DELETE /wp/v2/menu-items/{id}`, effect: destructive
- Permission keys: `menu-items.delete`, `menu-items.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api menu-items-get [options]`

- What: getWpV2MenuItemsById — read (GET /wp/v2/menu-items/{id})
- Call: `GET /wp/v2/menu-items/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api menu-items-list [options]`

- What: getWpV2MenuItems — read (GET /wp/v2/menu-items)
- Call: `GET /wp/v2/menu-items`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | Limit response to posts published after a given ISO8601 compliant date. |
| `--before <value>` | no | Limit response to posts published before a given ISO8601 compliant date. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--menu-order <value>` | no | Limit result set to posts with a specific menu\_order value. |
| `--menus <value>` | no | Limit result set to items with specific terms assigned in the menus taxonomy. |
| `--menus-exclude <value>` | no | Limit result set to items except those with specific terms assigned in the menus taxonomy. |
| `--modified-after <value>` | no | Limit response to posts modified after a given ISO8601 compliant date. |
| `--modified-before <value>` | no | Limit response to posts modified before a given ISO8601 compliant date. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by object attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--search-columns <value>` | no | Array of column names to be searched. |
| `--search-semantics <value>` | no | How to interpret the search input. |
| `--slug <value>` | no | Limit result set to posts with one or more specific slugs. |
| `--status <value>` | no | Limit result set to posts assigned one or more statuses. |
| `--tax-relation <value>` | no | Limit result set based on relationship between multiple taxonomies. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api menu-items-update [options]`

- What: postWpV2MenuItemsById — write (POST /wp/v2/menu-items/{id})
- Call: `POST /wp/v2/menu-items/{id}`, effect: write
- Permission keys: `menu-items.publish`
- Body: `PostWpV2MenuItemsByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
