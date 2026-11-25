<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: categories

## `wordpress api categories-create [options]`

- What: postWpV2Categories — write (POST /wp/v2/categories)
- Call: `POST /wp/v2/categories`, effect: write
- Body: `PostWpV2CategoriesRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api categories-delete [options]`

- What: deleteWpV2CategoriesById — destructive (DELETE /wp/v2/categories/{id})
- Call: `DELETE /wp/v2/categories/{id}`, effect: destructive
- Permission keys: `categories.delete`, `categories.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as terms do not support trashing. |

## `wordpress api categories-get [options]`

- What: getWpV2CategoriesById — read (GET /wp/v2/categories/{id})
- Call: `GET /wp/v2/categories/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api categories-list [options]`

- What: getWpV2Categories — read (GET /wp/v2/categories)
- Call: `GET /wp/v2/categories`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--hide-empty <value>` | no | Whether to hide terms not assigned to any posts. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by term attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--parent <value>` | no | Limit result set to terms assigned to a specific parent. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--post <value>` | no | Limit result set to terms assigned to a specific post. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--slug <value>` | no | Limit result set to terms with one or more specific slugs. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api categories-update [options]`

- What: postWpV2CategoriesById — write (POST /wp/v2/categories/{id})
- Call: `POST /wp/v2/categories/{id}`, effect: write
- Body: `PostWpV2CategoriesByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
