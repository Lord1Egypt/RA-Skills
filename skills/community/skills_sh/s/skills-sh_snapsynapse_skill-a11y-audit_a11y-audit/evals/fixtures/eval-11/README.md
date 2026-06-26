# Eval 11 Fixture

This fixture exercises the delta case where a rule keeps the same total
instance count but moves to different pages between audits.

## Goal

`color-contrast` has 2 instances in both runs:

- Previous audit: both instances are on `blog/*` pages
- Current scan: both instances are on `docs/*` pages

A page-aware delta implementation should report `color-contrast` as
changed, not unchanged.

## Files

- `previous-audit.json`: prior report-shaped JSON passed to `--previous`
- `current-scan.json`: current scan-shaped JSON passed to `--input`
- `discover.json`: optional discovery data so the generated report also
  includes template-group context

## Run

```bash
node a11y-audit/scripts/report.js \
  --input a11y-audit/evals/fixtures/eval-11/current-scan.json \
  --previous a11y-audit/evals/fixtures/eval-11/previous-audit.json \
  --discover a11y-audit/evals/fixtures/eval-11/discover.json \
  --project-name "Eval 11 Delta Fixture" \
  --runtime-url https://example.com \
  --expected-url https://example.com \
  --output-dir /tmp/a11y-audit-eval-11
```

## Expected Behavior

- The markdown `Delta from Previous Audit` section should treat
  `color-contrast` as changed because its affected pages moved.
- The JSON `delta` payload should contain page-aware or route-aware
  change data for `color-contrast`.
- `region` should remain unchanged because both count and page coverage
  are stable.
