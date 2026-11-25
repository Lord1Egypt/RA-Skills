<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: menus

## `wordpress api menus-create [options]`

- What: postWpV2Menus — write (POST /wp/v2/menus)
- Call: `POST /wp/v2/menus`, effect: write
- Body: `PostWpV2MenusRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api menus-delete [options]`

- What: deleteWpV2MenusById — destructive (DELETE /wp/v2/menus/{id})
- Call: `DELETE /wp/v2/menus/{id}`, effect: destructive
- Permission keys: `menus.delete`, `menus.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as terms do not support trashing. |

## `wordpress api menus-get [options]`

- What: getWpV2MenusById — read (GET /wp/v2/menus/{id})
- Call: `GET /wp/v2/menus/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api menus-list [options]`

- What: getWpV2Menus — read (GET /wp/v2/menus)
- Call: `GET /wp/v2/menus`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--hide-empty <value>` | no | Whether to hide terms not assigned to any posts. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by term attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--post <value>` | no | Limit result set to terms assigned to a specific post. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--slug <value>` | no | Limit result set to terms with one or more specific slugs. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api menus-update [options]`

- What: postWpV2MenusById — write (POST /wp/v2/menus/{id})
- Call: `POST /wp/v2/menus/{id}`, effect: write
- Body: `PostWpV2MenusByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
