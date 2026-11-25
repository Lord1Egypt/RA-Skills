# Optional AI-WCAG-Gauntlet extension

This directory supports the AI-WCAG-Gauntlet experiment. It is separate from
the production WCAG workflow because tag-count coverage is a benchmark
constraint, not evidence of WCAG conformance.

## Use only for an explicit benchmark request

Before running setup or a test suite, read the Gauntlet's `BENCHMARK.md` and
the task-specific instructions. Run setup in the Gauntlet repository to create
a fresh run folder, use that same folder throughout, and build an original
candidate for the assigned task. Do not copy a previous submission or the
reference template into a scored run.

### Mandatory preflight before scoring

The official suite increments `iterations_count.txt`; it is a scored run, not
a preflight tool. Before its first invocation, run **all five** checks below
against the completed candidate. Preflight is unscored and must not change the
counter, `test_results.json`, or any official report.

From the skill repository root, run the source-level pre-check on the candidate
in the separate Gauntlet checkout:

```bash
python3 benchmark/scripts/check-tag-coverage.py <gauntlet-run-folder>/index.html
```

This is a useful local check, but the official preflight must also run the
Gauntlet's required-tag checker. Change to the Gauntlet repository root and run
all five validators there:

1. **Required tag coverage:**

   ```bash
   node scripts/check-html5-tags.mjs <run-folder>/index.html <temp>/tags.json
   ```

   Require `missing_tags` to be empty.
2. **W3C:** run
   `node resources/run-w3c-validator.mjs <run-folder>/index.html <temp>/w3c.json`;
   require a valid report with `errorCount: 0`.
3. **axe:** serve the candidate over HTTP and run
   `node scripts/run-axe.mjs <candidate-http-url> <temp>/axe.json`. Require no
   `violations`; inspect and resolve or explicitly verify each `incomplete`
   result.
4. **Pa11y:** run the local `node_modules/pa11y/bin/pa11y.js` with
   `--runner axe --standard WCAG2AAA --config <temp>/pa11y-config.json
   --include-warnings --include-notices --reporter json` against the same
   candidate URL. The config must point to the same Chrome for Testing binary
   used by the Gauntlet suite and a browser profile under `<temp>`. Exit code
   2 means findings; inspect the JSON. Any other nonzero exit is a tool error.
   Require no issues.
5. **QualWeb:** run
   `node resources/run-qualweb.mjs <run-folder>/index.html <temp>/qualweb.json`.
   Require a fresh valid object with an integer `failedCount` of 0, a `results`
   array, and neither an `error` nor `note` field.

Serve from the Gauntlet repository's parent directory so the candidate's
`/AI-WCAG-Gauntlet/resources/` URLs resolve as they do in the official suite.
Choose an available local port and encode the run-folder path the same way as
the suite when constructing the candidate URL. Wait until the candidate
responds over HTTP before running axe and Pa11y.
Use the suite's normal Chrome for Testing discovery and launch configuration;
do not use personal Chrome, wrappers, or an improvised executable. Put every
preflight report and isolated browser profile in a uniquely allocated OS
temporary directory, never in the run folder. Stop the temporary HTTP server
and remove only that scratch directory when preflight is complete. On
PowerShell, allocate the scratch directory under
`[System.IO.Path]::GetTempPath()` and remove only the allocated path. W3C
validation sends HTML to the Nu Html Checker service; do not submit
confidential content.

Treat a missing, skipped, malformed, or stale report as a tool failure, not a
zero-finding result. If any validator finds an issue, fix the candidate and
repeat **all five** preflight checks. Do not start a scored run until every
check has completed cleanly and axe incomplete results have been reviewed.
Record each unscored preflight, its findings, and repairs in `benchmark_log.md`
without retaining temporary reports in the benchmark folder.

### Scored run

After preflight is clean, run the official `test-suite.sh` (or
`test-suite.ps1`) against the same fresh run folder. Read its final `STATUS:`
line, not just the process exit code. Stop after `STATUS: PASS` or the
maximum-iterations status. For `STATUS: FAIL — Fix the errors`, repair the
candidate and immediately rerun the scored suite, respecting the Gauntlet's
iteration cap. Preflight does not replace the required scored run or this
post-failure loop.

For a [legacy-repair task](https://github.com/turbolego/AI-WCAG-Gauntlet/blob/main/BENCHMARK.md#legacy-repair-task),
preserve the fixture's content, destinations, and behavior while removing
obsolete markup. All 113 required tags still apply; run the suite's legacy and
preservation checks as well.

## Integrity rule

`benchmark/templates/` is reference and validator-smoke-test material only.
Never copy a template or the bare starter into a scored benchmark submission.
A valid benchmark run must contain an original implementation tailored to its
prompt. A clean template smoke test is not a model score.

The benchmark checker uses `benchmark/resources/html_tags.json` for its 113
required tags and `resources/legacy_tags.json` as the shared obsolete-element
list. It is a benchmark pre-check, not the production legacy-audit tool or the
Gauntlet's full legacy-pattern and preservation checker. Production repairs
can use [`scripts/check-legacy-markup.py`](../scripts/check-legacy-markup.py)
for a source inventory, then follow the production validator and manual-test
workflow.
