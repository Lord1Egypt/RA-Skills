<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# WordPress API: settings

## `wordpress api settings-create [options]`

- What: postWpV2Settings — write (POST /wp/v2/settings)
- Call: `POST /wp/v2/settings`, effect: write
- Body: `PostWpV2SettingsRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `wordpress api settings-list`

- What: getWpV2Settings — read (GET /wp/v2/settings)
- Call: `GET /wp/v2/settings`, effect: read
