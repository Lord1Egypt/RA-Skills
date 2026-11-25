<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: widgets

## `wordpress api widgets-create [options]`

- What: postWpV2Widgets — write (POST /wp/v2/widgets)
- Call: `POST /wp/v2/widgets`, effect: write
- Body: `PostWpV2WidgetsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api widgets-delete [options]`

- What: deleteWpV2WidgetsById — destructive (DELETE /wp/v2/widgets/{id})
- Call: `DELETE /wp/v2/widgets/{id}`, effect: destructive
- Permission keys: `widgets.delete`, `widgets.delete.force`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--force <value>` | no | Whether to force removal of the widget, or move it to the inactive sidebar. |

## `wordpress api widgets-get [options]`

- What: getWpV2WidgetsById — read (GET /wp/v2/widgets/{id})
- Call: `GET /wp/v2/widgets/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api widgets-list [options]`

- What: getWpV2Widgets — read (GET /wp/v2/widgets)
- Call: `GET /wp/v2/widgets`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--sidebar <value>` | no | The sidebar to return widgets for. |

## `wordpress api widgets-update [options]`

- What: postWpV2WidgetsById — write (POST /wp/v2/widgets/{id})
- Call: `POST /wp/v2/widgets/{id}`, effect: write
- Body: `PostWpV2WidgetsByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
