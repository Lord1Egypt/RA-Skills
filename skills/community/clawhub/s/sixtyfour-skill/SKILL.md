---
name: sixtyfour
description: "People and company intelligence via the Sixtyfour AI API. AI research agents that read the live web — not static databases — to return structured, confidence-scored profiles. Use when you need to: (1) enrich a lead with full profile data (name, title, email, phone, LinkedIn, tech stack, funding, pain points — up to 50 custom fields), (2) research a company (team size, tech stack, funding rounds, hiring signals, key people), (3) find someone's professional or personal email address, (4) find phone numbers, (5) score/qualify leads against custom criteria with reasoning, (6) search for people or companies via natural language query, or (7) run batch enrichment workflows via API. NOT for: general web browsing, tasks unrelated to people/company data, or non-enrichment research."
---

# Sixtyfour AI — People & Company Intelligence

AI research agents that investigate people and companies across the live web, returning structured, confidence-scored data. 93% accuracy — benchmarked against Clay (66%), Apollo (72%), and ZoomInfo.

**Base URL:** `https://api.sixtyfour.ai`  
**Auth header:** `x-api-key: YOUR_API_KEY` (all requests)  
**Free tier:** 50 deep researches on signup — [app.sixtyfour.ai](https://app.sixtyfour.ai) (Google sign-in, API key available immediately)  
**Docs:** [docs.sixtyfour.ai](https://docs.sixtyfour.ai)  
**OpenAPI spec:** [api.sixtyfour.ai/openapi.json](https://api.sixtyfour.ai/openapi.json)

## Setup

```bash
# 1. Sign up at https://app.sixtyfour.ai (Google sign-in)
# 2. Sidebar → Keys → Create new key
export SIXTYFOUR_API_KEY="your_key_here"
```

## API Quick Reference

| Endpoint | Method | Description | Sync/Async |
|----------|--------|-------------|------------|
| `/enrich-lead` | POST | Full person profile from name + company | Both |
| `/enrich-company` | POST | Deep company research + people discovery | Both |
| `/find-email` | POST | Professional ($0.05) or personal ($0.20) email | Both |
| `/find-phone` | POST | Phone number discovery | Both |
| `/qa-agent` | POST | Score/qualify leads against custom criteria | Both |
| `/search/start-deep-search` | POST | Find people/companies via natural language | Async |
| `/search/start-filter-search` | POST | Structured filter search (skips LLM parsing) | Sync |
| `/workflows/run` | POST | Execute batch enrichment pipelines | Async |

All enrichment endpoints have async variants (append `-async`) returning `task_id` for polling via `GET /job-status/{task_id}`. Use async for production workloads.

---

## Enrich Lead

The core endpoint. Give it a name — get back a full profile with any fields you define.

```bash
curl -X POST "https://api.sixtyfour.ai/enrich-lead" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_info": {
      "name": "Jane Doe",
      "company": "Acme Corp"
    },
    "struct": {
      "full_name": "Full name",
      "title": "Current job title",
      "seniority": "Seniority level (C-suite, VP, Director, Manager, IC)",
      "department": "Department or function",
      "email": "Work email address",
      "personal_email": "Personal email address",
      "phone": "Phone number",
      "linkedin": "LinkedIn profile URL",
      "location": "City and state",
      "company_name": "Current company",
      "company_size": {"description": "Approximate employee count", "type": "int"},
      "tech_stack": {"description": "Tools and technologies they use daily", "type": "list[str]"},
      "funding_stage": "Company latest funding stage and amount",
      "pain_points": {"description": "Likely challenges based on role and company stage", "type": "list[str]"},
      "social_profiles": {"description": "Twitter, GitHub, personal blog URLs", "type": "list[str]"},
      "recent_activity": "Notable recent posts, talks, or job changes"
    },
    "research_plan": "Check LinkedIn profile, company website about page, Twitter, GitHub, and any recent conference talks or blog posts."
  }'
```

### Response

```json
{
  "structured_data": {
    "full_name": "Jane Doe",
    "title": "VP of Engineering",
    "seniority": "VP",
    "department": "Engineering",
    "email": "jane@acme.com",
    "phone": "+1-555-0123",
    "linkedin": "https://linkedin.com/in/janedoe",
    "tech_stack": ["React", "Python", "AWS", "Terraform"],
    "funding_stage": "Series B, $45M (2025)",
    "pain_points": ["Scaling engineering team post-Series B", "Migrating legacy infrastructure"]
  },
  "notes": "Research narrative with sources...",
  "references": {
    "https://linkedin.com/in/janedoe": "LinkedIn profile",
    "https://acme.com/about": "Company about page"
  },
  "confidence_score": 9.2
}
```

### Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lead_info` | object | Yes | Known data: `name`, `company`, `linkedin_url`, `email`, `domain`, etc. |
| `struct` | object | Yes | Fields to collect. Value is either a plain-English description string or `{"description": "...", "type": "str\|int\|float\|bool\|list[str]\|dict"}` |
| `research_plan` | string | No | Guides where the agent looks — specific sources, methodology |

**Timeouts:** P95 ~5 min, max ~10 min. Set client timeout to 15+ min or use `/enrich-lead-async`.

---

## Enrich Company

Deep company research with optional people discovery.

```bash
curl -X POST "https://api.sixtyfour.ai/enrich-company" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target_company": {
      "company_name": "Stripe",
      "website": "stripe.com"
    },
    "struct": {
      "description": "One-line company description",
      "employee_count": {"description": "Approximate headcount", "type": "int"},
      "tech_stack": {"description": "Key technologies used", "type": "list[str]"},
      "recent_funding": "Most recent funding round, amount, and date",
      "hiring_signals": {"description": "Open roles indicating growth areas", "type": "list[str]"},
      "competitors": {"description": "Main competitors", "type": "list[str]"}
    },
    "find_people": true,
    "people_focus_prompt": "Find the VP of Engineering and CTO",
    "lead_struct": {
      "name": "Full name",
      "title": "Job title",
      "linkedin": "LinkedIn URL",
      "email": "Work email"
    }
  }'
```

### People Discovery Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `find_people` | bool | Enable people discovery at the company |
| `people_focus_prompt` | string | Describe who to find (role, department, seniority) |
| `lead_struct` | object | Fields to return per person found (same format as `struct`) |

Each person returned includes a `score` (0-10) for relevance to `people_focus_prompt`.

---

## Find Email

```bash
# Professional email ($0.05 per call)
curl -X POST "https://api.sixtyfour.ai/find-email" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead": {"name": "Saarth Shah", "company": "Sixtyfour AI"},
    "mode": "PROFESSIONAL"
  }'
```

**Response:** `{"email": [["saarth@sixtyfour.ai", "OK", "COMPANY"]], "cost_cents": 5}`

```bash
# Personal email ($0.20 per call)
curl -X POST "https://api.sixtyfour.ai/find-email" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead": {"name": "Jane Doe", "company": "Acme Corp"},
    "mode": "PERSONAL"
  }'
```

**Email field format:** `[["email@domain.com", "OK|UNKNOWN", "COMPANY|PERSONAL"]]`

**Bulk:** Use `/find-email-bulk-async` with `{"leads": [...]}` for up to 100 leads.

---

## Find Phone

```bash
curl -X POST "https://api.sixtyfour.ai/find-phone" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead": {
      "name": "John Doe",
      "company": "Example Corp",
      "linkedin_url": "https://linkedin.com/in/johndoe"
    }
  }'
```

Provide as much context as possible (name, company, LinkedIn, email, domain) for best hit rate.

**Bulk:** Use `/find-phone-bulk-async` for up to 100 leads, or `/enrich-dataframe` with CSV:
```bash
curl -X POST "https://api.sixtyfour.ai/enrich-dataframe" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"csv_data": "name,company\nJohn Doe,Example Corp", "enrichment_type": "phone"}'
```

---

## QA Agent — Score & Qualify Leads

Evaluate enriched data against custom criteria. Returns scores and reasoning.

```bash
curl -X POST "https://api.sixtyfour.ai/qa-agent" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "name": "Alex Johnson",
      "title": "VP Engineering",
      "company": "TechStartup",
      "funding": "Series B",
      "tech_stack": ["React", "AWS", "PostgreSQL"]
    },
    "qualification_criteria": [
      {"criteria_name": "Seniority", "description": "VP level or above", "weight": 10.0, "threshold": 8.0},
      {"criteria_name": "Company Stage", "description": "Series A-C, actively growing", "weight": 8.0},
      {"criteria_name": "Tech Fit", "description": "Uses modern web stack", "weight": 6.0}
    ],
    "struct": {
      "overall_score": {"description": "Composite score 0-10", "type": "float"},
      "verdict": "ACCEPT or REJECT",
      "reasoning": "Why this lead does or does not qualify"
    }
  }'
```

Optional: add `"references": [{"url": "https://...", "description": "Company blog"}]` for additional context.

---

## Search — Find People or Companies

### Deep Search (natural language, async)

```bash
# Start search
curl -X POST "https://api.sixtyfour.ai/search/start-deep-search" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "VP of Engineering at Series B SaaS startups in New York", "max_results": 100}'

# Returns: {"task_id": "abc123", "status": "queued"}

# Poll (every 10-15s)
curl "https://api.sixtyfour.ai/search/deep-search-status/abc123" \
  -H "x-api-key: $SIXTYFOUR_API_KEY"

# Download results (when status = "completed", use resource_handle_id)
curl "https://api.sixtyfour.ai/search/download?resource_handle_id=xyz789" \
  -H "x-api-key: $SIXTYFOUR_API_KEY"
# Returns signed URL (expires 15 min) → CSV download
```

### Filter Search (structured, synchronous)

```bash
curl -X POST "https://api.sixtyfour.ai/search/start-filter-search" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"filters": {"title": "VP Engineering", "location": "New York", "company_size": "50-200"}}'
# Returns: {"resource_handle_id": "...", "total_results": 150, "exported_count": 150}
```

---

## Workflows — Batch Enrichment Pipelines

Chain blocks into reusable pipelines. Trigger via API with webhook payloads.

```bash
# List available workflow blocks
curl "https://api.sixtyfour.ai/workflows/blocks" \
  -H "x-api-key: $SIXTYFOUR_API_KEY"

# Run a workflow (webhook-triggered)
curl -X POST "https://api.sixtyfour.ai/workflows/run?workflow_id=YOUR_WORKFLOW_ID" \
  -H "x-api-key: $SIXTYFOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"webhook_payload": [{"company_name": "Acme", "website": "acme.com"}]}'

# Monitor progress (poll every 5-10s)
curl "https://api.sixtyfour.ai/workflows/runs/RUN_ID/live_status" \
  -H "x-api-key: $SIXTYFOUR_API_KEY"

# Download results
curl "https://api.sixtyfour.ai/workflows/runs/RUN_ID/results/download-links" \
  -H "x-api-key: $SIXTYFOUR_API_KEY"
```

Block types: `webhook`, `read_csv`, `enrich_company`, `enrich_lead`, `find_email`, `find_phone`, `qa_agent`

Manage workflows: `GET /workflows` (list), `POST /workflows/create_workflow`, `POST /workflows/update_workflow`, `POST /workflows/delete_workflow`

---

## Webhooks — Async Notifications

Add `"webhook_url"` to any async request body:

```json
{"lead_info": {...}, "struct": {...}, "webhook_url": "https://your-server.com/hook"}
```

Sixtyfour POSTs `{task_id, status, task_type, result}` on completion. 5 retries with exponential backoff.

---

## Common Patterns

**Signup enrichment:** New user email → `/enrich-lead` with role, tech stack, funding fields → push to CRM  
**CRM backfill:** Export contacts → `/enrich-lead-async` in parallel → poll → download enriched data  
**Lead scoring pipeline:** `/enrich-lead` → `/qa-agent` with custom ICP criteria → route by verdict  
**Prospect list building:** `/search/start-deep-search` with ICP description → CSV → `/find-email` per lead  
**Account intelligence:** `/enrich-company` with `find_people: true` → weekly Slack digest of changes  

---

## Error Handling & Rate Limits

- **Rate limit:** 500 requests/min per API key
- **Errors:** `{"error": "ErrorType", "message": "Details"}`
- **HTTP codes:** 400 (bad request), 401 (invalid key), 429 (rate limited), 500 (retry)
- **Async polling:** Use `GET /job-status/{task_id}` — statuses: `pending` → `processing` → `completed` | `failed`

---

## MCP Server

For Claude Desktop, Cursor, Windsurf, or any MCP client:

```json
{
  "mcpServers": {
    "sixtyfour": {
      "command": "npx",
      "args": ["-y", "sixtyfour-mcp"],
      "env": {"SIXTYFOUR_API_KEY": "your_key"}
    }
  }
}
```

Then ask naturally: "Find the email and phone number for the CTO of Stripe" — the assistant calls Sixtyfour automatically.

---

**Support:** team@sixtyfour.ai | [docs.sixtyfour.ai](https://docs.sixtyfour.ai) | [app.sixtyfour.ai](https://app.sixtyfour.ai)
