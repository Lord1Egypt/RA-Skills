# X popular people

`POST https://api.rootdata.com/open/skill/leading_figures_on_crypto_x`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `page` | int | false | Page number, default 1 |
| `page_size` | int | false | Items per page; default 100, maximum 100. |
| `rank_type` | string | false | heat (default) or influence. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `people_id` | long | ID |
| `score` | string | Hot Index / Influence Index |
| `head_img` | string | Logo |
| `one_liner` | string | One sentence introduction |
| `people_name` | string | People name |
