---
name: research-memory
description: Give AI agents Everything you read becomes knowledge. using BlueColumn persistent memory. Use when an agent researches and needs to keep findings; when the user wants to store, recall, or search research memory context. Requires a BlueColumn API key (bc_live_*).
---

# Research Memory — BlueColumn Skill

Everything you read becomes knowledge.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Research: pgvector vs pinecone — pgvector wins for BYO DB story. Source: docs comparison.", "title": "research-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Research: pgvector vs pinecone — pgvector wins for BYO DB story. Source: docs comparison.", "tags": ["research-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What did our research conclude about vector stores?"}'
```

## Workflow
1. On new context, first recall: `What did our research conclude about vector stores?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
