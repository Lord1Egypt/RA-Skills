# Optional AI-WCAG-Gauntlet extension

This directory supports the AI-WCAG-Gauntlet experiment. It is separate from
the production WCAG workflow because tag-count coverage is a benchmark
constraint, not evidence of WCAG conformance.

## Use only for an explicit benchmark request

1. Run the Gauntlet setup in its own repository to create a fresh submission
   directory.
2. Write original HTML, CSS, and scripts in that submission directory.
3. Run the local pre-check from this extension:

   ```bash
   python3 benchmark/scripts/check-tag-coverage.py <submission-directory>/index.html
   ```

4. For a [legacy-repair task](https://github.com/turbolego/AI-WCAG-Gauntlet/blob/main/BENCHMARK.md#legacy-repair-task),
   preserve the fixture's content, destinations, and behavior while removing
   obsolete markup. All 113 required tags still apply in that task. Run the
   Gauntlet test suite, including its legacy and preservation checks, and retain
   its output separately from production accessibility reports.

## Integrity rule

`benchmark/templates/` is reference material only. Do not copy a template or
the bare starter into a benchmark submission. A valid benchmark run must contain
an original implementation tailored to its prompt.

The benchmark checker uses `benchmark/resources/html_tags.json` for its 113
required tags and `resources/legacy_tags.json` as the shared obsolete-element
list. It is a benchmark pre-check, not the production legacy-audit tool or the
Gauntlet's full legacy-pattern and preservation checker. Production repairs
can use [`scripts/check-legacy-markup.py`](../scripts/check-legacy-markup.py)
for a source inventory, then follow the production validator and manual-test
workflow.
