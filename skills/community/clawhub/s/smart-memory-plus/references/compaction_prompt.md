# Session Compaction Guide

## Keyword Extraction (Default)

Use `compact_session.py --extract` for zero-cost regex-based compaction.

### How It Works
- Extracts decisions, facts (PROJ/TECH), pending actions, blockers from conversation text
- Sanitizes output: removes sensitive data, redacts paths/URLs/IPs
- Saves to `memory/compacts/YYYY-MM-DD-HHMM.md`
- Keeps only last 30 compacts, auto-deletes oldest

### When to Use
| Scenario | Method |
|----------|--------|
| Simple Q&A, <20 turns | Keyword (`--extract`) |
| Multi-topic, 20-50 turns | Keyword (`--extract`) |
| Complex debugging, >50 turns | Keyword (`--extract`) with manual summary |
| Quick save before /new | Keyword (`--extract`) — fast, zero cost |

### Agent Instruction Template

When the agent decides to compact a session, draft content following this structure:

```
## Decisions Made
- [date] Decision description

## Facts Established
- [TYPE] Fact (use [PROJ] [TECH] [PREF] [PEOPLE] tags)

## Pending Actions
- [ ] Action description

## Blockers
- Blocker description

## Session Summary
(2-3 sentences max)

Rules:
1. Max 15 items total across all sections
2. No passwords, tokens, or API keys
3. No file paths, internal URLs, or infrastructure details — use placeholders
4. Skip debugging noise unless it led to a lesson
5. Be specific about decisions but vague about locations
```

Then pipe through security checks:
```
echo "compact content" | python3 scripts/compact_session.py --write
```

The agent applies this reasoning internally — no external LLM calls are made.
