---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill selection before any response (including clarifying questions)
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply, you MUST invoke that skill.

If a skill applies to the task, you do not have a choice. Use it.
</EXTREMELY-IMPORTANT>

## Instruction Priority

Superpowers skills augment default behavior, but **user/system/developer instructions always take precedence**:

1. **User + system/developer instructions** (AGENTS.md, direct requests, runtime policy) — highest priority
2. **Superpowers skills** — workflow/method guidance
3. **Default model behavior** — lowest priority

If project instructions conflict with a skill, follow project instructions.

## How to Access Skills in OpenClaw

Use the standard OpenClaw skill flow:
1. Scan available skills
2. Choose the one that clearly applies
3. Use `read` to load that skill's `SKILL.md`
4. Follow it exactly

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.**
Even a 1% chance a skill applies means check it.

## Red Flags

These thoughts mean STOP — you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. |
| "I can check files quickly" | Files lack workflow context. Check for skills. |
| "I remember this skill" | Skills evolve. Read current version. |
| "The skill is overkill" | Simple tasks become complex. Use the workflow. |

## Skill Priority

When multiple skills could apply:

1. **Process skills first** (brainstorming, debugging)
2. **Implementation skills second**

"Build X" ... brainstorming first, then implementation.
"Fix bug Y" ... debugging first, then domain-specific skills.

## Skill Types

**Rigid** (TDD, debugging): Follow exactly.

**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW.
"Add X" or "Fix Y" does not mean skip workflow discipline.
