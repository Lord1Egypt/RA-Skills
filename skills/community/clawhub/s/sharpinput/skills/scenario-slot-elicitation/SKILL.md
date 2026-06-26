---
name: sharpinput-scenario-slot-elicitation
description: Use when SharpInput detected a known scenario and needs to collect the few scenario-specific variables that most affect prompt quality.
---

# Scenario Slot Elicitation

Ask for the highest-impact scenario variables, not generic background.

## Inputs

- `scenario`
- `slot_template`
- `known_context`
- `user_instruction`

## Output

```json
{
  "missing_fields": [],
  "slot_questions": [],
  "placeholder_strategy": true
}
```

## Rules

- Ask at most 1-3 slots at once.
- Prefer slots marked `required` in `references/scenario-slot-templates.md`.
- If the user says "直接给/别问", use placeholders instead of asking.
- Do not ask for slots already present in the user's input.
- If all critical slots are missing and output quality would collapse, ask before compiling.

## Ask Format

Use `AskUserQuestion` patterns from `references/interaction-patterns.md`.
