# RD Hot Index Top 100

`POST https://api.rootdata.com/open/skill/hot_index`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Returns at most 100 projects. `days: 1` selects the current daily hot ranking; `days: 7` selects the weekly ranking. `eval` is the score on this ranking endpoint.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `days` | int | true | Only supports querying data for the past 1 day/7 days, 1 or 7. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `project_id` | long | Project ID |
| `rd_hot_index` | double | Hot Index |
| `rank` | int | Ranking |
| `logo` | string | Project Logo |
| `one_liner` | string | One sentence introduction |
| `token_symbol` | string | Token |
| `project_name` | string | Project Name |
| `tags` | array | Project tags (array of tag names) |
