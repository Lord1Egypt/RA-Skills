# List IDs

`POST https://api.rootdata.com/open/skill/id_map`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `type` | int | true | Type: 1 Project 2 VC 3 People |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `id` | long | id |
| `name` | string | name |
| `token_symbol` | string | Token Ticker |
| `active` | boolean | true: Active; false: Inactive |
| `project_type` | string | Crypto or Non-Crypto |
