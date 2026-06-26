---
name: smart-api-connector
description: "Connect to any REST API using the agent's built-in web_fetch. Handles authentication headers, JSON payloads, error parsing, and retries. Use when: user wants to query an API, test an endpoint, automate API calls, parse API responses, or integrate with external services. Homepage: https://clawhub.ai/skills/smart-api-connector"
---

# Smart API Connector v3.0

**Install:** `clawhub install smart-api-connector`

REST API integration using built-in tools. No code, no curl, no dependencies.

## Language

Detect from user's message language. Default: English.

## Quick Start

User provides: API URL + what they want. Agent handles everything.

> User: "Hent brukerinfo fra https://api.example.com/v1/users/123"
>
> Agent runs: `web_fetch https://api.example.com/v1/users/123` (with auth headers if provided)
>
> Returns parsed response.

## Authentication

### API Key in Header

```
web_fetch url --headers '{"Authorization": "Bearer KEY", "X-API-Key": "KEY"}'
```

### API Key via Environment Variable

```
exec: API_KEY="your_key" curl -s -H "Authorization: Bearer $API_KEY" "https://..."
```

### Session-only Keys

API keys provided in conversation are used in-session only. Never persisted to files.

## Error Handling

| HTTP Status | Action |
|-------------|--------|
| 200-299 | Parse and return response |
| 429 | Rate limited — wait and retry (max 3 retries) |
| 400 | Bad request — show error, suggest fix |
| 401/403 | Auth failed — check key, permissions |
| 404 | Not found — verify URL |
| 5xx | Server error — retry once, then report |

## HTTP Methods

| Method | Use Case |
|--------|----------|
| GET | Fetch data |
| POST | Create data / send JSON body |
| PUT | Update data |
| DELETE | Remove data |

For POST/PUT: prompt user for JSON body if not provided.

## Response Parsing

Always extract and present the useful parts. For JSON APIs:

```
Response:
  Name: John
  Email: john@example.com
  Created: 2026-03-28

Raw: {first 200 chars if user wants detail}
```

## Security

- Keys are session-only — never written to files
- Prefer environment variables over command-line args
- Scoped/test keys over production secrets
- Show user the exact request before executing (URL + method + headers, not the key value)

## Quick Commands

| User says | Action |
|-----------|--------|
| "query {url}" | GET request |
| "POST to {url}" | POST with body |
| "test API {url}" | Request + show response |
| "API health check" | GET and report status |

## Guidelines for Agent

1. **Use web_fetch first** — built-in, no dependencies
2. **Fall back to exec/curl** only if web_fetch can't handle the request
3. **Never persist API keys** — session only
4. **Show request before executing** — confirm with user for POST/PUT/DELETE
5. **Parse responses** — extract useful data, don't dump raw JSON
6. **Handle errors gracefully** — retry on 429, explain 401/403
7. **Match user language** in responses

## What This Skill Does NOT Do

- Does NOT persist API keys or credentials
- Does NOT require npm packages or external tools
- Does NOT modify any local files
- Does NOT make requests without user knowledge (for POST/PUT/DELETE)

## More by TommoT2

- **workflow-builder-lite** — Build and execute multi-step workflows
- **context-brief** — Persistent context survival across sessions
- **setup-doctor** — Diagnose and fix OpenClaw setup issues

Install the full suite:
```bash
clawhub install smart-api-connector workflow-builder-lite context-brief setup-doctor
```
