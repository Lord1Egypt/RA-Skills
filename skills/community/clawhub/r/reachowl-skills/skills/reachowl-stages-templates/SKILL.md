---
name: reachowl-stages-templates
description: "Manage the ReachOwl sales pipeline (CRM stages) and reusable message templates for follow-ups. Use when the user wants to add, rename, reorder, or delete pipeline stages, or write, save, or update follow-up message templates tied to a stage."
license: MIT
compatibility: Requires the ReachOwl MCP server (https://reachowl.com/mcp).
metadata:
  author: ReachOwl
  version: "1.1.0"
  homepage: https://reachowl.com
  tags: reachowl, crm, sales-pipeline, message-templates, follow-ups
---

# ReachOwl Stages & Message Templates

## Before you start

- Requires the ReachOwl MCP server connected with the user's token. If a tool reports a missing token, run the `reachowl-auth` flow.

## MCP tools

| Tool | Purpose |
|------|---------|
| `list_stages` | All stages |
| `get_stage` | `{ id }` |
| `create_or_update_stage` | `{ body: { name, id?, order? } }` |
| `reorder_stages` | `{ stages: [{ id, order }, …] }` |
| `delete_stage` | `{ id }` |
| `list_message_templates` | All templates |
| `upsert_message_template` | `{ body: { message, stage_id, image?, id? } }` |
| `delete_message_template` | `{ id }` |

## Workflow

1. `list_stages` before anything else — templates need a real `stage_id`.
2. Create missing stages with `create_or_update_stage { body: { name } }`.
3. Save templates with `upsert_message_template`. Placeholders: `{{name}}`, `{{first_name}}`.
4. Reorder with explicit pairs: `reorder_stages { stages: [{ id: 3, order: 1 }, { id: 5, order: 2 }] }`.

## Example

```
User: Add an "Interested" stage with a follow-up template
→ list_stages
→ create_or_update_stage { body: { name: "Interested" } }        // → id 9
→ upsert_message_template { body: { stage_id: 9, message: "Hi {{first_name}}, great to hear you're interested! When's a good time for a quick call?" } }
```

## Rules

- Confirm before `delete_stage`; templates and contacts may reference it.
