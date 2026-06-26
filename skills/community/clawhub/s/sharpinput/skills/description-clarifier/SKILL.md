---
name: sharpinput-description-clarifier
description: Use when SharpInput receives vague, subjective, emotional, or imprecise input that needs to be converted into analyzable dimensions before prompt compilation.
---

# Description Clarifier

Convert vague user phrasing into concrete dimensions without inventing goals.

## Inputs

- `target_input`
- `primary_intent`
- `scenario`
- `known_context`

## Output

```json
{
  "clarified_dimensions": [],
  "likely_hidden_intent": "",
  "needs_confirmation": false
}
```

## Examples

| Raw Phrase | Clarified Dimensions |
|-----------|----------------------|
| "页面很乱" | information hierarchy, visual focus, entry clarity, layout consistency |
| "方案不太对" | assumptions, target mismatch, missing constraints, execution risk |
| "提示词太普通" | missing role, weak constraints, no evaluation criteria, no trade-off |
| "我说不清楚" | intent ambiguity, scenario missing, desired output unclear |

## Rules

- If the clarified dimensions could change the user's intent, request confirmation.
- Do not treat emotional wording as noise; it often signals risk or urgency.
- Do not over-specify domain details not present in the input.
