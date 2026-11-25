<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: plugins

## `wordpress api plugins-create [options]`

- What: postWpV2Plugins — write (POST /wp/v2/plugins)
- Call: `POST /wp/v2/plugins`, effect: write
- Body: `PostWpV2PluginsRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api plugins-list [options]`

- What: getWpV2Plugins — read (GET /wp/v2/plugins)
- Call: `GET /wp/v2/plugins`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |
| `--search <value>` | no | Limit results to those matching a string. |
| `--status <value>` | no | Limits results to plugins with the given status. |
