<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: sidebars

## `wordpress api sidebars-get [options]`

- What: getWpV2SidebarsById — read (GET /wp/v2/sidebars/{id})
- Call: `GET /wp/v2/sidebars/{id}`, effect: read

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api sidebars-list [options]`

- What: getWpV2Sidebars — read (GET /wp/v2/sidebars)
- Call: `GET /wp/v2/sidebars`, effect: read

| Flag | Required | What |
|---|---|---|
| `--context <value>` | no | Scope under which the request is made; determines fields present in response. |

## `wordpress api sidebars-update [options]`

- What: postWpV2SidebarsById — write (POST /wp/v2/sidebars/{id})
- Call: `POST /wp/v2/sidebars/{id}`, effect: write
- Body: `PostWpV2SidebarsByIdRequest`

| Flag | Required | What |
|---|---|---|
| `--id <value>` | yes | id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
