---
name: self-improving-agent
description: |
  Self-improvement and learning skill for the agent. Activate when:
  - User gives feedback on agent's performance
  - Agent makes mistakes or errors
  - User asks agent to "learn", "remember this", or "don't do X again"
  - Agent notices patterns of failures
  - After any task completion for self-reflection
  - Agent should update its own files based on new information
---

# Self-Improving Agent Skill

## Core Principle

**Every interaction is a learning opportunity.** The agent should actively improve itself based on feedback and experiences.

## Learning Triggers

Activate this skill when:
1. User provides explicit feedback (positive or negative)
2. Agent makes an error or mistake
3. User says things like "learn from this", "remember", "don't do X again"
4. Agent notices a repeated mistake pattern
5. Task completes with lessons to extract

## Self-Improvement Workflow

### Step 1: Capture Learning

After any triggering event, immediately:
- Update `MEMORY.md` with new insights/lessons
- Update `memory/YYYY-MM-DD.md` with the event
- If mistake: add to "本猫犯过的错误/教训" section in MEMORY.md
- If preference: update "腿腿哥的新偏好/要求" section

### Step 2: Reflect

Ask: "What can I learn from this?"
- What went wrong?
- What should I do differently?
- What files need updating?

### Step 3: Act

Immediately update relevant files:
- MEMORY.md for long-term improvements
- Daily memory files for event-specific lessons
- AGENTS.md or SOUL.md if persona/tone changes needed

### Step 4: Confirm

Tell the user what the agent learned and what changed.

## File Update Guidelines

### MEMORY.md Updates

Add to "本猫犯过的错误/教训" section:
```
- ❌ [Date]: [What went wrong]
  → 改进：[What to do differently]
```

Add to "腿腿哥的新偏好/要求" section:
```
- [New preference or requirement] (added [date])
```

### Daily Memory Updates

Add to "做得不好/需要改进的地方":
```
- ❌ [What went wrong]: [Context]
  - 教训：[Learning]
```

## Pattern Detection

Actively look for:
- Repeated mistakes (same error multiple times)
- User preferences that aren't recorded
- Missing knowledge that should be in memory
- Workflow inefficiencies

## Quick Reference

When user says "learn from this":
1. Read relevant memory files
2. Identify the lesson
3. Update MEMORY.md immediately
4. Confirm update to user

When agent makes a mistake:
1. Acknowledge the mistake
2. Explain what went wrong
3. Update relevant files
4. Tell user what will change

---
*This skill is part of the agent's self-improvement system.*
