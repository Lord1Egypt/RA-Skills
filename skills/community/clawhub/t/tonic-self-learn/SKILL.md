---
name: self-learn
description: >
  Continuous self-improvement through learning from corrections and task self-evaluation.
  Use when: (1) User corrects the agent (No that is wrong, Actually, I prefer, Stop doing X),
  (2) After completing any task - evaluate your own output,
  (3) User asks what the agent has learned,
  (4) User says remember this or note that.
  Stores learnings in LanceDB memory + memory/corrections.md for human review.
---

# Self-Learn Skill

Two-part continuous improvement loop: learn from corrections, learn from self-evaluation.

## On Every Task Completion

After finishing any task, briefly self-evaluate (1–3 sentences internally):
- Did the output meet the intent?
- What could be better next time?
- Is this a repeatable pattern worth storing?

If yes → log it. If it was routine with no issues → skip logging (don't over-log).

**Log format:**
```
CONTEXT: [task type]
REFLECTION: [what I noticed]
LESSON: [what to do differently / keep doing]
```

Append to `memory/corrections.md` under today's date. Also call `memory_store` with:
- category: `decision`
- importance: 0.75
- text: `[LESSON] <lesson text>` + relevant keywords

## On User Corrections

Trigger phrases (detect these):
- "No, that's wrong / not right"
- "Actually..." / "I prefer..." / "Remember that I..."
- "Stop doing X" / "Why do you keep..."
- "I told you before..." / "Always do X"

When triggered:
1. Acknowledge the correction briefly
2. Append to `memory/corrections.md` under `## Corrections` with today's date
3. Call `memory_store` with:
   - category: `preference` (style/tone) or `decision` (behaviour/approach)
   - importance: 0.85
   - text: `[CORRECTION] <what was wrong> → <correct behaviour>` + keywords
4. Recall to verify it stored correctly

**Log format:**
```
[YYYY-MM-DD] CORRECTION: <what was wrong> → <correct behaviour>
```

## memory/corrections.md Structure

```markdown
# Corrections & Learnings Log

## Corrections
[YYYY-MM-DD] CORRECTION: ...

## Self-Evaluations
[YYYY-MM-DD] CONTEXT: ... | LESSON: ...
```

Create the file if it doesn't exist.

## On "What have you learned?" / "Show my patterns"

Read `memory/corrections.md` and show last 10 entries. Also `memory_recall` with query "CORRECTION OR LESSON" for LanceDB results.

## Installation on a New OpenClaw

1. Copy `skills/self-learn/` into your workspace `skills/` folder — skill activates automatically
2. Create `memory/corrections.md` (copy from `references/corrections-template.md`)
3. Optionally update `AGENTS.md` skill table for easy reference

## Rules

- **Don't over-log** — skip routine tasks with no notable outcome
- **Atomic entries** — one lesson per entry, under 100 words
- **Keywords matter** — include domain keywords in memory_store text for good recall
- **No secrets** — never log credentials, personal data, or sensitive info
- **Corrections always log** — user corrections are always worth storing (importance ≥ 0.85)
