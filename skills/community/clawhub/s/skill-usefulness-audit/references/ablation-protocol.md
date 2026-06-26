# Ablation Protocol

Use this protocol for `general` skills selected by the ablation plan.

## Contents

- Goal
- Cost-Efficient Triage
- Sampling
- Replay Method
- Judge Method
- Borrowed Idea Validation
- Case Judgment
- Judgment Rule
- Early Stop Rules
- Model Cost
- Reporting

## Goal

Measure whether the skill changes outcomes in a meaningful way.

High consistency between skill-on and skill-off runs means the skill adds little value.

## Cost-Efficient Triage

Generate a plan before running replay:

```bash
python scripts/skill_usefulness_audit.py audit \
  --skills-root ./skills \
  --usage-file ./usage.json \
  --json-out ./skill-audit-report.json \
  --ablation-plan-out ./skill-ablation-plan.json
```

The plan uses local evidence first:

- final score
- overlap
- quality burden
- activation volume
- evidence confidence
- missing or weak prior ablation

It then estimates model cost against a full protocol and writes an early-stop plan.

## Sampling

Start with `3` historical tasks per candidate skill.
Choose tasks where the skill should plausibly matter.
Prefer real user turns over synthetic prompts.
Expand to `5` cases when the first batch is mixed.
Expand to `10` cases only for high-impact or deletion-boundary decisions.

Override these defaults with:

- `--ablation-baseline-cases`
- `--ablation-initial-cases`
- `--ablation-expand-cases`
- `--ablation-max-cases`

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
Subagents are optional. They improve isolation and parallelism, but they increase total model spend when every branch runs full replay.

## Borrowed Idea Validation

Borrowed idea validation uses the same replay discipline as normal ablation.
For a borrowed idea, compare the current baseline and changed version with the same input fixture.
Use identical installed-skill fixtures, usage files, ablation files, and output fields.
Keep the idea only when the target behavior improves or becomes clearer and unrelated skills do not receive stricter actions.
Rollback if a non-target skill moves to `delete`, `merge-delete`, or `quarantine-review` without new risk evidence.

## Judge Method

Use pairwise comparison when judging open-ended outputs:

1. Compare `with_skill` and `without_skill` side by side.
2. Randomize A/B order.
3. Spot-check reversed order on boundary cases.
4. Prefer `pass/fail`, `same/better/worse`, and short reasons over long open-ended grading.

## Case Judgment

Record:

- `pass`: whether the run solved the task
- `score`: optional `0.0-1.0` quality score
- `tool_cost`: optional rough measure of tool calls, latency, or retries
- `verdict`: `better`, `same`, or `worse`
- `notes`: one short reason

## Normalized JSON Example

```json
[
  {
    "skill": "emotion-orchestrator",
    "case_id": "case-001",
    "with_skill": {"pass": true, "score": 0.92},
    "without_skill": {"pass": true, "score": 0.81},
    "verdict": "better",
    "notes": "with-skill run adapted reply style and avoided a follow-up correction"
  },
  {
    "skill": "tone-polisher",
    "case_id": "case-002",
    "with_skill": {"pass": true, "score": 0.84},
    "without_skill": {"pass": true, "score": 0.83},
    "verdict": "same",
    "notes": "final answer stayed materially equivalent"
  }
]
```

## Judgment Rule

Use `same` when the final answer, correctness, and workflow remain materially equivalent.
Use `better` when the skill improves correctness, speed, structure, or user-fit in a way the baseline did not.
Use `worse` when the skill adds friction, drift, or errors.

## Early Stop Rules

- Stop as low-value when `3/3` cases are `same` and `better_rate` is `0`.
- Stop as useful when at least `2/3` cases are `better` and no case is `worse`.
- Expand to `5` when the first batch is mixed.
- Expand to `10` only for delete-boundary or high-impact decisions.

Delete-boundary means "needs stronger human review evidence", not automatic deletion authority.

## Model Cost

The audit script does not call an LLM during planning.
The plan estimates replay cost with three profiles:

- `light`: about `6.2k` model-cost units per case
- `realistic`: about `24k` model-cost units per case
- `coding`: about `50k` model-cost units per case

Each case assumes two replays plus one compact pairwise judge.
The JSON field `model_cost_estimates.unit` records this as `estimated_context_units_per_case`.

## Reporting

Feed the normalized ablation file into:

```bash
python scripts/skill_usefulness_audit.py audit --ablation-file ./ablation.json
```
