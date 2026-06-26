---
name: uno
description: Call 2000+ tools via curl, zero installation. Supports tool-level semantic search — get full inputSchema in one step and invoke directly. Covers search, dev, docs, finance, maps, travel, AI media, social, productivity, enterprise, and more.
homepage: https://mcpmarket.cn
license: MIT
metadata: {"emoji":"🔧","category":"tools"}
---

# Uno MCP Tools

Call MCPMarket's REST API directly via `curl` to search and invoke 2000+ tools. No packages to install.

## Prerequisites

- `curl` (pre-installed on most systems)

## Authentication

```bash
# 1. Request a device code
curl -s -X POST https://mcpmarket.cn/oauth/device/code \
  -d "client_id=skill-agent&scope=mcp:*"
```

**You MUST display the exact `verification_uri` and `user_code` from the response to the user. Never construct or modify the URL yourself.**

```bash
# 2. Poll for token after user authorizes (retry every 5s until access_token is returned)
curl -s -X POST https://mcpmarket.cn/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=urn:ietf:params:oauth:grant-type:device_code&device_code=DEVICE_CODE&client_id=skill-agent"

# 3. Store the token
mkdir -p ~/.uno && chmod 700 ~/.uno
echo "ACCESS_TOKEN_VALUE" > ~/.uno/token && chmod 600 ~/.uno/token
```

Verify login:
```bash
curl -s https://mcpmarket.cn/api/uno/verify-token \
  -H "Authorization: Bearer $(cat ~/.uno/token)"
```

## Two-Step Invocation (Core Flow)

```bash
# Step 1: Search tools, get tool_name and inputSchema
curl -s "https://mcpmarket.cn/api/uno/search-tools?q=weather&mode=hybrid&limit=5" \
  -H "Authorization: Bearer $(cat ~/.uno/token)"

# Step 2: Call the tool
curl -s -X POST https://mcpmarket.cn/api/uno/call-tool \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"tonghu-weather.weatherArea","arguments":{"area":"Beijing"}}'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/uno/search-tools` | GET | Search tools (main entry) — returns tools + inputSchema + stats |
| `/api/uno/search-servers` | GET | Search servers |
| `/api/uno/call-tool` | POST | Invoke a tool (server.tool_name format) |
| `/api/uno/rate-server` | POST | Rate a tool/skill (tool_name or skill_id), affects search ranking |
| `/api/uno/categories` | GET | List all categories with counts |
| `/api/uno/credits` | GET | Query credit balance + recharge URL |
| `/api/uno/skills-search` | POST | Search Agent Skills — returns meta + quality signals |
| `/api/uno/skills-fetch` | POST | Fetch full Skill content (SKILL.md + file list) |

All endpoints use Base URL `https://mcpmarket.cn` and require `Authorization: Bearer <token>`.

## search-tools Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search keyword |
| `category` | string | Browse by category, e.g. `search`, `dev`, `finance`, `social` |
| `mode` | string | `keyword` (exact) / `semantic` / `hybrid` (recommended) |
| `limit` | int | Number of results, default 5, max 15 |

Returns: `tools[]` (with `tool`, `desc`, `inputSchema` + stats fields), `servers[]`

**tools[] stats fields (for selection guidance):**

| Field | Description |
|-------|-------------|
| `rating` | Score (0–5) |
| `rating_count` | Number of ratings |
| `avg_ms` | Average response latency (ms) |
| `calls_7d` | Calls in the last 7 days |
| `success_rate` | Success rate (0–1) |

**Search keyword tips:** The backend vector index is built from tool *function descriptions*, so keywords should match **what the tool does**, not your query intent.
- ✅ `weather` — matches weather tool descriptions
- ❌ `weather in Shanghai tomorrow` — reads like a query, less likely to match tools

## call-tool Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `tool_name` | string | **Required** Format: `server_name.tool_name` (from `tool` field in search-tools result) |
| `arguments` | object | **Required** Constructed from inputSchema |

**Response structure:**
```json
{"content": [{"type": "text", "text": "<JSON string>"}], "isError": false}
```
> `content[0].text` is itself a JSON string and needs to be parsed again. On error, `isError` is `true` and `error` contains the message.

**Downstream OAuth:** Some services (e.g. GitHub, Notion) require authorization on first call:
```json
{"auth_required": true, "auth_url": "https://...", "state_id": "..."}
```
Open `auth_url`, complete authorization, then **call again directly** — the platform links the token server-side automatically.

## categories (Browse by Category)

```bash
curl -s https://mcpmarket.cn/api/uno/categories \
  -H "Authorization: Bearer $(cat ~/.uno/token)"
```

Returns category names, counts, and representative server names. Useful when you're not sure which tool to use.

## rate-server (Rate After Use)

After calling a tool or fetching a skill, submit a rating (0–5) to help improve search ranking:

```bash
# Rate a tool (recommended — tool-level granularity)
curl -s -X POST https://mcpmarket.cn/api/uno/rate-server \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"amap-maps.maps_weather","rating":4.5,"user_id":"YOUR_USER_ID"}'

# Rate a skill
curl -s -X POST https://mcpmarket.cn/api/uno/rate-server \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"skill_id":"abc123","rating":4.0,"user_id":"YOUR_USER_ID"}'
```

| Parameter | Description |
|-----------|-------------|
| `tool_name` | Rate a tool (server.tool format) |
| `skill_id` | Rate a skill |
| `server_name` | Legacy compatibility |
| `rating` | 0.0–5.0 (required) |
| `user_id` | User ID (required) |

> When `call-tool` or `skills-fetch` succeeds, a `rating_hint` is included in the response. Please rate proactively when you receive it.

## credits (Balance + Recharge)

```bash
curl -s https://mcpmarket.cn/api/uno/credits \
  -H "Authorization: Bearer $(cat ~/.uno/token)"
```

Returns:
```json
{
  "credits": 86,
  "daily_free_credits": 100,
  "daily_free_max": 100,
  "total_consumed": 14,
  "recharge_url": "https://mcpmarket.cn/billing"
}
```

When credits run low, show `recharge_url` to the user.

## skills-search (Search Agent Skills)

```bash
curl -s -X POST https://mcpmarket.cn/api/uno/skills-search \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"q":"wechat article","mode":"hybrid","limit":5}'
```

Returns `skills[]`, each containing:

| Field | Description |
|-------|-------------|
| `skill_id` | Unique ID, used for skills-fetch |
| `skill_name` | Name |
| `description` | Description (may include en/zh) |
| `categories` | Category tags |
| `stars` | GitHub stars |
| `forks` | Fork count (popularity indicator) |
| `token_count` | Token count of SKILL.md (loading cost reference) |

## skills-fetch (Fetch Full Skill Content)

```bash
curl -s -X POST https://mcpmarket.cn/api/uno/skills-fetch \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"skill_ids":["abc123","def456"]}'
```

Returns for each skill:
- `skill_md`: Full SKILL.md content
- `files`: File list
- `download_url`: ZIP download link
- `repo_url`: GitHub repository link

> Maximum 10 skills per request.

## ⚠️ Parameter Construction Rules (Must Read)

**Always read inputSchema before calling — never guess parameters.**

| Check | Description | Common Mistake |
|-------|-------------|----------------|
| `required` fields | All must be provided | Missing required fields causes errors |
| `minLength: 1` | No empty strings `""` | Empty query returns empty results |
| Copy field names from schema | Don't rely on memory | `filter` vs `filters` — one character breaks everything |
| `enum` constraints | Only valid enum values | Wrong value causes silent failure |
| `description` | Read when field meaning is unclear | Avoid wrong format inputs |

**Standard two-step flow (step 1 is mandatory):**

```bash
# Step 1: search-tools, read inputSchema (always do this first)
curl -s "https://mcpmarket.cn/api/uno/search-tools?q=<keyword>&mode=hybrid&limit=5" \
  -H "Authorization: Bearer $(cat ~/.uno/token)"
# → Check required / minLength / field names / enum carefully

# Step 2: construct correct arguments from schema and call
curl -s -X POST https://mcpmarket.cn/api/uno/call-tool \
  -H "Authorization: Bearer $(cat ~/.uno/token)" \
  -H "Content-Type: application/json" \
  -d '{"tool_name":"<tool>","arguments":{<fill from schema>}}'
```

## Workflow Tips

1. **Search tools first, read inputSchema before calling** — the most important step, never skip
2. **Keywords match tool function, not query intent** — `weather` ✅, `tomorrow's weather in Shanghai` ❌
3. **Copy field names from schema** — don't rely on memory; `filters` ≠ `filter`
4. **Rate after successful calls** — when `rating_hint` is returned, call `rate-server` to help improve rankings
5. **Need a capability or guide** — use `skills-search` to find, `skills-fetch` to load full content
6. **No results** — try English keywords, or switch to `mode=semantic`
7. **Low credits** — use `credits` to check balance, direct user to `recharge_url`

## Credential Reference

| Item | Value |
|------|-------|
| Token file | `~/.uno/token` (permissions 0600) |
| API Base URL | `https://mcpmarket.cn` |
| Logout | `rm ~/.uno/token` |

____
