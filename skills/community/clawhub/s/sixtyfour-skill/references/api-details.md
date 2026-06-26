# Sixtyfour API — Detailed Reference

## Enrich Lead — Full Specification

### Endpoint
```
POST https://api.sixtyfour.ai/enrich-lead       (sync, timeout 15min)
POST https://api.sixtyfour.ai/enrich-lead-async  (async, returns task_id)
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lead_info` | object | Yes | Key-value pairs of known lead data (name, company, linkedin, etc.) |
| `struct` | object | Yes | Fields to collect — key is field name, value is description string or `{"description": "...", "type": "str\|int\|float\|bool\|list\|list[str]\|list[int]\|dict"}` |
| `research_plan` | string | No | Guide agent methodology — where to look and how |

### Response
```json
{
  "notes": "Research narrative...",
  "structured_data": { "...your struct fields filled..." },
  "references": { "url": "description of source" },
  "confidence_score": 9.5
}
```

### Type Casting
Supported types: `str`, `int`, `float`, `bool`, `list`, `list[str]`, `list[int]`, `list[float]`, `dict`. Priority: explicit type → input type → inferred → string.

---

## Enrich Company — Full Specification

### Endpoint
```
POST https://api.sixtyfour.ai/enrich-company       (sync)
POST https://api.sixtyfour.ai/enrich-company-async  (async)
```

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `target_company` | object | Yes | Company data (company_name, website, address, phone, etc.) |
| `struct` | object | Yes | Company fields to collect (same format as enrich-lead) |
| `lead_struct` | object | No | Fields to return per person found |
| `find_people` | boolean | No | Whether to discover people at the company |
| `research_plan` | string | No | Guide research methodology |
| `people_focus_prompt` | string | No | Describe which people to find (role, department, seniority) |

### Response
Same structure as enrich-lead, plus `structured_data.leads[]` array if `find_people: true`. Each lead includes a `score` (0-10) for relevance to `people_focus_prompt`.

---

## Find Email — Full Specification

### Endpoint
```
POST https://api.sixtyfour.ai/find-email
POST https://api.sixtyfour.ai/find-email-async
POST https://api.sixtyfour.ai/find-email-bulk-async  (up to 100 leads)
```

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lead` | object | Yes | name, company, title, phone, linkedin — more = better |
| `mode` | string | No | `"PROFESSIONAL"` (default, $0.05) or `"PERSONAL"` ($0.20) |

### Response
- `email`: `[["addr", "OK\|UNKNOWN", "COMPANY\|PERSONAL"]]`
- PERSONAL mode also returns `personal_email` field

---

## Find Phone — Full Specification

### Endpoint
```
POST https://api.sixtyfour.ai/find-phone
POST https://api.sixtyfour.ai/find-phone-async
POST https://api.sixtyfour.ai/find-phone-bulk-async  (up to 100 leads)
```

### Bulk via DataFrame
```
POST https://api.sixtyfour.ai/enrich-dataframe
{"csv_data": "name,company\nJohn,Acme", "enrichment_type": "phone"}
```

### Response Formats
- Single: `{"phone": "+1 555-123-4567"}`
- Multiple: `{"phone": [{"number": "+1...", "region": "US"}]}`
- Not found: `{"phone": ""}`

---

## QA Agent — Full Specification

### Endpoint
```
POST https://api.sixtyfour.ai/qa-agent
POST https://api.sixtyfour.ai/qa-agent-async
```

### Request Body
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `data` | object | Yes | Data to evaluate |
| `qualification_criteria` | array | Yes | Each: `{criteria_name, description, weight, threshold?}` |
| `references` | array | No | URLs for additional research: `[{url, description}]` |
| `struct` | object | No | Output field definitions |

---

## Search — Full Specification

### Start Search
```
POST https://api.sixtyfour.ai/search/start-deep-search
{"query": "...", "mode": "people", "max_results": 1000}
```
Returns: `{"task_id": "...", "status": "queued"}`

### Poll Status
```
GET https://api.sixtyfour.ai/search/deep-search-status/{task_id}
```
Statuses: `queued` → `running` → `completed` (includes `resource_handle_id`) or `failed`
Poll every 10-15 seconds.

### Download Results
```
GET https://api.sixtyfour.ai/search/download?resource_handle_id={id}
```
Returns signed URL (expires 15 min). Results in CSV format.

---

## Workflows — Management & Execution

### Manage
```
GET    /workflows                           — List all workflows
GET    /workflows/{id}                      — Get workflow definition
POST   /workflows                           — Create (workflow_name + workflow_definition)
PATCH  /workflows/{id}                      — Update (partial)
DELETE /workflows/{id}                      — Delete (204)
```

### Execute
```
POST /workflows/run?workflow_id={id}
{"webhook_payload": [{"company_name": "Acme", "website": "acme.com"}]}
```
Returns `{"job_id": "...", "status": "queued"}`

### Monitor
```
GET /workflows/runs/{run_id}/live_status    — Real-time progress (poll every 5-10s)
GET /workflows/runs?status=active           — List active runs
POST /workflows/cancel?job_id={id}          — Cancel a run
```

### Download Results
```
GET /workflows/runs/{run_id}/results/download-links
```
Returns signed CSV download URLs (expire 15 min).

### Available Block Types
`webhook`, `read_csv`, `enrich_company`, `enrich_lead`, `find_email`, `find_phone`, `qa_agent`

---

## Async Job Polling

All async endpoints return `{"task_id": "...", "status": "pending"}`.

```
GET https://api.sixtyfour.ai/job-status/{task_id}
```

Poll every 10s. Status values: `pending`, `processing`, `completed`, `failed`.

Completed response includes full `result` object.

---

## Webhook Notifications

Add `"webhook_url": "https://..."` to any async request. Payload on completion:
```json
{
  "task_id": "...",
  "status": "completed",
  "task_type": "enrich_lead",
  "result": { "...enriched data..." }
}
```
Retries: 5 attempts with exponential backoff (1s, 2s, 4s, 8s, 16s). 10s timeout per attempt.

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad request | Check required fields, validate JSON |
| 401 | Bad API key | Verify x-api-key header |
| 429 | Rate limited (500 req/min) | Implement backoff, use async |
| 500 | Server error | Retry after brief wait |

## Help
Email: team@sixtyfour.ai
