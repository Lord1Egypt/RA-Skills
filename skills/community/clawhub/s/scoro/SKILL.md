---
name: scoro
description: "Scoro API v2 integration for time tracking, task management, utilization reporting, team status reports, and billable corrections. Use when: user asks about Scoro tasks, time entries, hours (billable/non-billable), utilization reports, team status, or any Scoro data."
homepage: https://api.scoro.com/api/v2
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "env": ["SCORO_API_KEY", "SCORO_COMPANY_URL"] },
        "primaryEnv": "SCORO_API_KEY",
      },
  }
---

# Scoro Integration

Full Scoro API v2 integration for OpenClaw. Provides task management, time tracking, hours calculation, utilization reports, team dashboards, and billable status corrections.

## Setup

1. Get your Scoro API key from **Settings → External connections → API** in your Scoro account.
2. Set your company URL (e.g. `https://yourcompany.scoro.com/api/v2`).
3. Add both to your OpenClaw config:

```json
{
  "env": {
    "vars": {
      "SCORO_API_KEY": "ScoroAPI_your_key_here",
      "SCORO_COMPANY_URL": "https://yourcompany.scoro.com/api/v2"
    }
  }
}
```

4. Add `"scoro"` to your agent's skills list in `openclaw.json`.


## Standard Prompts

Users can trigger these capabilities with natural language:

### Task Management
- `fetch my scoro tasks` / `show my tasks for this week`
- `fetch tasks for <user email or name>`
- `show overdue tasks`

### Hours & Time Entries
- `show my hours this week` / `how many hours have I logged?`
- `calculate my billable hours` / `show billable vs non-billable hours`
- `send me a report of my billable and non-billable hours`
- `show time entries for <user> from <date> to <date>`

### Team & Manager Reports
- `show team status` / `team pulse`
- `generate team hours report`

### Utilization Reporting
- `generate weekly utilization report`
- `show billable ratio for <user>`

### Billable Corrections
- `find incorrect billable entries`
- `fix billable status for entries <IDs>`
- `adjust all logs on task X to be billable`


## Environment Variables

- `SCORO_COMPANY_URL` — full base URL (e.g. `https://yourcompany.scoro.com/api/v2`)
- `SCORO_API_KEY` — company API key (starts with `ScoroAPI_`)

Both must be set in `openclaw.json` under `env.vars`. They are available as shell environment variables. Do NOT use `.env` files.


## API Basics

**All Scoro API v2 requests are POST.** Every request body must include `apiKey` and `company_account_id`.

The `company_account_id` is the subdomain from your Scoro URL. For `https://yourcompany.scoro.com`, it is `yourcompany`.

### Example Request (curl)

```bash
curl -X POST "$SCORO_COMPANY_URL/timeEntries/list" \
  -H "Content-Type: application/json" \
  -d '{
    "apiKey": "'"$SCORO_API_KEY"'",
    "company_account_id": "yourcompany",
    "filter": {
      "time_entry_date": {
        "from": "2026-03-10",
        "to": "2026-03-16"
      },
      "user_ids": [123]
    },
    "per_page": 100,
    "page": 1,
    "detailed_response": true
  }'
```

### Example Request (PowerShell / Windows)

```powershell
$body = @{
    apiKey = $env:SCORO_API_KEY
    company_account_id = 'yourcompany'
    filter = @{
        time_entry_date = @{ from = '2026-03-10'; to = '2026-03-16' }
        user_ids = @(123)
    }
    per_page = 100
    page = 1
    detailed_response = $true
} | ConvertTo-Json -Depth 10

$response = Invoke-RestMethod -Method Post `
    -Uri "$env:SCORO_COMPANY_URL/timeEntries/list" `
    -ContentType 'application/json' -Body $body
```


## Key Endpoints

All endpoints: `POST $SCORO_COMPANY_URL/{module}/{action}`

| Endpoint | Purpose |
|----------|---------|
| `tasks/list` | Fetch tasks with filters |
| `tasks/view/ID` | View single task details |
| `timeEntries/list` | Fetch time entries (with date, user, billable filters) |
| `timeEntries/modify/ID` | Update a time entry (e.g. fix billable status) |
| `users/list` | Fetch all users (includes reporting manager info) |
| `projects/list` | Fetch projects |
| `contacts/list` | Fetch contacts |


## Filtering

### Tasks

```json
{
  "filter": {
    "responsible_person_ids": [123],
    "deadline": { "from": "2026-03-16", "to": "2026-03-22" },
    "status": "in_progress"
  }
}
```

- `responsible_person_ids` — array of assigned user IDs
- `deadline` — `{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}`
- `modified_date` — `{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}`

### Time Entries

**CRITICAL: The date filter field is `time_entry_date` with `from`/`to` keys. NOT `start_date`/`end_date`.**

```json
{
  "filter": {
    "time_entry_date": { "from": "2026-03-10", "to": "2026-03-16" },
    "user_ids": [123]
  }
}
```

- `user_ids` — **array** of user IDs (not a single value)

### Users

No specific filter needed. Returns all active users.


## Response Fields

### Task Fields
- `event_id` — unique task ID
- `event_name` — task name/title
- `datetime_due` — deadline (ISO datetime)
- `is_completed` — 0 or 1
- `activity_type` — project/category name
- `responsible_person_id` — assigned user ID
- `description` — task description

### Time Entry Fields
- `time_entry_id` — unique ID
- `user_id` — the user who logged it
- `duration` — format "HH:MM:SS" (e.g. "01:30:00" = 1.5h)
- `title` — task/event name
- `billable_time_type` — "billable", "non_billable", or "custom"
- `time_entry_date` — "YYYY-MM-DD"
- `event_id` — the task/event this entry is for
- `is_billable` — 0 or 1

### User Fields
- `id` — unique user ID
- `full_name` — display name
- `email` — email address
- `position` — job title

### Duration Parsing
Format is "HH:MM:SS". Convert to decimal hours: `hours + minutes/60 + seconds/3600`.


## Pagination — CRITICAL

**Scoro caps page size at 25 items regardless of `per_page` setting.**

You MUST paginate through ALL pages for any list operation:

```
page = 1
all_results = []
loop:
  response = POST .../endpoint { per_page: 100, page: page }
  if length(response.data) == 0: break
  all_results += response.data
  page += 1
  sleep 1 second (rate limit)
```

**Important:** Do NOT use `data.length < per_page` as a stop condition — the API returns a max of 25 items per page even if you request 100. Stop when a page returns 0 results.


## Calculating Hours

1. Determine date range (default: this week Monday to today)
2. Fetch all time entries for the date range and user(s), paginating all pages
3. Calculate:
   ```
   total_hours = sum(duration)
   billable_hours = sum(duration where billable_time_type == "billable")
   non_billable_hours = sum(duration where billable_time_type == "non_billable")
   billable_ratio = (billable_hours / total_hours) * 100
   ```
4. Present with 2 decimal places


## Team Reports

Teams are organized by direct manager (reporting lines).

### Workflow for Team Status

1. Resolve user IDs for all team members (by email, from `users/list`, all pages)
2. Fetch today's time entries for all team members at once
3. Per member: total hours, billable split, latest task name
4. Calculate team totals and billable ratio


## Billable Status Correction

### Detection
1. Retrieve time entries for the period
2. Retrieve task billing type for each task
3. Flag mismatches: task is billable but time entry is non_billable

### Correction
```json
POST /timeEntries/modify/<ENTRY_ID>
{
  "apiKey": "...",
  "company_account_id": "yourcompany",
  "request": {
    "billable_time_type": "billable"
  }
}
```

**Always confirm with the user before modifying entries.**


## Rate Limits

- 2-second rate limit window
- Add 1-second delay between paginated API calls
- On 429 errors, wait and retry


## Response Format

```json
{
  "status": "OK",
  "statusCode": 200,
  "messages": null,
  "data": []
}
```


## All Available Modules

`tasks`, `timeEntries`, `users`, `projects`, `contacts`, `invoices`, `quotes`, `orders`, `bills`, `expenses`, `products`, `calendarEvents`, `bookings`, `purchaseOrders`, `tags`, `customModules`, `vatCodes`, `financeAccounts`

Each module supports: `list`, `view`, `modify`, `delete`.

**Use `modify` and `delete` only with explicit user permission.**


## Notes

- All requests are POST (even "list" and "view")
- Always include `apiKey` and `company_account_id` in the JSON body
- Use `detailed_response: true` for full field data in list requests
- Duration format: "HH:MM:SS" → convert to decimal hours for reporting
- The `lang` parameter is optional (defaults to site language)
- On Windows, prefer PowerShell `Invoke-RestMethod` over curl
