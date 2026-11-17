# Search projects, investors and people

`POST https://api.rootdata.com/open/skill/ser_inv`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `query` | string | true | Search keywords, which can be project/VC names, tokens, or other related terms. |
| `precise_x_search` | boolean | false | Based on X Handle (@...), accurately search for corresponding entity. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `id` | int | Unique Identifier |
| `type` | int | 1 Project; 2 VC; 3 People |
| `name` | string | Name |
| `logo` | string | URL of the logo |
| `introduce` | string | Introduction |
| `active` | boolean | true: Active; false: Inactive |
| `rootdataurl` | string | Corresponding RootData link. |
