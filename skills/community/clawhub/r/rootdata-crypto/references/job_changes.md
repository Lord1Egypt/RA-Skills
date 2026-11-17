# Personnel position changes

`POST https://api.rootdata.com/open/skill/job_changes`

Send `Authorization: Bearer {ROOTDATA_SKILL_KEY}`, `Content-Type: application/json`, and optionally `language: cn` (default: `en`).
Success envelope: `{"result":200,"data":...}`. Fields without source data can be null or absent.

Uses the same result set as OpenAPI Pro. The old skill-specific 20-entry cap is removed. Enable the desired `recent_joinees` / `recent_resignations` flags; both false returns an empty object.

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `recent_joinees` | boolean | true | Recent employment. |
| `recent_resignations` | boolean | true | Recent resignation. |

## Response fields

| Field | Type | Meaning |
|---|---|---|
| `recent_joinees` | array | Recent employment. |
| `recent_joinees.people_id` | long | People ID |
| `recent_joinees.head_img` | string | Logo |
| `recent_joinees.people_name` | string | People Name |
| `recent_joinees.company` | string | Company |
| `recent_joinees.position` | string | Position |
| `recent_joinees.X` | string | X |
| `recent_joinees.linkedin` | string | linkedin |
| `recent_resignations` | array | Recent resignation. |
| `recent_resignations.people_id` | long | People ID |
| `recent_resignations.head_img` | string | Profile picture |
| `recent_resignations.people_name` | string | People Name |
| `recent_resignations.company` | string | Company |
| `recent_resignations.position` | string | Position |
| `recent_resignations.X` | string | X |
| `recent_resignations.linkedin` | string | linkedin |
