---
name: sharpinput-pressure-strategy
description: Use when SharpInput needs to strengthen a compiled prompt with stance, trade-off, default-answer stress testing, or executable next steps.
---

# Pressure Strategy

Add judgment pressure without becoming contrarian for its own sake.

## Rename

Use **default-answer stress test** instead of "anti-consensus" when possible.

The goal is not to oppose the mainstream. The goal is to test whether the default answer fits this user's actual scenario.

## Pressure Types

1. **Falsifiable stance**: require a clear recommendation and failure condition.
2. **Default-answer stress test**: challenge the generic answer only when it would be weak.
3. **Trade-off exposure**: force the answer to say what is sacrificed.
4. **Executable next step**: require one concrete action, not only analysis.

## Output

```json
{
  "pressure_requirements": [],
  "overpressure_risk": "low | medium | high",
  "notes": []
}
```

## Rules

- Strongly enable for decision, comparison, validation, and high-stakes analysis.
- Use medium pressure for optimization and product/technical analysis.
- Use weak pressure or skip for factual explanation, translation, light copy polish, and direct debugging.
- If pressure changes the user's intent, reduce pressure and mark the risk.
