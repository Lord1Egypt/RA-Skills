<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: users

## `wordpress api users-application-passwords-delete [options]`

- What: deleteWpV2UsersByUserIdApplicationPasswordsByUuid — destructive (DELETE…
- Call: `DELETE /wp/v2/users/{user_id}/application-passwords/{uuid}`, effect: destructive
- Permission keys: `users.delete`

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | yes | user\_id |
| `--uuid <value>` | yes | uuid |

## `wordpress api users-application-passwords-delete-all [options]`

- What: deleteWpV2UsersByUserIdApplicationPasswords — destructive (DELETE…
- Call: `DELETE /wp/v2/users/{user_id}/application-passwords`, effect: destructive
- Permission keys: `users.delete`

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | yes | user\_id |

## `wordpress api users-create [options]`

- What: postWpV2Users — write (POST /wp/v2/users)
- Call: `POST /wp/v2/users`, effect: write
- Body: `PostWpV2UsersRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api users-delete [options]`

- What: deleteWpV2UsersById — destructive (DELETE /wp/v2/users/{id})
- Call: `DELETE /wp/v2/users/{id}`, effect: destructive
- Permission keys: `users.delete`, `users.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Required to be true, as users do not support trashing. |
| `--reassign <value>` | yes | Reassign the deleted user's posts and links to this user ID. |

## `wordpress api users-get [options]`

- What: getWpV2UsersById — read (GET /wp/v2/users/{id})
- Call: `GET /wp/v2/users/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api users-list [options]`

- What: getWpV2Users — read (GET /wp/v2/users)
- Call: `GET /wp/v2/users`, effect: read
- Pages: page number: send `page` (query), one more for each page; page size in `per_page` (query)

| Flag | Required | What |
|---|---|---|
| `--capabilities <value>` | no | Limit result set to users matching at least one specific capability provided. Accepts csv list or single capability. |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--exclude <value>` | no | Ensure result set excludes specific IDs. |
| `--has-published-posts <value>` | no | Limit result set to users who have published posts. |
| `--include <value>` | no | Limit result set to specific IDs. |
| `--offset <value>` | no | Offset the result set by a specific number of items. |
| `--order <value>` | no | Order sort attribute ascending or descending. |
| `--orderby <value>` | no | Sort collection by user attribute. |
| `--page <value>` | no | Current page of the collection. |
| `--per-page <value>` | no | Maximum number of items to be returned in result set. |
| `--roles <value>` | no | Limit result set to users matching at least one specific role provided. Accepts csv list or single role. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--search-columns <value>` | no | Array of column names to be searched. |
| `--slug <value>` | no | Limit result set to users with one or more specific slugs. |
| `--who <value>` | no | Limit result set to users who are considered authors. |
| `--all` | no | read every page, as the API pages it |

## `wordpress api users-me-create [options]`

- What: postWpV2UsersMe — write (POST /wp/v2/users/me)
- Call: `POST /wp/v2/users/me`, effect: write
- Body: `PostWpV2UsersMeRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api users-me-delete [options]`

- What: deleteWpV2UsersMe — destructive (DELETE /wp/v2/users/me)
- Call: `DELETE /wp/v2/users/me`, effect: destructive
- Permission keys: `users.delete`, `users.delete.force`

| Flag | Required | What |
|---|---|---|
| `--force <value>` | no | Required to be true, as users do not support trashing. |
| `--reassign <value>` | yes | Reassign the deleted user's posts and links to this user ID. |

## `wordpress api users-me-get [options]`

- What: getWpV2UsersMe — read (GET /wp/v2/users/me)
- Call: `GET /wp/v2/users/me`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api users-update [options]`

- What: postWpV2UsersById — write (POST /wp/v2/users/{id})
- Call: `POST /wp/v2/users/{id}`, effect: write
- Body: `PostWpV2UsersByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
