---
name: research-memory
description: Build a persistent, searchable knowledge base from articles, papers, documents, and notes using BlueColumn. Use when a user wants to save research for later retrieval, store articles or PDFs, build a second brain, or ask questions across their saved content. Triggers on phrases like "save this article", "store this paper", "add to my knowledge base", "what do I know about", "search my research", "recall what I saved about". Requires a BlueColumn API key (bc_live_*).
---

# Research Memory Skill

Turn articles, papers, and notes into a searchable knowledge base backed by BlueColumn.

## Setup
Read `TOOLS.md` for the BlueColumn API key (`bc_live_*`). Keys are generated at bluecolumn.ai/dashboard. Store securely — never log or expose them.

Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1` (BlueColumn's official backend — bluecolumn.ai runs on Supabase Edge Functions)

## Save Research

**From URL (PDF or document):**
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{"file_url": "https://arxiv.org/pdf/...", "title": "Attention Is All You Need"}'
```

**From text/paste:**
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -d '{"text": "<article content>", "title": "Article Title - Source - Date"}'
```

Response: `session_id`, `summary`, `key_topics[]` — confirm to user what was stored.

## Query Knowledge Base

```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -d '{"q": "what have I saved about transformer attention mechanisms?"}'
```

Returns synthesized answer across all stored research + source citations.

## Save a Quick Note

```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -d '{"text": "Interesting idea from paper: sparse attention reduces complexity to O(n sqrt(n))", "tags": ["transformers", "attention", "efficiency"]}'
```

## Workflow

1. User shares article URL, PDF URL, or pastes content
2. Store via `/agent-remember` with descriptive title (include source + date)
3. Confirm: show summary + key topics extracted
4. For queries → `/agent-recall` with natural language question
5. For quick observations → `/agent-note` with relevant tags

## Title Naming Convention
`"<Topic> - <Source> - <YYYY-MM-DD>"`
Example: `"Sparse Attention - Arxiv - 2026-04-14"`

Consistent naming improves recall accuracy over time.

See [references/api.md](references/api.md) for full API reference.
