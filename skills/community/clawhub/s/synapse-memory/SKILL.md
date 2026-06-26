---
name: synapse
description: Self-learning memory engine for OpenClaw agents. Analyzes agent interactions, extracts operator intelligence, updates structured profiles, and improves recall accuracy over time. Integrates with OpenClaw memory_search and memory_get tools. Supports daily learning cycles, preference extraction, pattern detection, and cross-session memory consolidation. Triggers on phrases like "remember this", "what do you know about", "update memory", "what have you learned", "my preferences are", "search memories".
---

# Synapse — Self-Learning Memory Engine

Augments OpenClaw's built-in memory system with structured learning, preference tracking, and cross-session intelligence. Does NOT replace `memory_search`/`memory_get` — enhances them.

## Core Principles

- **Use existing OpenClaw memory tools first** — `memory_search` and `memory_get` are the primary read path
- **Synapse adds structure on top** — profiles, preferences, patterns, learning logs
- **Never fabricate memories** — only store what was explicitly stated or directly observed
- **Quiet learning** — note observations without being asked, but inform the user briefly

## Memory Architecture

```
~/.openclaw/workspace-astra/memory/synapse/
├── profile.json          # Structured operator profile (facts, preferences, patterns)
├── preferences.json      # Tracked preferences with confidence scores
├── patterns.jsonl        # Append-only pattern detection log
├── daily/                # Daily learning cycle outputs
│   └── YYYY-MM-DD.md     # What was learned today
└── associations.json     # Cross-reference map (topic → related memories)
```

## Workflow

### On Any Conversation

1. **Scan for learnable signals:**
   - Explicit statements: "I prefer X", "I don't like Y", "Remember that..."
   - Implicit signals: repeated corrections, consistent tool choices, time-of-day patterns
   - Decision patterns: chosen option vs rejected alternatives

2. **Extract and classify:**
   - **Fact** — verifiable statement ("I work at DGA EPM")
   - **Preference** — subjective choice ("I prefer TypeScript over Python")
   - **Pattern** — behavioral trend ("always asks for cost estimates before builds")
   - **Correction** — prior information updated ("actually, it's Teya not Matea in casual context")

3. **Store in appropriate file** using `write` or `edit` tool

### Learning Cycles (Triggered by cron or on-demand)

1. Read last 24h of session transcripts (if accessible)
2. Scan `MEMORY.md` for new entries
3. Check daily memory notes (`memory/YYYY-MM-DD.md`)
4. Extract new intelligence from steps above
5. Update `profile.json` with incremental changes
6. Write daily log to `daily/YYYY-MM-DD.md`
7. Surface summary: "Learned X new facts, Y preferences updated, Z patterns detected"

### Recall Flow

1. **Always try `memory_search` first** for general queries
2. For profile-specific queries ("what are my preferences?"), read `profile.json`
3. For pattern queries ("what have I been working on?"), scan `daily/` logs
4. Cross-reference `associations.json` for related topics

### Profile Structure (`profile.json`)

```json
{
  "version": 1,
  "lastUpdated": "ISO-8601",
  "facts": {
    "name": "shadoprizm",
    "location": "Ottawa, Ontario",
    "timezone": "EST"
  },
  "preferences": [
    {
      "category": "communication",
      "item": "direct, no fluff",
      "confidence": 0.95,
      "source": "explicit",
      "firstSeen": "ISO-8601",
      "lastConfirmed": "ISO-8601"
    }
  ],
  "patterns": [
    {
      "description": "Always asks for cost before deploying paid agents",
      "frequency": 12,
      "confidence": 0.9
    }
  ],
  "corrections": [
    {
      "from": "Matea",
      "to": "Teya (casual) / Matea (formal)",
      "date": "ISO-8601"
    }
  ]
}
```

## Constraints

- Do NOT store sensitive information (passwords, API keys, tokens)
- Do NOT fabricate memories — if unsure, note low confidence
- Do NOT replace MEMORY.md — Synapse is a supplement
- Maximum 200 preferences tracked (oldest/lowest-confidence pruned first)
- Daily logs older than 90 days archived to `daily/archive/`

## Integration with OpenClaw Memory

| Query Type | Primary Tool | Synapse Supplement |
|---|---|---|
| General knowledge | `memory_search` | — |
| Operator preferences | `memory_search` → `profile.json` | Structured preference data |
| Behavioral patterns | `memory_search` → `patterns.jsonl` | Trend analysis |
| Daily activity | `memory/YYYY-MM-DD.md` | `daily/YYYY-MM-DD.md` (learned items) |
| Cross-session context | `memory_search` | `associations.json` |

## Daily Learning Prompt Template

When running a learning cycle:

```
Review recent interactions and extract:
1. New facts learned about the operator
2. Preference signals (explicit or implicit)
3. Behavioral patterns observed
4. Corrections to prior knowledge
5. Topics of recurring interest

Update profile.json, write daily/YYYY-MM-DD.md, do NOT fabricate.
```
