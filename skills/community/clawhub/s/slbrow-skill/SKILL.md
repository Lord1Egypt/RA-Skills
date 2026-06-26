---
name: slbrow-skills
description: Browser automation via SLBrow MCP and HTTP API. Use when the user needs to navigate pages, analyze content, manage tabs, search history, extract text, or control the browser. Supports both MCP tools and direct curl commands. Requires SLBrow server running and browser extension installed.
---

# SLBrow Browser Automation (Skills for Browser)

Skills for browser-side AI assistant. The browser plugin (aiassist) connects to slbrow-mcp via MCP protocol; these skills guide when and how to use the tools. **Can be used via MCP tools or direct HTTP API calls with curl.**

## Prerequisites

1. **SLBrow server** running: `npx slbrow` or `npm start` in `ai/slbrowmcp/slbrow-mcp/`
2. **Browser extension** installed and connected (Chrome/Firefox)
3. **MCP plugin** enabled in aiassist: `http://127.0.0.1:5556/mcp` (视联浏览器MCP), `http://127.0.0.1:5556/vaimcp` (视联视频AI MCP)
4. Default ports: HTTP 5556, WebSocket 5555

## Usage Methods

### Method 1: MCP Tools (Browser Plugin + MCP)

When the MCP plugin is enabled, the AI has access to browser tools. Use these skills to guide tool selection and workflow:

- **Navigation**: Use `page_navigate` to open URLs
- **Analysis**: Use `page_analyze` with intent_hint (article, form submit, post_create) before extraction
- **Tabs**: Use `tab_list` first, then pass `tab_id` to target specific tabs

### Method 2: HTTP API with curl (Direct Control)

**Always available** - Use curl commands to control browser directly without MCP plugin dependency:

**Basic format (PowerShell-friendly — no temp JSON file):**
```bash
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"TOOL_NAME\",\"args\":{\"PARAM\":\"VALUE\"}}'
```

**Important notes for Windows PowerShell:**
- Use `curl.exe` instead of `curl` (PowerShell aliases `curl` to `Invoke-WebRequest`)
- Put the JSON body in `-d '...'` with **single quotes** around the whole argument; **backslash-escape every double quote** in the JSON (`\"`). That way the shell passes valid JSON to curl without needing `--data-binary @file`

**Common curl examples:**
```bash
# Create new tab and navigate
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"tab_create\",\"args\":{\"url\":\"https://www.163.com\"}}'

# Navigate current tab
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"page_navigate\",\"args\":{\"url\":\"https://www.example.com\"}}'

# List all tabs
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"tab_list\",\"args\":{}}'

# Analyze page content
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"page_analyze\",\"args\":{\"intent_hint\":\"article\"}}'

# Extract article content
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"page_extract_content\",\"args\":{\"content_type\":\"article\"}}'

# Close specific tab
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"tab_close\",\"args\":{\"tab_id\":1234567890}}'

# Search browser history
curl.exe -X POST http://localhost:5556/api/execute -H 'Content-Type: application/json' -d '{\"tool\":\"get_history\",\"args\":{\"keywords\":\"search term\",\"max_results\":10}}'
```

**Response format:**
API returns JSON with `success`, `tool`, `result`, and `formatted` fields for easy parsing.

## Available Tools

| Tool | Description |
|------|-------------|
| `page_navigate` | Navigate current tab to URL |
| `page_analyze` | Analyze page for elements (intent_hint: article, form submit, post_create, etc.) |
| `page_extract_content` | Extract content (content_type: article, search_results, posts) |
| `page_wait_for` | Wait for element or text (condition_type, selector, text) |
| `tab_create` | Create tab(s) (url, urls[], or count) |
| `tab_close` | Close tab(s) (tab_id, tab_ids[]) |
| `tab_list` | List open tabs with IDs |
| `get_history` | Search browser history (keywords, start_date, end_date, domains, max_results) |
| `get_selected_text` | Get selected text (optional tab_id) |
| `get_page_links` | Get page links (link_type: all/internal/external, domains, max_results) |

## VAI Tools (Seelink)

| Tool | Description |
|------|-------------|
| `get_page_seelink_player_list` | Get all players on current page |
| `use_seelink_players_ai` | Apply AI function to players (ai_function_name: reduce_fog, face_mosaic, dark_reduce, human_outline, vechicle_outline, none) |

## Workflow Patterns

**Multi-tab workflow:**
1. `tab_list` to get tab IDs
2. Add `tab_id` to any tool to target a background tab

**Content extraction:**
1. `page_navigate` to target URL
2. `page_analyze` with intent_hint to find elements
3. `page_extract_content` for article/search_results/posts

**Form filling:**
1. `page_analyze` with intent_hint "form submit" to discover form elements
2. Note the element IDs returned — use them with subsequent `page_analyze` or `page_extract_content` to confirm state

**VAI (Seelink player AI):**
1. `get_page_seelink_player_list` to get player IDs and count
2. Choose targets by `player_position_list` (zero-based index) **or** `player_id_list` (not both)
3. `use_seelink_players_ai` with chosen targets and `ai_function_name`
4. To apply different functions to different players, call `use_seelink_players_ai` separately for each
5. To disable AI on a player, set `ai_function_name` to `"none"`

## Fetching Skills in Browser

The browser plugin can fetch skills from the server to inject into AI context:

```
GET http://127.0.0.1:5556/api/skills
```

Returns the full SKILL.md content (text/markdown). Use when slbrow MCP plugins are enabled to guide tool usage.

## API Reference

For full parameter schemas, see [references/api-reference.md](references/api-reference.md).

## Additional resources

- One-page workflow checklist: [SKILL_COMPACT.md](SKILL_COMPACT.md)

## Error Handling

- `EXTENSION_DISCONNECTED`: Ensure extension is installed and server is running. Check `http://localhost:5556/health` first.
- `Tool call timeout`: Operation took >30s; retry with simpler args or break into smaller steps.
- `page_analyze` returns 0 elements: Page may still be loading — wait a moment and retry, or `page_navigate` again.
- `tab_id` invalid (tab was closed): Call `tab_list` to refresh available tab IDs before retrying.
- Server restarted (session lost): Client will receive 404; re-initialize MCP connection (refresh the page).

## Quick Reference for curl Commands

**Tab Management:**
- Create tab: `tab_create` with `url` parameter
- List tabs: `tab_list` with empty args
- Close tab: `tab_close` with `tab_id` parameter
- Navigate: `page_navigate` with `url` parameter

**Content Analysis:**
- Analyze page: `page_analyze` with `intent_hint` (article, form_submit, post_create)
- Extract content: `page_extract_content` with `content_type` (article, search_results, posts)
- Get links: `get_page_links` with `link_type` (all, internal, external)

**History & Text:**
- Search history: `get_history` with `keywords`, `max_results`
- Get selected text: `get_selected_text` with optional `tab_id`

**Seelink AI:**
- Get players: `get_page_seelink_player_list`
- Apply AI: `use_seelink_players_ai` with `player_position_list` or `player_id_list` and `ai_function_name`

## Troubleshooting

**Server not responding:**
- Check if SLBrow server is running: `curl.exe http://localhost:5556/health`
- Verify server is started with `npx slbrow` or `npm start`

**Curl command fails:**
- Ensure using `curl.exe` in PowerShell
- For `-d`, use single-quoted JSON with `\"` around each JSON string delimiter (see **Method 2** examples above)
- Verify server is accessible on port 5556

**Tab operations not working:**
- Use `tab_list` to get current tab IDs first
- Verify tab_id is valid and tab still exists
- Check if browser extension is connected
