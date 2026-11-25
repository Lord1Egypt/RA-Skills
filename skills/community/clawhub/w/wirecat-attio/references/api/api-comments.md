<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Comments

## `attio api comments-create [options]`

- What: Create a comment
- Call: `POST /v2/comments`, effect: write
- Sign-in: oauth2 (comment:read-write)
- Body: `PostV2CommentsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api comments-delete [options]`

- What: Delete a comment
- Call: `DELETE /v2/comments/{comment_id}`, effect: destructive
- Sign-in: oauth2 (comment:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--comment-id <value>` | yes | comment\_id |

## `attio api comments-get [options]`

- What: Get a comment
- Call: `GET /v2/comments/{comment_id}`, effect: read
- Sign-in: oauth2 (comment:read)

| Flag | Required | What |
|---|---|---|
| `--comment-id <value>` | yes | comment\_id |
