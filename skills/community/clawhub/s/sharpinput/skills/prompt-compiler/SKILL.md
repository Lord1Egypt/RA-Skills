---
name: sharpinput-prompt-compiler
description: Use when SharpInput has enough intent and context to compile the user's weak input into a stronger copy-ready prompt.
---

# Prompt Compiler

Compile the upgraded prompt. This is the core transformation step.

## Inputs

- `target_input`
- `primary_intent`
- `secondary_intent`
- `scenario`
- `known_context`
- `missing_fields`
- `clarified_dimensions`
- `pressure_requirements`

## Must Include

- role or perspective
- task goal
- relevant context
- constraints
- judgment criteria
- output format
- explicit ban on vague answers

## Output

```json
{
  "compiled_prompt_draft": "",
  "missing_placeholders": [],
  "compile_notes": []
}
```

## Rules

- Do not answer the underlying task.
- Use placeholders for missing but non-blocking fields.
- Make the prompt directly copyable.
- Avoid generic phrases such as "根据我的需求" unless the needs are specified.
- For decision prompts, force a recommendation and trade-off.
- For generation prompts, specify audience, output format, and acceptance criteria.
