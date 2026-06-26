# Eval 2 Fixture

This fixture mitigates the remaining `markdown+issues` validation gap
without requiring live tracker credentials.

## Goal

Exercise the dry-run issue planning path with:

- workspace context settings
- priority threshold filtering
- additional standards metadata
- priority and WCAG labels
- duplicate skipping based on existing deduplication keys

## Files

- `context.md`: workspace-local project context
- `current-scan.json`: helper scan JSON input
- `existing-keys.json`: deduplication keys that simulate open tickets

## Run

```bash
node a11y-audit/scripts/plan-issues.js \
  --input a11y-audit/evals/fixtures/eval-2/current-scan.json \
  --context a11y-audit/evals/fixtures/eval-2/context.md \
  --existing a11y-audit/evals/fixtures/eval-2/existing-keys.json \
  --output /tmp/a11y-eval-2-issue-plan.md
```

## Expected Behavior

- Only P0 and P1 issues are included because the context threshold is `P1`
- Labels come from the project context
- WCAG principle labels are added when the rule maps to a WCAG principle
- Existing deduplication keys are marked as `duplicate` rather than `create`
- Additional standards are recorded in the plan for reviewer confirmation
