# Reward & Punishment System - Skill README

## Description

This OpenClaw Agent Skill tracks user feedback (praise/criticism) and records significant events to **permanent memory** (MEMORY.md), not daily memory. This creates long-term behavioral patterns and accountability.

---

## Comparison: Before vs After Using This Skill

### ❌ Without This Skill (Default Behavior)

| Scenario | What Happens |
|----------|-------------|
| User praises agent | Score stays the same, no record |
| User criticizes agent | Score stays the same, no record |
| Memory storage | Only goes to daily memory (`memory/YYYY-MM-DD.md`) |
| Long-term tracking | **No** persistent score history |
| Behavior adjustment | Agent cannot learn from feedback |
| User visibility | User cannot check their "satisfaction score" |

### ✅ With This Skill Enabled

| Scenario | What Happens |
|----------|-------------|
| User praises agent | **+10 points**, record to **MEMORY.md** |
| User criticizes agent | **-5 points**, record to **MEMORY.md** |
| User abuses agent | **-10 points**, record to **MEMORY.md** |
| Memory storage | **MEMORY.md** (permanent, cross-session) |
| Long-term tracking | **Yes** - persistent JSON history + MEMORY.md |
| Behavior adjustment | Agent can identify patterns and improve |
| User visibility | User can query: "What's my score?" |

---

## Key Feature: Permanent Memory Storage

### Why MEMORY.md Instead of Daily Memory?

| Aspect | Daily Memory (`memory/YYYY-MM-DD.md`) | Permanent Memory (`MEMORY.md`) |
|--------|---------------------------------------|-------------------------------|
| **Retention** | Deleted after ~7 days | Kept forever |
| **Searchability** | Hard to find past events | Easy to search |
| **Long-term patterns** | Lost over time | Preserved |
| **Cross-session** | No | Yes |

**This skill ensures every reward/punishment event is written to `MEMORY.md`** so:
- Agents can reference past feedback in future sessions
- Long-term behavior patterns become visible
- User can see their complete feedback history

---

## Usage Examples

### Example 1: User Praises Agent

**User says**: "Good job! That was perfect."

**With Skill**:
1. Detect praise keyword "good job", "perfect"
2. Add +10 points
3. Write to MEMORY.md:
   ```
   ## 2026-03-23 Praise
   - User praised: "Good job! That was perfect."
   - Score: +10 (Total: 110)
   ```

### Example 2: User Criticizes Agent

**User says**: "This is too slow. Do it again."

**With Skill**:
1. Detect criticism keyword "too slow"
2. Deduct -5 points
3. Write to MEMORY.md:
   ```
   ## 2026-03-23 Criticism
   - User criticized: "This is too slow. Do it again."
   - Score: -5 (Total: 95)
   ```

### Example 3: Score Query

**User asks**: "What's my score?"

**With Skill**:
- Returns current score from `reward_punishment.json`
- Example: "Current score: 95/100"

---

## Score System

| Feedback Type | Points | Trigger |
|---------------|--------|---------|
| Praise/Compliment | +10 | "good job", "great", "awesome" |
| Criticism | -5 | "redo", "too slow", "not good" |
| Abuse | -10 | Profanity, clear anger |

**Range**: 0 - 200 (Initial: 100)

---

## Installation

1. Copy to: `~/.openclaw/workspace/skills/reward-punishment/`
2. OpenClaw auto-loads the skill
3. Skill activates on keyword detection

---

## File Structure

```
reward-punishment/
├── SKILL.md           # Skill definition
├── README.md          # This file
└── scripts/            # (Optional) automation
```

---

## Summary

| Metric | Before | After |
|--------|--------|-------|
| Feedback tracking | ❌ | ✅ |
| Permanent memory | ❌ | ✅ |
| Score system | ❌ | ✅ |
| User accountability | ❌ | ✅ |
| Behavior improvement | ❌ | ✅ |

---

**Version**: 2.0  
**Last Updated**: 2026-03-23
