---
name: sharpinput-context-completion
description: Use when SharpInput needs generic context completion after intent detection, especially when no scenario template applies.
---

# Context Completion

Fill only the missing fields that materially improve the upgraded prompt.

## Inputs

- `primary_intent`
- `secondary_intent`
- `target_input`
- `known_context`
- `scenario`

## Generic Fields

- goal
- audience
- constraints
- output format
- evaluation criteria
- attempted solutions
- unacceptable outcomes

## Output

```json
{
  "context_status": "complete | partial | insufficient",
  "known_context": {},
  "missing_fields": [],
  "placeholder_strategy": true
}
```

## Rules

- Do not ask "背景/目标/场景" as a generic bundle.
- Ask only the field that changes the final prompt most.
- **Level-aware gate (mandatory)**:
  - Level 0-1: placeholders allowed; may skip asking if prompt is usable.
  - Level 2: **MUST ask** for missing `audience`, `goal`, or `constraints` before compiling. No skipping.
  - Level 3: **MUST ask** for all missing fields that affect decision quality. Judge mode requires complete context.
- If a decision or purchase scenario lacks constraints, ask for the non-negotiable constraint first.
- **Prohibited**: Never skip to Compiler when `missing_fields` is non-empty and Level >= 2. Skipping is a workflow violation.
