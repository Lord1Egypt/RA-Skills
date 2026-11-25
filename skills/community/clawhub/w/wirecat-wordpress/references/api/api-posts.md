<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: posts

## `wordpress api posts-autosaves-create [options]`

- What: postWpV2PostsByIdAutosaves — write (POST /wp/v2/posts/{id}/autosaves)
- Call: `POST /wp/v2/posts/{id}/autosaves`, effect: write
- Permission keys: `posts.publish`
- Body: `PostWpV2PostsByIdAutosavesRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api posts-autosaves-get [options]`

- What: getWpV2PostsByParentAutosavesById — read (GET…
- Call: `GET /wp/v2/posts/{parent}/autosaves/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api posts-autosaves-list [options]`

- What: getWpV2PostsByIdAutosaves — read (GET /wp/v2/posts/{id}/autosaves)
- Call: `GET /wp/v2/posts/{id}/autosaves`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--parent <value>` | no | The ID for the parent of the autosave. |

## `wordpress api posts-create [options]`

- What: postWpV2Posts — write (POST /wp/v2/posts)
- Call: `POST /wp/v2/posts`, effect: write
- Permission keys: `posts.publish`, `posts.create`
- Body: `PostWpV2PostsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api posts-delete [options]`

- What: deleteWpV2PostsById — destructive (DELETE /wp/v2/posts/{id})
- Call: `DELETE /wp/v2/posts/{id}`, effect: destructive
- Permission keys: `posts.delete`, `posts.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api posts-get [options]`

- What: getWpV2PostsById — read (GET /wp/v2/posts/{id})
- Call: `GET /wp/v2/posts/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--excerpt-length <value>` | no | Override the default excerpt length. |
| `--password <value>` | no | The password for the post if it is password protected. |

## `wordpress api posts-list [options]`

- What: getWpV2Posts — read (GET /wp/v2/posts)
- Call: `GET /wp/v2/posts`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | Limit response to posts published after a given ISO8601 compliant date. |
| `--author <value>` | no | Limit result set to posts assigned to specific authors. |
| `--author-exclude <value>` | no | Ensure result set excludes posts assigned to specific authors. |
| `--before <value>` | no | Limit response to posts published before a given ISO8601 compliant date. |
| `--categories <value>` | no | Limit result set to items with specific terms assigned in the categories taxonomy. |
| `--categories-exclude <value>` | no | Limit result set to items except those with specific terms assigned in the categories taxonomy. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--format <value>` | no | Limit result set to items assigned one or more given formats. |
| `--ignore-sticky <value>` | no | Whether to ignore sticky posts or not. |
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
| `--sticky <value>` | no | Limit result set to items that are sticky. |
| `--tags <value>` | no | Limit result set to items with specific terms assigned in the tags taxonomy. |
| `--tags-exclude <value>` | no | Limit result set to items except those with specific terms assigned in the tags taxonomy. |
| `--tax-relation <value>` | no | Limit result set based on relationship between multiple taxonomies. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api posts-revisions-delete [options]`

- What: deleteWpV2PostsByParentRevisionsById — destructive (DELETE…
- Call: `DELETE /wp/v2/posts/{parent}/revisions/{id}`, effect: destructive
- Permission keys: `posts.delete`, `posts.delete.force`

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as revisions do not support trashing. |

## `wordpress api posts-revisions-get [options]`

- What: getWpV2PostsByParentRevisionsById — read (GET…
- Call: `GET /wp/v2/posts/{parent}/revisions/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--parent <value>` | yes | parent |
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api posts-revisions-list [options]`

- What: getWpV2PostsByParentRevisions — read (GET /wp/v2/posts/{parent}/revisions)
- Call: `GET /wp/v2/posts/{parent}/revisions`, effect: read
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

## `wordpress api posts-update [options]`

- What: postWpV2PostsById — write (POST /wp/v2/posts/{id})
- Call: `POST /wp/v2/posts/{id}`, effect: write
- Permission keys: `posts.publish`, `posts.update`
- Body: `PostWpV2PostsByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
