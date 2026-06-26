---
name: seekdb-memory
version: 0.2.1
description: "Cloud-native persistent memory for OpenClaw agents. Auto-captures facts after conversations, auto-recalls relevant context before each reply. Hybrid search (vector + fulltext + RRF + rerank), query rewrite, experience learning — all behind one API key. Use this when the agent needs long-term memory, persistent context, or cross-session recall."
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env: []
      plugins:
        - m0
---

# SeekDB Memory — Cloud-Native Agent Memory

Persistent long-term memory for OpenClaw agents. Once the m0 plugin is installed, your agent automatically remembers facts across conversations and recalls relevant context before each reply.

## What It Does

| Capability | How It Works |
|------------|-------------|
| **Auto-Capture** | After each conversation, extracts key facts via LLM and stores them in the cloud |
| **Auto-Recall** | Before each reply, searches for relevant memories and injects them as context |
| **Hybrid Search** | Vector similarity (HNSW) + fulltext (BM25) + RRF fusion + rerank |
| **Query Rewrite** | Resolves pronouns, splits compound questions, expands keywords |
| **Experience Learning** | Distills successful tool-use patterns into reusable recipes |
| **Cross-Device** | Cloud-native — memories are available from any device, no sync needed |

## Memory Tools

Use these tools to manage the agent's long-term memory:

### memory_recall

Search memories by semantic similarity. Returns the most relevant memories.

```
memory_recall query="user's preferred programming language" limit=5
```

Use when:
- The user asks about something discussed in a previous conversation
- You need context about user preferences, past decisions, or facts
- The user references something with "last time", "before", "remember when"

### memory_store

Save an important fact, preference, or decision to long-term memory.

```
memory_store text="User prefers TypeScript over JavaScript for all new projects" metadata={"category": "preference", "importance": 0.9}
```

Use when:
- The user states a preference ("I always use...", "I prefer...")
- A decision is made ("Let's go with...", "We decided...")
- The user corrects you ("Actually, it's...", "No, I meant...")
- Important facts are shared (deadlines, names, project details)

### memory_forget

Delete a specific memory by ID.

```
memory_forget id=42
```

Use when:
- The user asks to forget something
- A memory is outdated or incorrect
- Cleaning up duplicate memories

## Automatic Behavior

With default configuration, the agent does NOT need to call tools manually for basic memory operations:

1. **Before each conversation**: The m0 plugin automatically searches for relevant memories based on the user's message and injects them as context. The agent sees them as `<relevant-memories>` in the prompt.

2. **After each conversation**: The m0 plugin automatically extracts key facts from the conversation and stores them. No manual `memory_store` needed for routine facts.

3. **Manual tools** are for explicit user requests ("remember this", "forget that", "what did I say about X?").

## Experience System

The m0 plugin tracks successful tool-use patterns and distills them into reusable experiences.

### experience_detail

View the full description of a distilled experience.

```
experience_detail id=7
```

Experiences are automatically injected alongside memories when relevant. They help the agent avoid repeating mistakes and reuse proven approaches.

## Best Practices

1. **Don't over-store**: Auto-capture handles routine facts. Only use `memory_store` for high-importance items the user explicitly wants remembered.
2. **Use metadata**: Add `category` (preference, decision, fact, deadline) and `importance` (0.0-1.0) to help with retrieval.
3. **Trust auto-recall**: Don't call `memory_recall` at the start of every conversation — the plugin already injects relevant context automatically.
4. **Respect forget requests**: When a user says "forget X", use `memory_forget` immediately.

## Setup

If the m0 plugin is not yet installed, run the setup skill:

```
/openclaw-m0-setup
```

Or install manually:

```bash
openclaw add m0
```

Then configure in `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "m0": {
        "enabled": true,
        "config": {
          "apiKey": "ak_your_key_here",
          "baseUrl": "https://your-endpoint",
          "autoCapture": true,
          "autoRecall": true,
          "recallLimit": 10
        }
      }
    }
  }
}
```

## Requirements

- OpenClaw >= 2026.2.2
- m0 plugin installed and configured with a valid API key
