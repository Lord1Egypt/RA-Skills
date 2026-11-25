<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: widget-types

## `wordpress api widget-types-encode [options]`

- What: postWpV2WidgetTypesByIdEncode — write (POST /wp/v2/widget-types/{id}/encode)
- Call: `POST /wp/v2/widget-types/{id}/encode`, effect: write
- Body: `PostWpV2WidgetTypesByIdEncodeRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api widget-types-get [options]`

- What: getWpV2WidgetTypesById — read (GET /wp/v2/widget-types/{id})
- Call: `GET /wp/v2/widget-types/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api widget-types-list [options]`

- What: getWpV2WidgetTypes — read (GET /wp/v2/widget-types)
- Call: `GET /wp/v2/widget-types`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api widget-types-render [options]`

- What: postWpV2WidgetTypesByIdRender — write (POST /wp/v2/widget-types/{id}/render)
- Call: `POST /wp/v2/widget-types/{id}/render`, effect: write
- Body: `PostWpV2WidgetTypesByIdRenderRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
