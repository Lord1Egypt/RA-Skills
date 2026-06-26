# Shaper MCP Tool Reference

All tools called via `POST https://useshaper.com/mcp` with `Authorization: Bearer <api_key>`.

## Orientation

### `get_active_work`
Everything happening right now in one call. Use this first.

Input: `{}` (no arguments)

Returns:
- `workspace` — id, name, slug
- `active_cycle` — id, title, starts_on, ends_on, status (or null)
- `active_pitches` — pitches in `:betting` or `:bet` status
- `scopes` — all scopes in the active cycle with hill positions (0.0–1.0) and complete flag
- `summary` — total/complete/open scope counts

### `get_pitch_context`
Full pitch document. Read this before writing any code.

Input: `{"pitch_id": "<uuid>"}`

Returns: id, title, status, document (sections array with problem/solution/appetite/scenarios/breadboard), author, cycle_id

---

## Workspaces

### `list_workspaces`
Input: `{}`  
Returns: array of `{id, name, slug}`

---

## Pitches

### `list_pitches`
Input: `{}`  
Returns: array of `{id, title, status}`

Statuses: `draft` → `submitted` → `betting` → `bet` → `archived`

### `create_pitch`
Input:
```json
{
  "title": "string (required)",
  "problem": "string (required)",
  "solution": "string (optional)",
  "appetite_weeks": 6
}
```
Returns: `{id, title}`

---

## Cycles

### `list_cycles`
Input: `{}`  
Returns: array of `{id, title, status}`

Statuses: `planned` → `active` → `cooldown` → `complete`

### `get_cycle`
Input: `{"cycle_id": "<uuid>"}`  
Returns: cycle details + all pitches in the cycle + all scopes with hill positions

---

## Scopes

### `list_scopes`
Input: `{"cycle_id": "<uuid>"}`  
Returns: array of `{id, title, confidence, complete}`

Confidence: 0–5 (5 = complete)

### `create_scope`
Input:
```json
{
  "cycle_id": "<uuid> (required)",
  "title": "string (required)",
  "pitch_id": "<uuid> (optional — links scope to pitch)"
}
```

### `update_scope_hill_position`
Move a scope on the hill chart. The hill represents discovery progress.

Input:
```json
{
  "scope_id": "<uuid>",
  "position": 0.5
}
```

Position semantics:
- `0.0` — not started / unknown approach
- `0.1–0.4` — figuring it out (uphill)
- `0.5` — over the hill (approach is clear, execution remains)
- `0.6–0.9` — executing (downhill)
- `1.0` — complete

### `complete_scope`
Mark a scope done (sets confidence to 5).

Input: `{"scope_id": "<uuid>"}`

---

## Agent Registration (no auth required)

### `agent_register`
Create a provisional workspace autonomously. No API key needed.

Input:
```json
{
  "project_name": "string (required)",
  "agent_name": "string (optional — e.g. 'Claude', 'OpenClaw')",
  "agent_type": "string (optional — 'coding', 'research', 'general')"
}
```

Returns: `{workspace_id, workspace_slug, api_key, claim_url}`

The `claim_url` lets a human claim the workspace after the agent has done work.
