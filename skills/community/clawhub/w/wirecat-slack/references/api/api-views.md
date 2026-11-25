<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: views

## `slk api views open [options]`

- What: views\_open — write (GET /views.open)
- Call: `GET /views.open`, effect: write

| Flag | Required | What |
|---|---|---|
| `--trigger-id <value>` | yes | Exchange a trigger to post to the user. |
| `--view <value>` | yes | A \[view payload\](https://api.slack.com/reference/surfaces/views). This must be a JSON-encoded string. |

## `slk api views publish [options]`

- What: views\_publish — write (GET /views.publish)
- Call: `GET /views.publish`, effect: write

| Flag | Required | What |
|---|---|---|
| `--user-id <value>` | yes | \`id\` of the user you want publish a view to. |
| `--view <value>` | yes | A \[view payload\](https://api.slack.com/reference/surfaces/views). This must be a JSON-encoded string. |
| `--hash <value>` | no | A string that represents view state to protect against possible race conditions. |

## `slk api views push [options]`

- What: views\_push — write (GET /views.push)
- Call: `GET /views.push`, effect: write

| Flag | Required | What |
|---|---|---|
| `--trigger-id <value>` | yes | Exchange a trigger to post to the user. |
| `--view <value>` | yes | A \[view payload\](https://api.slack.com/reference/surfaces/views). This must be a JSON-encoded string. |

## `slk api views update [options]`

- What: views\_update — write (GET /views.update)
- Call: `GET /views.update`, effect: write

| Flag | Required | What |
|---|---|---|
| `--view-id <value>` | no | A unique identifier of the view to be updated. Either \`view\_id\` or \`external\_id\` is required. |
| `--external-id <value>` | no | A unique identifier of the view set by the developer. Must be unique for all views on a team. Max length of 255 characters. Either \`view\_id\` or \`external\_id\` is required. |
| `--view <value>` | no | A \[view object\](https://api.slack.com/reference/surfaces/views). This must be a JSON-encoded string. |
| `--hash <value>` | no | A string that represents view state to protect against possible race conditions. |
