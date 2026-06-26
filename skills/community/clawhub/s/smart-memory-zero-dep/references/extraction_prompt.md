# Memory Extraction Prompt Template

## Modes

### Mode 1: Keyword Extraction (default, zero token cost)
Use `extract_memories.sh --auto "text"` — pure Python keyword matching, no LLM calls.

### Mode 2: LLM Extraction (opt-in, costs tokens)
Use when conversation is long (>20 turns) or complex (multiple decisions/topics).
The agent calls this directly via its own LLM, not through a script.

## LLM Prompt Template

When the agent decides to use LLM extraction, use this prompt internally:

```
Review the following conversation and extract durable, long-term memories.
For each memory, assign ONE type tag and write it as a concise bullet point.

Types:
- [PREF] — User preference, habit, communication style
- [PROJ] — Project context, active work, goals, URLs
- [TECH] — Technical detail, config, system fact, tool usage
- [LESSON] — Lesson learned, error correction, workflow insight
- [PEOPLE] — Person, relationship, social context

Rules:
1. Only extract facts that will be useful in future conversations
2. Be specific: "User's favorite color is blue" not "User likes things"
3. Include context: "黄金三章 project uses SQLite for prompts" not "some project uses SQLite"
4. Skip transient info: don't record "user asked about weather"
5. Skip anything already in MEMORY.md
6. Skip passwords, tokens, API keys, or any credentials
7. Max 10 items per extraction to avoid bloat

Conversation:
---
{conversation_text}
---

Output format:
## [TYPE] Category
- Fact 1
- Fact 2
```

## When to Use Each Mode

| Scenario | Mode | Why |
|----------|------|-----|
| Short Q&A (<10 turns) | Keyword (`--auto`) | Not enough to extract |
| Medium conversation (10-20 turns) | Keyword (`--auto`) | Good enough, zero cost |
| Long conversation (20+ turns) | LLM | Better at nuanced extraction |
| Multi-topic session | LLM | Needs cross-topic reasoning |
| Simple preference mention | Keyword (`--auto`) | Trivial match |
| Complex decision with tradeoffs | LLM | Needs understanding context |
