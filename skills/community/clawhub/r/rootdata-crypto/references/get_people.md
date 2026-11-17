# Person details

`POST https://api.rootdata.com/open/skill/get_people`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `people_id` | long | true | People ID |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `people_id` | long | ID |
| `introduce` | string | Detailed Introduction |
| `head_img` | string | Logo |
| `one_liner` | string | One sentence introduction |
| `X` | string | X link |
| `people_name` | string | People name |
| `linkedin` | string | LinkedIn Link |
| `heat` | string | X Hot Index |
| `heat_rank` | int | X Hot Ranking |
| `influence` | string | X Influence Index |
| `influence_rank` | int | X Influence Ranking |
| `followers` | int | Number of followers |
| `following` | int | Number of following |
| `education_experience` | array | Education experience list |
| `education_experience.school_name` | string | School name |
| `education_experience.school_logo` | string | School logo URL |
