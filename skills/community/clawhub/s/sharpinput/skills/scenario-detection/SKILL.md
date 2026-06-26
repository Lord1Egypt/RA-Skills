---
name: sharpinput-scenario-detection
description: Use when SharpInput needs to recognize the concrete user scenario behind an input, such as computer purchase, AI subscription choice, PRD generation, or UI review.
---

# Scenario Detection

Identify the concrete scenario so SharpInput can ask useful slot questions instead of generic background questions.

## Inputs

- `primary_intent`
- `secondary_intent`
- `target_input`
- `known_context`

## Output

```json
{
  "scenario": "",
  "slot_template": "",
  "confidence": 0.0,
  "reason": ""
}
```

## Known Scenarios

Use `references/scenario-slot-templates.md` for slot definitions.

Common scenarios:

- computer_purchase
- ai_subscription_choice
- ai_model_selection
- frontend_demo_generation
- prd_srs_generation
- ui_review
- learning_exam_prep
- code_debugging
- server_network_troubleshooting
- product_plan_review
- hardware_purchase_decision

## Rules

- Scenario is not the same as intent. "决策" can appear in many scenarios.
- If no known scenario matches, leave `scenario` empty and let `context-completion` handle generic fields.
- If scenario confidence is low, do not force a template; use placeholders instead.
