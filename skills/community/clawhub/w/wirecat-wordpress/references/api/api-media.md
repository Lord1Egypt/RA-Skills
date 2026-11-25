<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: media

## `wordpress api media-create [options]`

- What: postWpV2Media — write (POST /wp/v2/media)
- Call: `POST /wp/v2/media`, effect: write
- Permission keys: `media.publish`
- Body: `PostWpV2MediaRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api media-delete [options]`

- What: deleteWpV2MediaById — destructive (DELETE /wp/v2/media/{id})
- Call: `DELETE /wp/v2/media/{id}`, effect: destructive
- Permission keys: `media.delete`, `media.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |

## `wordpress api media-edit [options]`

- What: postWpV2MediaByIdEdit — write (POST /wp/v2/media/{id}/edit)
- Call: `POST /wp/v2/media/{id}/edit`, effect: write
- Body: `PostWpV2MediaByIdEditRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api media-get [options]`

- What: getWpV2MediaById — read (GET /wp/v2/media/{id})
- Call: `GET /wp/v2/media/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api media-list [options]`

- What: getWpV2Media — read (GET /wp/v2/media)
- Call: `GET /wp/v2/media`, effect: read
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
| `--media-type <value>` | no | Limit result set to attachments of a particular media type or media types. |
| `--mime-type <value>` | no | Limit result set to attachments of a particular MIME type or MIME types. |
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

## `wordpress api media-post-process [options]`

- What: postWpV2MediaByIdPostProcess — write (POST /wp/v2/media/{id}/post-process)
- Call: `POST /wp/v2/media/{id}/post-process`, effect: write
- Body: `PostWpV2MediaByIdPostProcessRequest`, required

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api media-update [options]`

- What: postWpV2MediaById — write (POST /wp/v2/media/{id})
- Call: `POST /wp/v2/media/{id}`, effect: write
- Permission keys: `media.publish`
- Body: `PostWpV2MediaByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
