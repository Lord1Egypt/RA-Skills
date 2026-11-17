# RD Growth Index Top 300

`POST https://api.rootdata.com/open/skill/get_rd_top300`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

## Request body

Use `{}`; this endpoint has no query parameters.

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `project_id` | long | Project ID |
| `project_name` | string | Project Name |
| `logo` | string | Project Logo URL |
| `rd_score` | decimal | RD Growth Index score |
| `rd_rank` | int | RD Growth Index ranking (1~300) |
