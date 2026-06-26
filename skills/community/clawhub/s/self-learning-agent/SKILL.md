---
name: self-learning-agent
version: 1.0.0
description: "Knowledge card memory system with semantic search. Agents wake up fresh each session but remember everything through atomic ~350-token cards with YAML frontmatter, daily logs, and a slim master index. Captures lessons, corrections, preferences, and facts automatically. Built for agents that need persistent memory across sessions."
tags:
  - memory
  - learning
  - self-improving
  - knowledge-management
  - agent-memory
  - persistence
category: agent
---

# Self-Learning Agent — Knowledge Card Memory System

A production-tested memory architecture for AI agents that wake up fresh each session. Instead of one monolithic memory file that grows until it's unusable, this system uses atomic knowledge cards (~350 tokens each) searched semantically, daily logs for raw notes, and a slim master index loaded every session.

## Architecture

```
workspace/
├── MEMORY.md              # Master index (~2KB, loaded every session)
├── memory/
│   ├── cards/             # Knowledge cards (~350 tokens each)
│   │   ├── topic-name.md  # One topic per file, YAML frontmatter
│   │   ├── another-topic.md
│   │   └── ...
│   └── YYYY-MM-DD.md      # Daily session logs (raw notes)
```

### Why This Works

- **MEMORY.md** is tiny (~2KB). It loads fast, gives the agent orientation, and points to everything else.
- **Knowledge cards** are atomic. Each one covers ONE topic in ~350 tokens. Semantic search finds the right cards without loading everything.
- **Daily logs** are append-only scratch pads. Raw session notes, not curated.
- **Cards are curated wisdom. Daily logs are raw data.** The agent periodically distills daily logs into cards during maintenance.

## Setup

### 1. Create the directory structure

```bash
mkdir -p memory/cards
```

### 2. Create MEMORY.md (master index)

This file is loaded every session. Keep it under 2KB. It should contain:

```markdown
# MEMORY.md — Master Index

## How Memory Works
- **This file:** Slim index (~2KB). Loaded every main session.
- **Knowledge cards:** `memory/cards/*.md` (~N cards, ~350 tokens each). Searched semantically.
- **Daily logs:** `memory/YYYY-MM-DD.md`. Raw session notes.
- **DO NOT** dump everything here. Write knowledge cards instead.

## Identity
[Agent name, model, owner, key facts]

## Quick Context
[2-3 lines of what matters right now]

## Card Categories
[Table mapping categories to card topics]

## Current Priorities
[What's actively being worked on]
```

### 3. Add to your AGENTS.md / system prompt

```markdown
## Every Session
1. Read MEMORY.md (slim index)
2. Search `memory_search` for context relevant to the current task
3. Skim today + yesterday daily logs for recent context
4. Start working

## Memory Rules
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → write a knowledge card
- When you learn a lesson → write a knowledge card
- When you make a mistake → document it so future-you doesn't repeat it
```

## Knowledge Card Format

Every card has YAML frontmatter and dense content:

```markdown
---
topic: Descriptive Topic Name
category: system|human|infrastructure|tools|workflow|projects|lessons|career|security|models
tags: [tag1, tag2, tag3]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

The actual content. Dense, factual, no fluff.
Write for future-you who has zero context.
Include specific commands, paths, config values.
Keep under 350 tokens.
```

### Card Quality Rules

1. **ONE topic per card.** Three insights = three cards.
2. **~350 tokens max.** Dense beats verbose.
3. **Zero-context readable.** Include specifics (commands, paths, values).
4. **Tags are searchable keywords.** Lowercase, hyphenated.
5. **Update, don't duplicate.** If a card exists for the topic, merge new info into it.
6. **No fluff.** Every sentence should contain a fact, a command, or a decision.

### Good Card Example

```markdown
---
topic: Cortex CSRF Automation
category: infrastructure
tags: [cortex, csrf, thehive, api, security]
created: 2026-03-19
updated: 2026-03-19
---

Cortex 3.1.8 uses non-standard CSRF. Cookie: CORTEX-XSRF-TOKEN, header: X-CORTEX-XSRF-TOKEN.
Standard Play Framework bypass headers (Csrf-Token: nocheck) do NOT work.

Flow: Login → GET any endpoint with session cookie → capture CORTEX-XSRF-TOKEN from Set-Cookie →
send as both cookie AND X-CORTEX-XSRF-TOKEN header on all POST/PUT/DELETE.

Shortcut: After generating first API key, use Authorization: Bearer which bypasses CSRF entirely.
First-user POST /api/user (no auth) only works when zero users exist in DB.
```

### Bad Card Example

```markdown
---
topic: Stuff I Learned Today
---

Today I learned a bunch of things about Cortex and TheHive. The CSRF thing was really tricky
and took a while to figure out. I also learned about how to set up organizations and users.
It was a productive session overall.
```

(Too vague, no specifics, no actionable info, multiple topics in one card)

## Capture Triggers

### Automatic (agent should capture without being asked)
- Hard-won debugging lessons (3+ attempts to fix something)
- Configuration gotchas (things that work differently than expected)
- User corrections ("no, do it THIS way")
- Non-obvious facts about infrastructure, people, or projects
- Workflow improvements discovered during a task

### Manual
- User says `/learn`, "remember this", or "save this"
- User explicitly corrects the agent's approach

### What NOT to Capture
- Obvious/trivial information
- Temporary context (one-time fixes that won't recur)
- Things already in existing cards
- Conversation summaries (that's what daily logs are for)

## Daily Log Format

Append to `memory/YYYY-MM-DD.md`:

```markdown
## HH:MM — Brief Title

What happened, what was decided, what was learned.
Link to any cards created: `→ card: topic-name`
```

## Memory Maintenance

Periodically (every few days), the agent should:

1. Read recent daily logs
2. Identify significant events worth preserving long-term
3. Create or update knowledge cards from insights
4. Remove outdated info from MEMORY.md
5. Update the card categories table in MEMORY.md

Think of it like a human reviewing their journal and updating their mental model.

## Promotion Rules

When the same lesson appears 3+ times in cards:
- Promote it to AGENTS.md as a permanent rule
- Mark the original card as "promoted"
- This prevents the agent from re-learning the same lesson

## Session Workflow

```
Session Start
    │
    ├── Read MEMORY.md (always, ~2KB)
    ├── memory_search for task-relevant cards
    ├── Skim today + yesterday daily logs
    │
    ├── [Do work]
    │
    ├── Capture insights → knowledge cards
    ├── Log session → daily log
    │
Session End
```

## Scaling

This system has been tested with:
- ~36 knowledge cards (~350 tokens each = ~12.6K tokens total)
- Daily logs spanning months
- Semantic search via embeddings (qwen3-embedding or similar)

At this scale, semantic search finds relevant cards in <100ms. The master index stays under 2KB. The agent loads only what it needs.

If you hit 100+ cards, consider:
- Archiving cards older than 6 months that haven't been accessed
- Splitting categories into subdirectories
- Adding a card index file per category

## Comparison with Monolithic Memory

| | Monolithic (one big file) | Knowledge Cards |
|---|---|---|
| Load time | Grows forever | Constant (~2KB index) |
| Search | Full-text scan | Semantic vector search |
| Updates | Append-only chaos | Atomic card updates |
| Noise ratio | High (old + new mixed) | Low (curated cards) |
| Session cost | Tokens scale with history | Tokens stay flat |
