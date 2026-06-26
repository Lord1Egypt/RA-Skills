# Handoff Contract

All SharpInput modules update the same handoff object. The object prevents natural-language handoff drift between capability skills.

## Canonical Object

```json
{
  "raw_input": "",
  "target_input": "",
  "user_instruction": "",
  "task_mode": "prompt_optimization",
  "ambiguity_level": "low | medium | high",
  "level": 1,
  "route": "quick_rewrite | clarify_first | pressure_prompt | judge_mode",
  "primary_intent": "",
  "secondary_intent": "",
  "intent_confidence": 0.0,
  "scenario": "",
  "scenario_confidence": 0.0,
  "slot_template": "",
  "known_context": {},
  "missing_fields": [],
  "slot_questions": [],
  "clarified_dimensions": [],
  "context_status": "complete | partial | insufficient",
  "pressure_requirements": [],
  "overpressure_risk": "low | medium | high",
  "compiled_prompt_draft": "",
  "missing_placeholders": [],
  "fidelity_check": {
    "status": "pass | minor_drift | fail",
    "notes": []
  },
  "quality_score": {
    "overall": 0.0,
    "weak_dimensions": []
  },
  "judge_result": {},
  "final_prompt": "",
  "risk_notes": [],
  "user_feedback": ""
}
```

## Lifecycle

1. Input normalization sets `raw_input`, `target_input`, `user_instruction`, and `task_mode`.
2. Gate sets `level` and provisional `route`.
3. Intent detection sets `primary_intent`, `secondary_intent`, and confidence.
4. Scenario detection sets `scenario`, `slot_template`, and confidence.
5. Slot/context completion fills `known_context`, `missing_fields`, `context_status`, and questions.
6. Compiler writes `compiled_prompt_draft`.
7. Pressure strategy writes `pressure_requirements`.
8. Fidelity and quality checks write `fidelity_check` and `quality_score`.
9. Judge writes `judge_result` when used.
10. Renderer writes `final_prompt`.

## Merge Rules

- Never delete earlier fields unless they were clearly wrong.
- Prefer arrays for missing fields, questions, risks, and notes.
- Mark uncertainty explicitly instead of guessing.
- If a module cannot run, leave its fields empty and add a `risk_notes` entry.
