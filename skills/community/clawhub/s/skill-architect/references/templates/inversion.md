# Inversion Template

Use this template when the skill must collect specific information from the user before it can act.

---

```markdown
---
name: {{skill-name}}
description: {{Describe what the skill does AND when it should trigger. Emphasize that it interviews/gathers requirements before acting.}}
---

# {{Skill Name}}

{{Brief explanation of what this skill does and why the interview phase matters.}}

## Phase 1: {{Discovery Phase Name}}

Understand the user's goal at a high level. Extract from context first — they may have already described what they want.

Ask only what you don't already know:
- {{Question 1}} — {{why this is blocking}}
- {{Question 2}} — {{why this is blocking}}

**Ask one question at a time. Wait for the answer before proceeding.**

## Phase 2: {{Constraints Phase Name}}

Now that the goal is clear, gather the specific constraints:
- {{Question 3}} — {{why this is blocking}}
- {{Question 4}} — {{why this is blocking}}

## Phase 3: Confirmation

Summarize what you've learned and present it back to the user:

```
Here's what I understand:
- Goal: {{...}}
- Constraints: {{...}}
- Key decisions: {{...}}

Does this look right, or should I adjust anything?
```

**HARD GATE: Do NOT proceed to execution until the user confirms.**

## Phase 4: Execute

{{What to do with the collected information — generate output, execute steps, hand off to another pattern, etc.}}
```
