# Calendar events

`POST https://api.rootdata.com/open/skill/get_event`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Only Beijing today through today + 4 days (five dates, inclusive). The server intersects requested dates with this window, including when `m_id` is set. A completely out-of-window request returns an empty page. Macroeconomic events are not included. Omitting dates selects the allowed window. Dates use `yyyy-MM-dd`.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `page` | int | false | Page number, default 1 |
| `page_size` | int | false | Items per page; default 10, maximum 100. |
| `m_id` | long | false | Project ID. If not provided, returns events for all projects. |
| `begin_time` | string | false | Event start date (yyyy-MM-dd), filters on hap_date field. |
| `end_time` | string | false | Event end date (yyyy-MM-dd), filters on hap_date field. |
| `type` | int | false | Event type: 1 Mainnet Launch, 2 Testnet Launch, 3 Security Incident, 4 Token Issuance (includes latest and planned), 5 Death Events, 7 Product Progress, 9 Others, 13 Unlock, 16 Conference & Event, 21 Incentive Events, 22 Public Sale Events. If not provided, returns all supported types. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `id` | long | Event ID |
| `project_id` | long | Project ID |
| `name` | string | Project name |
| `logo` | string | Project logo URL |
| `type` | int | Event type: 1 Mainnet Launch, 2 Testnet Launch, 3 Security Incident, 4 Token Issuance, 5 Death Events, 7 Product Progress, 9 Others, 13 Unlock, 16 Conference & Event, 21 Incentive Events, 22 Public Sale Events |
| `type_name` | string | Event type name (e.g. Mainnet Launch, Token Issuance, Security Incident, etc.) |
| `hap_date` | string | Event occurrence date (yyyy-MM-dd) |
| `o_name` | string | Event title/description (multilingual JSON with cn_value and en_value) |
| `site_url` | string | Event related URL |
| `start_date` | string | Event start date (yyyy-MM-dd, used for conference & event types) |
| `end_date` | string | Event end date (yyyy-MM-dd, used for conference & event types) |
