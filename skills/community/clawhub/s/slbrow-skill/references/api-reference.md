# SLBrow REST API Reference

Base URL: `http://localhost:5556/api` (port configurable via `--port`)

## Endpoints

### GET /api/tools

Returns available browser and VAI tools.

**Response:**
```json
{
  "browser": [...],
  "vai": [...],
  "all": [...]
}
```

### POST /api/execute

Execute a tool.

**Request body:**
```json
{
  "tool": "page_navigate",
  "args": { "url": "https://example.com" }
}
```

**Response (success):**
```json
{
  "success": true,
  "tool": "page_navigate",
  "result": { "url": "https://example.com", "execution_time": 123 },
  "formatted": "✅ Successfully navigated to: https://example.com"
}
```

**Response (error):**
```json
{
  "success": false,
  "error": "Error message",
  "code": "EXTENSION_DISCONNECTED"
}
```

## Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| `EXTENSION_DISCONNECTED` | Browser extension not connected | Install extension, check server is running |
| `TOOL_TIMEOUT` | Tool execution exceeded 30s | Retry with simpler parameters |
| `UNKNOWN_TOOL` | Tool name not found | Check tool name against `/api/tools` |
| `INVALID_ARGS` | Missing or invalid parameters | Verify required fields per tool schema |

## Browser Tools

### page_navigate
Navigate current tab to URL.
- `url` (string, required)

### page_analyze
Analyze page for elements.
- `intent_hint` (string, required): article, form submit, post_create, etc.
- `tab_id` (number, optional): target background tab

### page_extract_content
Extract content from page.
- `content_type` (string, required): article | search_results | posts
- `tab_id` (number, optional)

### page_wait_for
Wait for element or text.
- `condition_type` (string, required): element_visible | text_present
- `selector` (string, optional)
- `text` (string, optional)

### tab_create
Create tab(s).
- `url` (string)
- `urls` (array of strings)
- `count` (number, 1-50)

### tab_close
Close tab(s).
- `tab_id` (number)
- `tab_ids` (array of numbers)

### tab_list
List open tabs with IDs.

### get_history
Search browser history.
- `keywords` (string)
- `start_date`, `end_date` (ISO date-time)
- `domains` (array of strings)
- `max_results` (number, max 500)

### get_selected_text
Get selected text.
- `tab_id` (number, optional)

### get_page_links
Get page links.
- `link_type`: all | internal | external
- `domains` (array)
- `max_results` (max 200)

## VAI Tools (Seelink)

### get_page_seelink_player_list
Get all players on current page. No args.

### use_seelink_players_ai
Apply AI function to players.
- `ai_function_name` (required): reduce_fog | face_mosaic | dark_reduce | human_outline | vechicle_outline | none
- `player_position_list` (array of numbers): zero-based positions (use OR `player_id_list`, not both)
- `player_id_list` (array of strings): player IDs (use OR `player_position_list`, not both)

**Example response:**
```json
{
  "success": true,
  "tool": "use_seelink_players_ai",
  "result": { "result": "success", "message": "AI function control action for all players are completed successfully" },
  "formatted": "{\"result\":\"success\",...}"
}
```

## Health Check

### GET /health

Check server status.

**Response:**
```json
{ "status": "ok", "ws_clients": 1 }
```

## cURL Examples

```bash
# Navigate to a URL
curl -X POST http://localhost:5556/api/execute \
  -H 'Content-Type: application/json' \
  -d '{"tool":"page_navigate","args":{"url":"https://example.com"}}'

# List open tabs
curl -X POST http://localhost:5556/api/execute \
  -H 'Content-Type: application/json' \
  -d '{"tool":"tab_list","args":{}}'

# Get Seelink player list
curl -X POST http://localhost:5556/api/execute \
  -H 'Content-Type: application/json' \
  -d '{"tool":"get_page_seelink_player_list","args":{}}'

# Apply AI function to player at position 0
curl -X POST http://localhost:5556/api/execute \
  -H 'Content-Type: application/json' \
  -d '{"tool":"use_seelink_players_ai","args":{"player_position_list":[0],"ai_function_name":"face_mosaic"}}'
```
