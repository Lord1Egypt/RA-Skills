---
name: sales-memory
description: Give AI agents Sales memory: objections and follow-ups. using BlueColumn persistent memory. Use when an agent runs sales and needs deal history; when the user wants to store, recall, or search sales memory context. Requires a BlueColumn API key (bc_live_*).
---

# Sales Memory — BlueColumn Skill

Sales memory: objections and follow-ups.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jane's objection: price. Addressed with annual discount. Follow-up set for Aug 5.", "title": "sales-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Jane's objection: price. Addressed with annual discount. Follow-up set for Aug 5.", "tags": ["sales-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What objections has Jane raised and how did we handle them?"}'
```

## Workflow
1. On new context, first recall: `What objections has Jane raised and how did we handle them?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
