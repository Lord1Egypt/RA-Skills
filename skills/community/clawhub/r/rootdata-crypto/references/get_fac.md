# Funding rounds

`POST https://api.rootdata.com/open/skill/get_fac`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Only the last six calendar months through Beijing today. The server intersects requested dates with this window, even when filtering by round `id` or `project_id`. Out-of-window requests return an empty page. Each round includes at most five investors, in source order (lead investors first). `valuation` is included when available. Month inputs expand to their first/last date before clipping.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `page` | int | false | Page number, default 1. |
| `page_size` | int | false | Items per page; default 10, maximum 100. |
| `start_time` | string | false | Announcement date (start) yyyy-MM |
| `end_time` | string | false | Announcement date (end) yyyy-MM |
| `min_amount` | int | false | Minimum fundraising amount (in USD) |
| `max_amount` | int | false | Maximum fundraising amount (USD) |
| `project_id` | int | false | Project ID |
| `id` | long | false | Financing record ID for precise single record query, can be combined with other filter conditions. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `id` | long | Financing record ID |
| `logo` | string | The URL of the project logo. |
| `name` | string | Project Name |
| `rounds` | string | Round Name |
| `published_time` | string | Announcement date |
| `amount` | long | Fundraising amount (USD) |
| `project_id` | int | Project ID |
| `valuation` | long | Valuation (USD) |
| `invests` | array | Investor information array, including Logo and Name. |
| `invests.type` | int | Type: 1 Project 2 VC 3 People |
| `invests.invest_id` | int | Investor ID |
| `invests.name` | string | Investor Name |
| `invests.logo` | string | Investor Logo |
| `invests.lead_investor` | int | Is it a leading investor? 1: Yes, 0: No |
| `invests.rootdataurl` | string | RootData link |
| `data_status` | int | Whether this financing is credible |
| `source_url` | string | The link to the source of this financing information |
| `X` | string | X link |
| `one_liner` | string | A brief introduction. |
