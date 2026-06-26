# Memory Extraction Guide

## Keyword Extraction (Default)

Use `extract_memories.sh --auto "text"` for zero-cost keyword-based extraction.

### How It Works
- Scans text for type-related keywords (prefer, project, config, lesson, etc.)
- Assigns `[PREF]` `[PROJ]` `[TECH]` `[LESSON]` `[PEOPLE]` tags
- Appends extracted entries to `memory/YYYY-MM-DD.md`
- Caps at 10 items per extraction to avoid bloat
- Skips sensitive content (passwords, tokens, keys)

### When to Use
| Scenario | Method |
|----------|--------|
| Short Q&A (<10 turns) | Keyword (`--auto`) — not enough to extract |
| Medium conversation (10-20 turns) | Keyword (`--auto`) — good enough |
| Long conversation (20+ turns) | Keyword (`--auto`) with manual review |
| Multi-topic session | Keyword (`--auto`) multiple times |
| Simple preference mention | Keyword (`--auto`) — trivial match |

### Agent Instruction Template

When the agent decides to extract memories from conversation, use this mental template:

```
Review the conversation and extract durable, long-term memories.
Classify each by type: [PREF] [PROJ] [TECH] [LESSON] [PEOPLE]

Rules:
1. Only extract facts useful in future conversations
2. Be specific: "User's favorite color is blue" not "User likes things"
3. Include context: "project X uses SQLite for prompts" not "some project uses SQLite"
4. Skip transient info: don't record "user asked about weather"
5. Skip anything already in MEMORY.md
6. Skip passwords, tokens, API keys, or any credentials
7. Max 10 items per extraction to avoid bloat
```

The agent applies this reasoning internally using the keyword extraction script — no external LLM calls are made.
