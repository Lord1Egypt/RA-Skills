<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: comments

## `wordpress api comments-create [options]`

- What: postWpV2Comments — write (POST /wp/v2/comments)
- Call: `POST /wp/v2/comments`, effect: write
- Body: `PostWpV2CommentsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api comments-delete [options]`

- What: deleteWpV2CommentsById — destructive (DELETE /wp/v2/comments/{id})
- Call: `DELETE /wp/v2/comments/{id}`, effect: destructive
- Permission keys: `comments.delete`, `comments.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to bypass Trash and force deletion. |
| `--password <value>` | no | The password for the parent post of the comment (if the post is password protected). |

## `wordpress api comments-get [options]`

- What: getWpV2CommentsById — read (GET /wp/v2/comments/{id})
- Call: `GET /wp/v2/comments/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--password <value>` | no | The password for the parent post of the comment (if the post is password protected). |

## `wordpress api comments-list [options]`

- What: getWpV2Comments — read (GET /wp/v2/comments)
- Call: `GET /wp/v2/comments`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--after <value>` | no | Limit response to comments published after a given ISO8601 compliant date. |
| `--author <value>` | no | Limit result set to comments assigned to specific user IDs. Requires authorization. |
| `--author-email <value>` | no | Limit result set to that from a specific author email. Requires authorization. |
| `--author-exclude <value>` | no | Ensure result set excludes comments assigned to specific user IDs. Requires authorization. |
| `--before <value>` | no | Limit response to comments published before a given ISO8601 compliant date. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by comment attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--parent <value>` | no | Limit result set to comments of specific parent IDs. |
| `--parent-exclude <value>` | no | Ensure result set excludes specific parent IDs. |
| `--password <value>` | no | The password for the post if it is password protected. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--post <value>` | no | Limit result set to comments assigned to specific post IDs. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--status <value>` | no | Limit result set to comments assigned a specific status. Requires authorization. |
| `--type <value>` | no | Limit result set to comments assigned a specific type. Requires authorization. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api comments-update [options]`

- What: postWpV2CommentsById — write (POST /wp/v2/comments/{id})
- Call: `POST /wp/v2/comments/{id}`, effect: write
- Body: `PostWpV2CommentsByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
