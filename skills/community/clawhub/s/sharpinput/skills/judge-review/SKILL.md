---
name: sharpinput-judge-review
description: Use when SharpInput is in Level 3, high-risk, multi-path, or user-requested review mode and needs an independent quality and fidelity check.
---

# Judge Review

Judge is a high-level fuse, not a daily engine.

## Trigger Conditions

Use Judge when any of these apply:

- Level 3
- high-risk decision
- multi-path prompt
- likely intent drift
- user asks for challenge, review, counterargument, or stress test
- money, career, project direction, or irreversible choice is involved

## Review Dimensions

Use `references/judge-rubric.md`.

Judge checks:

- intent fidelity
- scenario slot completeness
- constraint strength
- over-complexity
- default-answer stress test appropriateness
- copy readiness
- flip condition

## Output

```json
{
  "verdict": "pass | minor_fix | rewrite_required",
  "main_problem": "",
  "intent_fidelity": "high | medium | low",
  "missing_slots": [],
  "overreach": "",
  "fix_instruction": "",
  "flip_condition": ""
}
```

## Rules

- If `verdict = rewrite_required`, return to prompt compiler.
- If Judge is unavailable, perform inline review and mark it as downgraded.
- Do not use Judge for simple Level 0/1 polish.
