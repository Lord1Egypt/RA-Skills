# Judge Rubric

Judge is used for Level 3, high-risk, multi-path, or explicitly requested review. It is not part of every quick rewrite.

## Verdicts

| Verdict | Meaning | Action |
|---|---|---|
| pass | prompt is faithful, useful, and copy-ready | render final output |
| minor_fix | one or two targeted issues remain | patch the prompt once |
| rewrite_required | intent drift, missing critical slot, or unusable structure | return to compiler/context |

## Scoring Dimensions

Score each from 1-5.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Intent fidelity | changes user's goal | mostly aligned | preserves exact goal and nuance |
| Scenario fit | generic | partly scenario-aware | slots match the concrete scenario |
| Context sufficiency | critical gaps hidden | some placeholders | asks or exposes the key missing fields |
| Constraint strength | vague | usable constraints | clear boundaries and non-goals |
| Pressure fit | absent or forced | useful but rough | improves answer quality without overreach |
| Output readiness | fragmented | copyable with edits | directly copy-ready |
| Risk clarity | no risks | generic warning | clear flip condition or failure signal |

## Rewrite Triggers

Return `rewrite_required` if any condition is true:

- upgraded prompt answers the underlying task instead of improving the input
- primary intent changes
- scenario is guessed despite low confidence
- a critical required slot is missing and not represented as a placeholder
- pressure forces a conclusion or adversarial tone not requested by the user
- final prompt lacks output format or acceptance criteria for generation tasks

## Judge Output Shape

```json
{
  "verdict": "pass | minor_fix | rewrite_required",
  "scores": {
    "intent_fidelity": 0,
    "scenario_fit": 0,
    "context_sufficiency": 0,
    "constraint_strength": 0,
    "pressure_fit": 0,
    "output_readiness": 0,
    "risk_clarity": 0
  },
  "main_problem": "",
  "fix_instruction": "",
  "flip_condition": ""
}
```

## Quality Thresholds

- Average >= 4.2 and no rewrite trigger: `pass`
- Average 3.4-4.1 or one local issue: `minor_fix`
- Average < 3.4 or any rewrite trigger: `rewrite_required`
