# Eval 9 Fixture

This fixture exercises discovery against a site whose published sitemap
is hosted on a different origin than the runtime URL.

## Goal

- `robots.txt` lives on `http://base.test`
- It publishes a sitemap on `http://cdn.test/sitemap.xml`
- That sitemap is a sitemap index which points to `http://cdn.test/nested.xml`
- The nested sitemap publishes final page URLs on `http://cdn.test`

Discovery should preserve those published URLs exactly as published
instead of rewriting them onto `http://base.test`.

## Files

- `config.json`: runtime URL and fixture execution settings
- `responses.json`: mocked HTTP responses keyed by URL
- `expected.json`: expected discovery result

## Run

```bash
node a11y-audit/evals/run-discover-fixture.js \
  --fixture a11y-audit/evals/fixtures/eval-9
```

## Expected Behavior

- `source` records the published sitemap URL on `http://cdn.test`
- `scanList` contains only `http://cdn.test/...` page URLs
- No sitemap or page URL is rewritten onto `http://base.test`
