---
name: shaper
description: >
  Connect to a Shaper (useshaper.com) workspace via MCP to execute Shape Up methodology as an AI agent.
  Use when the user wants an agent to work inside their Shaper workspace, read pitch documents before
  writing code, create or track scopes, update hill chart progress, complete scopes when done, or orient
  on what's currently in-cycle. Requires a Shaper API key from the workspace Settings page.
---

# Shaper

Shaper is a Shape Up project management tool at useshaper.com. This skill connects you to a workspace via MCP (JSON-RPC 2.0) so you can act as an agent inside a human's Shape Up cycle.

## Setup

Get the API key from: `https://useshaper.com/<workspace-slug>/settings` → "Connect Agents" → Generate API key.

Store it:
```bash
export SHAPER_API_KEY="shp_..."
export SHAPER_WORKSPACE_SLUG="your-slug"
```

Or ask the user to provide it directly.

## Core Workflow

**Always orient before working:**

1. Call `get_active_work` — see current cycle, pitches in flight, all scopes + hill positions
2. Call `get_pitch_context` on the relevant pitch — read the full spec before touching code  
3. Do the work
4. Call `update_scope_hill_position` as you make progress (0.0 = not started → 0.5 = over the hill → 1.0 = done)
5. Call `complete_scope` when a scope is finished

## MCP Endpoint

```
POST https://useshaper.com/mcp
Authorization: Bearer <api_key>
Content-Type: application/json
```

JSON-RPC 2.0 format:
```json
{"jsonrpc":"2.0","method":"tools/call","params":{"name":"<tool>","arguments":{...}},"id":1}
```

## Essential Tools

### Orient (use first)
```bash
curl -s -X POST https://useshaper.com/mcp \
  -H "Authorization: Bearer $SHAPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_active_work","arguments":{}},"id":1}'
```
Returns: active cycle + all betting/bet pitches + all scopes with hill positions + completion summary.

### Read a pitch spec
```bash
-d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"get_pitch_context","arguments":{"pitch_id":"<ID>"}},"id":1}'
```
Returns: full pitch document — problem, solution, appetite, BDD scenarios.

### Create a scope
```bash
-d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"create_scope","arguments":{"cycle_id":"<ID>","title":"<title>","pitch_id":"<ID>"}},"id":1}'
```

### Update hill chart position
```bash
-d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"update_scope_hill_position","arguments":{"scope_id":"<ID>","position":0.5}},"id":1}'
```
Position is 0.0–1.0. Use 0.25 = figuring it out, 0.5 = over the hill (approach clear), 0.75 = mostly done, 1.0 = complete.

### Complete a scope
```bash
-d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"complete_scope","arguments":{"scope_id":"<ID>"}},"id":1}'
```

## All Tools

See `references/tools.md` for full input schemas and all available tools.

## Discovery

Full tool schemas: `GET https://useshaper.com/.well-known/mcp.json`
