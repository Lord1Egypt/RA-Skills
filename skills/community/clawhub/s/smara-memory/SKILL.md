---
name: smara-memory
description: Persistent memory for AI agents — store, search, and recall user context via the Smara Memory API
version: 1.0.0
author: parallelromb
metadata:
  openclaw:
    emoji: "🧠"
    tags:
      - smara
      - memory
      - persistence
      - recall
    requires:
      env:
        - SMARA_API_KEY
    primaryEnv: "SMARA_API_KEY"
---

# Smara Memory Skill

Gives your agent persistent memory across conversations. Store facts about users, search by meaning, and retrieve full context — powered by Smara's Ebbinghaus decay scoring.

## When to use

- When the agent learns something about a user that should persist (preferences, facts, context)
- When the agent needs to recall what it knows about a user
- When the agent should check if it already knows something before asking again
- After meaningful conversations to extract and store key facts

## Setup

1. Get a free API key at https://smara.io
2. Set `SMARA_API_KEY` in your environment

## Actions

### Store a memory

```bash
curl -X POST https://api.smara.io/v1/memories \
  -H "Authorization: Bearer $SMARA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_id_here",
    "fact": "User prefers dark mode and uses vim keybindings",
    "importance": 0.7
  }'
```

### Search memories

```bash
curl "https://api.smara.io/v1/memories/search?user_id=user_id_here&query=editor+preferences&limit=5" \
  -H "Authorization: Bearer $SMARA_API_KEY"
```

### Get full user context

```bash
curl "https://api.smara.io/v1/users/user_id_here/context" \
  -H "Authorization: Bearer $SMARA_API_KEY"
```

### Delete a memory

```bash
curl -X DELETE "https://api.smara.io/v1/memories/MEMORY_ID" \
  -H "Authorization: Bearer $SMARA_API_KEY"
```

## Instructions for the agent

1. **After conversations**: Extract key facts (preferences, decisions, context) and store them as memories with relevant tags
2. **Before responding**: Search for relevant memories to personalize responses
3. **Contradiction handling**: Smara automatically handles contradictions — if a user changes a preference, just store the new one and the old one is soft-deleted
4. **Duplicate handling**: Smara skips duplicates automatically — safe to store the same fact multiple times
5. **Decay scoring**: Memories naturally lose weight over time. Recent, frequently-accessed memories rank higher. This is automatic.

## Example workflow

```
User: "I switched to Neovim last week"

Agent thinks:
1. Search memories for "editor preferences" → finds "Uses vim keybindings"
2. Store new memory: "Switched to Neovim (from vim)" with tags ["preferences", "editor"]
3. Smara auto-detects contradiction with old vim memory → soft-deletes it
4. Respond acknowledging the switch
```

## API Reference

Full docs: https://api.smara.io/docs/
