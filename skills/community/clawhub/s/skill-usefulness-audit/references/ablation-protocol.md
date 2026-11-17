# Ablation Protocol

Use this protocol for `general` skills selected by the ablation plan.

## Goal

Measure whether the skill changes outcomes in a meaningful way.
High consistency between skill-on and skill-off runs means the skill adds little value.

## Sampling

Start with `3` historical tasks where the skill should plausibly matter. Prefer real user turns over synthetic prompts. Expand to `5` when results are mixed and to `10` only for high-impact or delete-boundary decisions.

## Replay Method

For each selected case, run two isolated replays:

1. `with_skill`
2. `without_skill`

Keep these constant:

- same prompt
- same files and artifacts
- same model class when possible
- same tool permissions
- same success criteria

Use a fresh thread or isolated run if the host supports it.

## Judge Method

For open-ended outputs:

1. Compare `with_skill` and `without_skill` side by side.
2. Randomize A/B order.
3. Spot-check reversed order on boundary cases.
4. Prefer `pass/fail`, `same/better/worse`, and short reasons over long open-ended grading.

Record a standard `verdict` and one short `notes` reason. Each arm may also include optional `pass` and/or `score` from `0.0-1.0` for fallback inference. Optional `tool_cost` may describe calls, latency, or retries and currently does not affect the audit score.

### Normalized JSON

```json
[
  {
    "skill": "emotion-orchestrator",
    "case_id": "case-001",
    "with_skill": {"pass": true, "score": 0.92},
    "without_skill": {"pass": true, "score": 0.81},
    "verdict": "better"
  }
]
```

## Judgment Rule

Use `same` when the final answer, correctness, and workflow remain materially equivalent.
Use `better` when the skill improves correctness, speed, structure, or user-fit in a way the baseline did not.
Use `worse` when the skill adds friction, drift, or errors.

Ignore verdict-only cases with unsupported values. A case with an unknown or missing verdict is usable only when both arms provide comparable `pass` and/or `score` fields for inference.

## Early Stop Rules

- Stop as low-value when `3/3` cases are `same` and `better_rate` is `0`.
- Stop as useful when at least `2/3` cases are `better` and no case is `worse`.
- Expand to `5` when the first batch is mixed.
- Expand to `10` only for delete-boundary or high-impact decisions.

Delete-boundary means "needs stronger human review evidence", not automatic deletion authority.

## Planning and Model Cost

Create the replay plan with `--ablation-plan-out`. Planning uses local evidence and does not call an LLM.

The plan estimates replay cost for `light`, `realistic`, and `coding` profiles. Each case assumes two replays and one compact pairwise judge. `model_cost_estimates.unit` records `estimated_context_units_per_case`.

Feed normalized results back with `--ablation-file`.
