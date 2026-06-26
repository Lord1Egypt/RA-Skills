---
name: sharpinput-intent-detection
description: Use when SharpInput needs to identify the user's primary and secondary intent before optimizing a prompt or question.
---

# Intent Detection

Identify what the user wants the eventual AI response to do. Do not identify the business scenario here; scenario detection is separate.

## Inputs

- `raw_input`
- `target_input`
- `user_instruction`

## Output

Return these fields into the handoff object:

```json
{
  "primary_intent": "",
  "secondary_intent": "",
  "intent_confidence": 0.0,
  "reason": ""
}
```

## Canonical Intents

Use `references/intent-taxonomy.md` for full definitions.

| Intent | Meaning |
|--------|---------|
| 理解 | explain a concept |
| 决策 | choose under constraints |
| 生成 | produce an artifact |
| 分析 | judge an existing object |
| 探索 | broaden possible directions |
| 诊断 | explain failure or abnormal behavior |
| 说服 | influence a person or group |
| 验证 | test an existing belief |
| 规划 | design a path from start to end |
| 学习 | acquire a skill |
| 优化 | improve an existing object |
| 对比 | compare alternatives |
| 梳理 | structure messy information |
| 求助 | locate a stuck point |

## Rules

- Semantic pattern beats keyword matching.
- Preserve secondary intent when it affects routing.
- If confidence < 0.65 or multiple interpretations are plausible, request intent confirmation using `references/interaction-patterns.md`.
- Do not upgrade a lightweight wording request into a strategic decision unless the user implies stakes or choice.
