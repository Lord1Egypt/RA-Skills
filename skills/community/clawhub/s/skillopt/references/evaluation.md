# SkillOpt Evaluation Reference

Use this reference when building task suites or interpreting scores.

## JSONL Task Schema

Each line is one task:

```json
{
  "id": "val_spreadsheet_001",
  "prompt": "Use the skill to inspect the workbook and report the revenue delta.",
  "inputs": ["fixtures/revenue.xlsx"],
  "tags": ["spreadsheet", "calculation"],
  "scorer": {
    "type": "contains",
    "expected": "$42,100"
  }
}
```

Required fields:

- `id`: Stable unique id. Use split prefixes such as `train_` or `val_`.
- `prompt`: The user-facing task prompt.
- `scorer`: A scoring object.

Optional fields:

- `inputs`: Files, URLs, or notes needed for the task.
- `tags`: Capabilities or risk areas covered by the task.
- `metadata`: Any non-secret context useful for reporting.

## Scorer Types

### exact

Pass when normalized output equals normalized expected text.

```json
{"type": "exact", "expected": "PASS"}
```

### contains

Pass when output contains the expected string. If `expected` is a list, every item must appear.

```json
{"type": "contains", "expected": ["root cause", "rollback plan"]}
```

### regex

Pass when the regular expression matches the output.

```json
{"type": "regex", "pattern": "\\b[0-9]+\\.[0-9]{2}%\\b"}
```

### command

Run an external scorer. The command may use `{output_path}`, `{expected}`, `{task_id}`, and `{skill_path}` placeholders. The score is pass when the command exits `0`.

```json
{
  "type": "command",
  "command": "python3 scorers/check_report.py --output {output_path}"
}
```

### manual

Use when judgment is required. Store the output and record the score separately in the report.

```json
{"type": "manual", "rubric": "0-1 score for factual correctness and format compliance"}
```

## Split Discipline

- Use train tasks to discover failures and propose edits.
- Use validation tasks only for gating.
- Do not copy validation answers, ids, or benchmark-specific tricks into the skill.
- If validation becomes familiar after many rounds, create a fresh holdout split.

## Suggested Metrics

For each split, report:

- `avg_score`: Mean score over scored tasks.
- `pass_rate`: Share of tasks with score `1.0`.
- `scored_tasks`: Number of tasks with automatic or completed manual scores.
- `unscored_tasks`: Number of manual or failed-to-score tasks.
- `critical_regressions`: Validation tasks that changed from pass to fail.

## Acceptance Defaults

Accept a candidate only if:

- validation `avg_score` improves by at least `0.02`
- no critical validation task regresses
- no new safety, privacy, or tool-use issue appears
- skill metadata remains valid

Raise the threshold for noisy scorers; lower it only when tasks are expensive and the observed improvement is qualitatively strong.
