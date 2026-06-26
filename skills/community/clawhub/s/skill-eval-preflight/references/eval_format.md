# Skill Eval File Formats

Use these files under `evals/`:

- `evals.json`: realistic author requests for first-pass skill evaluation
- `triggers.json`: positive and negative trigger checks for the skill description
- `README.md`: notes for maintaining the eval files

## evals.json

Expected shape:

```json
[
  {
    "id": "core-happy-path",
    "prompt": "A realistic author request that should trigger the skill",
    "expected_artifacts": [
      "What a good response, file, or behavior should include"
    ],
    "files": []
  }
]
```

Notes:

- `id` should be stable and readable
- `prompt` should sound like a real author request, not a placeholder
- `expected_artifacts` should describe observable outcomes, not vague aspirations
- `files` is optional and can stay `[]` if the case has no file constraints
- keep at least one case focused on scaffolding/readiness and one focused on trigger coverage review when possible

## triggers.json

Expected shape:

```json
{
  "should_trigger": [
    {
      "id": "positive-basic",
      "prompt": "A request that should clearly trigger the skill"
    }
  ],
  "should_not_trigger": [
    {
      "id": "negative-basic",
      "prompt": "A request that should not trigger the skill"
    }
  ]
}
```

Notes:

- keep both positive and negative cases
- make the difference obvious
- avoid placeholders
- include at least one negative case that asks for a deeper runtime benchmark, so the skill boundary stays explicit
- include at least one negative case that belongs to another skill family entirely

## runs/

`run_eval.py` writes outputs under:

```text
evals/runs/<run-group>/<mode>/
```

Typical files:

- `summary.json`
- `summary.md`
- `run_metadata.json`

`compare_runs.py` writes at the run-group root:

- `comparison.json`
- `comparison.md`
