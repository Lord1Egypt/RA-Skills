# X hot projects

`POST https://api.rootdata.com/open/skill/hot_project_on_x`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `heat` | boolean | true | X Hot Projects Ranking List |
| `influence` | boolean | true | X Influence Ranking List |
| `followers` | boolean | true | X Followers Ranking |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `heat` | array | Hot Ranking |
| `heat.score` | string | Hot Index / Influence Index / Followers Number |
| `heat.project_id` | long | Project ID |
| `heat.logo` | string | Project Logo |
| `heat.one_liner` | string | One sentence introduction |
| `heat.project_name` | string | Project Name |
| `heat.token_symbol` | string | Token Ticker |
| `influence` | array | Influence Ranking |
| `influence.score` | string | Hot Index/Influence Index/Followers number |
| `influence.project_id` | long | Project ID |
| `influence.logo` | string | Project Logo |
| `influence.one_liner` | string | One sentence introduction |
| `influence.project_name` | string | Project Name |
| `influence.token_symbol` | string | Token Ticker |
| `followers` | array | Followers Ranking |
| `followers.score` | string | Hot Index/Influence Index/Followers number |
| `followers.project_id` | long | Project ID |
| `followers.logo` | string | Project Logo |
| `followers.one_liner` | string | One sentence introduction |
| `followers.project_name` | string | Project Name |
| `followers.token_symbol` | string | Token Ticker |
