# Eval 10 Fixture

This fixture exercises repeated discovery against the same sitemap and
page content to confirm deterministic representative selection.

## Goal

- Discovery runs twice against the same mocked site
- DOM fingerprinting is enabled
- Both runs should produce identical output and the same scan list

## Files

- `config.json`: runtime URL and repeat count
- `responses.json`: mocked HTTP responses keyed by URL
- `expected.json`: expected repeated-run result

## Run

```bash
node a11y-audit/evals/run-discover-fixture.js \
  --fixture a11y-audit/evals/fixtures/eval-10
```

## Expected Behavior

- `repeatIdentical` is `true`
- Both runs return the same `scanList`
- The selected pages stay stable across repeated execution
